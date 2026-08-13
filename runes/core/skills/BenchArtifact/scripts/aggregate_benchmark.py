#!/usr/bin/env python3
"""
Aggregate individual run results into benchmark summary statistics.

Reads grading.json files from run directories and produces:
- run_summary with mean, stddev, min, max for each metric, per configuration and model
- delta between the primary and baseline configurations, computed within each model

Usage:
    python3 -m scripts.aggregate_benchmark <benchmark_dir>

Example:
    python3 -m scripts.aggregate_benchmark benchmarks/2026-01-15T10-30-00/

A configuration directory may carry a model suffix after `@`, e.g.
`with_rule@claude-opus-5`. Runs then aggregate per configuration and model,
and each model gets its own delta (`delta` when one model ran, `delta@<model>`
when several did). Deltas are never averaged across models.

The delta direction is primary minus baseline. The pairs with_artifact vs
without_artifact, with_rule vs without_rule, with_agent vs without_agent,
with_skill vs without_skill, and new_artifact vs old_artifact are recognized
automatically; any other configuration names require --primary-config and
--baseline-config (base names, without the model suffix).

Expected directory layout:

    <benchmark_dir>/
    └── eval-N/
        ├── with_rule@claude-opus-5/
        │   ├── run-1/grading.json
        │   └── run-2/grading.json
        └── without_rule@claude-opus-5/
            ├── run-1/grading.json
            └── run-2/grading.json
"""

import argparse
import json
import math
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

KNOWN_CONFIG_PAIRS = (
    ("with_artifact", "without_artifact"),
    ("with_rule", "without_rule"),
    ("with_agent", "without_agent"),
    ("with_skill", "without_skill"),
    ("new_artifact", "old_artifact"),
    ("new_skill", "old_skill"),
)

DEFAULT_MODEL = "default"


def split_config(name: str) -> tuple[str, str]:
    """Split a configuration directory name into (base, model)."""
    if "@" in name:
        base, model = name.split("@", 1)
        return base, model or DEFAULT_MODEL
    return name, DEFAULT_MODEL


def calculate_stats(values: list[float]) -> dict:
    """Calculate mean, stddev, min, max, skipping unavailable (null) values."""
    values = [value for value in values if value is not None]
    if not values:
        return {"mean": 0.0, "stddev": 0.0, "min": 0.0, "max": 0.0}

    n = len(values)
    mean = sum(values) / n

    if n > 1:
        variance = sum((x - mean) ** 2 for x in values) / (n - 1)
        stddev = math.sqrt(variance)
    else:
        stddev = 0.0

    return {
        "mean": round(mean, 4),
        "stddev": round(stddev, 4),
        "min": round(min(values), 4),
        "max": round(max(values), 4)
    }


def load_run_results(benchmark_dir: Path) -> dict:
    """
    Load all run results from a benchmark directory.

    Returns dict keyed by configuration directory name (base plus optional
    `@model` suffix), each containing a list of run results.
    """
    if not list(benchmark_dir.glob("eval-*")):
        print(f"No eval directories found in {benchmark_dir}")
        return {}

    results: dict[str, list] = {}

    for eval_idx, eval_dir in enumerate(sorted(benchmark_dir.glob("eval-*"))):
        eval_id = eval_idx
        eval_name = None
        metadata_path = eval_dir / "eval_metadata.json"
        if metadata_path.exists():
            try:
                with open(metadata_path, encoding="utf-8") as mf:
                    metadata = json.load(mf)
                eval_id = metadata.get("eval_id", eval_idx)
                eval_name = metadata.get("eval_name") or metadata.get("name")
            except (json.JSONDecodeError, OSError):
                pass
        else:
            try:
                eval_id = int(eval_dir.name.split("-", 1)[1])
            except (IndexError, ValueError):
                pass

        # Discover config directories dynamically rather than hardcoding names
        for config_dir in sorted(eval_dir.iterdir()):
            if not config_dir.is_dir():
                continue
            # Skip non-config directories (inputs, outputs, etc.)
            if not list(config_dir.glob("run-*")):
                continue
            config = config_dir.name
            if config not in results:
                results[config] = []

            for run_dir in sorted(config_dir.glob("run-*")):
                try:
                    run_number = int(run_dir.name.split("-", 1)[1])
                except (IndexError, ValueError):
                    print(f"Warning: malformed run directory name '{run_dir.name}' in {config_dir}, skipping")
                    continue
                grading_file = run_dir / "grading.json"

                if not grading_file.exists():
                    print(f"Warning: grading.json not found in {run_dir}")
                    continue

                try:
                    with open(grading_file, encoding="utf-8") as f:
                        grading = json.load(f)
                except json.JSONDecodeError as e:
                    print(f"Warning: Invalid JSON in {grading_file}: {e}")
                    continue

                # Extract metrics
                result = {
                    "eval_id": eval_id,
                    "eval_name": eval_name,
                    "run_number": run_number,
                    "pass_rate": grading.get("summary", {}).get("pass_rate", 0.0),
                    "passed": grading.get("summary", {}).get("passed", 0),
                    "failed": grading.get("summary", {}).get("failed", 0),
                    "total": grading.get("summary", {}).get("total", 0),
                }

                # Extract timing — check grading.json first, then sibling timing.json
                timing = grading.get("timing", {})
                result["time_seconds"] = timing.get("total_duration_seconds", 0.0)
                timing_file = run_dir / "timing.json"
                if timing_file.exists():
                    try:
                        with open(timing_file, encoding="utf-8") as tf:
                            timing_data = json.load(tf)
                        if result["time_seconds"] == 0.0:
                            result["time_seconds"] = timing_data.get("total_duration_seconds", 0.0)
                        result["tokens"] = timing_data.get("total_tokens", 0)
                        if timing_data.get("model"):
                            result["model"] = timing_data["model"]
                    except json.JSONDecodeError:
                        pass

                # Extract metrics if available
                metrics = grading.get("execution_metrics", {})
                result["tool_calls"] = metrics.get("total_tool_calls", 0)
                if not result.get("tokens"):
                    result["tokens"] = metrics.get("output_chars", 0)
                result["errors"] = metrics.get("errors_encountered", 0)

                # Extract expectations — viewer requires fields: text, passed, evidence
                raw_expectations = grading.get("expectations", [])
                for exp in raw_expectations:
                    if "text" not in exp or "passed" not in exp:
                        print(f"Warning: expectation in {grading_file} missing required fields (text, passed, evidence): {exp}")
                result["expectations"] = raw_expectations

                # Extract notes from user_notes_summary
                notes_summary = grading.get("user_notes_summary", {})
                notes = []
                notes.extend(notes_summary.get("uncertainties", []))
                notes.extend(notes_summary.get("needs_review", []))
                notes.extend(notes_summary.get("workarounds", []))
                result["notes"] = notes

                results[config].append(result)

    return results


def resolve_config_pair(
    base_names: list[str],
    primary: str | None = None,
    baseline: str | None = None,
) -> tuple[str, str] | None:
    """Resolve the (primary, baseline) base-name pair for delta direction.

    Explicit flags win; otherwise known pairs are recognized. Returns None
    when the direction cannot be determined — never falls back to
    alphabetical or discovery order.
    """
    if primary or baseline:
        if not (primary and baseline):
            raise ValueError("--primary-config and --baseline-config must be given together")
        for name in (primary, baseline):
            if name not in base_names:
                raise ValueError(
                    f"Configuration '{name}' not found; discovered: {', '.join(sorted(base_names)) or '(none)'}"
                )
        return primary, baseline

    for pair in KNOWN_CONFIG_PAIRS:
        if pair[0] in base_names and pair[1] in base_names:
            return pair

    return None


def derive_runs_per_configuration(results: dict) -> int:
    """Derive runs-per-configuration from the discovered run directories."""
    counts = Counter()
    for config, runs in results.items():
        for run in runs:
            counts[(config, run["eval_id"])] += 1
    if not counts:
        return 0
    distinct = set(counts.values())
    if len(distinct) > 1:
        print(f"Warning: run counts differ across configurations: {sorted(distinct)}")
    return max(distinct)


def aggregate_results(results: dict, pair: tuple[str, str] | None) -> dict:
    """
    Aggregate run results into summary statistics.

    Returns run_summary keyed by configuration directory name, primary before
    baseline within each model when the pair is known, plus one delta entry
    per model (`delta` for a single model, `delta@<model>` for several).
    """
    run_summary = {}
    models = sorted({split_config(config)[1] for config in results})
    single_model = len(models) <= 1

    for model in models:
        model_configs = [c for c in results if split_config(c)[1] == model]
        if pair:
            ordered = [c for base in pair for c in model_configs if split_config(c)[0] == base]
            ordered += [c for c in model_configs if c not in ordered]
        else:
            ordered = sorted(model_configs)

        for config in ordered:
            runs = results.get(config, [])

            if not runs:
                run_summary[config] = {
                    "pass_rate": {"mean": 0.0, "stddev": 0.0, "min": 0.0, "max": 0.0},
                    "time_seconds": {"mean": 0.0, "stddev": 0.0, "min": 0.0, "max": 0.0},
                    "tokens": {"mean": 0, "stddev": 0, "min": 0, "max": 0}
                }
                continue

            run_summary[config] = {
                "pass_rate": calculate_stats([r["pass_rate"] for r in runs]),
                "time_seconds": calculate_stats([r["time_seconds"] for r in runs]),
                "tokens": calculate_stats([r.get("tokens", 0) for r in runs])
            }

        if not pair:
            continue

        by_base = {split_config(c)[0]: c for c in ordered}
        primary_name = by_base.get(pair[0])
        baseline_name = by_base.get(pair[1])
        if not (primary_name and baseline_name):
            print(f"Warning: model '{model}' is missing one side of {pair[0]} vs {pair[1]}; delta omitted for it")
            continue

        primary_summary = run_summary[primary_name]
        baseline_summary = run_summary[baseline_name]

        delta_pass_rate = primary_summary["pass_rate"]["mean"] - baseline_summary["pass_rate"]["mean"]
        delta_time = primary_summary["time_seconds"]["mean"] - baseline_summary["time_seconds"]["mean"]
        delta_tokens = primary_summary["tokens"]["mean"] - baseline_summary["tokens"]["mean"]

        delta_key = "delta" if single_model else f"delta@{model}"
        run_summary[delta_key] = {
            "pass_rate": f"{delta_pass_rate:+.2f}",
            "time_seconds": f"{delta_time:+.1f}",
            "tokens": f"{delta_tokens:+.0f}"
        }

    if not pair and len(results) >= 2:
        base_names = sorted({split_config(c)[0] for c in results})
        print(
            "Warning: cannot determine delta direction for configurations "
            f"{', '.join(base_names)}; pass --primary-config and --baseline-config. Delta omitted."
        )

    return run_summary


def generate_benchmark(
    benchmark_dir: Path,
    artifact_name: str = "",
    artifact_path: str = "",
    primary_config: str | None = None,
    baseline_config: str | None = None,
) -> dict:
    """
    Generate complete benchmark.json from run results.
    """
    results = load_run_results(benchmark_dir)
    base_names = sorted({split_config(c)[0] for c in results})
    pair = resolve_config_pair(base_names, primary_config, baseline_config)
    run_summary = aggregate_results(results, pair)
    models = sorted({split_config(c)[1] for c in results})

    # Build runs array for benchmark.json
    runs = []
    for config in results:
        base, model = split_config(config)
        for result in results[config]:
            runs.append({
                "eval_id": result["eval_id"],
                "eval_name": result.get("eval_name"),
                "configuration": config,
                "configuration_base": base,
                "model": result.get("model", model),
                "run_number": result["run_number"],
                "result": {
                    "pass_rate": result["pass_rate"],
                    "passed": result["passed"],
                    "failed": result["failed"],
                    "total": result["total"],
                    "time_seconds": result["time_seconds"],
                    "tokens": result.get("tokens", 0),
                    "tool_calls": result.get("tool_calls", 0),
                    "errors": result.get("errors", 0)
                },
                "expectations": result["expectations"],
                "notes": result["notes"]
            })

    # Determine eval IDs from results
    eval_ids = sorted({
        result["eval_id"]
        for config_results in results.values()
        for result in config_results
    })

    benchmark = {
        "metadata": {
            "artifact_name": artifact_name or "<artifact-name>",
            "artifact_path": artifact_path or "<path/to/artifact>",
            # The review viewer labels its Benchmark tab from skill_name.
            "skill_name": artifact_name or "<artifact-name>",
            "models": models,
            "analyzer_model": "<model-name>",
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "evals_run": eval_ids,
            "runs_per_configuration": derive_runs_per_configuration(results),
            "primary_config": pair[0] if pair else None,
            "baseline_config": pair[1] if pair else None
        },
        "runs": runs,
        "run_summary": run_summary,
        "notes": []  # To be filled by analyzer
    }

    return benchmark


def generate_markdown(benchmark: dict) -> str:
    """Generate human-readable benchmark.md from benchmark data."""
    metadata = benchmark["metadata"]
    run_summary = benchmark["run_summary"]

    models = metadata.get("models") or [DEFAULT_MODEL]
    lines = [
        f"# Artifact Benchmark: {metadata['artifact_name']}",
        "",
        f"**Models**: {', '.join(models)}",
        f"**Date**: {metadata['timestamp']}",
        f"**Evals**: {', '.join(map(str, metadata['evals_run']))} ({metadata['runs_per_configuration']} runs each per configuration)",
    ]

    for model in models:
        configs = [
            key for key in run_summary
            if not key.startswith("delta") and split_config(key)[1] == model
        ]
        if len(models) > 1:
            lines.extend(["", f"## {model}"])
        config_a = configs[0] if len(configs) >= 1 else "config_a"
        config_b = configs[1] if len(configs) >= 2 else "config_b"
        label_a = split_config(config_a)[0].replace("_", " ").title()
        label_b = split_config(config_b)[0].replace("_", " ").title()
        delta = run_summary.get("delta" if len(models) <= 1 else f"delta@{model}", {})

        a_summary = run_summary.get(config_a, {})
        b_summary = run_summary.get(config_b, {})
        a_pr = a_summary.get("pass_rate", {})
        b_pr = b_summary.get("pass_rate", {})
        a_time = a_summary.get("time_seconds", {})
        b_time = b_summary.get("time_seconds", {})
        a_tokens = a_summary.get("tokens", {})
        b_tokens = b_summary.get("tokens", {})

        lines.extend([
            "",
            f"| Metric | {label_a} | {label_b} | Delta |",
            "|--------|------------|---------------|-------|",
            f"| Pass Rate | {a_pr.get('mean', 0)*100:.0f}% ± {a_pr.get('stddev', 0)*100:.0f}% | {b_pr.get('mean', 0)*100:.0f}% ± {b_pr.get('stddev', 0)*100:.0f}% | {delta.get('pass_rate', '—')} |",
            f"| Time | {a_time.get('mean', 0):.1f}s ± {a_time.get('stddev', 0):.1f}s | {b_time.get('mean', 0):.1f}s ± {b_time.get('stddev', 0):.1f}s | {delta.get('time_seconds', '—')}s |",
            f"| Tokens | {a_tokens.get('mean', 0):.0f} ± {a_tokens.get('stddev', 0):.0f} | {b_tokens.get('mean', 0):.0f} ± {b_tokens.get('stddev', 0):.0f} | {delta.get('tokens', '—')} |",
        ])

    # Notes section
    if benchmark.get("notes"):
        lines.extend([
            "",
            "## Notes",
            ""
        ])
        for note in benchmark["notes"]:
            lines.append(f"- {note}")

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(
        description="Aggregate benchmark run results into summary statistics"
    )
    parser.add_argument(
        "benchmark_dir",
        type=Path,
        help="Path to the benchmark directory"
    )
    parser.add_argument(
        "--artifact-name",
        default="",
        help="Name of the artifact being benchmarked"
    )
    parser.add_argument(
        "--artifact-path",
        default="",
        help="Path to the artifact being benchmarked"
    )
    parser.add_argument(
        "--primary-config",
        default=None,
        help="Base configuration treated as primary in the delta (auto-detected for the with_/new_ families)"
    )
    parser.add_argument(
        "--baseline-config",
        default=None,
        help="Base configuration treated as baseline in the delta (auto-detected for the without_/old_ families)"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Output path for benchmark.json (default: <benchmark_dir>/benchmark.json)"
    )

    args = parser.parse_args()

    if not args.benchmark_dir.exists():
        print(f"Directory not found: {args.benchmark_dir}")
        sys.exit(1)

    # Generate benchmark
    try:
        benchmark = generate_benchmark(
            args.benchmark_dir,
            args.artifact_name,
            args.artifact_path,
            args.primary_config,
            args.baseline_config,
        )
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Determine output paths
    output_json = args.output or (args.benchmark_dir / "benchmark.json")
    output_md = output_json.with_suffix(".md")

    # Write benchmark.json
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(benchmark, f, indent=2)
        f.write("\n")
    print(f"Generated: {output_json}")

    # Write benchmark.md
    markdown = generate_markdown(benchmark)
    with open(output_md, "w", encoding="utf-8") as f:
        f.write(markdown)
    print(f"Generated: {output_md}")

    # Print summary
    run_summary = benchmark["run_summary"]
    configs = [k for k in run_summary if not k.startswith("delta")]

    print("\nSummary:")
    for config in configs:
        pr = run_summary[config]["pass_rate"]["mean"]
        label = config.replace("_", " ")
        print(f"  {label}: {pr*100:.1f}% pass rate")
    for key in run_summary:
        if key.startswith("delta"):
            print(f"  {key}: {run_summary[key].get('pass_rate', '—')}")


if __name__ == "__main__":
    main()
