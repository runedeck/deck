---
name: rune
description: "Drive the rune CLI to stage, deploy, and verify runes (skills, agents, rules) from a deck into AI harness directories. USE WHEN install runes, add skills to a project, deploy deck content, check drift, .rune manifest, rune validate, spec-driven change, rune spec. Not for authoring deck content (use the deck's build-* skills)."
---

# rune

rune deploys markdown instruction files (runes) from a deck into provider directories (`.claude`, `.codex`, `.gemini`, `.opencode`). The consumer manifest is `.rune` at the repository root. Deployment records are in per-provider `.manifest` files.

## Constraints

- Inspection commands (`context`, `status`, `doctor`, `drift`, `provenance`, `config`, `spec …`) accept `--json` for structured output. Staging commands print plain text.
- `rune install --dry-run` previews pruning without writing.
- `rune doctor --repair` restores missing files and quarantines orphans. It never overwrites user edits. Use `rune install --force` to overwrite edits.
- Never edit deployed files under provider directories. Edit the deck source and reinstall. Local exceptions are in a rune's `user/` override.
- Use `rune validate --scan` only in commit and push hooks. It runs gitleaks and semgrep, and it is slow.

## Instructions

### Orient

Run `rune context --json` first. It reports the root, role, target binding, manifest selection, provider deployments, active changes, and next steps. `rune status --source <deck>` is the deck-side dashboard.

### Stage and deploy

```sh
rune add development                 # stage a whole deck domain
rune add --cast development          # stage a cast (named selection)
rune add development/skills/deslop   # stage one rune by qualified id
rune install                         # assemble and deploy to all providers
```

`rune add` acts on the bound target when the current directory has no `.rune`. It prints a note when it redirects. Ambiguous IDs list every candidate. Retry with the qualified form `<domain>/<kind>/<name>`.

### Drive a spec change

```sh
rune spec propose <change-id> --capability <name>
rune spec list                       # active changes; --specs for capabilities
rune spec show <id>                  # one change or capability spec
rune spec context <id>               # agent-ready work order
rune spec doctor                     # relationship health
rune spec archive <id>               # refuses on unchecked tasks; --abandon drops
```

## Verification

```sh
rune validate                        # schemas and structure
rune drift --target .                # deployed content matches source?
rune doctor --target .               # integrity: ok / modified / missing / orphan
```
