# Prose length caps design

## Commands

A requirement names a role. This table names the command, flags, and diagnostic ids behind each row, so nothing is lost when a command moves out of a requirement.

| Requirement | Command | Notes |
|---|---|---|
| Repository prose stays under the rune caps | `rune spec validate` | the validator for the requirement cap (100 words) and the scenario step cap (30 words) in `docs/specs/` and `docs/changes/`, run in the commit stage |
| Repository prose stays under the rune caps | `rune docs check` | the validator for the `CHANGELOG.md` line cap (200 characters), diagnostic `entry-length`, run by the quality job in CI |
