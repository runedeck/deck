#!/usr/bin/env python3
"""bench: minimal cross-harness benchmark pipeline over one config file.

Usage: bench <snapshot|plan|run|grade|judge|report|all> <config.json>

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


def iteration_manifest(config: dict) -> Path:
    return iteration_dir(config) / "manifest.json"


def grade(config: dict) -> None:
    argv = [
        sys.executable, path(config, "grader"),
        "--iteration", iteration_dir(config),
        "--manifest", iteration_manifest(config),
        "--checker", path(config, "checker"),
    ]
    if config.get("checker_config"):
        argv += ["--checker-config", path(config, "checker_config")]
    run(argv)


def judge(config: dict) -> None:
    for judge_pass in config["judges"]:
        argv = [
            sys.executable, path(config, "judge_script"),
            "--iteration", iteration_dir(config),
            "--manifest", iteration_manifest(config),
            "--routes", path(config, "routes"),
            "--judge-route", judge_pass["route"],
            "--seed", config["seed"],
        ]
        for model in judge_pass["models"]:
            argv += ["--model", model]
        run(argv)


def report(config: dict) -> None:
    bench_dir = scripts_dir(config).parent
    run(
        [
            sys.executable, "-m", "scripts.aggregate_benchmark",
            iteration_dir(config),
            "--manifest", iteration_manifest(config),
            "--artifact-name", config["artifact_name"],
        ],
        cwd=bench_dir,
    )
    run(
        [
            sys.executable, "-m", "scripts.build_report",
            iteration_dir(config) / "benchmark.json",
            "--local-links",
        ],
        cwd=bench_dir,
    )
    print("[bench] report:", iteration_dir(config) / "report.html")


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
    quick_config["repeats"] = 1
    argv = matrix_argv(quick_config)
    for route in routes:
        argv += ["--route", route]
    for case in cases:
        argv += ["--case", case]
    run(argv + ["--approve", len(routes) * len(cases) * 2])
    grade(quick_config)
    bench_dir = scripts_dir(config).parent
    run(
        [
            sys.executable, "-m", "scripts.aggregate_benchmark", scratch,
            "--manifest", iteration_manifest(quick_config),
            "--artifact-name", config["artifact_name"],
        ],
        cwd=bench_dir,
    )
    print()
    print((scratch / "benchmark.md").read_text())
    print("[bench] scratch run: no blind judging, no repeats, low confidence")


def push(config: dict) -> None:
    for target in config.get("push", []):
        run([
            "git", "-C", target["repo"], "push",
            f"--force-with-lease={target['branch']}",
            "origin", target["branch"],
        ])


def pr(config: dict) -> None:
    """Create one branch and pull request carrying listed working-tree files."""
    spec = config["pr"]
    repo, branch = spec["repo"], spec["branch"]
    worktree = Path("/tmp") / f"bench-pr-{branch.replace('/', '-')}"
    run(["git", "-C", repo, "fetch", "origin", "main"])
    subprocess.run(["git", "-C", repo, "worktree", "remove", "--force", str(worktree)],
                   check=False, capture_output=True)
    if worktree.exists():
        shutil.rmtree(worktree)
    run(["git", "-C", repo, "worktree", "add", "-b", branch, str(worktree), "origin/main"])
    for name in spec["files"]:
        target = worktree / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(Path(repo) / name, target)
        run(["git", "-C", str(worktree), "add", name])
    run(["git", "-C", str(worktree), "commit", "-S", "-m", spec["message"]])
    run(["git", "-C", str(worktree), "push", "-u", "origin", branch])
    run(["gh", "pr", "create", "--title", spec["title"], "--body", spec["body"]],
        cwd=worktree)
    run(["git", "-C", repo, "worktree", "remove", "--force", str(worktree)])


STEPS = {
    "quick": [quick],
    "push": [push],
    "pr": [pr],
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
