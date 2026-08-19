#!/usr/bin/env python3
"""Grade valid STE benchmark outputs with frozen deterministic checks."""

import argparse
import json
import re
import subprocess
from pathlib import Path


def has_all(text: str, patterns: list[str]) -> tuple[bool, list[str]]:
    lowered = text.casefold()
    missing = [pattern for pattern in patterns if pattern.casefold() not in lowered]
    return not missing, missing


def expectation(text: str, passed: bool, evidence: str) -> dict:
    return {"text": text, "passed": passed, "evidence": evidence}


def grade_case(case: dict, text: str) -> list[dict]:
    words = len(re.findall(r"\b[\w.-]+\b", text))
    checks = []
    assertions = case.get("assertions")
    if not isinstance(assertions, list) or not assertions:
        raise ValueError("each case needs a non-empty assertions array")
    for assertion in assertions:
        if not isinstance(assertion, dict):
            raise TypeError("each assertion must be an object with kind and text")
        kind = assertion["kind"]
        if kind == "word_range":
            minimum = case.get("minimum_words")
            maximum = case.get("maximum_words")
            if minimum is None and maximum is None:
                raise ValueError("a word_range assertion needs minimum_words or maximum_words")
            passed = (minimum is None or words >= minimum) and (maximum is None or words <= maximum)
            if minimum is None:
                evidence = f"{words} words; required at most {maximum}."
            elif maximum is None:
                evidence = f"{words} words; required at least {minimum}."
            else:
                evidence = f"{words} words; required {minimum} to {maximum}."
        elif kind == "required_patterns":
            passed, missing = has_all(text, assertion["patterns"])
            evidence = "Missing: " + (", ".join(missing) if missing else "none.")
        elif kind == "forbidden_patterns":
            lowered = text.casefold()
            found = [pattern for pattern in assertion["patterns"] if pattern.casefold() in lowered]
            passed = not found
            evidence = "Forbidden text: " + (", ".join(found) if found else "none.")
        else:
            raise ValueError(f"unsupported assertion kind: {kind}")
        checks.append(expectation(assertion["text"], passed, evidence))
    return checks


def lint(checker: Path, mode: str, response: Path, checker_config: Path | None = None) -> dict:
    command = ["python3", str(checker), "--json"]
    if mode == "strict":
        command.append("--strict")
    if checker_config is not None:
        command.extend(["--config", str(checker_config)])
    command.append(str(response))
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if result.returncode not in (0, 1):
        raise RuntimeError(result.stderr.strip() or "checker failed")
    data = json.loads(result.stdout)
    return data.get("files", [data])[0] if isinstance(data.get("files"), list) else data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--iteration", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--checker", type=Path, required=True)
    parser.add_argument("--checker-config", type=Path)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    cases = {int(case["id"]): case for case in manifest["evals"]}
    count = 0
    for result_path in sorted(args.iteration.glob("eval-*/**/result.json")):
        execution = json.loads(result_path.read_text(encoding="utf-8"))
        if execution.get("state") != "valid":
            continue
        response = result_path.parent / "outputs" / "response.md"
        text = response.read_text(encoding="utf-8")
        case = cases[int(execution["eval_id"])]
        checks = grade_case(case, text)
        passed = sum(item["passed"] for item in checks)
        payload = {
            "grader_version": 1,
            "expectations": checks,
            "summary": {"passed": passed, "failed": len(checks) - passed, "total": len(checks), "pass_rate": passed / len(checks)},
            "lint": lint(args.checker, case.get("lint_mode", "flavored"), response, args.checker_config),
            "notes": [],
        }
        (result_path.parent / "grading.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        count += 1
    print(f"Graded {count} valid runs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
