## 1. Specifications

- [x] 1.1 State each principle as a requirement with a scenario that can fail
- [x] 1.2 Define every term the specifications use in the ontology and cite it at first use
- [x] 1.3 Write one record per decision, citing its requirements as upstream
- [ ] 1.4 Decide the open questions: the Directories Direct citation, templates, measurable, flat frontmatter

## 2. Linters

- [x] 2.1 Reference tags: rumdl reports an undefined or unused tag
- [x] 2.2 Defined terms: `rune validate` and `rune spec validate` read the ontology
- [x] 2.3 Proposal shape: `docs/changes/.mdschema` and its hook
- [x] 2.4 Citations and the word directory: the Core Vale style
- [x] 2.5 A rule for a noun made from a verb: Core.Nominalization
- [x] 2.6 A rule for a wikilink or an `@path` in a record, a specification, or a proposal: Core.DeckLinks
- [x] 2.7 A rule for a user value and a harness placeholder in an instruction: Core.UserValue, Core.HarnessPlaceholder
- [x] 2.8 The deck as an OKF bundle: `scripts/check-okf` against a baseline that only shrinks
- [ ] 2.9 Add `type` to every deck file and the root `index.md`, then empty `tests/baselines/okf.txt`
- [x] 2.10 Coverage rows against requirements: `scripts/check-coverage`
- [x] 2.11 A fixture or a test for every check script and every Core Vale rule: `scripts/check-fixtures` against a baseline
- [ ] 2.12 Fixtures for the six scripts in `tests/baselines/fixtures.txt`, then empty it
- [x] 2.13 A description beside every binary asset: `scripts/check-binary-assets`
- [ ] 2.14 Rewrite the nominalized steps in other changes, then raise Core.Nominalization to error
- [x] 2.15 The glossary as a render of the ontology: `scripts/fallback/generate-glossary --check` in the `glossary-current` hook, `rune spec glossary --write` and `--check` in the cli change render-spec-glossary

## 3. Verification

- [x] 3.1 `openspec validate --all --strict` and `rune spec validate` pass
- [x] 3.2 Every requirement has a row in the coverage table with a linter or a missed requirement
- [ ] 3.3 Every missed requirement in the table has a task above
