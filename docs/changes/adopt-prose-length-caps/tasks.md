# Tasks

## 1. Rewrite

- [x] 1.1 Split the six requirement statements over 100 words, every scenario kept under the requirement it proves
- [x] 1.2 Rewrite `CHANGELOG.md` to one line per change in the Keep a Changelog order

## 2. Verification

- [x] 2.1 `rune spec validate` and `rune docs check` from the cli `prose-length-caps` build print no error for the deck
- [x] 2.2 Both prek stages in an isolated clone
- [x] 2.3 `RUNE_CLI_REV` in `quality.yaml` moved to cli `1e4e0639`, which carries the caps
- [x] 2.4 `.pre-commit-config.yaml` carries the `rune-docs-check` hook from skeleton `64e7d2c`, so the commit stage checks `CHANGELOG.md` here too

## 3. Record

- [ ] 3.1 Archive moves `adr.md` to `docs/decisions/` with the next free DECK number
