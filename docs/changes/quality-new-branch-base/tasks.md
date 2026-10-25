# Tasks

## 1. Implementation

- [x] 1.1 The range selection step starts at the merge base with `main` when a push off `main` names no earlier head (`d6ebd85d`)
- [x] 1.2 The same fallback covers a rewritten branch whose earlier head no ref reaches

## 2. Verification

- [x] 2.1 The first push of a new `change/**` branch runs the `quality` check over the branch's files, and the Draft Open workflow opens the draft: pull request #78 opened that way on 2026-10-25
- [ ] 2.2 A push to `main` keeps its range, and a pull request keeps its base

## 3. Record

- [ ] 3.1 A record for the decision before archive, under `docs/decisions/` with the next free DECK number
