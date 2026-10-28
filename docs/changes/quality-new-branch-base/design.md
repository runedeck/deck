# New branch checks from merge base design

## Design

The quality workflow selects the range once and hands it to both prek stages. GitHub sends a pull request's base and head, and a push's earlier head and new head. The first push of a branch sends an all-zero earlier head. A branch that jj rewrote and pushed again sends an earlier head that no ref reaches, so the full-history checkout does not contain it. In both cases on a branch other than `main`, the step asks git for the merge base of `origin/main` and the range end, which exists because the checkout fetches the full history. A push to `main` with an all-zero earlier head keeps the all-files path, because no base exists to compare against.

## Commands

A requirement names a role. This table names the workflow, step, hook, and command behind each row, so nothing is lost when a command moves out of a requirement.

| Requirement | Command | Notes |
|---|---|---|
| New branch checks start at the merge base | `.github/workflows/quality.yaml`, step `Select check range` | The validator's range selection. It writes the `usable`, `from`, and `to` outputs that both prek stages read. |
| New branch checks start at the merge base | `git merge-base origin/main "$to"` | The start commit for a push off `main` whose `github.event.before` is all zeros or fails `git cat-file -e`. |
| New branch checks start at the merge base | `prek run --from-ref "$FROM_REF" --to-ref "$TO_REF"` and the same with `--stage pre-push` | Both stages run over the selected range. Without a usable start they run with `--all-files`. |
| New branch checks start at the merge base | `sync-idea` hook, `python3 scripts/sync-idea --check` | The hook that needs a desktop tool, because the Obsidian CLI answers only while Obsidian runs. It watches `docs/ideas/`. |
| New branch checks start at the merge base | `.github/workflows/draft-open.yaml`, job `checks` | Calls the quality workflow on the first push of a ceremony branch. The draft opens only when it passes. |
