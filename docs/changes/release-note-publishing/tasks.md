## 0. Owner Review

- [ ] 0.1 Choose the initial release tag and its commit boundary
- [ ] 0.2 Choose a manual dispatch or tag event as the release trigger
- [ ] 0.3 Choose deletion or a Releases pointer for `CHANGELOG.md` after migration
- [ ] 0.4 Choose merge-time or run-time pull request bodies as the note source

## 1. Skeleton Ceremony

- [ ] 1.1 Add the compiler, workflow, and warning gate to the Skeleton root and template payload
- [ ] 1.2 Remove `CHANGELOG.md` from the Skeleton template payload
- [ ] 1.3 Deliver the Skeleton change to Deck through Copier

## 2. Release Publishing

- [ ] 2.1 Implement pull request selection and note extraction from the delta specification
- [ ] 2.2 Create and update one draft with minimum GitHub permissions
- [ ] 2.3 Import the current changelog into the first draft
- [ ] 2.4 Apply the owner-selected post-migration state to `CHANGELOG.md`

## 3. Changelog Ownership Gate

- [ ] 3.1 Add the warning gate and its declared-debt baseline
- [ ] 3.2 Record the specification's flip condition in the debt registry
- [ ] 3.3 Add fixtures for baseline seeding, head refresh, removal, warning, and blocking states

## 4. Verification

- [ ] 4.1 `rune spec validate release-note-publishing` passes
- [ ] 4.2 `rune validate` reports no new errors
- [ ] 4.3 Compiler tests cover squash selection, invalid notes, migration order, extraction, and repeat runs
- [ ] 4.4 A fixture release creates one complete draft and publishes nothing
- [ ] 4.5 The changelog ownership gate fires on a seeded feature change
