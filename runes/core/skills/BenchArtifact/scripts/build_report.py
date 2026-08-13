#!/usr/bin/env python3
"""Build the self-contained comparison report from benchmark.json.

Usage:
    python3 -m scripts.build_report <benchmark.json> [--output report.html]

Inlines the benchmark data into assets/report-template.html as UTF-8 base64,
so the report is one file that renders offline with no external requests.
"""

import argparse
import base64
import json
import sys
from pathlib import Path

TEMPLATE_PATH = Path(__file__).resolve().parent.parent / "assets" / "report-template.html"
DATA_PLACEHOLDER = "__BENCHMARK_DATA_BASE64__"


def build_report(benchmark_path: Path, output_path: Path) -> None:
    benchmark = json.loads(benchmark_path.read_text(encoding="utf-8"))
    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    encoded = base64.b64encode(
        json.dumps(benchmark, ensure_ascii=False).encode("utf-8")
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
    except (ValueError, json.JSONDecodeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
