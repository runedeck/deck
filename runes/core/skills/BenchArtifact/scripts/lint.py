#!/usr/bin/env python3
"""Generic pattern-density checker for artifacts without a dedicated checker.

The checker counts configured patterns for each 100 words. It shares the
CLI and the output contract of a dedicated checker, so grading and
aggregation work unchanged. An artifact ships only a small JSON config.
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

SCORE_VERSION = 1
DENSITY_RELIABLE_WORDS = 40
DEFAULT_CONFIG = Path(__file__).resolve().parent.parent / "config" / "rules.sample.json"


def load_config(path: Path) -> tuple[dict, str, str]:
    raw = path.read_bytes()
    config = json.loads(raw)
    rules = config.get("rules")
    if not isinstance(rules, list) or not rules:
        raise ValueError(f"config {path} needs a non-empty rules array")
    for rule in rules:
        if not isinstance(rule.get("id"), str) or not rule["id"]:
            raise ValueError(f"config {path} rule needs an id")
        patterns = rule.get("patterns")
        if not isinstance(patterns, list) or not all(isinstance(p, str) and p for p in patterns):
            raise ValueError(f"config {path} rule {rule['id']} needs pattern strings")
    return config, str(path.resolve()), hashlib.sha256(raw).hexdigest()


def strip_code(text: str) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    return re.sub(r"`[^`]*`", " ", text)


def word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'\-/]*", text))


def count_rule(text: str, rule: dict) -> int:
    total = 0
    for pattern in rule["patterns"]:
        if rule.get("regex"):
            total += len(re.findall(pattern, text, re.IGNORECASE))
        else:
            escaped = re.escape(pattern)
            total += len(re.findall(rf"(?<![A-Za-z]){escaped}(?![A-Za-z])", text, re.IGNORECASE))
    return total


def check(text: str, config: dict, config_path: str, config_digest: str) -> dict:
    body = strip_code(text)
    words = word_count(body)
    violations = {rule["id"]: count_rule(body, rule) for rule in config["rules"]}
    total = sum(violations.values())
    density_reliable = words >= DENSITY_RELIABLE_WORDS
    return {
        "score_version": SCORE_VERSION,
        "checker": "check_patterns",
        "config_path": config_path,
        "config_sha256": config_digest,
        "words": words,
        "violations": violations,
        "total": total,
        "total_per100w": round(total * 100.0 / words, 2) if words else 0.0,
        "density_reliable": density_reliable,
        "density_note": None if density_reliable else "Advisory: fewer than 40 words.",
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Count configured patterns for each 100 words")
    parser.add_argument("files", nargs="+")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true", help="Accepted for CLI compatibility")
    args = parser.parse_args(argv)
    try:
        config, config_path, config_digest = load_config(args.config)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"cannot load config: {error}", file=sys.stderr)
        return 2
    results = []
    for name in args.files:
        text = Path(name).read_text(encoding="utf-8")
        result = check(text, config, config_path, config_digest)
        result["file"] = name
        results.append(result)
    if args.json:
        print(json.dumps(results[0] if len(results) == 1 else {"files": results}, indent=2))
    else:
        for result in results:
            print(f"{result['file']}  words={result['words']} total={result['total']} "
                  f"per100w={result['total_per100w']}")
    return 1 if any(result["total"] for result in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
