# Local push validation design

## Design

The change makes a push check only the target it names. The push hook hands an explicit bookmark push to a bookmark helper. The helper clones that commit into a disposable Git checkout, runs the pre-push checks there, and publishes only the validated bookmark, remote, and operation. The authorship checker reads the outgoing range instead of the current head. The identity checker accepts formatted model identities under approved domains.

## Commands

A requirement names a role. This table names the program, flags, hook, and path behind each row, so nothing is lost when a command moves out of a requirement.

| Requirement | Command | Notes |
|---|---|---|
| Exact bookmark validation | `.githooks/jj-push`, `.githooks/jj-push-bookmark.py` | The push hook routes `-b` and `--bookmark` to the helper. `scripts/test_jj_push_environment.py` covers the isolated checkout (task 2.1). |
| Outgoing authorship validation | `scripts/check-authorship` | Target order: `--to-ref`, `PRE_COMMIT_TO_REF`, `GITLEAKS_PUSH_TO_REF`, then `HEAD`. The trusted policy is `origin/main:authors.yaml`. |
| Future model attribution | `scripts/author-identity.py` | Accepts a formatted identity such as `claude-fable-5.2` under an approved Claude domain. |
