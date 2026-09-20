# Tasks

## 1. Implementation

- [x] 1.1 `.githooks/jj-push` routes `-b` and `--bookmark` through `.githooks/jj-push-bookmark.py`
- [x] 1.2 `jj-push-bookmark.py` runs the pre-push checks in a disposable Git checkout and publishes only the validated bookmark, remote, and operation
- [x] 1.3 `scripts/check-authorship` validates the outgoing range with the documented target order
- [x] 1.4 `scripts/author-identity.py` accepts formatted model identities under approved domains
- [ ] 1.5 A push that names a change, revision, or `--named` target checks only that target (`change/casts`)

## 2. Verification

- [x] 2.1 `scripts/test_jj_push_environment.py` covers the isolated checkout
- [ ] 2.2 One recorded proof per scenario under `docs/proofs/local-push-validation/`

## 3. Record

- [ ] 3.1 Archive moves `adr.md` to `docs/decisions/` with the next free DECK number
