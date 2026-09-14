---
name: ContinuousIntegration
description: "Run the repository's own check stages locally and repeatedly: the commit stage with every tool required, the push stage on the exact outgoing head, and the checked push dry run on the frozen head before publication. USE WHEN an edit batch is finished, a candidate is frozen, a push or pull request is next, a check failed in CI, or a push hook stopped a publication. NOT FOR configuring hooks or CI, bypassing a failing check, or reviewing code."
metadata:
    version: 0.1.0
---

# ContinuousIntegration

The repository declares its checks once, in `.pre-commit-config.yaml`, and CI runs that file. A local run of the same file, with the same tools required, is the only evidence that a candidate will pass. Run it after every edit batch, not once before the push.

## Constraints

- Run the repository's own configuration. Do not select hooks by hand, and do not replace a hook with a direct call to the tool it wraps.
- Require every tool. Set `REQUIRE_GATES=1` so an absent linter fails instead of skipping. Hooks that wrap `rune` or `mdschema` skip silently when the binary is absent unless the repository's hooks honor a stricter variable (the cli's `REQUIRE_RUNE`), so confirm both binaries are on the path before the run and report their versions in the receipt.
- Record the exit status of the check itself, never the status of a filter behind a pipe. Keep one log per stage with the candidate commit id beside it.
- Never bypass a failing check with `--no-verify`, a hook edit, or an exemption added for the occasion. Fix the finding or hand it to the owner.
- A passing run proves the tree it ran on. Run again after any edit, and once more on the exact head that will be pushed.
- Fix at most three rounds. A finding that survives three fix-and-rerun rounds goes to the owner with the receipts, not into a fourth attempt.
- Signing needs the owner at the key. Finish every check before the step that signs.

## Instructions

### Run the commit stage after each edit batch

```sh
REQUIRE_GATES=1 make validate
```

`make validate` runs `prek run --all-files` through the repository's commit hook. When there is no Makefile, run `REQUIRE_GATES=1 prek run --all-files`. Fix every error-level finding before the next edit batch. A warning does not block, but it goes into the receipt.

### Run the push stage on the outgoing head

In a jj colocated repository with the checked push hook:

```sh
REQUIRE_GATES=1 bash .githooks/jj-push -b <bookmark> --dry-run
```

This replays the pre-push stage in a disposable checkout of the exact bookmark head and pushes nothing. The hook inherits the environment, so `REQUIRE_GATES=1` reaches the hooks it runs. The stage covers the range secret scan, semgrep, authorship, and the rune checks. In a git repository:

```sh
REQUIRE_GATES=1 prek run --stage pre-push --from-ref origin/main --to-ref HEAD
```

When the branch already exists on the remote, pass its remote tip as `--from-ref` so the range matches what the push sends.

### Freeze, then run once more

Describe the change and park the working copy with `jj new`. Run both stages on the frozen head. Any edit after this point restarts the sequence. Only then hand the push, or the signing step, to the owner.

### Declare completion

The checks are complete when every condition holds at once:

- Both stages exit 0 with every tool required. A warning-level finding is reported. An error-level finding is a failure.
- The final run changed no file. Record the working-copy commit id before the run (`jj log -r @ --no-graph -T commit_id`) and compare after it. jj snapshots on every command, so any write changes the id. In git, compare `git diff HEAD | sha256sum`. A formatter or a fixer that wrote something means one more round.
- The run was on the exact commit that will be pushed, and the receipt names that commit id.
- At most three fix rounds were spent. Past that, stop and report.

Anything short of all four is not complete. Report it as a finding with the receipt, never as "passed with notes".

### Record the receipt

Write one log per stage, named for the candidate, and end it with the check's own exit line:

```sh
log="${TMPDIR:-/tmp}/<id>-commit.log"
status=0
REQUIRE_GATES=1 make validate > "$log" 2>&1 || status=$?
echo "exit=$status" >> "$log"
```

Beside the exit line, record what judged the tree, so a later reader can tell whether a pass still means anything:

- The source commit: `jj log -r @- --no-graph -T commit_id` or `git rev-parse HEAD`.
- The check configuration digest: `sha256sum .pre-commit-config.yaml`, and `scripts/tool-versions` when it exists.
- The validator versions: `prek --version` and each pinned tool through `--version`, plus the `rune` binary's path and version when the rune hooks ran.

Report the exit lines, the commit id, and those identities together. A log that ends in a nonzero exit is a finding, not a note.

## Verification

- Both stages exit 0 on the head that will be pushed, with every tool required.
- The final run left the tree unchanged: the working-copy commit id, or the digest of `git diff HEAD`, is the same before and after.
- The receipt names the same commit id as the bookmark or branch head, the configuration digest, and the validator versions.
- No more than three fix rounds were spent.

## Troubleshooting

- `REQUIRE_GATES set and <tool> is absent`: run `make install`, which activates the hooks and runs `scripts/install-tools` for the pinned check tools, then follow `INSTALL.md` for prek and gitleaks.
- `rune` or `mdschema` absent: their hooks skip and print nothing. Install both, or report the skipped checks by name. A receipt without their versions is incomplete.
- semgrep fails inside a sandbox: point `XDG_CONFIG_HOME` and `XDG_CACHE_HOME` at a writable scratch directory.
- `rune spec doctor` reports a change with no proposal: the base is broken, not your edit. Add the proposal in its own commit or report it.
- The push hook stops with `The bookmark changed during validation`: another workspace moved it. Fetch, reconcile, and run again.
