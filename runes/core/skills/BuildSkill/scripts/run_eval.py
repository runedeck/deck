#!/usr/bin/env python3
"""Measure how often the agent picks a skill for each query of an eval set.

Every query is probed ``runs_per_query`` times inside a throwaway project
directory, optionally across a pool of worker processes. The per-query
trigger rate is then compared with a threshold to decide pass or fail.

Usage, from the skill directory:

    python3 -m scripts.run_eval --eval-set evals.json --skill-path ../my-skill
"""

import argparse
import json
import re
import shutil
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from pathlib import Path

from scripts.harness import get_harness
from scripts.utils import parse_skill_md

SKILL_NAME_MAX_LENGTH = 64
_SKILL_NAME_PATTERN = re.compile(r"^[A-Za-z0-9]+(?:[-_][A-Za-z0-9]+)*$")
QUERY_DISPLAY_WIDTH = 70


@dataclass(frozen=True)
class ProbeJob:
    """One probe of one query; picklable so a process pool can carry it."""

    query: str
    skill_name: str
    description: str
    project_root: str
    timeout: int
    model: str | None
    harness_name: str


def validate_skill_name(skill_name: str) -> None:
    """Raise ValueError unless the name fits the allowed shape."""
    if len(skill_name) > SKILL_NAME_MAX_LENGTH:
        raise ValueError(
            f"skill name {skill_name!r} is longer than {SKILL_NAME_MAX_LENGTH} characters"
        )
    if not _SKILL_NAME_PATTERN.match(skill_name):
        raise ValueError(
            f"skill name {skill_name!r} must be groups of letters and digits "
            "joined by single '-' or '_' characters"
        )


def validate_eval_set(eval_set: list[dict]) -> None:
    """Raise ValueError on malformed items or repeated query text."""
    seen: set[str] = set()
    for position, item in enumerate(eval_set):
        if not isinstance(item, dict) or "query" not in item or "should_trigger" not in item:
            raise ValueError(
                f"eval set item {position} must be an object with 'query' and 'should_trigger'"
            )
        query = item["query"]
        if not isinstance(query, str):
            # A malformed eval set is bad input; callers report every input error as ValueError.
            raise ValueError(f"eval set item {position}: 'query' must be a string")  # noqa: TRY004
        if query in seen:
            raise ValueError(f"duplicate query in eval set: {query!r}")
        seen.add(query)


def run_probe(job: ProbeJob) -> bool:
    """Run one probe. A failure counts as not picked and is reported on stderr."""
    try:
        harness = get_harness(job.harness_name)
        picked = harness.probe_trigger(
            job.query,
            job.skill_name,
            job.description,
            job.project_root,
            job.timeout,
            model=job.model,
        )
        return bool(picked)
    # Any probe failure counts as not picked, so one broken run cannot stop the eval.
    except Exception as exc:  # noqa: BLE001
        shown = job.query[:QUERY_DISPLAY_WIDTH]
        print(f"warning: probe failed for {shown!r}: {exc}", file=sys.stderr)
        return False


def shorten_query(query: str, width: int = QUERY_DISPLAY_WIDTH) -> str:
    """Return the query on one line, cut to ``width`` characters."""
    return " ".join(query.split())[:width]


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
    """Probe every query and report trigger rates against the threshold."""
    validate_eval_set(eval_set)
    validate_skill_name(skill_name)
    if runs_per_query < 1:
        raise ValueError("runs_per_query must be at least 1")

    harness = get_harness(harness_name)
    if not hasattr(harness, "probe_trigger"):
        raise ValueError(f"harness {harness_name!r} does not support trigger probes")

    project_root = tempfile.mkdtemp(prefix="trigger-eval-")
    try:
        (Path(project_root) / ".claude" / "commands").mkdir(parents=True, exist_ok=True)
        jobs = [
            ProbeJob(
                query=item["query"],
                skill_name=skill_name,
                description=description,
                project_root=project_root,
                timeout=timeout,
                model=model,
                harness_name=harness_name,
            )
            for item in eval_set
            for _ in range(runs_per_query)
        ]
        if num_workers > 1:
            with ProcessPoolExecutor(max_workers=num_workers) as pool:
                outcomes = list(pool.map(run_probe, jobs))
        else:
            outcomes = [run_probe(job) for job in jobs]
    finally:
        shutil.rmtree(project_root, ignore_errors=True)

    results = []
    for position, item in enumerate(eval_set):
        picks = outcomes[position * runs_per_query : (position + 1) * runs_per_query]
        triggers = sum(1 for picked in picks if picked)
        rate = triggers / runs_per_query
        should_trigger = bool(item["should_trigger"])
        passed = rate >= trigger_threshold if should_trigger else rate < trigger_threshold
        results.append(
            {
                "query": item["query"],
                "should_trigger": should_trigger,
                "trigger_rate": rate,
                "triggers": triggers,
                "runs": runs_per_query,
                "pass": passed,
            }
        )

    passed_count = sum(1 for result in results if result["pass"])
    return {
        "skill_name": skill_name,
        "description": description,
        "results": results,
        "summary": {
            "total": len(results),
            "passed": passed_count,
            "failed": len(results) - passed_count,
        },
    }


def print_verbose_summary(result: dict, stream=None) -> None:
    """Print the tested description, the pass count, and one line per query."""
    stream = stream or sys.stderr
    summary = result["summary"]
    print(f"Description under test: {result['description']}", file=stream)
    print(f"Passed {summary['passed']}/{summary['total']}", file=stream)
    for entry in result["results"]:
        status = "PASS" if entry["pass"] else "FAIL"
        expected = "should trigger" if entry["should_trigger"] else "should not trigger"
        print(
            f"  {status}  {entry['triggers']}/{entry['runs']} picks  "
            f"{expected:<18}  {shorten_query(entry['query'])}",
            file=stream,
        )


def load_eval_set(path: Path) -> list[dict]:
    """Read an eval set file; raise ValueError when it is not a JSON list."""
    with Path(path).open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        # A malformed eval set is bad input; the command line reports it as ValueError.
        raise ValueError(f"{path}: the eval set must be a JSON array")  # noqa: TRY004
    return data


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Measure how often a skill triggers for each eval query"
    )
    parser.add_argument("--eval-set", type=Path, required=True, help="eval set JSON file")
    parser.add_argument("--skill-path", type=Path, required=True, help="skill directory")
    parser.add_argument(
        "--description",
        default=None,
        help="test this description instead of the one in SKILL.md",
    )
    parser.add_argument("--num-workers", type=int, default=10)
    parser.add_argument("--timeout", type=int, default=30, help="seconds per probe")
    parser.add_argument("--runs-per-query", type=int, default=3)
    parser.add_argument("--trigger-threshold", type=float, default=0.5)
    parser.add_argument("--model", default=None)
    parser.add_argument("--harness", default="claude")
    parser.add_argument("--verbose", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)

    if not (args.skill_path / "SKILL.md").is_file():
        print(f"error: no SKILL.md in {args.skill_path}", file=sys.stderr)
        sys.exit(1)

    try:
        skill_name, frontmatter_description, _ = parse_skill_md(args.skill_path)
        eval_set = load_eval_set(args.eval_set)
        description = (
            args.description if args.description is not None else frontmatter_description
        )
        result = run_eval(
            eval_set,
            skill_name,
            description,
            num_workers=args.num_workers,
            timeout=args.timeout,
            runs_per_query=args.runs_per_query,
            trigger_threshold=args.trigger_threshold,
            model=args.model,
            harness_name=args.harness,
        )
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.verbose:
        print_verbose_summary(result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
