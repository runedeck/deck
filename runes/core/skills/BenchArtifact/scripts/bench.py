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
    manifest_path = path(config, "manifest")
    source_path = source.resolve()
    manifest_directory = manifest_path.parent.resolve()
    target_path = target.resolve()
    if not source_path.is_dir():
        raise ValueError("artifact_source must be an existing directory")
    if (
        source_path == target_path
        or source_path in target_path.parents
        or target_path in source_path.parents
    ):
        raise ValueError("artifact_source and snapshot must be separate directories")
    try:
        manifest_artifact = target_path.relative_to(manifest_directory)
    except ValueError as error:
        raise ValueError(
            "snapshot must be below the manifest directory"
        ) from error
    if target_path == manifest_directory:
        raise ValueError("snapshot must be below the manifest directory")
    template = config.get("manifest_template", config["manifest"])
    manifest = json.loads((config["_root"] / template).read_text())
    arm = manifest["arms"][config["treatment_arm"]]
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
    arm["artifact_path"] = manifest_artifact.as_posix()
    arm["artifact_sha256"] = digest
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
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
    argv = matrix_argv(config)
    if "approve" in config:
        argv += ["--approve", config["approve"]]
    run(argv)


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


def quick_matrix_argv(
    config: dict,
    routes: list,
    cases: list,
    approve=None,
) -> list:
    argv = matrix_argv(config)
    for route in routes:
        argv += ["--route", route]
    for case in cases:
        argv += ["--case", case]
    if approve is not None:
        argv += ["--approve", approve]
    return argv


def repeat_summary(config: dict) -> str:
    repeats = config.get("repeats", 1)
    label = "repeat" if repeats == 1 else "repeats"
    return f"{repeats} {label}"


def quick(config: dict) -> None:
    """Scratch run: two routes, two cases, no judging. Roughly five minutes."""
    settings = config.get("quick") or {}
    routes = settings.get("routes") or []
    cases = [str(case) for case in (settings.get("cases") or [])]
    if not routes or not cases:
        raise ValueError(
            "quick.routes and quick.cases must each select at least one value"
        )
    iteration = settings.get("iteration", 999)
    if not isinstance(iteration, int) or isinstance(iteration, bool):
        raise TypeError("quick iteration must be an integer")
    scratch = config["_root"] / f"iteration-{iteration}"
    if scratch.exists():
        shutil.rmtree(scratch)
    quick_config = dict(config)
    quick_config["iteration"] = iteration
    run(quick_matrix_argv(
        quick_config,
        routes,
        cases,
        settings.get("approve"),
    ))
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
