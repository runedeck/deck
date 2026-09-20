## 1. Implementation

- [x] 1.1 State the foundation requirements
- [x] 1.2 Map each requirement to its enforcing check (using a linter) and record every gap
- [ ] 1.3 Add the missing checkers from the gap list. A new checker starts as a warning with a declared baseline.
- [ ] 1.4 When the directories-direct change arrives, move the Directories Direct requirement out of markdown-first-authoring with a REMOVED delta

## 2. Verification

- [x] 2.1 `openspec validate --all --strict` passes (2026-09-20)
- [ ] 2.2 Every requirement names an enforcing check or a declared gap
- [ ] 2.3 Commit a passing and a failing fixture for each script under `scripts/` that checks names, record ids, record fields, and record links (CORE-0018)
