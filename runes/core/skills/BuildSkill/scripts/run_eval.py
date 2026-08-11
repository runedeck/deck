#!/usr/bin/env python3
"""Run trigger evaluation for a skill description.

Tests whether a skill's description causes the harness to trigger (read the
skill) for a set of queries. Outputs results as JSON.

Trigger probes run inside an isolated temporary project directory so the
target repository is never written to.
"""

import argparse
import json
import re
import shutil
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from scripts.harness import get_harness
from scripts.utils import parse_skill_md

SKILL_NAME_PATTERN = re.compile(r"^[A-Za-z0-9]+(?:[-_][A-Za-z0-9]+)*$")
SKILL_NAME_MAX_LENGTH = 64


def run_single_query(
    query: str,
    skill_name: str,
    skill_description: str,
    timeout: int,
    project_root: str,
    model: str | None = None,
    harness_name: str = "claude",
) -> bool:
    """Probe one query through the harness adapter and report triggering."""
    harness = get_harness(harness_name)
    probe = getattr(harness, "probe_trigger", None)
    if probe is None:
        raise ValueError(f"Harness '{harness_name}' does not support trigger evals")
    return probe(
        query=query,
        skill_name=skill_name,
        skill_description=skill_description,
        project_root=project_root,
        timeout=timeout,
        model=model,
    )


def run_eval(
    eval_set: list[dict],
    skill_name: str,
    description: str,
    num_workers: int,
    timeout: int,
    runs_per_query: int = 1,
    trigger_threshold: float = 0.5,
    model: str | None = None,
    harness_name: str = "claude",
) -> dict:
    """Run the full eval set inside an isolated project directory."""
    if len(skill_name) > SKILL_NAME_MAX_LENGTH or not SKILL_NAME_PATTERN.match(skill_name):
        raise ValueError(
            f"Invalid skill name '{skill_name}': must match {SKILL_NAME_PATTERN.pattern}"
            f" and stay within {SKILL_NAME_MAX_LENGTH} characters"
        )

    get_harness(harness_name)

    isolated_root = Path(tempfile.mkdtemp(prefix="skill-trigger-eval-"))
    try:
        (isolated_root / ".claude" / "commands").mkdir(parents=True)
        return _run_eval_in_root(
            eval_set=eval_set,
            skill_name=skill_name,
            description=description,
            num_workers=num_workers,
            timeout=timeout,
            project_root=isolated_root,
            runs_per_query=runs_per_query,
            trigger_threshold=trigger_threshold,
            model=model,
            harness_name=harness_name,
        )
    finally:
        shutil.rmtree(isolated_root, ignore_errors=True)


def _run_eval_in_root(
    eval_set: list[dict],
    skill_name: str,
    description: str,
    num_workers: int,
    timeout: int,
    project_root: Path,
    runs_per_query: int,
    trigger_threshold: float,
    model: str | None,
    harness_name: str,
) -> dict:
    results = []

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        future_to_info = {}
        for item in eval_set:
            for run_idx in range(runs_per_query):
                future = executor.submit(
                    run_single_query,
                    item["query"],
                    skill_name,
                    description,
                    timeout,
                    str(project_root),
                    model,
                    harness_name,
                )
                future_to_info[future] = (item, run_idx)

        query_triggers: dict[str, list[bool]] = {}
        query_items: dict[str, dict] = {}
        for future in as_completed(future_to_info):
            item, _ = future_to_info[future]
            query = item["query"]
            query_items[query] = item
            if query not in query_triggers:
                query_triggers[query] = []
            try:
                query_triggers[query].append(future.result())
            # Worker failures become failed query results.
            except Exception as error:  # noqa: BLE001
                print(f"Warning: query failed: {error}", file=sys.stderr)
                query_triggers[query].append(False)

    for query, triggers in query_triggers.items():
        item = query_items[query]
        trigger_rate = sum(triggers) / len(triggers)
        should_trigger = item["should_trigger"]
        if should_trigger:
            did_pass = trigger_rate >= trigger_threshold
        else:
            did_pass = trigger_rate < trigger_threshold
        results.append({
            "query": query,
            "should_trigger": should_trigger,
            "trigger_rate": trigger_rate,
            "triggers": sum(triggers),
            "runs": len(triggers),
            "pass": did_pass,
        })

    passed = sum(1 for r in results if r["pass"])
    total = len(results)

    return {
        "skill_name": skill_name,
        "description": description,
        "results": results,
        "summary": {
            "total": total,
            "passed": passed,
            "failed": total - passed,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Run trigger evaluation for a skill description")
    parser.add_argument("--eval-set", required=True, help="Path to eval set JSON file")
    parser.add_argument("--skill-path", required=True, help="Path to skill directory")
    parser.add_argument("--description", default=None, help="Override description to test")
    parser.add_argument("--num-workers", type=int, default=10, help="Number of parallel workers")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout per query in seconds")
    parser.add_argument("--runs-per-query", type=int, default=3, help="Number of runs per query")
    parser.add_argument("--trigger-threshold", type=float, default=0.5, help="Trigger rate threshold")
    parser.add_argument("--model", default=None, help="Model to use (default: the harness's configured model)")
    parser.add_argument("--harness", default="claude", help="Harness adapter to use (default: claude)")
    parser.add_argument("--verbose", action="store_true", help="Print progress to stderr")
    args = parser.parse_args()

    eval_set = json.loads(Path(args.eval_set).read_text(encoding="utf-8"))
    skill_path = Path(args.skill_path)

    if not (skill_path / "SKILL.md").exists():
        print(f"Error: No SKILL.md found at {skill_path}", file=sys.stderr)
        sys.exit(1)

    name, original_description, _content = parse_skill_md(skill_path)
    description = args.description or original_description

    if args.verbose:
        print(f"Evaluating: {description}", file=sys.stderr)

    try:
        output = run_eval(
            eval_set=eval_set,
            skill_name=name,
            description=description,
            num_workers=args.num_workers,
            timeout=args.timeout,
            runs_per_query=args.runs_per_query,
            trigger_threshold=args.trigger_threshold,
            model=args.model,
            harness_name=args.harness,
        )
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.verbose:
        summary = output["summary"]
        print(f"Results: {summary['passed']}/{summary['total']} passed", file=sys.stderr)
        for r in output["results"]:
            status = "PASS" if r["pass"] else "FAIL"
            rate_str = f"{r['triggers']}/{r['runs']}"
            print(f"  [{status}] rate={rate_str} expected={r['should_trigger']}: {r['query'][:70]}", file=sys.stderr)

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
