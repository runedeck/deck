#!/usr/bin/env python3
"""Build the self-contained comparison report from benchmark.json.

Usage:
    python3 -m scripts.build_report <benchmark.json> [--output report.html]

Inlines the benchmark data into assets/report-template.html as UTF-8 base64,
so the report is one file that renders offline with no external requests.
"""

import argparse
import base64
import copy
import json
import sys
from pathlib import Path

TEMPLATE_PATH = Path(__file__).resolve().parent.parent / "assets" / "report-template.html"
DATA_PLACEHOLDER = "__BENCHMARK_DATA_BASE64__"
JUDGMENT_FIELDS = {
    "schema_version", "comparison", "eval_id", "model", "repeat", "run_number",
    "judge_route", "judge_model", "seed", "blind_order", "state",
    "clarity_winner", "clarity_winner_arm", "clarity_reason",
    "fluency_winner", "fluency_winner_arm", "fluency_reason",
    "directness_winner", "directness_winner_arm", "directness_reason",
}


def sanitize_report_data(benchmark: dict) -> dict:
    """Remove local paths and provider diagnostics from shareable data."""
    safe = copy.deepcopy(benchmark)
    metadata = safe.get("metadata")
    if isinstance(metadata, dict):
        artifact_path = metadata.get("artifact_path")
        if isinstance(artifact_path, str):
            metadata["artifact_path"] = Path(artifact_path).name
        identities = metadata.get("identities")
        if isinstance(identities, dict):
            for identity in identities.values():
                if isinstance(identity, dict) and isinstance(identity.get("path"), str):
                    identity_path = Path(identity["path"]).expanduser().resolve()
                    identity["path_url"] = identity_path.as_uri()
                    identity["path"] = identity_path.name
    manifest_path = (
        benchmark.get("metadata", {}).get("identities", {}).get("manifest", {}).get("path")
    )
    manifest_root = (
        Path(manifest_path).expanduser().resolve().parent
        if isinstance(manifest_path, str) else None
    )
    for spec in safe.get("arms", {}).values():
        if not isinstance(spec, dict) or not isinstance(spec.get("artifact_path"), str):
            continue
        artifact_path = Path(spec["artifact_path"]).expanduser()
        if not artifact_path.is_absolute():
            if manifest_root is None:
                continue
            artifact_path = manifest_root / artifact_path
        if spec.get("artifact_kind") == "skill":
            artifact_path /= "SKILL.md"
        spec["artifact_url"] = artifact_path.resolve().as_uri()
    for run in safe.get("runs", []):
        route = run.get("route") if isinstance(run, dict) else None
        if isinstance(route, dict) and isinstance(route.get("resolved_binary"), str):
            route["resolved_binary"] = Path(route["resolved_binary"]).name
    preferences = safe.get("preference_judgments")
    if isinstance(preferences, list):
        safe["preference_judgments"] = [
            {key: value for key, value in judgment.items() if key in JUDGMENT_FIELDS}
            for judgment in preferences if isinstance(judgment, dict)
        ]
    return safe


def build_report(benchmark_path: Path, output_path: Path) -> None:
    benchmark = json.loads(benchmark_path.read_text(encoding="utf-8"))
    if benchmark.get("schema_version") != 2:
        raise ValueError("benchmark schema_version must be 2")
    comparisons = benchmark.get("comparisons")
    if not isinstance(comparisons, list):
        raise TypeError("benchmark comparisons must be a list")
    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    encoded = base64.b64encode(
        json.dumps(sanitize_report_data(benchmark), ensure_ascii=False).encode("utf-8")
    ).decode("ascii")
    if DATA_PLACEHOLDER not in template:
        raise ValueError(f"template {TEMPLATE_PATH} is missing {DATA_PLACEHOLDER}")

    output_path.write_text(template.replace(DATA_PLACEHOLDER, encoded), encoding="utf-8")
    print(f"Generated: {output_path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the comparison report")
    parser.add_argument("benchmark", type=Path, help="Path to benchmark.json")
    parser.add_argument(
        "--output", "-o", type=Path,
        help="Output path (default: report.html beside benchmark.json)"
    )
    args = parser.parse_args()

    if not args.benchmark.is_file():
        print(f"Benchmark file not found: {args.benchmark}", file=sys.stderr)
        return 1

    output = args.output or args.benchmark.parent / "report.html"
    try:
        build_report(args.benchmark, output)
    except (TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
