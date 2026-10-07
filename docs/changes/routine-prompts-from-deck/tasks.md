---
type: tasks
---

# Tasks

## 1. Implementation

- [x] 1.1 `routines/RepositoryDigest.md` and `routines/WeeklyCeremonyAudit.md`: the prompt bodies with an Inputs section and the rewritten Authority section
- [x] 1.2 `routines/README.md`: the stub contract, the value forms, and the trust model
- [x] 1.3 `routines/.mdschema` and the `mdschema-routines` prek hook
- [x] 1.4 The `README.md` layout row and the CHANGELOG line
- [x] 1.5 Record the decision in `adr.md`
- [x] 1.6 The notification format in all four routine files: a result-first headline, grouped bullets, one next step, health only when degraded
- [x] 1.7 The Repository Digest and the Weekly Ceremony Audit end with the notification text as the final message

## 2. Deployment

- [ ] 2.1 Replace the two live routine prompts with the stubs through `RemoteTrigger update`, with the environment, the session context, and the sources in the same call
- [ ] 2.2 One manual run of each routine reads the file and ends with a status other than CONFIGURATION_FAILURE

## 3. Verification

- [x] 3.1 `make validate`, `mdschema check`, `vale --no-global`, and `typos` on the changed files
- [x] 3.2 Cross-harness review of the stubs and the files, 2026-09-28: six findings, all fixed (stub-side checkout check, issue match count, nested-file rejection)

## 4. Deferred by owner decision

- [ ] 4.1 Pin the file by digest or signed tag
- [ ] 4.2 `rune routine`: render and verify a stub from the deck file and the consumer values
- [ ] 4.3 The three scanner routines under `runes/security/`: Dotfiles Scanner, GitHub Exposure, and Online Mentions
