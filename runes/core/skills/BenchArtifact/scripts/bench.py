#!/usr/bin/env python3
"""bench: minimal cross-harness benchmark pipeline over one config file.

Usage: bench <quick|snapshot|plan|run|grade|judge|report|all> <config.json>

The config file lives in the benchmark workspace. Paths in the config
resolve against the config file directory. This wrapper is a stopgap
until runedeck/bench absorbs the flow.
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path


def load(config_path: Path) -> dict:
    config = json.loads(config_path.read_text())
    config["_root"] = config_path.parent.resolve()
    return config


def path(config: dict, key: str) -> Path:
    value = Path(config[key])
    return value if value.is_absolute() else config["_root"] / value


def run(argv: list, **kwargs) -> None:
    print("[bench]", " ".join(str(part) for part in argv), flush=True)
    subprocess.run([str(part) for part in argv], check=True, **kwargs)


def scripts_dir(config: dict) -> Path:
    if config.get("bench_scripts"):
        return path(config, "bench_scripts")
    return Path(__file__).resolve().parent


def snapshot(config: dict) -> None:
    source = path(config, "artifact_source")
    target = path(config, "snapshot")
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target)
    sys.path.insert(0, str(scripts_dir(config)))
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "rb", scripts_dir(config) / "run_benchmark.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    digest = module.artifact_digest(target)
    template = config.get("manifest_template", config["manifest"])
    manifest = json.loads((config["_root"] / template).read_text())
    arm = manifest["arms"][config["treatment_arm"]]
    arm["artifact_path"] = target.name
    arm["artifact_sha256"] = digest
    path(config, "manifest").write_text(json.dumps(manifest, indent=2) + "\n")
    print("[bench] snapshot digest:", digest)


def matrix_argv(config: dict) -> list:
    return [
        sys.executable,
        scripts_dir(config) / "run_benchmark.py",
        "--cross-harness",
        "--workspace", config["_root"],
        "--iteration", config["iteration"],
        "--manifest", path(config, "manifest"),
        "--routes", path(config, "routes"),
        "--repeats", config.get("repeats", 1),
        "--seed", config["seed"],
        "--comparison", config["comparison"],
        "--timeout", config.get("timeout", 600),
    ]


def plan(config: dict) -> None:
    run(matrix_argv(config) + ["--plan"])


def matrix(config: dict) -> None:
    run(matrix_argv(config) + ["--approve", config["approve"]])


def iteration_dir(config: dict) -> Path:
    return config["_root"] / f"iteration-{config['iteration']}"


def grade(config: dict) -> None:
    argv = [
        sys.executable, path(config, "grader"),
        "--iteration", iteration_dir(config),
        "--manifest", path(config, "manifest"),
        "--checker", path(config, "checker"),
    ]
    if config.get("checker_config"):
        argv += ["--checker-config", path(config, "checker_config")]
    run(argv)


def judge(config: dict) -> None:
    for judge_pass in config["judges"]:
        argv = [
            sys.executable, path(config, "judge_script"),
            "--cross-harness",
            "--iteration", iteration_dir(config),
            "--manifest", path(config, "manifest"),
            "--routes", path(config, "routes"),
            "--judge-route", judge_pass["route"],
            "--seed", config["seed"],
        ]
        if "approve" in judge_pass:
            argv += ["--approve", judge_pass["approve"]]
        for model in judge_pass["models"]:
            argv += ["--model", model]
        run(argv)


def report(config: dict) -> None:
    bench_dir = scripts_dir(config).parent
    run(
        [
            sys.executable, "-m", "scripts.aggregate_benchmark",
            iteration_dir(config),
            "--manifest", path(config, "manifest"),
            "--artifact-name", config["artifact_name"],
        ],
        cwd=bench_dir,
    )
    run(
        [
            sys.executable, "-m", "scripts.build_report",
            iteration_dir(config) / "benchmark.json",
        ],
        cwd=bench_dir,
    )
    print("[bench] report:", iteration_dir(config) / "report.html")


def selected_count(items, values: list) -> int:
    available = {str(item) for item in items}
    if not values:
        return len(available)
    wanted = set(values)
    missing = wanted - available
    if missing:
        raise ValueError(f"filter values not found: {', '.join(sorted(missing))}")
    return len(wanted)


def quick_approval(config: dict, routes: list, cases: list) -> int:
    manifest = json.loads(path(config, "manifest").read_text())
    registry = json.loads(path(config, "routes").read_text()).get("routes", {})
    comparison = next(
        (
            item for item in manifest["comparisons"]
            if item["id"] == config["comparison"]
        ),
        None,
    )
    if comparison is None:
        raise ValueError(f"comparison not found: {config['comparison']}")
    arms = {comparison["primary"], comparison["baseline"]}
    route_count = selected_count(registry, routes)
    case_count = selected_count(
        (case["id"] for case in manifest["evals"]), cases
    )
    matrix_calls = (
        case_count
        * len(arms)
        * route_count
        * config.get("repeats", 1)
    )
    return matrix_calls + route_count * 2


def repeat_summary(config: dict) -> str:
    repeats = config.get("repeats", 1)
    label = "repeat" if repeats == 1 else "repeats"
    return f"{repeats} {label}"


def quick(config: dict) -> None:
    """Scratch run: two routes, two cases, no judging. Roughly five minutes."""
    settings = config.get("quick", {})
    routes = settings.get("routes", [])
    cases = [str(case) for case in settings.get("cases", [])]
    iteration = settings.get("iteration", 999)
    scratch = config["_root"] / f"iteration-{iteration}"
    if scratch.exists():
        shutil.rmtree(scratch)
    quick_config = dict(config)
    quick_config["iteration"] = iteration
    argv = matrix_argv(quick_config)
    for route in routes:
        argv += ["--route", route]
    for case in cases:
        argv += ["--case", case]
    run(argv + ["--approve", quick_approval(config, routes, cases)])
    grade(quick_config)
    bench_dir = scripts_dir(config).parent
    run(
        [
            sys.executable, "-m", "scripts.aggregate_benchmark", scratch,
            "--manifest", path(config, "manifest"),
            "--artifact-name", config["artifact_name"],
        ],
        cwd=bench_dir,
    )
    print()
    print((scratch / "benchmark.md").read_text())
    print(
        "[bench] scratch run: no blind judging, "
        f"{repeat_summary(config)}, low confidence"
    )



STEPS = {
    "quick": [quick],
    "snapshot": [snapshot],
    "plan": [plan],
    "run": [matrix],
    "grade": [grade],
    "judge": [judge],
    "report": [report],
    "all": [snapshot, plan, matrix, grade, judge, report],
}


def main() -> int:
    if len(sys.argv) != 3 or sys.argv[1] not in STEPS:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    config = load(Path(sys.argv[2]))
    for step in STEPS[sys.argv[1]]:
        step(config)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
