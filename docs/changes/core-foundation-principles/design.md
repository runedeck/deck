# Design

## Coverage table

The table has one row for each foundation requirement. Each row states the check that enforces the requirement, or the missed requirement a later analysis tool closes.

| Capability | Requirement | Check or missed requirement |
|---|---|---|
| plain-text-wins | Plain Text Representation | missed requirement: because representability stays a review judgment |
| plain-text-wins | UTF-8 Encoding | missed requirement: no check decodes every text file as UTF-8 or rejects a byte order mark |
| plain-text-wins | Binary Assets Carry a Description | `scripts/check-binary-assets` |
| plain-text-wins | Lossless Renders | the `glossary-current` hook for the glossary render, and a missed requirement for every other render, because no check regenerates a proof GIF or a Vale style from its source |
| plain-text-wins | Projections Are Never a Source | the `sync-idea` hook for an idea snapshot against its vault source, and a missed requirement for a snapshot committed without a sidecar |
| markdown-first-authoring | Markdown System Language | the `rune validate` artifact checks, rumdl MD033 for raw HTML, the Core.DeckLinks Vale rule for wikilinks, and a missed requirement for callouts |
| markdown-first-authoring | Metadata Inside Files | missed requirement: because no mechanical check detects an external metadata index |
| markdown-first-authoring | Flat Frontmatter | the mdschema frontmatter checks and the missed requirement for nested-value detection |
| markdown-first-authoring | Reference Citations | the Core.Citations Vale rule |
| markdown-first-authoring | Defined Terms Cite the Ontology | `rune spec validate` for a first italic use without its tag, and rumdl MD052 and MD053 for the reference tags |
| markdown-first-authoring | The Ontology Defines Every Term | `rune spec validate` for the ontology entry, and the `check-terms` hook without rune |
| markdown-first-authoring | Glossary Renders From The Ontology | the `glossary-current` hook: `scripts/fallback/generate-glossary --check`, which hands over to `rune spec glossary --check` when the installed rune has the flag |
| linked-markdown-notes | Markdown Links Between Files | the Core.DeckLinks Vale rule on records, specifications, and proposals |
| linked-markdown-notes | Link Targets Resolve | the lychee offline link check with fragments |
| open-knowledge-format | Type On Every File | `scripts/check-okf` against `tests/baselines/okf.txt`, a baseline that only shrinks |
| open-knowledge-format | Path Is The Identifier | `scripts/check-okf` |
| open-knowledge-format | Reserved Names | `scripts/check-okf` |
| open-knowledge-format | Bundle Declares Its Version | `scripts/check-okf`, warning-first until the repository root `index.md` exists |
| directories-direct-routing | Directories Direct | the Core.Terminology Vale rule for the word `folder`, and a missed requirement for the routing judgment |
| directories-direct-routing | Catch-All Directories Drain | missed requirement: no check reads a queue at session end |
| instruction-environment-variables | Variables Are $NAME | the Core.UserValue Vale rule on instructions |
| instruction-environment-variables | The Shell Resolves the Variable | missed requirement: no check finds a named variable that no step reads, and substitution at assembly time is a later capability |
| instruction-environment-variables | Harness Placeholders Stay in the Harness File | the Core.HarnessPlaceholder Vale rule on instructions, off in a harness companion directory |
| harness-independent-authoring | Reusable Across Harnesses and Models | `rune validate` for one entrypoint per instruction, and the deployment drift check |
| harness-independent-authoring | Layout Is Enforced | `rune validate`, mdschema, and the deployment manifest, with the Agent Skills validator as a missed requirement: when it joins the hooks it runs strict on the `agentskills` assembly only, because a harness assembly is allowed to differ (Claude Code uses PascalCase skill directories where the specification uses kebab-case) |
| harness-independent-authoring | Harness Specifics Stay Beside the Source | `rune validate` for the harness-file layout, and the missed requirement for harness wording inside a source |
| harness-independent-authoring | One Instance per Harness | `rune validate` for the deployment manifest and `scripts/check-provenance` for the sidecar |
| harness-independent-authoring | Portable Instructions | missed requirement: closable with an assembly run for every harness with no harness file present |
| minimal-complexity-possible | Ceremony Matches The Task | missed requirement: because task size is a review judgment |
| one-source-of-truth | Code Is Truth | missed requirement: because no check compares a comment with its code |
| one-source-of-truth | One Home Per Fact | missed requirement: because no check finds a copied statement |
| minimal-complexity-possible | Semantic Density | missed requirement for a sentence that states nothing, while Vale with the STE and Deslop styles reports filler |
| minimal-complexity-possible | Verbs Name Actions | the Core.Nominalization Vale rule on headings and steps, warning-first until its baseline is clean |
| lint-enforced-foundations | Analysis Tool Coverage | `scripts/check-coverage`: every stated requirement has a row and every row names a stated requirement |
| lint-enforced-foundations | Record Cites Its Proofs | missed requirement: the graph has the `proves` edge and no check reads it against a record's status yet |
| lint-enforced-foundations | Analysis Tool Has Fixtures | `scripts/check-fixtures` against `tests/baselines/fixtures.txt`, a missed requirement for the scripts in the baseline |
