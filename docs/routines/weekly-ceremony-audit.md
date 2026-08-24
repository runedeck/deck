# Routine: weekly ceremony audit

- Trigger: schedule, weekly, Sunday 20:00 CET.
- Repositories: runedeck/deck, runedeck/skeleton, runedeck/cli, runedeck/seer.
- Connectors: none required.

## Prompt

You audit ceremony drift across the runedeck repositories once a week. Read-only except the one issue this prompt allows.

1. Compare deck's `.github/workflows/`, `.githooks/`, and `.pre-commit-config.yaml` against the skeleton's `templates/base/` copies. Record every difference and classify it: intentional (documented in a PR body or commit message) or drift.
2. Check label-name consistency: the spec waiver label and body-line format that `attestations.yaml` greps in each repo, against the labels that actually exist (`gh label list`). Flag any repo where the workflow greps a name the label set does not carry, and any naming split across repos (for example `ignore:spec` against `spec:none`).
3. Check provenance freshness in deck: for every file under `runes/` with a `.provenance/<name>.yaml` record, compare the recorded subject sha256 with the file's current hash. List mismatches.
4. Report: update the single standing issue titled "Weekly ceremony audit" in runedeck/deck (create it once if absent) with this week's findings as a dated comment: drift table, label findings, provenance mismatches, and a one-line verdict (clean, or N findings). Keep it under 40 lines.
5. Success: the standing issue has one new dated comment with accurate findings. Do not fix anything, push commits, or open other issues.
