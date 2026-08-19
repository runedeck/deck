#!/usr/bin/env python3
"""Run blinded clarity, fluency, and directness judgments for valid pairs."""

import argparse
import json
import random
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import quote

DEFAULT_JUDGING_PATH = Path(__file__).resolve().parent.parent / "config" / "judging.json"
DEFAULT_JUDGING = json.loads(DEFAULT_JUDGING_PATH.read_text(encoding="utf-8"))


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def pair_key(result: dict) -> tuple:
    return int(result["eval_id"]), result["model"], int(result["repeat"])


def collect(iteration: Path) -> dict[tuple, dict[str, Path]]:
    pairs: dict[tuple, dict[str, Path]] = {}
    for path in iteration.glob("eval-*/**/result.json"):
        result = load(path)
        if result.get("state") != "valid":
            continue
        pairs.setdefault(pair_key(result), {})[result["arm"]] = path
    return pairs


def prompt(case: dict, left: str, right: str, judging: dict) -> str:
    criteria = "\n".join(
        f"{dimension['label']}: {dimension['criterion']}" for dimension in judging["dimensions"]
    )
    guards = "\n".join(judging.get("guards", []))
    schema = ",\n".join(
        f'  "{dimension["id"]}": {{"winner": "A"|"B"|"tie", "reason": "one short sentence"}}'
        for dimension in judging["dimensions"]
    )
    return f"""Compare two rewrites without knowing which treatment produced them.

Judge each dimension independently.

{criteria}

{guards}

Task context:
{case['prompt']}

Output A:
---
{left.strip()}
---

Output B:
---
{right.strip()}
---

Return one JSON object only:
{{
{schema}
}}
"""


def parse(stdout: str, dimension_ids: tuple = ("clarity", "fluency", "directness")) -> dict:
    data = json.loads(stdout)
    text = next(
        (data.get(key) for key in ("text", "response", "output") if isinstance(data.get(key), str)),
        "",
    )
    lines = text.strip().splitlines()
    if len(lines) >= 3 and lines[0] in {"```", "```json"} and lines[-1] == "```":
        text = "\n".join(lines[1:-1])
    verdict = json.loads(text)
    for dimension in dimension_ids:
        result = verdict.get(dimension)
        if not isinstance(result, dict):
            raise TypeError(f"judge result needs {dimension}")
        if result.get("winner") not in {"A", "B", "tie"}:
            raise ValueError(f"{dimension} winner must be A, B, or tie")
        if not isinstance(result.get("reason"), str) or not result["reason"].strip():
            raise ValueError(f"{dimension} reason must be a non-empty string")
    return verdict


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--iteration", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--routes", type=Path, required=True)
    parser.add_argument("--judge-route", required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--model", action="append")
    parser.add_argument("--timeout", type=float, default=300)
    args = parser.parse_args()
    manifest = load(args.manifest)
    judging = manifest.get("judging") or DEFAULT_JUDGING
    dimension_ids = tuple(dimension["id"] for dimension in judging["dimensions"])
    cases = {int(case["id"]): case for case in manifest["evals"]}
    route = load(args.routes)["routes"][args.judge_route]
    selected_models = set(args.model or [])
    pairs = collect(args.iteration)
    output_root = args.iteration / "preferences"
    output_root.mkdir(exist_ok=True)
    count = 0
    for comparison in manifest["comparisons"]:
        primary = comparison["primary"]
        baseline = comparison["baseline"]
        for key, arms in sorted(pairs.items()):
            if primary not in arms or baseline not in arms:
                continue
            eval_id, model, repeat = key
            if selected_models and model not in selected_models:
                continue
            pair_seed = f"{args.seed}:{comparison['id']}:{eval_id}:{model}:{repeat}"
            left_arm, right_arm = (
                (primary, baseline)
                if random.Random(pair_seed).randrange(2) == 0
                else (baseline, primary)
            )
            texts = {
                arm: (arms[arm].parent / "outputs" / "response.md").read_text(encoding="utf-8")
                for arm in (left_arm, right_arm)
            }
            target = (
                output_root / comparison["id"] / f"eval-{eval_id}"
                / quote(model, safe="._-") / f"run-{repeat}.json"
            )
            if target.is_file() and load(target).get("state") == "valid":
                continue
            blind = {"A": left_arm, "B": right_arm}
            judge_prompt = prompt(cases[eval_id], texts[left_arm], texts[right_arm], judging)
            print(
                f"Progress: event=judgment-start comparison={comparison['id']} "
                f"case={eval_id} model={model} judge={route['model']}",
                flush=True,
            )
            timed_out = False
            with tempfile.TemporaryDirectory(prefix="bench-judge-") as scratch:
                prompt_file = Path(scratch) / "prompt.txt"
                prompt_file.write_text(judge_prompt, encoding="utf-8")
                context = {
                    "scratch": scratch,
                    "prompt_file": str(prompt_file),
                    "prompt": judge_prompt,
                    "artifact": "",
                    "artifact_source": "",
                    "model": route["model"],
                    "state": str(Path(scratch) / "state"),
                }
                argv = [route["binary"], *(part.format_map(context) for part in route["argv"])]
                try:
                    process = subprocess.run(
                        argv, text=True, capture_output=True, timeout=args.timeout, check=False,
                    )
                except subprocess.TimeoutExpired:
                    timed_out = True
            record = {
                "schema_version": 2,
                "comparison": comparison["id"],
                "eval_id": eval_id,
                "model": model,
                "repeat": repeat,
                "judge_route": args.judge_route,
                "judge_model": route["model"],
                "seed": args.seed,
                "blind_order": blind,
                "state": "timeout" if timed_out else "valid" if process.returncode == 0 else "provider_failure",
                "returncode": None if timed_out else process.returncode,
                "stderr": "" if timed_out else process.stderr,
            }
            if timed_out:
                record["error"] = f"judge call timed out after {args.timeout} seconds"
            elif process.returncode == 0:
                try:
                    verdict = parse(process.stdout, dimension_ids)
                    for dimension in dimension_ids:
                        winner = verdict[dimension]["winner"]
                        winner_arm = blind.get(winner) if winner != "tie" else "tie"
                        record.update({
                            f"{dimension}_winner": winner,
                            f"{dimension}_winner_arm": winner_arm,
                            f"{dimension}_reason": verdict[dimension]["reason"],
                        })
                except (json.JSONDecodeError, TypeError, ValueError) as error:
                    record.update({"state": "invalid_output", "error": str(error), "stdout": process.stdout})
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            print(
                f"Progress: event=judgment-finish comparison={comparison['id']} "
                f"case={eval_id} model={model} state={record['state']}",
                flush=True,
            )
            count += 1
    print(f"Wrote {count} blinded preference judgments.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
