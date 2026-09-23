# Draft artifact skill design

## Approach

The skill teaches a session the draft lifecycle the cli already has: register a draft where the harness loads it, check it, then promote it into the repository or drop it. The specification names the roles. This table names the commands that implement them.

## Commands

| Requirement | Command | Notes |
|---|---|---|
| New runes start as registered drafts | `rune draft <kind> <name>` | Run at the consumer root. Writes the draft where the harness loads it, records it in `.drafts`, and prints the file path. |
| New runes start as registered drafts | `rune draft --list`, `rune doctor` | Either confirms the draft is registered. `rune doctor` reports a hand-written rune as an orphan. |
| Promotion opens the change | `rune promote <name> --domain <domain> --change <id>` | Example: `rune promote ReviewSpec --domain core --change review-spec-interaction` leaves `runes/core/skills/ReviewSpec/SKILL.md` and `docs/changes/review-spec-interaction/` in the repository, and `rune draft --list` in the consumer prints `no drafts`. The change record is `proposal.md`, `tasks.md`, and `adr.md`. |
| Promotion opens the change | `rune draft --drop <name>` | Removes every provider copy and the `.drafts` entries. `rune doctor --verify` then exits 0. |
