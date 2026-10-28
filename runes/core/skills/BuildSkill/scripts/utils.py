"""Shared helpers for the trigger-evaluation scripts.

The only helper so far reads a skill's frontmatter. The standard library has
no YAML parser, so the frontmatter is read by hand. That is enough for the
toolkit's needs: top-level keys with plain, quoted, or block-scalar values.
"""

import re
from pathlib import Path

FRONTMATTER_FENCE = "---"

# A top-level key starts at column zero; indented keys belong to nested maps.
_TOP_LEVEL_KEY = re.compile(r"^([A-Za-z0-9_.-]+):(.*)$")
_BLOCK_SCALAR_INDICATORS = frozenset({">", "|", ">-", "|-", ">+", "|+"})


def _unquote(value: str) -> str:
    """Remove one layer of matching quotes and undo the escapes they allow."""
    if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
        return value[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    if len(value) >= 2 and value[0] == "'" and value[-1] == "'":
        return value[1:-1].replace("''", "'")
    return value


def _read_block_scalar(lines: list[str], start: int) -> tuple[str, int]:
    """Join the indented lines that follow a block indicator with single spaces.

    Returns the joined text and the index of the first line that is not part
    of the block.
    """
    pieces: list[str] = []
    index = start
    while index < len(lines):
        candidate = lines[index]
        if candidate.strip() == "":
            index += 1
            continue
        if not candidate[0].isspace():
            break
        pieces.append(candidate.strip())
        index += 1
    return " ".join(pieces), index


def parse_frontmatter_fields(lines: list[str]) -> dict[str, str]:
    """Return the top-level scalar fields found in frontmatter lines."""
    fields: dict[str, str] = {}
    index = 0
    while index < len(lines):
        match = _TOP_LEVEL_KEY.match(lines[index])
        index += 1
        if match is None:
            continue
        key = match.group(1)
        raw_value = match.group(2).strip()
        if raw_value in _BLOCK_SCALAR_INDICATORS:
            fields[key], index = _read_block_scalar(lines, index)
        else:
            fields[key] = _unquote(raw_value)
    return fields


def parse_skill_md(skill_path: Path) -> tuple[str, str, str]:
    """Return the name, the description, and the full text of a SKILL.md file.

    Raises ValueError when the frontmatter fences are missing or when the
    name or description is missing or empty.
    """
    skill_md = Path(skill_path) / "SKILL.md"
    content = skill_md.read_text(encoding="utf-8")
    lines = content.splitlines()

    if not lines or lines[0] != FRONTMATTER_FENCE:
        raise ValueError(
            f"{skill_md}: the file must begin with a '{FRONTMATTER_FENCE}' line "
            "that opens the frontmatter"
        )
    closing = next(
        (i for i in range(1, len(lines)) if lines[i] == FRONTMATTER_FENCE), None
    )
    if closing is None:
        raise ValueError(
            f"{skill_md}: no '{FRONTMATTER_FENCE}' line closes the frontmatter"
        )

    fields = parse_frontmatter_fields(lines[1:closing])
    name = fields.get("name", "").strip()
    description = fields.get("description", "").strip()
    if not name:
        raise ValueError(f"{skill_md}: the frontmatter needs a non-empty 'name'")
    if not description:
        raise ValueError(
            f"{skill_md}: the frontmatter needs a non-empty 'description'"
        )
    return name, description, content
