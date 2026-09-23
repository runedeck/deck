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
---

# Core foundation principles

## Why

We steer language models with written instructions, and we want those instructions to outlast any one model, harness, or vendor. A harness is replaced every year. A model changes with every release, and an instruction tuned for one generation over-specifies for the next ([context engineering][CTX], [persona study][PERSONA]). The instructions, the records of why they are what they are, and the specifications they answer to are the durable part, so they need a form that survives all of that turnover.

Plain text is that form. Anything with a text representation is something every tool we use can read, diff, search, and version ([Textuality][TAOUP]). Among plain-text formats, Markdown with YAML frontmatter is the one a person reads in an editor, a model reads through a harness, and a note-taking tool such as Obsidian indexes, with no conversion between them ([Obsidian Properties][OBS-PROPS], [Jekyll][JEKYLL], [Hugo][HUGO]). Markdown is also the format the models themselves were trained to read and write.

From that choice the rest follows:

- Metadata belongs inside the file it describes, so the file carries everything about itself wherever it goes ([MIF][MIF]). The frontmatter stays flat, because the Properties panel in Obsidian cannot render nested values ([Obsidian Properties][OBS-PROPS]).
- Files link to each other with relative Markdown links, and each file says what type it is, so a directory of files reads as a graph with no database beside it ([Open Knowledge Format][OKF]).
- The work sits in files the owner holds, in a format any tool reads, and a tool keeps at most a cache that rebuilds from the files ([File over app][FOA]).
- A directory name tells a tool what to do with the files inside it, so the tree needs no guide about where things go ([Convention over Configuration][RAILS]).
- A shared instruction refers to a user-specific value as `$NAME` and never spells it out. No harness expands an environment variable inside a file it loads, so the model reads the value through the shell.
- An instruction is written once and reused by every harness and model. What one harness needs sits beside the source, and assembly produces one instance per harness with its provenance sealed.
- Every expectation is a requirement with a scenario that can fail ([RFC 2119][RFC-2119]), and every decision with alternatives gets a record with a status lifecycle and a fixed structure ([Nygard][NYGARD], [MADR][MADR], [Structured MADR][SMADR]). A record cites a source by name where it uses it, never by a bare number.
- A requirement is proven, not asserted: each scenario ends in a recording a reader can replay, and an analysis tool is proven by one input it accepts and one it rejects.
- Complexity is removed wherever a way is found. Ceremony matches the task. Code is authoritative over prose, because the code is what runs. A fact has one home, and every other file links there. Every line in a model's context has to earn its place, since a line that stays in context costs tokens on every turn ([context engineering][CTX]). An action is named with a verb: `accepting a specification`, not `specification acceptance`.

Two ideas from science decide what stays in an instruction, *falsifiability* [FALSIFIABILITY] and *Occam's razor* [OCCAM]. A requirement states a check that can fail, and the shortest instruction that passes the check is the one we keep. Removing over 80 percent of a production system prompt kept the same evaluation score, which is the measure a cut has to meet ([context engineering][CTX]). Instructions say what gets done, not how it should feel. Compliance comes from four levers, strongest first:

1. **Architecture** removes the cause: better structure, better data. One canonical tree ends mirror drift.
2. **Tests and linters** catch every recurrence mechanically. A prose rule flags a banned word on write.
3. **Instructions**, meaning skills and rules, steer the model directly.
4. **Human review** comes last. Human attention is the most expensive resource, so it catches only what nothing else did.

Three positions argue against parts of this, and each gets an answer rather than silence:

- Prompts are technical debt ([Theo][THEO-DEBT]): behavioral steering decays silently with every model upgrade, so an instruction file holds concrete facts. Our answer is the benchmark. A behavioral instruction stays only while it beats a facts-only baseline, and the benchmark runs again when the model changes.
- HTML is the better output for people ([Theo][THEO-HTML]): an agent's report is denser and interactive as HTML. Our answer keeps the split. Markdown is the source, and HTML is derived from it, never the reverse.
- Markdown is a terrible language ([Theo][THEO-MD]): ambiguous syntax and dialect drift break the portability promise. Our answer is a defined subset. The deck names the Markdown it accepts and checks it on every write, because a shared file extension is not a shared parse.

## What Changes

The foundations are ten capabilities. Each capability has one specification, each requirement in it has a scenario that can fail, and each requirement is bound to its check or to a missed requirement in a coverage table.

## Capabilities

### New Capabilities

- `plain-text-wins`: every artifact has an authoritative plain-text representation, text is UTF-8, and a committed render regenerates from its source.
- `markdown-first-authoring`: GitHub Flavored Markdown with flat YAML frontmatter is the system language, metadata is inside the file, citations are reference links, defined terms come from the ontology, and the glossary is a render of it.
- `linked-markdown-notes`: files reference each other with relative Markdown links that resolve. Wikilinks belong to the vault and `@` references to a harness.
- `open-knowledge-format`: the deck is an Open Knowledge Format 0.2 bundle, with a type on every file, the path as the identifier, and the reserved names respected. The one exception is that a rune keeps its `type` under `metadata`.
- `directories-direct-routing`: a directory name tells a tool what to do.
- `instruction-environment-variables`: a shared instruction refers to a user-specific value as `$NAME`, and a placeholder that only one harness expands stays in that harness's file.
- `harness-independent-authoring`: an instruction is written once, harness specifics go beside the source, and assembly makes one instance per harness with sealed provenance.
- `minimal-complexity-possible`: ceremony matches the task, every line in context earns its place, and actions are named with verbs.
- `one-source-of-truth`: code is authoritative over prose, and each fact has one home that every other file links to.
- `lint-enforced-foundations`: a coverage table binds every foundation requirement to its check or to a missed requirement that closes warning-first, and every analysis tool is proven by fixtures.

## Impact

- Ten canonical specifications under `docs/specs/`.
- Nine records under `docs/decisions/`, each citing the requirements it answers as its upstream.
- An ontology, `ontology/rune.ttl`, that defines every term the specifications use, with SHACL constraints that a commit must pass and a JSON-LD context that maps every frontmatter key to its term.
- A coverage table in `design.md` with one row per requirement, and the linters and check scripts those rows name, each proven by fixtures.
- A plain-text snapshot of the canvas under `docs/ideas/`.

## Glossary

The ontology defines every term below, and the tag beside each one points at its definition.

- *artifact* [ARTIFACT]: any file the system tracks.
- *instruction* [INSTRUCTION]: a Markdown file a harness loads to steer a model.
- *representation* [REPRESENTATION]: one form an artifact's content takes. The plain-text one is authoritative.
- *render* [RENDER]: a committed representation that a command in the repository regenerates byte for byte from its plain-text source.
- *projection* [PROJECTION]: a representation that drops information from its source. An index stays uncommitted, and a snapshot is committed only with a provenance sidecar.
- *capability* [CAPABILITY]: one named area of required behavior with its canonical specification.
- *requirement* [REQUIREMENT]: one testable MUST statement inside a capability, with at least one scenario.
- *change* [CHANGE]: one proposal directory with requirement deltas, until a sync or an archive merges them.
- *delta specification* [DELTA]: a change-local specification in [OpenSpec][OPENSPEC] that lists added, modified, removed, or renamed requirements.
- *coverage* [COVERAGE]: the binding of each requirement to its check or missed requirement, kept as a table in the design.
- *missed requirement* [MISSED-REQUIREMENT]: a requirement with no mechanical check yet, recorded as such instead of pretended away.

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
[OKF]: https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md
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
[FALSIFIABILITY]: https://runedeck.ai/ns#Falsifiability
[OCCAM]: https://runedeck.ai/ns#OccamsRazor
[ARTIFACT]: https://runedeck.ai/ns#Artifact
[INSTRUCTION]: https://runedeck.ai/ns#Instruction
[REPRESENTATION]: https://runedeck.ai/ns#Representation
[RENDER]: https://runedeck.ai/ns#Render
[PROJECTION]: https://runedeck.ai/ns#Projection
[CAPABILITY]: https://runedeck.ai/ns#Capability
[REQUIREMENT]: https://runedeck.ai/ns#Requirement
[CHANGE]: https://runedeck.ai/ns#Change
[DELTA]: https://runedeck.ai/ns#Delta
[COVERAGE]: https://runedeck.ai/ns#Coverage
[MISSED-REQUIREMENT]: https://runedeck.ai/ns#MissedRequirement
