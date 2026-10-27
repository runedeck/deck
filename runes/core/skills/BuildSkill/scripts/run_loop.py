#!/usr/bin/env python3
"""Optimization loop: evaluate a description, improve it, repeat.

The eval set is split into train and held-out test queries. Every iteration
measures the current description on both, then asks the model for a better
one using the train failures only. The best description is chosen by test
score so that improvements that only memorize the train queries do not win.

Usage, from the skill directory:

    python3 -m scripts.run_loop --eval-set evals.json --skill-path ../my-skill \\
        --model <model-id> --max-iterations 5 --verbose
"""

import argparse
import html
import json
import random
import sys
import tempfile
import time
import webbrowser
from datetime import UTC, datetime
from pathlib import Path

from scripts.generate_report import best_iteration_index, generate_html
from scripts.improve_description import improve_description
from scripts.run_eval import run_eval, shorten_query
from scripts.utils import parse_skill_md


def split_eval_set(
    eval_set: list[dict], holdout: float, seed: int = 42
) -> tuple[list[dict], list[dict]]:
    """Split into train and test, keeping both query kinds in both sets.

    A private random generator makes the split reproducible for a seed and
    leaves the global random state alone. Groups with one item or none keep
    everything in the train set.
    """
    rng = random.Random(seed)
    train: list[dict] = []
    test: list[dict] = []
    for wanted in (True, False):
        group = [item for item in eval_set if bool(item["should_trigger"]) == wanted]
        if len(group) <= 1:
            train.extend(group)
            continue
        rng.shuffle(group)
        test_count = max(1, int(len(group) * holdout))
        test_count = min(test_count, len(group) - 1)
        test.extend(group[:test_count])
        train.extend(group[test_count:])
    return train, test


def _split_results(results: list[dict], test_queries: set[str]) -> tuple[list[dict], list[dict]]:
    train = [item for item in results if item["query"] not in test_queries]
    test = [item for item in results if item["query"] in test_queries]
    return train, test


def _count_passed(results: list[dict]) -> int:
    return sum(1 for item in results if item["pass"])


def make_history_entry(
    iteration: int,
    description: str,
    train_results: list[dict],
    test_results: list[dict] | None,
) -> dict:
    """Build one history entry, including the older aliases for train values."""
    train_passed = _count_passed(train_results)
    entry = {
        "iteration": iteration,
        "description": description,
        "train_passed": train_passed,
        "train_failed": len(train_results) - train_passed,
        "train_total": len(train_results),
        "train_results": train_results,
        "test_passed": None,
        "test_failed": None,
        "test_total": None,
        "test_results": None,
        "passed": train_passed,
        "failed": len(train_results) - train_passed,
        "total": len(train_results),
        "results": train_results,
    }
    if test_results is not None:
        test_passed = _count_passed(test_results)
        entry.update(
            {
                "test_passed": test_passed,
                "test_failed": len(test_results) - test_passed,
                "test_total": len(test_results),
                "test_results": test_results,
            }
        )
    return entry


def blind_history(history: list[dict]) -> list[dict]:
    """Copy the history without any key that starts with ``test_``."""
    return [
        {key: value for key, value in entry.items() if not key.startswith("test_")}
        for entry in history
    ]


def split_metrics(results: list[dict]) -> dict:
    """Run-level counts and rates for one split."""
    true_positives = false_positives = false_negatives = true_negatives = 0
    for item in results:
        runs = item["runs"]
        picks = item["triggers"]
        if item["should_trigger"]:
            true_positives += picks
            false_negatives += runs - picks
        else:
            false_positives += picks
            true_negatives += runs - picks
    total = true_positives + false_positives + false_negatives + true_negatives
    correct = true_positives + true_negatives
    predicted = true_positives + false_positives
    actual = true_positives + false_negatives
    return {
        "correct": correct,
        "total": total,
        "precision": true_positives / predicted if predicted else 1.0,
        "recall": true_positives / actual if actual else 1.0,
        "accuracy": correct / total if total else 1.0,
    }


def print_split_report(label: str, results: list[dict], elapsed: float, stream=None) -> None:
    stream = stream or sys.stderr
    metrics = split_metrics(results)
    print(
        f"{label}: {metrics['correct']}/{metrics['total']} correct runs, "
        f"precision {metrics['precision']:.2f}, recall {metrics['recall']:.2f}, "
        f"accuracy {metrics['accuracy']:.2f}, {elapsed:.1f}s",
        file=stream,
    )
    for item in results:
        status = "PASS" if item["pass"] else "FAIL"
        expected = "should trigger" if item["should_trigger"] else "should not trigger"
        print(
            f"  {status}  {item['triggers']}/{item['runs']} picks  "
            f"{expected:<18}  {shorten_query(item['query'])}",
            file=stream,
        )


def _score_text(passed: int | None, total: int | None) -> str | None:
    if passed is None or total is None:
        return None
    return f"{passed}/{total}"


def run_loop(
    eval_set: list[dict],
    skill_path: Path,
    description_override: str | None,
    num_workers: int,
    timeout: int,
    max_iterations: int,
    runs_per_query: int,
    trigger_threshold: float,
    holdout: float,
    model: str,
    verbose: bool,
    live_report_path: Path | None = None,
    log_dir: Path | None = None,
    harness_name: str = "claude",
) -> dict:
    """Run the evaluate-improve loop and return the full outcome."""
    skill_name, frontmatter_description, skill_content = parse_skill_md(skill_path)
    original_description = (
        description_override if description_override is not None else frontmatter_description
    )

    if holdout > 0:
        train_set, test_set = split_eval_set(eval_set, holdout)
    else:
        train_set, test_set = list(eval_set), []
    test_queries = {item["query"] for item in test_set}
    has_test = bool(test_set)

    history: list[dict] = []
    current_description = original_description
    exit_reason = f"max_iterations ({max_iterations})"
    iterations_run = 0

    for iteration in range(1, max_iterations + 1):
        started = time.monotonic()
        outcome = run_eval(
            train_set + test_set,
            skill_name,
            current_description,
            num_workers,
            timeout,
            runs_per_query=runs_per_query,
            trigger_threshold=trigger_threshold,
            model=model,
            harness_name=harness_name,
        )
        elapsed = time.monotonic() - started
        train_results, test_results = _split_results(outcome["results"], test_queries)
        entry = make_history_entry(
            iteration, current_description, train_results, test_results if has_test else None
        )
        history.append(entry)
        iterations_run = iteration

        if live_report_path is not None:
            partial = {
                "original_description": original_description,
                "best_description": current_description,
                "best_score": "in progress",
                "iterations_run": iterations_run,
                "holdout": holdout,
                "train_size": len(train_set),
                "test_size": len(test_set),
                "history": history,
            }
            Path(live_report_path).write_text(
                generate_html(partial, auto_refresh=True, skill_name=skill_name),
                encoding="utf-8",
            )

        if verbose:
            print_split_report(f"[iteration {iteration}] train", train_results, elapsed)
            if has_test:
                print_split_report(f"[iteration {iteration}] test", test_results, elapsed)

        if entry["train_failed"] == 0:
            exit_reason = f"all_passed (iteration {iteration})"
            break
        if iteration == max_iterations:
            exit_reason = f"max_iterations ({iteration})"
            break

        train_eval = {
            "skill_name": skill_name,
            "description": current_description,
            "results": train_results,
            "summary": {
                "total": entry["train_total"],
                "passed": entry["train_passed"],
                "failed": entry["train_failed"],
            },
        }
        current_description = improve_description(
            skill_name,
            skill_content,
            current_description,
            train_eval,
            blind_history(history),
            model,
            log_dir=log_dir,
            iteration=iteration,
            harness_name=harness_name,
        )

    best_index = best_iteration_index(history)
    if best_index is None:
        best_entry = None
        best_description = original_description
    else:
        best_entry = history[best_index]
        best_description = best_entry["description"]

    best_train_score = None
    best_test_score = None
    if best_entry is not None:
        best_train_score = _score_text(best_entry["train_passed"], best_entry["train_total"])
        best_test_score = _score_text(best_entry["test_passed"], best_entry["test_total"])
    best_score = best_test_score if has_test else best_train_score

    return {
        "exit_reason": exit_reason,
        "original_description": original_description,
        "best_description": best_description,
        "best_score": best_score,
        "best_train_score": best_train_score,
        "best_test_score": best_test_score,
        "final_description": current_description,
        "iterations_run": iterations_run,
        "holdout": holdout,
        "train_size": len(train_set),
        "test_size": len(test_set),
        "history": history,
    }


def holdout_fraction(text: str) -> float:
    """argparse type: 0, or a value strictly between 0 and 1."""
    try:
        value = float(text)
    except ValueError:
        raise argparse.ArgumentTypeError(f"not a number: {text!r}") from None
    if value == 0 or 0 < value < 1:
        return value
    raise argparse.ArgumentTypeError("holdout must be 0 or strictly between 0 and 1")


def placeholder_page(skill_name: str) -> str:
    """A tiny page shown until the first iteration writes a real report."""
    return (
        "<!DOCTYPE html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">\n"
        '<meta http-equiv="refresh" content="5">\n'
        f"<title>Trigger optimization: {html.escape(skill_name)}</title>\n"
        "<style>body{font-family:-apple-system,Helvetica,Arial,sans-serif;"
        "padding:3rem;color:#1f2430}</style></head>\n"
        f"<body><h1>{html.escape(skill_name)}</h1>"
        "<p>The optimization loop is starting. This page reloads itself every "
        "five seconds and will show results once the first iteration finishes.</p>"
        "</body></html>\n"
    )


def utc_stamp() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%d_%H%M%S")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Evaluate a skill description and improve it iteratively"
    )
    parser.add_argument("--eval-set", type=Path, required=True)
    parser.add_argument("--skill-path", type=Path, required=True)
    parser.add_argument("--description", default=None, help="start from this description")
    parser.add_argument("--num-workers", type=int, default=10)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--max-iterations", type=int, default=5)
    parser.add_argument("--runs-per-query", type=int, default=3)
    parser.add_argument("--trigger-threshold", type=float, default=0.5)
    parser.add_argument("--holdout", type=holdout_fraction, default=0.4)
    parser.add_argument("--model", required=True)
    parser.add_argument("--harness", default="claude")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument(
        "--report",
        default="none",
        help="'none', 'auto' (temporary file opened in the browser), or a file path",
    )
    parser.add_argument(
        "--results-dir",
        type=Path,
        default=None,
        help="directory that receives a timestamped run folder",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)

    if not (args.skill_path / "SKILL.md").is_file():
        print(f"error: no SKILL.md in {args.skill_path}", file=sys.stderr)
        sys.exit(1)
    try:
        skill_name, _, _ = parse_skill_md(args.skill_path)
        eval_set = json.loads(args.eval_set.read_text(encoding="utf-8"))
        if not isinstance(eval_set, list):
            # A malformed eval set is bad input; the handler below reports it.
            raise ValueError(f"{args.eval_set}: the eval set must be a JSON array")  # noqa: TRY004
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)

    run_dir: Path | None = None
    log_dir: Path | None = None
    if args.results_dir is not None:
        run_dir = args.results_dir / utc_stamp()
        run_dir.mkdir(parents=True, exist_ok=True)
        log_dir = run_dir / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)

    report_path: Path | None = None
    if args.report == "auto":
        report_path = Path(tempfile.gettempdir()) / (
            f"{args.skill_path.resolve().name}-trigger-report-{utc_stamp()}.html"
        )
    elif args.report != "none":
        report_path = Path(args.report)
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(placeholder_page(skill_name), encoding="utf-8")
        try:
            webbrowser.open(report_path.resolve().as_uri())
        # A missing browser must not stop the loop.
        except Exception as exc:  # noqa: BLE001
            print(f"warning: could not open the report: {exc}", file=sys.stderr)
        print(f"Live report: {report_path}", file=sys.stderr)

    try:
        result = run_loop(
            eval_set,
            args.skill_path,
            args.description,
            num_workers=args.num_workers,
            timeout=args.timeout,
            max_iterations=args.max_iterations,
            runs_per_query=args.runs_per_query,
            trigger_threshold=args.trigger_threshold,
            holdout=args.holdout,
            model=args.model,
            verbose=args.verbose,
            live_report_path=report_path,
            log_dir=log_dir,
            harness_name=args.harness,
        )
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)

    final_page = None
    if report_path is not None:
        final_page = generate_html(result, auto_refresh=False, skill_name=skill_name)
        report_path.write_text(final_page, encoding="utf-8")

    if run_dir is not None:
        (run_dir / "results.json").write_text(
            json.dumps(result, indent=2), encoding="utf-8"
        )
        if final_page is not None:
            (run_dir / "report.html").write_text(final_page, encoding="utf-8")
        print(f"Results written to {run_dir}", file=sys.stderr)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
