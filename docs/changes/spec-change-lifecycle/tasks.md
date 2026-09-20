# Tasks

## 1. Implementation

- [x] 1.1 State the lifecycle, grammar, and canonical-tree requirements
- [x] 1.2 Both spec CLIs operate on one tree: `openspec validate --all --strict` and `rune spec doctor` pass on `docs/`
- [x] 1.3 State the name, acceptance, and review rules from the 2026-09-20 alignment
- [x] 1.4 `scripts/check-spec-names` fails a change id or a capability name with fewer than three words, and fails a capability name that breaks the single or several rule

## 2. Verification

- [x] 2.1 `openspec validate --all --strict` passes (2026-09-20)
- [ ] 2.2 A canary change proves that archive merges its delta into the canonical tree without duplication. It fails today: the archive of adopt-session-state duplicated three requirements whose canonical headings differed in case
- [ ] 2.3 `rune spec archive` matches requirement headings without regard to case (cli)
- [ ] 2.4 `rune spec archive` refuses a change that has no record, moves `adr.md` to `docs/decisions/`, and assigns the id (cli)
- [ ] 2.5 `rune spec doctor` carries the name rules, so `scripts/check-spec-names` can retire (cli)
