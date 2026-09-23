# Design

## Coverage table

The table has one row for each foundation *[requirement][REQUIREMENT]*. Each row states the check that enforces the requirement, or the *[missed requirement][MISSEDREQUIREMENT]* a later *[analysis tool][ANALYSISTOOL]* closes. A requirement names a role. The Commands table below names the program behind each row.

| Capability | Requirement | Check or missed requirement |
|---|---|---|
| plain-text-is-futureproof | Plain Text Representation | missed requirement: because representability stays a review judgment |
| plain-text-is-futureproof | UTF-8 Encoding | missed requirement: no check decodes every text file as UTF-8 or rejects a byte order mark |
| plain-text-is-futureproof | Binary Assets Carry a Description | `scripts/check-binary-assets` |
| plain-text-is-futureproof | Lossless Renders | the `glossary-current` hook for the glossary pages, and a missed requirement for every other render, because no check regenerates a proof GIF or a Vale style from its state file |
| plain-text-is-futureproof | Projections Are Never Authoritative | the `sync-idea` hook for an idea snapshot against its vault source state, and a missed requirement for a snapshot committed without a provenance record and for a committed file generated from a projection |
| markdown-with-yaml-frontmatter | Markdown System Language | the `rune validate` artifact checks, rumdl MD033 for raw HTML, the Core.DeckLinks Vale rule for wikilinks, and a missed requirement for callouts |
| markdown-with-yaml-frontmatter | Metadata Inside Files | `scripts/check-provenance` for the sealed sidecar, and a missed requirement for an external metadata index, because no mechanical check detects one |
| markdown-with-yaml-frontmatter | Reference Citations | the Core.Citations Vale rule |
| markdown-with-yaml-frontmatter | Defined Terms Cite the Ontology | `rune spec validate` for a first use that is not emphasized or a later use that is, the `check-terms` hook without rune, rumdl MD052 and MD053 for the reference tags, and a missed requirement for the assembler stripping links from an instance |
| markdown-with-yaml-frontmatter | The Ontology Defines Every Term | `rune spec validate` for a term link with no ontology entry and a warning on a draft term, the `check-terms` hook without rune, and a missed requirement for the archive refusal until the archiver refuses a draft term |
| markdown-with-yaml-frontmatter | Glossary Renders From The Ontology | the `glossary-current` hook: `scripts/fallback/generate-glossary --check` over every page, which hands over to `rune spec glossary --check` when the installed rune writes a directory |
| markdown-relative-links-matching | Markdown Links Between Files | the Core.DeckLinks Vale rule for a wikilink or an at-sign reference in a record, a specification, or a proposal, and a missed requirement for the include translation until the assembler does it |
| markdown-relative-links-matching | Link Targets Resolve | the lychee offline link check with fragments and no exclusions on the commit path, `rune spec validate` and the `check-terms` hook for term links, the pre-push lychee hook that warns on external links in changed files, and the weekly `links.yaml` workflow that reports dead links |
| open-knowledge-format-bundle | Type On Every File | `scripts/check-okf`, which derives the type from the nearest structure schema and accepts an untyped file, and a missed requirement for the graph export filling the type in |
| open-knowledge-format-bundle | Path Is The Identifier | `scripts/check-okf` for an `id` key that differs from the path, and a missed requirement for the move that rewrites links until the move command exists |
| open-knowledge-format-bundle | Reserved Names | `scripts/check-okf` for frontmatter on a reserved name, and a missed requirement for a hand-edited directory index until the generator writes it |
| open-knowledge-format-bundle | Bundle Declares Its Version | `scripts/check-okf`, warning-first until the generator writes the root `index.md` |
| directories-direct-the-tools | Directories Direct | the Core.Terminology Vale rule for the word `folder`, and a missed requirement for the routing judgment, which review enforces |
| directories-direct-the-tools | Qualifier Directory Names Are Checked | missed requirement: the narrow check on the directory names a harness acts on has no tool chosen yet |
| directories-direct-the-tools | Catch-All Directories Drain | `scripts/check-stale-queue`: an item older than sixty days since its first commit is stale, older than sixty-seven days an error, and the unsorted archive never ages |
| user-values-and-variables | Variables Are $NAME | the Core.UserValue Vale rule on instructions, and a missed requirement for the assembler leaving a user variable unsubstituted |
| user-values-and-variables | Canon Stays Vendor-Neutral | the Core.HarnessPlaceholder Vale rule on instructions, off in a harness companion directory, `rune validate` for the harness-file layout, and a missed requirement for harness wording inside a canon |
| instructions-stay-vendor-neutral | Reusable Across Harnesses and Models | `rune validate` for one entrypoint per instruction, the deployment drift check, and a missed requirement for an assembly run for every harness with no sidecar present |
| instructions-stay-vendor-neutral | Layout Is Enforced | `rune validate` and mdschema for the canon and its sidecars, the deployment manifest for every target, and a missed requirement for each harness's own schema over its instances, where the Agent Skills validator runs strict only for a harness that loads that format |
| instructions-stay-vendor-neutral | One Instance per Harness | `rune validate` for the deployment manifest and `scripts/check-provenance` for the provenance record, and a missed requirement for the runtime hook that swaps a model variant |
| instructions-stay-vendor-neutral | Companions Earn Their Place | missed requirement: no evaluation run compares a companion with the canon alone in the hooks yet |
| ceremony-matches-the-task | Ceremony Matches The Task | missed requirement: no check challenges a commit marked small that touches a specification, the ontology, a record, or a test expectation |
| single-source-of-truth | Code Is Truth | missed requirement: no check compares a comment with its code, and the `glossary-current` hook is the only regeneration check so far |
| single-source-of-truth | One Home Per Fact | missed requirement: because no check finds a copied statement |
| ceremony-matches-the-task | Semantic Density | missed requirement for a sentence that states nothing, while Vale with the Simplified Technical English and Deslop styles reports filler |
| ceremony-matches-the-task | Verbs Name Actions | the Core.Nominalization Vale rule on headings and steps, warning-first until its baseline is clean |
| lint-enforced-foundation-requirements | Analysis Tool Coverage | `scripts/check-coverage`: every stated requirement has a row and every row names a stated requirement |
| lint-enforced-foundation-requirements | Record Cites Its Proofs | missed requirement: the graph has the `proves` edge and no check reads it against a record's status yet |
| lint-enforced-foundation-requirements | Analysis Tool Has Fixtures | `scripts/check-fixtures` against `tests/baselines/fixtures.txt`, a missed requirement for the scripts in the baseline |

## Commands

A requirement names a role. This table names the program, flags, hook, and diagnostic ids behind each row, so nothing is lost when a command moves out of a requirement. A row that says "not built" is a task in `tasks.md`.

| Requirement | Role | Command and flags | Hook | Diagnostic ids |
|---|---|---|---|---|
| Binary Assets Carry a Description | validator | `python3 scripts/check-binary-assets` | `check-binary-assets` | `binary` |
| Lossless Renders, Glossary Renders From The Ontology | validator, generator | `rune spec glossary --check`, `rune spec glossary --write`, fallback `scripts/fallback/generate-glossary --check` | `glossary-current` | |
| Projections Are Never Authoritative | validator | `scripts/sync-idea`, `python3 scripts/check-provenance <sidecar>` | `sync-idea`, `check-provenance` | `stale subject digest` |
| Markdown System Language | validator | `rune validate`, `rumdl check` (MD033), Vale Core.DeckLinks | `rune-validate`, `rumdl`, `vale` | |
| Metadata Inside Files | assembler | sidecar path `.provenance/<name>.yaml`, `python3 scripts/check-provenance` | `check-provenance` | |
| Reference Citations | validator | Vale Core.Citations | `vale` | |
| Defined Terms Cite the Ontology | validator, assembler | `rune spec validate`, fallback `python3 scripts/fallback/check-terms`, `rumdl` MD052 and MD053. Link stripping at assembly: not built | `check-terms`, `rumdl` | `spec-term-first-use`, `spec-term-page`, `spec-term-legacy`, with `delta-` twins |
| The Ontology Defines Every Term | validator, fixer, archiver | `rune spec validate`, `rune spec fix --terms` (fallback `scripts/fallback/fix-terms`), `rune spec archive` refusing a draft term | `fix-terms`, `check-terms` | `spec-term-undefined`, `spec-term-draft` |
| Markdown Links Between Files | validator, assembler | Vale Core.DeckLinks. Include translation at assembly: not built | `vale` | |
| Link Targets Resolve | validator, fixer | `lychee --offline --include-fragments` on commit, lychee online at the pre-push stage (warning only), `.github/workflows/links.yaml` weekly, `rune spec fix --terms` | `lychee`, pre-push lychee | |
| Type On Every File | validator, generator | `python3 scripts/check-okf`, `rune graph export` | `check-okf` | `type` |
| Path Is The Identifier | validator | `python3 scripts/check-okf`. Move command that rewrites links: not built | `check-okf` | `id` |
| Reserved Names | validator, generator | `python3 scripts/check-okf`. Index and changelog generators: not built | `check-okf` | `reserved` |
| Bundle Declares Its Version | validator, generator | `python3 scripts/check-okf` (warning until the root index exists). Root index generator: not built | `check-okf` | `version` |
| Directories Direct | validator | Vale Core.Terminology for `folder` | `vale` | |
| Qualifier Directory Names Are Checked | validator | tool not chosen: a custom linter or an extension to `rune validate` | | |
| Catch-All Directories Drain | validator | `python3 scripts/check-stale-queue`, age from read-only git history | `check-stale-queue` | |
| Variables Are $NAME | validator | Vale Core.UserValue. Core.BracedVariable is retired, because the braced form is allowed | `vale` | |
| Canon Stays Vendor-Neutral | validator | Vale Core.HarnessPlaceholder, off in a harness companion directory, `rune validate` | `vale`, `rune-validate` | |
| Reusable Across Harnesses and Models | validator, assembler | `rune validate`, `rune doctor --target <dir> --verify`, `rune install --force` | `rune-validate` | |
| Layout Is Enforced | validator | `rune validate`, `mdschema check`, `rune doctor --verify`. Per-harness schema check and the Agent Skills validator on the `agentskills` assembly: not in the hooks | `rune-validate`, `mdschema-skills` | |
| One Instance per Harness | assembler, deployer | `rune install`, the `.manifest` per target, `.provenance/` sidecars, `python3 scripts/check-provenance`. Runtime hook for a model variant: the change `one-instance-per-model` | `check-provenance` | |
| Companions Earn Their Place | validator | the benchmark harness (BenchArtifact skill) | | |
| Ceremony Matches The Task | validator | small-commit mark and the check that challenges it: not built | | |
| Code Is Truth | generator | `rune spec glossary --write` today. Root index, directory indexes, changelog: not built | `glossary-current` | |
| Semantic Density | validator | Vale with the Simplified Technical English and Deslop styles | `vale` | |
| Verbs Name Actions | validator | Vale Core.Nominalization | `vale` | |
| Analysis Tool Coverage | validator | `python3 scripts/check-coverage` | `check-coverage` | |
| Analysis Tool Has Fixtures | validator | `python3 scripts/check-fixtures` against `tests/baselines/fixtures.txt`, fixtures under `tests/fixtures/<name>/valid/` and `tests/fixtures/<name>/invalid/` | `check-fixtures` | |
| Record Cites Its Proofs | validator | none yet | | |

## Decisions

- The record CORE-0023 Rune Fills the Tool Roles says that rune fills the roles the requirements name: validator, assembler, generator, deployer, fixer, signer, archiver. The requirements stay a philosophy for treating instructions as artifacts, and the record lists the capabilities each role requires.
- Path Is The Identifier rejects two alternatives. A permanently minted id, such as a random id in the frontmatter, pays off only when outsiders hold links into the repository. A bare file name repeats, like every README and every skill's entrypoint.
- Reserved Names: `index.md` lists a directory and `log.md` is a newest-first history under date headings, as sections 8 and 9 of the Open Knowledge Format describe. The directory's authored page follows Obsidian's `folder note` pattern under the name directory note. The generator writes each directory's `index.md` as the directory note included with `![text](relative path)`, then the generated list of contents. The human text lives only in the directory note. The changelog is a separate file from `log.md`.
- Two changes carry what the foundations only name. `environment-variables-supported-syntax` says how a value gets resolved and absorbs the requirement The Shell Resolves the Variable. `one-instance-per-model` holds a variant per model and the runtime hook that swaps it in.
- Four requirements of the first draft are gone. Flat Frontmatter is dropped, and frontmatter may nest. The Shell Resolves the Variable moved to `environment-variables-supported-syntax`. Harness Specifics Stay Beside the Source merged into Canon Stays Vendor-Neutral. Portable Instructions merged into Reusable Across Harnesses and Models as its scenario Every sidecar is removed.
- Directories Direct split on 2026-10-18. The narrow check on the directory names a harness acts on is its own requirement, Qualifier Directory Names Are Checked. The 500-character cap on a requirement body left no room for both the examples and the check. The record CORE-0004 cites Directories Direct alone.
- Layout Is Enforced checks each instance against its own harness's schema because the schemas differ. Claude Code uses PascalCase skill directories where the Agent Skills specification uses kebab-case.
- Metadata Inside Files counts the deployment manifest as a derived store because it describes outputs and no authored file. Frontmatter wins over it, and the generator rewrites it.
- Type On Every File keeps its heading until the owner chooses between the name and its plain-words rewrite, Type Comes From The Directory. The record CORE-0006 cites the current anchor, so the rename changes the record too.

[REQUIREMENT]: ../../specs/glossary/requirement.md
[MISSEDREQUIREMENT]: ../../specs/glossary/missed-requirement.md
[ANALYSISTOOL]: ../../specs/glossary/analysis-tool.md
