#!/usr/bin/env python3
"""Run blinded clarity, fluency, and directness judgments for valid pairs."""

import argparse
import json
import random
import shutil
import sys
from pathlib import Path
from urllib.parse import quote

if __package__:
    from . import run_benchmark
else:
    import run_benchmark

DEFAULT_JUDGING_PATH = Path(__file__).resolve().parent.parent / "config" / "judging.json"
DEFAULT_JUDGING = json.loads(DEFAULT_JUDGING_PATH.read_text(encoding="utf-8"))


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def pair_key(result: dict) -> tuple:
    return int(result["eval_id"]), result["model"], int(result["repeat"])


def collect(iteration: Path, manifest: dict) -> dict[tuple, dict[str, Path]]:
    pairs: dict[tuple, dict[str, Path]] = {}
    cases = {int(case["id"]): case for case in manifest["evals"]}
    run_plan = run_benchmark.normalize_run_plan(manifest, required=True)
    for path in iteration.glob("eval-*/**/result.json"):
        if path.is_symlink() or not path.resolve().is_relative_to(iteration):
            raise ValueError(f"{path} is not a local result file")
        result = load(path)
        _, response, _ = run_benchmark.validate_execution(
            path, result, iteration, manifest, cases, run_plan,
        )
        if response is None:
            continue
        pairs.setdefault(pair_key(result), {})[result["arm"]] = path
    return pairs


def judgment_schedule(
    manifest: dict,
    pairs: dict[tuple, dict[str, Path]],
    output_root: Path,
    selected_models: set[str],
) -> list[dict]:
    schedule = []
    case_ids = {case["id"] for case in manifest["evals"]}
    iteration = output_root.parent.resolve()
    for comparison in manifest["comparisons"]:
        primary = comparison["primary"]
        baseline = comparison["baseline"]
        for key, arms in sorted(pairs.items()):
            if primary not in arms or baseline not in arms:
                continue
            eval_id, model, repeat = key
            if selected_models and model not in selected_models:
                continue
            if eval_id not in case_ids:
                raise ValueError(f"The result refers to unknown eval {eval_id}.")
            target = (
                output_root / comparison["id"] / f"eval-{eval_id}"
                / quote(model, safe="._-") / f"run-{repeat}.json"
            )
            if target.is_file() and load(target).get("state") == "valid":
                continue
            responses = {
                arm: arms[arm].parent / "outputs" / "response.md"
                for arm in (primary, baseline)
            }
            if any(
                path.is_symlink()
                or not path.is_file()
                or not path.resolve().is_relative_to(iteration)
                for path in responses.values()
            ):
                raise ValueError(
                    f"Eval {eval_id} model {model} has an invalid response path."
                )
            schedule.append({
                "comparison": comparison,
                "eval_id": eval_id,
                "model": model,
                "repeat": repeat,
                "responses": responses,
                "target": target,
            })
    return schedule


def validate_assignment(
    run_plan: dict,
    route: dict,
    schedule: list[dict],
    selected_models: set[str],
) -> None:
    frozen_routes = run_plan["routes"]
    planned_models = {entry["model"] for entry in frozen_routes}
    unknown = selected_models - planned_models
    if unknown:
        raise ValueError(f"unknown --model values: {', '.join(sorted(unknown))}")
    vendors = {entry["model"]: entry.get("vendor") for entry in frozen_routes}
    if any(not isinstance(vendor, str) or not vendor for vendor in vendors.values()):
        raise ValueError("the frozen run plan needs one vendor for each model")
    judge_vendor = route["vendor"].casefold()
    same_vendor = sorted({
        item["model"]
        for item in schedule
        if vendors[item["model"]].casefold() == judge_vendor
    })
    if same_vendor:
        raise ValueError(
            "the judge and subject models have the same vendor: "
            f"{', '.join(same_vendor)}"
        )


def validate_frozen_registry(run_plan: dict, routes_path: Path) -> None:
    if "models" in run_plan:
        return
    frozen_path = run_plan.get("registry_path")
    frozen_digest = run_plan.get("registry_sha256")
    if not isinstance(frozen_path, str) or not frozen_path:
        raise ValueError("the frozen run plan needs a route registry path")
    if not isinstance(frozen_digest, str) or not frozen_digest:
        raise ValueError("the frozen run plan needs a route registry digest")
    if routes_path != Path(frozen_path).expanduser().resolve():
        raise ValueError("the route registry path does not match the frozen run plan")
    actual_digest = run_benchmark.artifact_digest(routes_path)
    if actual_digest.casefold() != frozen_digest.casefold():
        raise ValueError("the route registry digest does not match the frozen run plan")


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


def parse(
    stdout: str,
    dimension_ids: tuple = ("clarity", "fluency", "directness"),
    response_kind: str = "json",
) -> dict:
    text, _, _ = run_benchmark.parse_response(stdout, response_kind)
    return parse_verdict(text, dimension_ids)


def parse_verdict(
    text: str,
    dimension_ids: tuple = ("clarity", "fluency", "directness"),
) -> dict:
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


def invoke(route_name: str, route: dict, judge_prompt: str, timeout: float) -> dict:
    return run_benchmark.invoke(route_name, route, judge_prompt, None, [], timeout)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cross-harness",
        action="store_true",
        help="Permit external harness and provider processes",
    )
    parser.add_argument("--iteration", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--routes", type=Path, required=True)
    parser.add_argument("--judge-route", required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--model", action="append")
    parser.add_argument("--approve", type=int)
    parser.add_argument(
        "--plan",
        action="store_true",
        help="Validate inputs and print the provider-call count",
    )
    parser.add_argument("--timeout", type=float, default=300)
    args = parser.parse_args(argv)
    try:
        if not args.cross_harness:
            raise ValueError("cross-harness execution requires --cross-harness")
        manifest = load(args.manifest.resolve())
        run_benchmark.validate_manifest(manifest, require_run_plan=True)
        run_plan = run_benchmark.normalize_run_plan(manifest, required=True)
        if not run_benchmark.finite_number(args.timeout) or args.timeout <= 0:
            raise ValueError("timeout must be greater than zero")
        judging = manifest.get("judging")
        if judging is None:
            judging = DEFAULT_JUDGING
        dimension_ids = run_benchmark.SUPPORTED_JUDGING_DIMENSIONS
        cases = {int(case["id"]): case for case in manifest["evals"]}
        routes_path = args.routes.resolve()
        validate_frozen_registry(run_plan, routes_path)
        registry = load(routes_path).get("routes")
        if not isinstance(registry, dict):
            raise TypeError("route registry routes must be an object")
        route = registry[args.judge_route]
        run_benchmark.validate_route(args.judge_route, route)
        if not shutil.which(route["binary"]):
            raise ValueError(
                f"route binary not found: {args.judge_route}: {route['binary']}"
            )
        selected_models = set(args.model or [])
        iteration = args.iteration.resolve()
        output_root = iteration / "preferences"
        schedule = judgment_schedule(
            manifest, collect(iteration, manifest), output_root, selected_models,
        )
        validate_assignment(run_plan, route, schedule, selected_models)
        route_checks = 2 if schedule else 0
        provider_calls = len(schedule) + route_checks
        print(
            f"Plan: {len(schedule)} blinded preference judgments and "
            f"{route_checks} route checks ({provider_calls} provider calls)."
        )
        if args.plan:
            return 0
        run_benchmark.require_provider_call_approval(provider_calls, args.approve)
        if not schedule:
            print("Wrote 0 blinded preference judgments.")
            return 0

        run_benchmark.progress(
            "route-check-start",
            check="preflight",
            route=args.judge_route,
            model=route["model"],
        )
        preflight = run_benchmark.preflight_route(
            args.judge_route, route, args.timeout,
        )
        run_benchmark.progress(
            "route-check-finish",
            check="preflight",
            route=args.judge_route,
            model=route["model"],
            state=preflight["state"],
        )
        if preflight["state"] != "valid":
            raise ValueError(f"judge route preflight failed: {args.judge_route}")

        run_benchmark.progress(
            "route-check-start",
            check="context-canary",
            route=args.judge_route,
            model=route["model"],
        )
        canary = run_benchmark.context_canary_route(
            args.judge_route, route, args.timeout,
        )
        run_benchmark.progress(
            "route-check-finish",
            check="context-canary",
            route=args.judge_route,
            model=route["model"],
            state=canary["state"],
        )
        if canary["state"] != "valid":
            raise ValueError(f"judge route context canary failed: {args.judge_route}")

        output_root.mkdir(exist_ok=True)
        count = 0
        for item in schedule:
            comparison = item["comparison"]
            primary = comparison["primary"]
            baseline = comparison["baseline"]
            eval_id = item["eval_id"]
            model = item["model"]
            repeat = item["repeat"]
            pair_seed = f"{args.seed}:{comparison['id']}:{eval_id}:{model}:{repeat}"
            left_arm, right_arm = (
                (primary, baseline)
                if random.Random(pair_seed).randrange(2) == 0
                else (baseline, primary)
            )
            texts = {
                arm: item["responses"][arm].read_text(encoding="utf-8")
                for arm in (left_arm, right_arm)
            }
            blind = {"A": left_arm, "B": right_arm}
            judge_prompt = prompt(
                cases[eval_id], texts[left_arm], texts[right_arm], judging,
            )
            run_benchmark.progress(
                "judgment-start",
                comparison=comparison["id"],
                case=eval_id,
                model=model,
                judge=route["model"],
            )
            result = invoke(
                args.judge_route, route, judge_prompt, args.timeout,
            )
            record = {
                "schema_version": 2,
                "comparison": comparison["id"],
                "eval_id": eval_id,
                "model": model,
                "repeat": repeat,
                "judge_route": args.judge_route,
                "judge_model": route["model"],
                "judge_vendor": route["vendor"],
                "seed": args.seed,
                "blind_order": blind,
                "state": result["state"],
                "returncode": result.get("returncode"),
                "stderr": result.get("stderr", ""),
            }
            if result["state"] != "valid":
                record["error"] = result.get("error", "The judge route failed.")
            else:
                try:
                    verdict = parse_verdict(result["response"], dimension_ids)
                    for dimension in dimension_ids:
                        winner = verdict[dimension]["winner"]
                        winner_arm = blind.get(winner) if winner != "tie" else "tie"
                        record.update({
                            f"{dimension}_winner": winner,
                            f"{dimension}_winner_arm": winner_arm,
                            f"{dimension}_reason": verdict[dimension]["reason"],
                        })
                except (json.JSONDecodeError, TypeError, ValueError) as error:
                    record.update({
                        "state": "invalid_output",
                        "error": str(error),
                        "stdout": result.get("provider_output", ""),
                    })
            target = item["target"]
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(
                json.dumps(record, indent=2, allow_nan=False) + "\n",
                encoding="utf-8",
            )
            run_benchmark.progress(
                "judgment-finish",
                comparison=comparison["id"],
                case=eval_id,
                model=model,
                state=record["state"],
            )
            count += 1
            if record["state"] == "model_mismatch":
                raise ValueError(f"judge route model mismatch: {args.judge_route}")
        print(f"Wrote {count} blinded preference judgments.")
        return 0
    except (KeyError, OSError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
