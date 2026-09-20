---
adr: docs/changes/local-push-validation/adr.md
status: proposed
decisions: []
---

# Validate each push locally before publication

## Why

A push from a jj workspace ran the pre-push checks against every diverged local head, so an unrelated stale head in another workspace blocked a clean push. The authorship check read `HEAD` instead of the outgoing range, so a bad identity reached CI. The spec merged on 2026-09-09 under the wrong directory name and without a proposal.

## What Changes

- `.githooks/jj-push` routes an explicit bookmark push through `.githooks/jj-push-bookmark.py`, which runs the pre-push checks against that commit in a disposable Git checkout and publishes only the validated bookmark.
- `scripts/check-authorship` validates the outgoing range and prefers `--to-ref`, `PRE_COMMIT_TO_REF`, `GITLEAKS_PUSH_TO_REF`, then `HEAD`.
- `scripts/author-identity.py` accepts formatted model identities under approved domains.
- A push that names a change, revision, or `--named` target checks only that target (the `change/casts` bookmark carries this part).

## Capabilities

- local-push-validation (new)

## Impact

- `.githooks/jj-push`, `.githooks/jj-push-bookmark.py`, `scripts/check-authorship`, `scripts/author-identity.py`, `scripts/test_jj_push_environment.py`.
- The record in `adr.md` states what the change wants and moves to `docs/decisions/` at archive.
