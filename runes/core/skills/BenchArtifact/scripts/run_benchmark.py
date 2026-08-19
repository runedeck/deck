#!/usr/bin/env python3
"""Run an explicit cross-harness benchmark matrix."""

import argparse
import concurrent.futures
import hashlib
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from urllib.parse import quote

SAFE_RUN_LIMIT = 20
PREFLIGHT_PROMPT = "Reply with exactly OK."
WORKSPACE_ROOT_VARIABLE = "ROOT_BENCHMARK"
DEFAULT_WORKSPACE_ROOT = Path.home() / "Data" / "Benchmarks"
RESPONSE_KINDS = {"text", "json", "jsonl"}
ROUTE_CONTEXT_KEYS = (
    "scratch", "state", "prompt", "prompt_file", "artifact", "artifact_source", "model",
)


def progress(event: str, **fields) -> None:
    details = " ".join(f"{key}={value}" for key, value in fields.items())
    suffix = f" {details}" if details else ""
    print(f"Progress: event={event}{suffix}", flush=True)


def default_workspace(manifest: dict) -> Path:
    name = manifest.get("artifact_name")
    if not isinstance(name, str) or not name:
        raise ValueError("manifest needs artifact_name when --workspace is omitted")
    root = Path(os.environ.get(WORKSPACE_ROOT_VARIABLE, str(DEFAULT_WORKSPACE_ROOT)))
    deck = manifest.get("deck")
    return root / deck / name if isinstance(deck, str) and deck else root / name


def load_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise TypeError(f"{path} must contain a JSON object")
    return data


def artifact_digest(path: Path) -> str:
    """Hash one artifact file or a directory's sorted relative paths and contents."""
    if path.is_file():
        return hashlib.sha256(path.read_bytes()).hexdigest()
    hasher = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        relative = item.relative_to(path).as_posix().encode("utf-8")
        content = item.read_bytes()
        for value in (relative, content):
            hasher.update(len(value).to_bytes(8, "big"))
            hasher.update(value)
    return hasher.hexdigest()


def display_model(model: str) -> str:
    lower = model.lower()
    if lower.endswith("[1m]"):
        return model[:-4]
    if lower.endswith(("-1m", "_1m")):
        return model[:-3]
    return model[:-2] if lower.endswith("1m") else model


def expand(value: str, context: dict[str, str]) -> str:
    return value.format_map(context)


def parse_response(stdout: str, kind: str) -> tuple[str, dict, dict]:
    if kind == "text":
        return stdout.strip(), {}, {}
    records = []
    if kind == "jsonl":
        records = [json.loads(line) for line in stdout.splitlines() if line.strip()]
        data = records[-1] if records else {}
    else:
        data = json.loads(stdout)
        records = [data]
    if not isinstance(data, dict):
        raise TypeError("provider output must contain a JSON object")
    text = next(
        (
            value
            for key in ("final_response", "response", "text", "output", "message")
            if isinstance((value := data.get(key)), str) and value.strip()
        ),
        "",
    )
    if kind == "jsonl" and not text:
        text_records = []
        for record in records:
            part = record.get("part") if isinstance(record, dict) else None
            value = part.get("text") if isinstance(part, dict) else None
            if isinstance(value, str):
                text_records.append(part)
        message_ids = [part.get("messageID") for part in text_records if isinstance(part.get("messageID"), str)]
        if message_ids:
            if len(message_ids) != len(text_records):
                raise ValueError("jsonl text parts mix identified and unidentified messages")
            final_message_id = message_ids[-1]
            text_records = [part for part in text_records if part.get("messageID") == final_message_id]
        text = "".join(part["text"] for part in text_records)
    usage = data.get("usage") if isinstance(data.get("usage"), dict) else {}
    route = {
        key: data.get(key)
        for key in ("requested_route", "requested_provider", "resolved_route", "resolved_model", "resolved_binary", "clean_harness_state", "clean_harness_state_scope")
        if key in data
    }
    return text.strip(), usage, route


def validate_manifest(manifest: dict) -> None:
    required = {"schema_version", "arms", "comparisons", "evals"}
    missing = sorted(required - manifest.keys())
    if missing:
        raise ValueError(f"manifest is missing: {', '.join(missing)}")
    if manifest["schema_version"] != 2:
        raise ValueError("manifest schema_version must be 2")
    arms = manifest["arms"]
    if not isinstance(arms, dict) or not arms:
        raise ValueError("manifest arms must be a non-empty object")
    if any(not isinstance(spec, dict) for spec in arms.values()):
        raise TypeError("each manifest arm must be an object")
    if any(not name or Path(name).name != name or "@" in name for name in arms):
        raise ValueError("manifest arm names must be safe directory names without @")
    for name, spec in arms.items():
        kind = spec.get("artifact_kind")
        if kind not in {None, "agent", "rule", "skill"}:
            raise ValueError(f"arm {name} has an invalid artifact_kind")
        if "artifact_path" in spec and not isinstance(spec["artifact_path"], str):
            raise TypeError(f"arm {name} artifact_path must be a string")
        if "artifact_sha256" in spec and not isinstance(spec["artifact_sha256"], str):
            raise TypeError(f"arm {name} artifact_sha256 must be a string")
        if spec.get("artifact_kind") is not None and not spec.get("artifact_path"):
            raise ValueError(f"treatment arm {name} needs artifact_path")
    if not isinstance(manifest["comparisons"], list):
        raise TypeError("manifest comparisons must be an array")
    if not isinstance(manifest["evals"], list):
        raise TypeError("manifest evals must be an array")
    if not manifest["evals"]:
        raise ValueError("manifest evals must be a non-empty array")
    eval_ids = [case.get("id") for case in manifest["evals"] if isinstance(case, dict)]
    if None in eval_ids or len(eval_ids) != len(manifest["evals"]) or len(set(map(str, eval_ids))) != len(eval_ids):
        raise ValueError("manifest eval ids must be present and unique")
    if any(
        not isinstance(case.get("name"), str)
        or not case["name"]
        or Path(case["name"]).name != case["name"]
        for case in manifest["evals"]
    ):
        raise ValueError("manifest eval names must be safe directory names")
    for case in manifest["evals"]:
        if not isinstance(case.get("prompt"), str) or not case["prompt"]:
            raise ValueError(f"manifest eval {case.get('id')} needs a prompt")
        files = case.get("files", [])
        if not isinstance(files, list) or not all(isinstance(path, str) for path in files):
            raise TypeError(f"manifest eval {case['id']} files must be strings")
        for field in ("minimum_words", "maximum_words"):
            value = case.get(field)
            if value is not None and (not isinstance(value, int) or isinstance(value, bool) or value < 0):
                raise ValueError(f"manifest eval {case['id']} {field} must be a non-negative integer")
        if case.get("maximum_words") is not None and case.get("minimum_words", 1) > case["maximum_words"]:
            raise ValueError(f"manifest eval {case['id']} word limits are reversed")
    comparison_ids = []
    for comparison in manifest["comparisons"]:
        if not isinstance(comparison, dict):
            raise TypeError("each manifest comparison must be an object")
        for field in ("primary", "baseline"):
            if comparison.get(field) not in arms:
                raise ValueError(f"comparison arm not found: {comparison.get(field)}")
        if comparison["primary"] == comparison["baseline"]:
            raise ValueError("comparison primary and baseline arms must differ")
        comparison_id = comparison.get("id")
        if (
            not isinstance(comparison_id, str)
            or not comparison_id
            or Path(comparison_id).name != comparison_id
        ):
            raise ValueError("each manifest comparison needs a safe id")
        comparison_ids.append(comparison_id)
    if len(comparison_ids) != len(set(comparison_ids)):
        raise ValueError("manifest comparison ids must be unique")


def selected(items, values, key):
    if not values:
        return list(items)
    wanted = set(values)
    result = [item for item in items if str(key(item)) in wanted]
    missing = wanted - {str(key(item)) for item in result}
    if missing:
        raise ValueError(f"filter values not found: {', '.join(sorted(missing))}")
    return result


def make_context(
    scratch: Path, control: Path, prompt: str,
    artifact: Path | None, artifact_source: Path | None, model: str,
) -> dict[str, str]:
    prompt_file = control / "prompt.txt"
    prompt_file.write_text(prompt, encoding="utf-8")
    return {
        "scratch": str(scratch),
        "state": str(control / "state"),
        "prompt": prompt,
        "prompt_file": str(prompt_file),
        "artifact": str(artifact) if artifact else "",
        "artifact_source": str(artifact_source) if artifact_source else "",
        "model": model,
    }


def treatment_prompt(prompt: str, artifact: Path | None, route: dict) -> str:
    if not artifact or artifact_arguments(route):
        return prompt
    if route.get("treatment_mode") != "prepend":
        raise ValueError("treatment route needs artifact_argv or treatment_mode=prepend")
    return f"{artifact.read_text(encoding='utf-8').rstrip()}\n\n{prompt}"


def artifact_arguments(route: dict) -> list[str]:
    return route.get("artifact_argv", route.get("system_argv", []))


def validate_route(name: str, route: dict) -> None:
    if not isinstance(route, dict):
        raise TypeError(f"route {name} must be an object")
    for field in ("binary", "model"):
        if not isinstance(route.get(field), str) or not route[field]:
            raise ValueError(f"route {name} needs {field}")
    argv = route.get("argv", [])
    if not isinstance(argv, list) or not all(isinstance(arg, str) for arg in argv):
        raise ValueError(f"route {name} arguments must be strings")
    if "artifact_argv" in route and "system_argv" in route:
        raise ValueError(f"route {name} cannot define both artifact_argv and system_argv")
    arguments = artifact_arguments(route)
    if not isinstance(arguments, list) or not all(isinstance(arg, str) for arg in arguments):
        raise ValueError(f"route {name} artifact arguments must be strings")
    env = route.get("env", {})
    if not isinstance(env, dict) or not all(isinstance(key, str) for key in env):
        raise ValueError(f"route {name} environment must be an object with string keys")
    if route.get("response", "text") not in RESPONSE_KINDS:
        raise ValueError(f"route {name} has an invalid response kind")
    if "stdin" in route and not isinstance(route["stdin"], bool):
        raise TypeError(f"route {name} stdin must be a boolean")
    if not isinstance(route.get("context_canary"), str) or not route["context_canary"]:
        raise ValueError(f"route {name} requires a context canary")
    markers = route.get("forbidden_context_markers")
    if not isinstance(markers, list) or not markers or not all(isinstance(marker, str) and marker for marker in markers):
        raise ValueError(f"route {name} requires at least one forbidden context marker")
    probe = {key: key for key in ROUTE_CONTEXT_KEYS}
    for value in [*argv, *arguments, *(str(value) for value in env.values())]:
        try:
            expand(value, probe)
        except KeyError as error:
            raise ValueError(f"route {name} uses unknown placeholder {error.args[0]}") from error


def stage_artifact(
    artifact: Path | None, scratch: Path, control: Path,
) -> tuple[Path | None, Path | None]:
    if not artifact:
        return None, None
    artifact_root = scratch / ".bench-artifact"
    artifact_root.mkdir()
    target = artifact_root / artifact.name
    if artifact.is_file():
        shutil.copy2(artifact, target)
        return target, target
    if any(path.is_symlink() for path in artifact.rglob("*")):
        raise ValueError(f"artifact directory contains a symbolic link: {artifact}")
    shutil.copytree(artifact, target)
    entrypoint = target / "SKILL.md"
    if not entrypoint.is_file():
        raise ValueError(f"artifact directory has no SKILL.md: {artifact}")
    staged = control / "artifact.md"
    staged.write_text(
        f"Skill directory: {target}\n\n{entrypoint.read_text(encoding='utf-8').rstrip()}\n",
        encoding="utf-8",
    )
    return staged, target


def invoke(route_name: str, route: dict, prompt: str, artifact: Path | None, files: list[Path], timeout: float) -> dict:
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="bench-input-") as scratch_name, tempfile.TemporaryDirectory(prefix="bench-control-") as control_name:
        scratch, control = Path(scratch_name), Path(control_name)
        artifact_context, artifact_source = stage_artifact(artifact, scratch, control)
        prompt = treatment_prompt(prompt, artifact_context, route)
        for source in files:
            target = scratch / source.name
            if target.exists():
                raise ValueError(f"duplicate input name: {source.name}")
            shutil.copy2(source, target)
        context = make_context(
            scratch, control, prompt, artifact_context, artifact_source, route["model"],
        )
        Path(context["state"]).mkdir()
        argv = [route["binary"], *(expand(arg, context) for arg in route.get("argv", []))]
        if artifact_context:
            argv.extend(expand(arg, context) for arg in artifact_arguments(route))
        env = os.environ.copy()
        env.pop("CLAUDECODE", None)
        env.update({key: expand(str(value), context) for key, value in route.get("env", {}).items()})
        stdin = prompt if route.get("stdin") else None
        try:
            process = subprocess.run(
                argv, cwd=scratch, env=env, input=stdin, text=True,
                capture_output=True, timeout=timeout, check=False,
            )
        except subprocess.TimeoutExpired as error:
            return {
                "state": "timeout", "duration_seconds": round(time.monotonic() - started, 4),
                "error": str(error), "route": {"requested_route": route_name},
            }
        result = {
            "state": "provider_failure" if process.returncode else "valid",
            "duration_seconds": round(time.monotonic() - started, 4),
            "returncode": process.returncode,
            "stderr": process.stderr,
            "command": argv,
            "provider_output": process.stdout,
            "route": {"requested_route": route_name},
        }
        if process.returncode:
            try:
                data = json.loads(process.stdout)
                details = data.get("details", {}) if isinstance(data, dict) else {}
            except json.JSONDecodeError:
                details = {}
            return {**result, "error": details or process.stderr.strip() or "provider exited with an error"}
        try:
            text, usage, resolved = parse_response(process.stdout, route.get("response", "text"))
        except (TypeError, ValueError, json.JSONDecodeError) as error:
            return {**result, "state": "invalid_output", "error": str(error)}
        return {
            **result, "response": text, "usage": usage,
            "route": {"requested_route": route_name, **resolved},
        }


def validate_output(result: dict, case: dict) -> dict:
    if result["state"] != "valid":
        return result
    text = result.get("response", "")
    words = len(text.split())
    if not text.strip():
        return {**result, "state": "invalid_output", "error": "provider returned empty output"}
    return {**result, "word_count": words}


def result_dir(root: Path, case: dict, arm: str, model: str, repeat: int) -> Path:
    safe_model = quote(display_model(model), safe="._-")
    return root / f"eval-{case['id']}-{case['name']}" / f"{arm}@{safe_model}" / f"run-{repeat}"


def case_files(input_root: Path, case: dict) -> list[Path]:
    input_dir = case.get("input_dir", f"eval-{case['id']}-{case['name']}")
    case_root = (input_root / input_dir).resolve()
    if not case_root.is_relative_to(input_root):
        raise ValueError(f"case {case['id']} input directory escapes input_root")
    files = [(case_root / value).resolve() for value in case.get("files", [])]
    if any(not path.is_file() or not path.is_relative_to(case_root) for path in files):
        raise ValueError(f"case {case['id']} has an invalid input path")
    return files


def artifact_path(manifest_path: Path, spec: dict) -> Path | None:
    value = spec.get("artifact_path")
    if not value:
        return None
    artifact = (manifest_path.parent / value).resolve()
    if not artifact.exists():
        raise ValueError(f"artifact snapshot not found: {artifact}")
    if not (artifact.is_file() or artifact.is_dir()):
        raise ValueError(f"artifact snapshot must be a file or directory: {artifact}")
    if artifact.is_dir() and any(path.is_symlink() for path in artifact.rglob("*")):
        raise ValueError(f"artifact directory contains a symbolic link: {artifact}")
    kind = spec.get("artifact_kind")
    if kind == "skill" and not artifact.is_dir():
        raise ValueError(f"skill artifact snapshot must be a directory: {artifact}")
    if kind in {"agent", "rule"} and not artifact.is_file():
        raise ValueError(f"{kind} artifact snapshot must be a file: {artifact}")
    expected_digest = spec.get("artifact_sha256")
    actual_digest = artifact_digest(artifact)
    if expected_digest and expected_digest.casefold() != actual_digest:
        raise ValueError(f"artifact snapshot digest does not match: {artifact}")
    return artifact


def write_result(path: Path, result: dict, metadata: dict) -> None:
    path.mkdir(parents=True, exist_ok=True)
    payload = {**metadata, **result}
    provider_output = payload.pop("provider_output", None)
    (path / "result.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if provider_output is not None or result.get("response"):
        outputs = path / "outputs"
        outputs.mkdir(exist_ok=True)
    if provider_output is not None:
        (outputs / "provider-output.txt").write_text(provider_output, encoding="utf-8")
    if result.get("response"):
        (outputs / "response.md").write_text(result["response"] + "\n", encoding="utf-8")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Run an explicit cross-harness artifact benchmark")
    parser.add_argument(
        "--cross-harness",
        action="store_true",
        help="Permit external harness and provider processes",
    )
    parser.add_argument("--workspace", type=Path)
    parser.add_argument("--iteration", type=int, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--routes", type=Path, required=True)
    parser.add_argument("--repeats", type=int, default=1)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--route", action="append")
    parser.add_argument("--case", action="append")
    parser.add_argument("--comparison", action="append")
    parser.add_argument("--approve", type=int)
    parser.add_argument("--timeout", type=float, default=300)
    parser.add_argument("--jobs", type=int)
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--plan", action="store_true", help="Validate inputs and print the provider-call count")
    args = parser.parse_args(argv)
    try:
        if not args.cross_harness:
            raise ValueError("cross-harness execution requires --cross-harness")
        manifest = load_json(args.manifest.resolve())
        validate_manifest(manifest)
        routes_path = args.routes.resolve()
        registry = load_json(routes_path).get("routes", {})
        if not isinstance(registry, dict):
            raise TypeError("route registry routes must be an object")
        routes = selected(registry.items(), args.route, lambda item: item[0])
        cases = selected(manifest["evals"], args.case, lambda case: case["id"])
        comparisons = selected(
            manifest["comparisons"], args.comparison, lambda comparison: comparison["id"]
        )
        if args.comparison:
            arm_names = list(dict.fromkeys(
                arm for comparison in comparisons
                for arm in (comparison["primary"], comparison["baseline"])
            ))
        else:
            arm_names = list(manifest["arms"])
        if not routes:
            raise ValueError("no routes selected")
        if args.repeats < 1:
            raise ValueError("repeats must be greater than zero")
        if args.timeout <= 0:
            raise ValueError("timeout must be greater than zero")
        if args.plan and args.preflight_only:
            raise ValueError("plan and preflight-only cannot be used together")
        model_routes = {}
        for name, route in routes:
            validate_route(name, route)
            model = display_model(route["model"])
            if model in model_routes:
                raise ValueError(f"routes {model_routes[model]} and {name} share model identity {model}")
            model_routes[model] = name
            if not shutil.which(route["binary"]):
                raise ValueError(f"route binary not found: {name}: {route['binary']}")
        manifest_path = args.manifest.resolve()
        input_root = (manifest_path.parent / manifest.get("input_root", ".")).resolve()
        resolved_files = {str(case["id"]): case_files(input_root, case) for case in cases}
        resolved_artifacts = {
            arm: artifact_path(manifest_path, manifest["arms"][arm]) for arm in arm_names
        }
        planned_runs = len(cases) * len(arm_names) * len(routes) * args.repeats
        route_checks = len(routes) * 2
        jobs = len(routes) if args.jobs is None else args.jobs
        if jobs < 1:
            raise ValueError("jobs must be greater than zero")
        if args.preflight_only:
            print(f"Plan: {route_checks} route checks. The benchmark matrix will not run.")
        else:
            print(f"Plan: {planned_runs} benchmark runs and {route_checks} route checks ({planned_runs + route_checks} provider calls).")
        if args.plan:
            return 0
        if not args.preflight_only and planned_runs > SAFE_RUN_LIMIT and args.approve != planned_runs:
            raise ValueError(f"matrix has {planned_runs} runs; pass --approve {planned_runs}")
        workspace = args.workspace or default_workspace(manifest)
        root = workspace.expanduser().resolve() / f"iteration-{args.iteration}"
        root.mkdir(parents=True, exist_ok=True)
        run_arms = {}
        for arm in arm_names:
            run_arms[arm] = {**manifest["arms"][arm]}
            if resolved_artifacts[arm]:
                run_arms[arm]["artifact_path"] = str(resolved_artifacts[arm])
                run_arms[arm]["artifact_sha256"] = artifact_digest(resolved_artifacts[arm])
        run_cases = [
            {
                **case,
                "resolved_files": [
                    {"path": str(path), "sha256": artifact_digest(path)}
                    for path in resolved_files[str(case["id"])]
                ],
            }
            for case in cases
        ]
        run_manifest = {
            **manifest,
            "source_manifest": str(manifest_path),
            "input_root": str(input_root),
            "arms": run_arms,
            "comparisons": comparisons,
            "evals": run_cases,
            "run_plan": {
                "registry_path": str(routes_path),
                "registry_sha256": artifact_digest(routes_path),
                "routes": [
                    {"id": name, "model": route["model"]} for name, route in routes
                ],
                "repeats": args.repeats,
                "seed": args.seed,
                "timeout_seconds": args.timeout,
                "jobs": jobs,
            },
        }
        manifest_output = root / "manifest.json"
        if any(root.glob("eval-*")):
            raise ValueError("iteration already contains benchmark runs; use a new iteration")
        if manifest_output.is_file() and load_json(manifest_output) != run_manifest:
            raise ValueError("iteration already has a different frozen manifest")
        if not manifest_output.is_file() and any(root.iterdir()):
            raise ValueError("non-empty iteration has no frozen manifest")
        manifest_output.write_text(
            json.dumps(run_manifest, indent=2) + "\n", encoding="utf-8"
        )
        preflights = {}
        for name, route in routes:
            progress("route-check-start", check="preflight", route=name, model=route["model"])
            result = invoke(name, route, PREFLIGHT_PROMPT, None, [], args.timeout)
            result = validate_output(result, {"minimum_words": 1})
            response = result.get("response", "").strip()
            if response.rstrip(".!") != "OK":
                result["state"] = "preflight_failure"
                result["error"] = "preflight response must equal OK with optional punctuation"
            resolved = result.get("route", {}).get("resolved_model")
            if resolved and resolved != route["model"]:
                result["state"] = "model_mismatch"
                result["error"] = f"resolved model {resolved} does not match {route['model']}"
            preflights[name] = result
            progress(
                "route-check-finish",
                check="preflight",
                route=name,
                model=route["model"],
                state=result["state"],
            )
        (root / "preflights.json").write_text(json.dumps(preflights, indent=2) + "\n", encoding="utf-8")
        failed = [name for name, result in preflights.items() if result["state"] != "valid"]
        if failed:
            raise ValueError(f"route preflight failed: {', '.join(failed)}")
        canaries = {}
        for name, route in routes:
            progress("route-check-start", check="context-canary", route=name, model=route["model"])
            result = validate_output(invoke(name, route, route["context_canary"], None, [], args.timeout), {"minimum_words": 1})
            response = result.get("response", "").casefold()
            markers = [marker for marker in route["forbidden_context_markers"] if marker.casefold() in response]
            result["forbidden_context_markers"] = markers
            if result["state"] == "valid" and markers:
                result["state"] = "context_failure"
                result["error"] = f"context contains forbidden markers: {', '.join(markers)}"
            canaries[name] = result
            progress(
                "route-check-finish",
                check="context-canary",
                route=name,
                model=route["model"],
                state=result["state"],
            )
        (root / "context-canaries.json").write_text(json.dumps(canaries, indent=2) + "\n", encoding="utf-8")
        failed = [name for name, result in canaries.items() if result["state"] != "valid"]
        if failed:
            raise ValueError(f"route context canary failed: {', '.join(failed)}")
        if args.preflight_only:
            return 0
        schedule = [(case, arm, name, route, repeat) for case in cases for arm in arm_names for name, route in routes for repeat in range(1, args.repeats + 1)]
        random.Random(args.seed).shuffle(schedule)

        def run_item(item):
            case, arm, route_name, route, repeat = item
            files = resolved_files[str(case["id"])]
            artifact = resolved_artifacts[arm]
            progress(
                "run-start",
                case=case["id"],
                arm=arm,
                route=route_name,
                model=route["model"],
                repeat=repeat,
            )
            try:
                result = validate_output(
                    invoke(route_name, route, case["prompt"], artifact, files, args.timeout),
                    case,
                )
            except (OSError, TypeError, ValueError, json.JSONDecodeError):
                progress(
                    "run-finish",
                    case=case["id"],
                    arm=arm,
                    route=route_name,
                    model=route["model"],
                    repeat=repeat,
                    state="runner_error",
                )
                raise
            target = result_dir(root, case, arm, route["model"], repeat)
            write_result(target, result, {
                "schema_version": 2, "eval_id": case["id"], "eval_name": case["name"],
                "arm": arm, "model": route["model"], "repeat": repeat,
                "seed": args.seed,
            })
            progress(
                "run-finish",
                case=case["id"],
                arm=arm,
                route=route_name,
                model=route["model"],
                repeat=repeat,
                state=result["state"],
            )

        route_batches = {name: [] for name, _ in routes}
        for item in schedule:
            route_batches[item[2]].append(item)

        def run_batch(batch):
            for item in batch:
                run_item(item)

        with concurrent.futures.ThreadPoolExecutor(max_workers=min(jobs, len(routes))) as executor:
            futures = [executor.submit(run_batch, batch) for batch in route_batches.values() if batch]
            for future in concurrent.futures.as_completed(futures):
                future.result()
        return 0
    except (KeyError, OSError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
