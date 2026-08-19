#!/usr/bin/env python3
"""Aggregate named benchmark arms and explicit comparisons."""

import argparse
import copy
import hashlib
import json
import math
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote

SCHEMA_VERSION = 2
TOKEN_FIELDS = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens", "total_tokens")
PREFERENCE_FIELDS = {
    "clarity_preference": "clarity_winner_arm",
    "fluency_preference": "fluency_winner_arm",
    "directness_preference": "directness_winner_arm",
}
METRICS = (
    "assertion_pass_rate", "lint_violations", "lint_per100w", "word_count",
    *PREFERENCE_FIELDS, "duration_seconds", *TOKEN_FIELDS,
)


def read_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def split_arm(name: str) -> tuple[str, str]:
    arm, separator, model = name.partition("@")
    return arm, unquote(model) if separator and model else "default"


def stats(values) -> dict:
    clean = [float(value) for value in values if isinstance(value, (int, float)) and not isinstance(value, bool)]
    if not clean:
        return {"count": 0, "mean": None, "stddev": None, "min": None, "max": None}
    mean = sum(clean) / len(clean)
    variance = sum((value - mean) ** 2 for value in clean) / (len(clean) - 1) if len(clean) > 1 else 0.0
    return {
        "count": len(clean), "mean": round(mean, 4), "stddev": round(math.sqrt(variance), 4),
        "min": round(min(clean), 4), "max": round(max(clean), 4),
    }


def metric(source: dict, *names):
    for name in names:
        value = source.get(name)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return value
    return None


def first_number(*values):
    return next((value for value in values if value is not None), None)


def safe_exclusion_reason(state: str, error) -> str:
    if state in {"missing_execution", "missing_grading", "timeout"}:
        return state
    if state == "invalid_output" and isinstance(error, str):
        return error
    if state == "provider_failure" and isinstance(error, dict):
        code = error.get("exit_code", error.get("code"))
        return f"provider_failure (code {code})" if code is not None else state
    return state


def load_run(run_dir: Path, eval_id, eval_name, arm: str, model: str) -> dict:
    execution_path = run_dir / "result.json"
    grading_path = run_dir / "grading.json"
    execution = read_json(execution_path) if execution_path.is_file() else {}
    grading = read_json(grading_path) if grading_path.is_file() else {}
    summary = grading.get("summary") if isinstance(grading.get("summary"), dict) else {}
    lint = grading.get("lint") if isinstance(grading.get("lint"), dict) else {}
    usage = execution.get("usage") if isinstance(execution.get("usage"), dict) else {}
    execution_result = grading.get("result") if isinstance(grading.get("result"), dict) else {}
    state = execution.get("state", "missing_execution")
    valid = state == "valid" and bool(grading)
    result_state = "valid" if valid else state if state != "valid" else "missing_grading"
    exclusion_reason = None if valid else safe_exclusion_reason(result_state, execution.get("error"))
    result = {
        "assertion_pass_rate": metric(summary, "pass_rate"),
        "assertions_passed": metric(summary, "passed"),
        "assertions_total": metric(summary, "total"),
        "lint_violations": first_number(metric(lint, "total", "raw_violations"), metric(execution_result, "lint_violations")),
        "lint_per100w": first_number(metric(lint, "total_per100w", "violations_per100w"), metric(execution_result, "lint_per100w")),
        "checker_word_count": metric(lint, "words"),
        "word_count": first_number(metric(execution, "word_count"), metric(lint, "words"), metric(execution_result, "word_count")),
        "clarity_preference": first_number(metric(grading, "clarity_preference"), metric(execution_result, "clarity_preference")),
        "fluency_preference": first_number(metric(grading, "fluency_preference"), metric(execution_result, "fluency_preference")),
        "directness_preference": first_number(metric(grading, "directness_preference"), metric(execution_result, "directness_preference")),
        "duration_seconds": first_number(metric(execution, "duration_seconds"), metric(execution_result, "duration_seconds")),
    }
    for field in TOKEN_FIELDS:
        result[field] = first_number(metric(usage, field), metric(execution_result, field))
    return {
        "eval_id": eval_id, "eval_name": eval_name, "arm": arm, "model": execution.get("model", model),
        "route": execution.get("route"), "run_number": int(run_dir.name.split("-", 1)[1]),
        "state": result_state,
        "valid": valid, "exclusion_reason": exclusion_reason,
        "result": result, "expectations": grading.get("expectations", []),
        "response": execution.get("response") if isinstance(execution.get("response"), str) else None,
        "notes": grading.get("notes", execution.get("notes", [])),
    }


def missing_run(case: dict, arm: str, route: dict, repeat: int) -> dict:
    result = {name: None for name in METRICS}
    result.update({"assertions_passed": None, "assertions_total": None})
    return {
        "eval_id": case["id"], "eval_name": case.get("name"),
        "arm": arm, "model": route["model"],
        "route": {"requested_route": route["id"]}, "run_number": repeat,
        "state": "missing_execution", "valid": False,
        "exclusion_reason": "missing_execution", "result": result,
        "expectations": [], "response": None, "notes": [],
    }


def apply_run_plan(runs: list[dict], manifest: dict) -> list[dict]:
    plan = manifest.get("run_plan")
    if not isinstance(plan, dict):
        return runs
    routes = plan.get("routes")
    repeats = plan.get("repeats")
    cases = manifest.get("evals")
    arms = manifest.get("arms")
    if (
        not isinstance(routes, list) or not routes
        or not all(
            isinstance(route, dict)
            and isinstance(route.get("id"), str)
            and isinstance(route.get("model"), str)
            for route in routes
        )
        or not isinstance(repeats, int) or isinstance(repeats, bool) or repeats < 1
        or not isinstance(cases, list) or not cases
        or not isinstance(arms, dict) or not arms
    ):
        raise ValueError("frozen run plan is invalid")
    planned = [
        (case, arm, route, repeat)
        for case in cases
        for arm in arms
        for route in routes
        for repeat in range(1, repeats + 1)
    ]
    by_key = {
        (str(run["eval_id"]), run["arm"], run["model"], run["run_number"]): run
        for run in runs
    }
    planned_keys = {
        (str(case["id"]), arm, route["model"], repeat)
        for case, arm, route, repeat in planned
    }
    extras = set(by_key) - planned_keys
    if extras:
        raise ValueError("run records do not match the frozen run plan")
    return [
        by_key.get(
            (str(case["id"]), arm, route["model"], repeat),
            missing_run(case, arm, route, repeat),
        )
        for case, arm, route, repeat in planned
    ]
def discover(root: Path) -> list[dict]:
    runs = []
    for eval_dir in sorted(root.glob("eval-*")):
        metadata_path = eval_dir / "eval_metadata.json"
        metadata = read_json(metadata_path) if metadata_path.is_file() else {}
        pieces = eval_dir.name.split("-", 2)
        eval_id = metadata.get("eval_id", pieces[1] if len(pieces) > 1 else eval_dir.name)
        eval_name = metadata.get("eval_name", metadata.get("name", pieces[2] if len(pieces) > 2 else None))
        for arm_dir in sorted(path for path in eval_dir.iterdir() if path.is_dir()):
            arm, model = split_arm(arm_dir.name)
            for run_dir in sorted(arm_dir.glob("run-*")):
                try:
                    runs.append(load_run(run_dir, eval_id, eval_name, arm, model))
                except (json.JSONDecodeError, OSError, ValueError) as error:
                    print(f"Warning: cannot load {run_dir}: {error}", file=sys.stderr)
    return runs


def discover_judgments(root: Path) -> list[dict]:
    judgments = []
    judgment_root = root / "preferences"
    if judgment_root.is_dir():
        for path in sorted(judgment_root.glob("**/*.json")):
            try:
                judgment = read_json(path)
            except (json.JSONDecodeError, OSError):
                continue
            if judgment.get("state") == "valid":
                parts = path.relative_to(judgment_root).parts
                eval_dir = path.parent.parent.name
                run_name = path.stem
                if parts and not judgment.get("comparison"):
                    judgment["comparison"] = parts[0]
                if eval_dir.startswith("eval-"):
                    judgment["eval_id"] = eval_dir.removeprefix("eval-")
                if run_name.startswith("run-"):
                    try:
                        judgment["run_number"] = int(run_name.removeprefix("run-"))
                    except ValueError:
                        pass
                blind_order = judgment.get("blind_order", {})
                for dimension in ("clarity", "fluency", "directness"):
                    arm_field = f"{dimension}_winner_arm"
                    winner = str(judgment.get(f"{dimension}_winner", "")).casefold()
                    if not judgment.get(arm_field) and winner == "tie":
                        judgment[arm_field] = "tie"
                    elif not judgment.get(arm_field) and winner in {"a", "b"} and isinstance(blind_order, dict):
                        judgment[arm_field] = blind_order.get(winner.upper())
                judgments.append(judgment)
    return judgments


def corpus_metrics(runs: list[dict]) -> dict:
    """Calculate corpus ratios from raw totals instead of response-level means."""
    assertions_passed = sum(
        value for run in runs
        if isinstance((value := run["result"].get("assertions_passed")), (int, float))
        and not isinstance(value, bool)
    )
    assertions_total = sum(
        value for run in runs
        if isinstance((value := run["result"].get("assertions_total")), (int, float))
        and not isinstance(value, bool)
    )
    lint_violations = sum(
        value for run in runs
        if isinstance((value := run["result"].get("lint_violations")), (int, float))
        and not isinstance(value, bool)
    )
    checker_word_count = sum(
        value for run in runs
        if isinstance(
            (value := first_number(
                run["result"].get("checker_word_count"),
                run["result"].get("word_count"),
            )),
            (int, float),
        )
        and not isinstance(value, bool)
    )
    return {
        "assertions_passed": assertions_passed,
        "assertions_total": assertions_total,
        "assertion_pass_rate": round(assertions_passed / assertions_total, 4) if assertions_total else None,
        "lint_violations": lint_violations,
        "word_count": checker_word_count,
        "lint_per100w": round(lint_violations * 100.0 / checker_word_count, 4)
        if checker_word_count else None,
    }


def summarize(runs: list[dict], arms: list[str]) -> dict:
    models = sorted({run["model"] for run in runs})
    result = {}
    for model in models:
        result[model] = {}
        for arm in arms:
            selected = [run for run in runs if run["model"] == model and run["arm"] == arm]
            valid = [run for run in selected if run["valid"]]
            reasons = Counter(run["exclusion_reason"] for run in selected if not run["valid"])
            result[model][arm] = {
                "planned_samples": len(selected), "valid_samples": len(valid),
                "exclusions": len(selected) - len(valid), "exclusion_reasons": dict(reasons),
                "metrics": {name: stats(run["result"].get(name) for run in valid) for name in METRICS},
            }
    return result


def compare(summaries: dict, comparisons: list[dict], judgments: list[dict], runs: list[dict]) -> list[dict]:
    output = []
    for definition in comparisons:
        models = {}
        for model, arms in summaries.items():
            primary = copy.deepcopy(arms.get(definition["primary"]))
            baseline = copy.deepcopy(arms.get(definition["baseline"]))
            valid_winners = {definition["primary"], definition["baseline"], "tie"}
            model_runs = [run for run in runs if run["model"] == model and run["valid"]]
            by_arm = {
                arm: {(run["eval_id"], run["run_number"]): run for run in model_runs if run["arm"] == arm}
                for arm in (definition["primary"], definition["baseline"])
            }
            pair_keys = sorted(set(by_arm[definition["primary"]]) & set(by_arm[definition["baseline"]]))
            comparable_keys = {(str(eval_id), run_number) for eval_id, run_number in pair_keys}
            comparable_judgments = [
                judgment for judgment in judgments
                if judgment.get("comparison") == definition.get("id")
                and judgment.get("model") == model
                and (str(judgment.get("eval_id")), judgment.get("run_number")) in comparable_keys
            ]
            preferences = {}
            for metric_name, winner_field in PREFERENCE_FIELDS.items():
                values = [
                    0.5 if judgment.get(winner_field) == "tie"
                    else 1.0 if judgment.get(winner_field) == definition["primary"]
                    else 0.0
                    for judgment in comparable_judgments
                    if judgment.get(winner_field) in valid_winners
                ]
                preferences[metric_name] = values
                if values and primary:
                    primary["metrics"][metric_name] = stats(values)
                if values and baseline:
                    baseline["metrics"][metric_name] = stats(1.0 - value for value in values)
            delta_stats = {}
            for name in METRICS:
                values = []
                for key in pair_keys:
                    left = by_arm[definition["primary"]][key]["result"].get(name)
                    right = by_arm[definition["baseline"]][key]["result"].get(name)
                    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                        values.append(left - right)
                delta_stats[name] = stats(values)
            for metric_name, values in preferences.items():
                if values:
                    delta_stats[metric_name] = stats(2.0 * value - 1.0 for value in values)
            deltas = {name: delta_stats[name]["mean"] for name in METRICS}
            primary_runs = [by_arm[definition["primary"]][key] for key in pair_keys]
            baseline_runs = [by_arm[definition["baseline"]][key] for key in pair_keys]
            primary_corpus = corpus_metrics(primary_runs)
            baseline_corpus = corpus_metrics(baseline_runs)
            corpus_deltas = {
                name: round(primary_corpus[name] - baseline_corpus[name], 4)
                if isinstance(primary_corpus[name], (int, float))
                and isinstance(baseline_corpus[name], (int, float)) else None
                for name in ("assertion_pass_rate", "lint_per100w")
            }
            deltas.update(corpus_deltas)
            models[model] = {
                "primary": primary,
                "baseline": baseline,
                "paired_samples": len(pair_keys),
                "planned_pairs": max(primary["planned_samples"] if primary else 0, baseline["planned_samples"] if baseline else 0),
                "deltas": deltas,
                "delta_stats": delta_stats,
                "paired_corpus": {
                    "primary": primary_corpus,
                    "baseline": baseline_corpus,
                    "deltas": corpus_deltas,
                },
            }
        output.append({**definition, "models": models})
    return output


def generate(root: Path, manifest_path: Path | None, artifact_name: str, artifact_path: str) -> dict:
    if manifest_path is None and (root / "manifest.json").is_file():
        manifest_path = root / "manifest.json"
    manifest = read_json(manifest_path) if manifest_path else {}
    runs = apply_run_plan(discover(root), manifest)
    discovered_arms = sorted({run["arm"] for run in runs})
    arms = list(manifest.get("arms", {})) or discovered_arms
    comparisons = manifest.get("comparisons", [])
    if not comparisons and len(arms) == 2:
        baseline = "baseline" if "baseline" in arms else arms[1]
        primary = next(arm for arm in arms if arm != baseline)
        comparisons = [{"id": "comparison", "label": "Comparison", "primary": primary, "baseline": baseline}]
    summaries = summarize(runs, arms)
    judgments = discover_judgments(root)
    identities = copy.deepcopy(manifest.get("identities", {}))
    if manifest_path:
        identities["manifest"] = {"path": str(manifest_path.resolve()), "sha256": digest(manifest_path)}
    return {
        "schema_version": SCHEMA_VERSION,
        "metadata": {
            "artifact_name": artifact_name or manifest.get("artifact_name", "<artifact-name>"),
            "artifact_path": artifact_path or None,
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "models": sorted(summaries), "arms": arms,
            "run_counts": {"total": len(runs), "valid": sum(run["valid"] for run in runs), "excluded": sum(not run["valid"] for run in runs)},
            "identities": identities,
        },
        "arms": manifest.get("arms", {arm: {} for arm in arms}),
        "comparisons": compare(summaries, comparisons, judgments, runs),
        "summaries": summaries,
        "runs": runs,
        "preference_judgments": judgments,
        "notes": manifest.get("notes", []),
        "limitations": manifest.get("limitations", [
            "Compare results only within one model.",
            "Lint uses heuristics and does not measure semantic quality.",
            "Assertions measure only their stated checks.",
            "Missing tokens mean the provider did not report usage.",
            "Invalid and excluded runs reduce the sample.",
            "The report does not average models.",
        ]),
    }


def format_cell(value, digits=2):
    return "—" if value is None else f"{value:.{digits}f}"


def preference_cell(value):
    if value is None:
        return "—"
    return f"{value:+.2f}"


def markdown(data: dict) -> str:
    """One compact table per executed comparison, ready for a pull request body."""
    lines = [f"# Artifact Benchmark: {data['metadata']['artifact_name']}", ""]
    for comparison in data["comparisons"]:
        cells = comparison["models"]
        if not any((values.get("paired_samples") or 0) > 0 for values in cells.values()):
            continue
        explainer = (
            "Deltas are treatment minus baseline within one model. "
            "Lower lint density is better. Preferences run from -1 (baseline) to +1 (treatment)."
        )
        lines.extend([
            f"## {comparison.get('label', comparison['id'])}", "",
            explainer, "",
            "| Model | Pairs | Assertions | Lint /100w | Clarity | Fluency | Directness |",
            "|---|---:|---|---|---:|---:|---:|",
        ])
        for model, values in cells.items():
            pairs = values.get("paired_samples") or 0
            if pairs == 0:
                lines.append(f"| {model} | 0 | — | — | — | — | — |")
                continue
            corpus = values.get("paired_corpus") or {}
            base, treat = corpus.get("baseline", {}), corpus.get("primary", {})
            deltas = values.get("deltas") or {}
            assertion = (
                f"{format_cell(base.get('assertion_pass_rate'))} → "
                f"{format_cell(treat.get('assertion_pass_rate'))}"
            )
            lint = (
                f"{format_cell(base.get('lint_per100w'))} → "
                f"{format_cell(treat.get('lint_per100w'))}"
            )
            lines.append(
                f"| {model} | {pairs} | {assertion} | {lint} "
                f"| {preference_cell(deltas.get('clarity_preference'))} "
                f"| {preference_cell(deltas.get('fluency_preference'))} "
                f"| {preference_cell(deltas.get('directness_preference'))} |"
            )
        lines.append("")
    if data["limitations"]:
        lines.extend(["## Limitations", "", *(f"- {item}" for item in data["limitations"]), ""])
    return "\n".join(lines)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Aggregate named benchmark arms")
    parser.add_argument("benchmark_dir", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--artifact-name", default="")
    parser.add_argument("--artifact-path", default="")
    parser.add_argument("--output", "-o", type=Path)
    args = parser.parse_args(argv)
    try:
        data = generate(args.benchmark_dir, args.manifest, args.artifact_name, args.artifact_path)
        output = args.output or args.benchmark_dir / "benchmark.json"
        output.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        output.with_suffix(".md").write_text(markdown(data), encoding="utf-8")
        print(f"Generated: {output}")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
