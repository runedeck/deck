## 1. Specifications

- [x] 1.1 State each principle as a requirement with a scenario that can fail
- [ ] 1.2 Define every term the specifications use in the ontology and link it at every use, first use emphasized. Every term is defined and the first use in each file is an emphasized link. Later uses are not all linked yet, and the owner decides the rule for them
- [x] 1.3 Write one record per decision, citing its requirements as upstream
- [x] 1.4 Decide flat frontmatter (dropped) and the Directories Direct check (review enforces it, one narrow check for qualifier names)
- [ ] 1.5 Decide the remaining open questions: templates, measurable
- [ ] 1.6 Decide the still-open requirements: Semantic Density, Verbs Name Actions, One Home Per Fact, Analysis Tool Coverage, Analysis Tool Has Fixtures, Record Cites Its Proofs

## 2. Linters

- [x] 2.1 Reference tags: rumdl reports an undefined or unused tag
- [x] 2.2 Defined terms: `rune validate` and `rune spec validate` read the ontology
- [x] 2.3 Proposal shape: `docs/changes/.mdschema` and its hook
- [x] 2.4 Citations and the word directory: the Core Vale style
- [x] 2.5 A rule for a noun made from a verb: Core.Nominalization
- [x] 2.6 A rule for a wikilink or an `@path` in a record, a specification, or a proposal: Core.DeckLinks
- [x] 2.7 A rule for a user value and a harness placeholder in an instruction: Core.UserValue, Core.HarnessPlaceholder
- [x] 2.8 The repository as an Open Knowledge Format bundle: `scripts/check-okf` against a baseline that only shrinks
- [x] 2.9 Confirm no Vale rule rejects the braced form `${NAME}`: Core.BracedVariable is gone from the tree, and a fixture with the braced form passes
- [x] 2.10 Coverage rows against requirements: `scripts/check-coverage`
- [x] 2.11 A fixture or a test for every check script and every Core Vale rule: `scripts/check-fixtures` against a baseline
- [ ] 2.12 Fixtures for the six scripts in `tests/baselines/fixtures.txt`, then empty it
- [x] 2.13 A description beside every binary asset: `scripts/check-binary-assets`
- [ ] 2.14 Rewrite the nominalized steps in other changes, then raise Core.Nominalization to error
- [ ] 2.15 The glossary as a directory of pages: `generate-glossary --check` over every page in the `glossary-current` hook, `rune spec glossary --write` and `--check` writing the directory in the cli change render-spec-glossary

## 3. Verification

- [ ] 3.1 `openspec validate --all --strict` and `rune spec validate` pass. The first passes today. The second reports every term link as an undefined term until the installed rune reads the link form
- [x] 3.2 Every requirement has a row in the coverage table with a linter or a missed requirement
- [ ] 3.3 Every missed requirement in the table has a task above
- [ ] 3.4 Re-record the two proofs against the renamed requirements and scenarios

## 4. Other tasks from the review of 2026-10-17

- [ ] 4.1 Choose a tool for the narrow check on qualifier directory names a harness acts on
- [ ] 4.2 Build the generators: root index, directory indexes with directory-note includes, glossary pages, changelog
- [ ] 4.3 Build the fixer that adds draft terms, and have the archiver refuse a draft term without a definition
- [ ] 4.4 Teach the assembler to translate exclamation-mark includes per harness, strip term links and the reference definition block, and add a per-instance definition block
- [ ] 4.5 Write the always-on ontology rule: the ontology exists, how to look a term up, when to ask
- [ ] 4.6 Add the push-time external link warning and the weekly online link job
- [ ] 4.7 Add a move command that rewrites links in the same commit
- [ ] 4.8 Add the stale-item check for queue directories, sixty days stale, sixty-seven days error, the unsorted archive never ages
- [ ] 4.9 Derive type from the directory structure schemas, and let the graph export fill it in
- [ ] 4.10 Add the style-checker rules for plain spoken language: unexplained abbreviation, sentence over twenty-five words, bare command in prose, hedging, noun stack, passive without an actor, and the jargon substitutions
- [ ] 4.11 Reword the remaining requirements that say deck for the repository, source for the source state, or italics for terms
- [ ] 4.12 Add the small-commit mark and the check that challenges it when a specification, the ontology, a record, or a test expectation is touched
- [ ] 4.13 Run the evaluation each companion must beat the canon on, and remove the ones that do not
