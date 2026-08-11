#!/usr/bin/env python3
"""Package a skill directory into a distributable .skill archive.

Usage:
    python3 -m scripts.package_skill <path/to/skill-folder> [output-directory]

Example:
    python3 -m scripts.package_skill skills/public/my-skill
    python3 -m scripts.package_skill skills/public/my-skill ./dist --harness claude
"""

import argparse
import sys
from pathlib import Path

from scripts.harness import get_harness
from scripts.utils import parse_skill_md


def main():
    parser = argparse.ArgumentParser(
        description="Package a skill directory into a distributable .skill archive"
    )
    parser.add_argument("skill_path", type=Path, help="Path to the skill directory")
    parser.add_argument(
        "output_dir",
        nargs="?",
        type=Path,
        default=None,
        help="Output directory for the .skill file (default: current directory)",
    )
    parser.add_argument("--harness", default="claude", help="Harness adapter to use (default: claude)")
    args = parser.parse_args()

    skill_path = args.skill_path.resolve()
    if not skill_path.is_dir():
        print(f"Error: skill directory not found: {skill_path}", file=sys.stderr)
        sys.exit(1)
    if not (skill_path / "SKILL.md").exists():
        print(f"Error: SKILL.md not found in {skill_path}", file=sys.stderr)
        sys.exit(1)

    try:
        parse_skill_md(skill_path)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        harness = get_harness(args.harness)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    output_dir = (args.output_dir or Path.cwd()).resolve()
    output_path = output_dir / f"{skill_path.name}.skill"

    result = harness.package(skill_path, output_path)
    print(f"Packaged skill to: {result}")


if __name__ == "__main__":
    main()
