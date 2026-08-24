# Routine: deck merge follow-up

- Trigger: GitHub event, pull_request.closed on runedeck/deck, filter: is merged = true.
- Repositories: runedeck/deck.
- Connectors: none required.

## Prompt

A pull request just merged into runedeck/deck. Your job is the consumer follow-up.

1. Read the merged PR (number is in the event): title, body, changed files.
2. Decide what deck consumers must do now. The cases:
   - New or changed artifact under `runes/` (a skill, rule, or agent): consumers refresh with `rune install`; a new artifact also needs `rune skill add <Name>` or `rune rule add <Name>` first.
   - Ceremony change (`.github/workflows/`, `.githooks/`, `.pre-commit-config.yaml`): consumers built from the skeleton receive it via `copier update`; note any drift risk with the skeleton repo.
   - Docs or specs only: no consumer action.
3. Post one comment on the merged PR titled "Consumer follow-up": the case, the exact commands, and any ordering constraint with other open PRs. Keep it under 15 lines. If no consumer action is needed, post exactly that in one line.
4. Success: the merged PR carries one accurate consumer-follow-up comment. Do not open issues, push commits, or edit anything.
