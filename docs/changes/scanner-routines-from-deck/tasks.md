---
type: tasks
---

# Tasks

## 1. Implementation

- [x] 1.1 `routines/scripts/exposure_scan.py`: the detector with versioned rules, hashed finding ids, locations, known-finding matching, finding status, and scan health
- [x] 1.2 `tests/test_exposure_scan.py`: fixtures in a temporary repository for every rule, the placeholders, deleted history, the working tree, a shallow clone, known findings, and a missing repository
- [x] 1.3 `routines/DotfilesScanner.md`: the run streams the detector, keeps its status, adds located review items, and reports a three-line push plus the session table
- [x] 1.4 `routines/OnlineMentions.md`: weekly, identity-qualified plan, namesakes discarded, exclusions reviewed, status apart from health
- [x] 1.5 `routines/README.md`: POLICY_REF in the stub contract, the streamed-code rule, the scanner inputs, GitHub Exposure retired
- [x] 1.6 The `exposure-scan-tests` hook, the quality workflow step, and the CHANGELOG line
- [x] 1.7 Record the decision in `adr.md`

## 2. Deployment

- [ ] 2.1 Replace the two live scanner prompts with the stubs through `RemoteTrigger update`, with the environment, the session context, the sources, and the stub values in the same call
- [ ] 2.2 Disable the live GitHub Exposure routine
- [ ] 2.3 One manual run of each routine ends with a health other than CONFIGURATION_FAILURE, and the owner copies the first report's ids into KNOWN_FINDINGS

## 3. Verification

- [x] 3.1 `make validate` in a scratch clone, the detector tests, `mdschema check`, `vale --no-global`, `typos`, and `rune spec validate`
- [x] 3.2 One detector run against a full local clone of the owner's dotfiles with the owner's sensitive domain on the command line, summary counts in the workshop receipt
- [x] 3.3 Cross-harness review round one by Astra and Lumo, 2026-10-02, every finding applied: isolated interpreter, literal secrets, whole lines, linear key blocks, explicit stack, credential-span suppression, every path of a blob, whole commit text, redacted paths and context, acknowledgement per commit, inputs as files, ledger without namesake URLs
- [x] 3.4 Cross-harness review round two, Lumo, 2026-10-03: a quoted value is a literal before any reference test, and an unterminated key header no longer merges with a later key block
- [ ] 3.5 Cross-harness review round two, Astra

## 4. Follow-up

- [ ] 4.1 The overlap between `runes/security/skills/ConfigureScanners/templates/claude/PublicRepositoryExposure.md` and `routines/DotfilesScanner.md`: retire the template or make it render the stub
- [ ] 4.2 A pre-commit or CI rule in the dotfiles repository that runs the detector, so a hostname leak fails before the daily scan sees it
- [ ] 4.3 Test `git fetch --unshallow` once by hand on the platform clone under a time budget before any routine relies on it
- [ ] 4.4 Pin the deck ref by digest or signed tag, and `rune routine` to render a stub from the file and the consumer values
