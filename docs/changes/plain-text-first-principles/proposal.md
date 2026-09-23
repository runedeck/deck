---
adr: "docs/decisions/CORE-0001 Markdown as System Language.md"
status: accepted
decisions:
    - "CORE-0001 Markdown as System Language"
    - "CORE-0002 Metadata Inside Files"
    - "CORE-0003 YAML Frontmatter for Machine Readability"
    - "CORE-0004 Directories Direct"
    - "CORE-0005 Variables in Markdown Instructions and Templates"
    - "CORE-0006 Open Knowledge Format Bundle"
    - "CORE-0007 Fixture-Based Canary Testing"
    - "CORE-0008 File over App"
    - "CORE-0009 Reference Citations"
    - "CORE-0023 Rune Fills the Tool Roles"
---

# Core foundation principles

## Why

We steer language *[models][MODEL]* with written *[instructions][INSTRUCTION]*, and we want those instructions to outlast any model, *[harness][HARNESS]*, or vendor. A harness is replaced every year. A model changes with every release, and an instruction tuned for one generation over-specifies for the next ([context engineering][CTX], [persona study][PERSONA]). The durable part is the instructions, the records of why they are what they are, and the specifications they answer to. That part needs a form that survives the turnover.

Plain text is that form. Anything with a text *[representation][REPRESENTATION]* is something every tool we use can read, diff, search, and version ([Textuality][TAOUP]). Among plain-text formats, Markdown with YAML frontmatter is the one a person reads in an editor and a model reads through a harness. A note-taking tool such as Obsidian indexes the same file with no conversion ([Obsidian Properties][OBS-PROPS], [Jekyll][JEKYLL], [Hugo][HUGO]). Markdown is also the format the models themselves were trained to read and write.

From that choice the rest follows:

- Metadata belongs inside the file it describes, so the file carries everything about itself wherever it goes ([MIF][MIF]). Frontmatter is YAML and may nest.
- Files link to each other with relative Markdown links. A file's type comes from its directory's *[structure schema][STRUCTURESCHEMA]* unless the file says otherwise. So a directory of files reads as a graph with no database beside it ([Open Knowledge Format][OKF]).
- The work sits in files the owner holds, in a format any tool reads. A tool keeps at most a cache that rebuilds from the files ([File over app][FOA]).
- A directory name tells a tool what to do with the files inside it. The tree then needs no guide about where things go ([Convention over Configuration][RAILS]).
- A shared instruction refers to a user-specific value as a shell variable, `$NAME` or `${NAME}`, and never spells it out. How the value gets resolved is the subject of the change `environment-variables-supported-syntax`.
- An instruction is written once and reused by every harness and model. What one harness needs sits beside the *[state file][STATEFILE]* as *[basis parameters][BASISPARAMETERS]*. The *[assembler][ASSEMBLER]* produces one *[instance][INSTANCE]* per harness with its *[provenance record][PROVENANCERECORD]* sealed. A model's variant is swapped in at run time, the subject of the change `one-instance-per-model`.
- Every expectation is a *[requirement][REQUIREMENT]* with a *[scenario][SCENARIO]* that can fail ([RFC 2119][RFC-2119]). Every decision with alternatives gets a record with a status lifecycle and a fixed structure ([Nygard][NYGARD], [MADR][MADR], [Structured MADR][SMADR]). A record cites a source by name where it uses it. A bare number is never a citation.
- A requirement is proven: each scenario ends in a recording a reader can replay. An analysis tool is proven by one input it accepts and one it rejects.
- Complexity is removed wherever a way is found. Ceremony matches the task. Code is authoritative over prose, because the code is what runs, and anything derived regenerates on demand or does not exist. A fact has one home, and every other file links there. Every line in a model's context has to earn its place. A line that stays in context costs tokens on every turn ([context engineering][CTX]). An action is named with a verb: `accepting a specification` rather than `specification acceptance`.

Two ideas from science decide what stays in an instruction, *[falsifiability][FALSIFIABILITY]* and *[Occam's razor][OCCAMSRAZOR]*. A requirement states a check that can fail, and the shortest instruction that passes the check is the one we keep. Removing over eighty percent of a production system prompt kept the same evaluation score. That is the measure a cut has to meet ([context engineering][CTX]). Instructions say what gets done, and never how it should feel. Compliance comes from four levers, strongest first:

1. **Architecture** removes the cause: better structure, better data. One canonical tree ends mirror drift.
2. **Tests and linters** catch every recurrence mechanically. A prose rule flags a banned word on write.
3. **Instructions**, meaning skills and rules, steer the model directly.
4. **Human review** comes last. Human attention is the most expensive resource, so it catches only what nothing else did.

Three positions argue against parts of this, and each gets an answer rather than silence:

- Prompts are technical debt ([Theo][THEO-DEBT]): behavioral steering decays silently with every model upgrade, so an instruction file holds concrete facts. Our answer is the benchmark. A behavioral instruction stays only while it beats a facts-only baseline, and the benchmark runs again when the model changes.
- HTML is the better output for people ([Theo][THEO-HTML]): an agent's report is denser and interactive as HTML. Our answer keeps the split. Markdown is the *[source state][SOURCESTATE]*, and HTML is a *[render][RENDER]* of it. The reverse never holds.
- Markdown is a terrible language ([Theo][THEO-MD]): ambiguous syntax and dialect drift break the portability promise. Our answer is a defined subset. The *[repository][REPOSITORY]* names the Markdown it accepts and checks it on every write, because a shared file extension is not a shared parse.

## What Changes

The foundations are ten *[capabilities][CAPABILITY]*. Each capability has one specification, and each requirement in it has a scenario that can fail. Each requirement is bound to its check or to a *[missed requirement][MISSEDREQUIREMENT]* in a *[coverage][COVERAGE]* table. A requirement names a role and never a program. The *[validator][VALIDATOR]* reports, the assembler builds, the *[generator][GENERATOR]* writes derived files, the *[fixer][FIXER]* repairs, and the *[archiver][ARCHIVER]* accepts a change. The record CORE-0023 says that rune fills those roles.

Two further *[changes][CHANGE]* carry what the foundations only name. `environment-variables-supported-syntax` says how a value a shared instruction refers to gets resolved. `one-instance-per-model` says how a model's variant is swapped in at run time.

## Capabilities

### New Capabilities

- `plain-text-is-futureproof`: every *[artifact][ARTIFACT]* has an authoritative plain-text representation, and text is UTF-8. A committed render regenerates from its state file, and a *[projection][PROJECTION]* is never authoritative.
- `markdown-with-yaml-frontmatter`: GitHub Flavored Markdown with YAML frontmatter is the system language, and metadata is inside the file. Citations are reference links, a defined term links to its glossary page, and the glossary is one generated page per term.
- `markdown-relative-links-matching`: files reference each other with relative Markdown links that all resolve. A state file includes another with the exclamation-mark link that the assembler translates per harness, and wikilinks stay out.
- `open-knowledge-format-bundle`: the repository is an Open Knowledge Format 0.2 bundle. A file's type comes from its directory's structure schema, and the path is the identifier. The reserved names are respected, and the root index is generated with the version.
- `directories-direct-the-tools`: a directory name tells a tool what to do. An item in a queue directory is stale after sixty days and an error after sixty-seven.
- `user-values-and-variables`: a shared instruction refers to a user-specific value as `$NAME` or `${NAME}`. The canon stays vendor-neutral, with harness specifics in its basis parameters.
- `instructions-stay-vendor-neutral`: an instruction is written once, and assembly makes one instance per harness with a sealed provenance record. Each instance is checked by its harness's schema, and a companion stays only while it beats the canon on an evaluation.
- `ceremony-matches-the-task`: ceremony matches the task and a check challenges a commit marked small. Every line in context earns its place, and actions are named with verbs.
- `single-source-of-truth`: code is authoritative over prose, and anything derived regenerates on demand or does not exist. Each fact has one home that every other file links to.
- `lint-enforced-foundation-requirements`: a coverage table binds every foundation requirement to its check or to a missed requirement that closes warning-first. Every analysis tool is proven by fixtures.

## Impact

- Ten canonical specifications under `docs/specs/`.
- Ten records under `docs/decisions/`, each citing the requirements it answers as its upstream. CORE-0003 is amended so frontmatter may nest, and CORE-0023 names the roles rune fills.
- An ontology, `ontology/rune.ttl`, that defines every term the specifications use. Shape constraints (SHACL) that a commit must pass sit beside it, with a JSON-LD context that maps every frontmatter key to its term.
- A glossary of one generated page per term under `docs/specs/glossary/`, which every term link points at.
- A coverage table in `design.md` with one row per requirement and the commands behind each row. The linters and check scripts those rows name are each proven by fixtures.
- A plain-text snapshot of the canvas under `docs/ideas/`.

## Sources

- [Plain Text Wins][CANVAS-PT], the canvas
- [The Art of Unix Programming, chapter 5: Textuality][TAOUP]
- [File over app][FOA], Steph Ango, 2023
- [Obsidian Properties][OBS-PROPS]
- [MIF][MIF], metadata inside files
- [Open Knowledge Format 0.2][OKF], a directory of Markdown files with a type and Markdown links
- [Jekyll][JEKYLL] and [Hugo][HUGO] front matter
- [Documenting Architecture Decisions][NYGARD], Michael Nygard
- [MADR][MADR], the [MADR Template Primer][MADR-PRIMER], and [Structured MADR][SMADR]
- [OpenSpec][OPENSPEC], the change lifecycle
- [RFC 2119][RFC-2119], the MUST vocabulary of requirements
- [Convention over Configuration][RAILS], the Rails doctrine
- [The new rules of context engineering for Claude 5 generation models][CTX] and the [persona study][PERSONA]
- Theo Browne (t3.gg) on [prompts as technical debt][THEO-DEBT], [HTML as agent output][THEO-HTML], and [Markdown as a terrible language][THEO-MD]
- Skill collections the adoption review measures against: [Matt Pocock's skills][MATT-SKILLS], [Lauren Tan's pstack][PSTACK], [obra/superpowers][SUPERPOWERS], [anthropics/skills][ANTHROPIC-SKILLS], [garrytan/gstack][GSTACK], and the [awesome-agent-skills][AWESOME-SKILLS] index

[CANVAS-PT]: obsidian://open?vault=Atlas&file=Library%2FCanvas%2FPlain%20Text%20Wins
[TAOUP]: https://www.catb.org/~esr/writings/taoup/html/ch05s01.html
[FOA]: https://stephango.com/file-over-app
[OBS-PROPS]: https://help.obsidian.md/properties
[MIF]: https://github.com/modeled-information-format/MIF
[OKF]: https://github.com/GoogleCloudPlatform/open-knowledge-format-bundle/blob/main/SPEC.md
[JEKYLL]: https://jekyllrb.com/docs/front-matter/
[HUGO]: https://gohugo.io/content-management/front-matter/
[NYGARD]: https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions
[MADR]: https://adr.github.io/madr/
[MADR-PRIMER]: https://www.ozimmer.ch/practices/2022/11/22/MADRTemplatePrimer.html
[SMADR]: https://github.com/modeled-information-format/structured-madr
[OPENSPEC]: https://github.com/Fission-AI/OpenSpec
[RFC-2119]: https://www.rfc-editor.org/rfc/rfc2119
[RAILS]: https://rubyonrails.org/doctrine#convention-over-configuration
[CTX]: https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models
[PERSONA]: https://arxiv.org/abs/2311.10054
[THEO-DEBT]: https://www.youtube.com/watch?v=rTMRlqT8Q8c
[THEO-HTML]: https://www.youtube.com/watch?v=S9EGx6ik-18
[THEO-MD]: https://www.youtube.com/watch?v=DWcqbPm_Rn4
[MATT-SKILLS]: https://github.com/mattpocock/skills
[PSTACK]: https://github.com/cursor/plugins/tree/main/pstack
[SUPERPOWERS]: https://github.com/obra/superpowers
[ANTHROPIC-SKILLS]: https://github.com/anthropics/skills
[GSTACK]: https://github.com/garrytan/gstack
[AWESOME-SKILLS]: https://github.com/VoltAgent/awesome-agent-skills
[MODEL]: ../../specs/glossary/model.md
[INSTRUCTION]: ../../specs/glossary/instruction.md
[HARNESS]: ../../specs/glossary/harness.md
[REPRESENTATION]: ../../specs/glossary/representation.md
[STRUCTURESCHEMA]: ../../specs/glossary/structure-schema.md
[STATEFILE]: ../../specs/glossary/state-file.md
[BASISPARAMETERS]: ../../specs/glossary/basis-parameters.md
[ASSEMBLER]: ../../specs/glossary/assembler.md
[INSTANCE]: ../../specs/glossary/instance.md
[PROVENANCERECORD]: ../../specs/glossary/provenance-record.md
[REQUIREMENT]: ../../specs/glossary/requirement.md
[SCENARIO]: ../../specs/glossary/scenario.md
[FALSIFIABILITY]: ../../specs/glossary/falsifiability.md
[OCCAMSRAZOR]: ../../specs/glossary/occams-razor.md
[SOURCESTATE]: ../../specs/glossary/source-state.md
[RENDER]: ../../specs/glossary/render.md
[REPOSITORY]: ../../specs/glossary/repository.md
[CAPABILITY]: ../../specs/glossary/capability.md
[MISSEDREQUIREMENT]: ../../specs/glossary/missed-requirement.md
[COVERAGE]: ../../specs/glossary/coverage.md
[VALIDATOR]: ../../specs/glossary/validator.md
[GENERATOR]: ../../specs/glossary/generator.md
[FIXER]: ../../specs/glossary/fixer.md
[ARCHIVER]: ../../specs/glossary/archiver.md
[CHANGE]: ../../specs/glossary/change.md
[ARTIFACT]: ../../specs/glossary/artifact.md
[PROJECTION]: ../../specs/glossary/projection.md
