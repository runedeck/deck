---
adr: "docs/decisions/CORE-0001 Markdown as System Language.md"
status: accepted
decisions:
    - "CORE-0001 Markdown as System Language"
    - "CORE-0002 Metadata Inside Files"
    - "CORE-0003 YAML Frontmatter for Machine Readability"
    - "CORE-0004 Directories Direct"
    - "CORE-0005 Variables in Markdown Instructions and Templates"
    - "CORE-0006 YAML Configuration Files"
    - "CORE-0007 Unified Module Validation"
    - "CORE-0008 Verified Remote Execution"
    - "CORE-0009 Reference Citations"
    - "CORE-0018 Fixture-Based Canary Testing"
---

# Core foundation principles

## Why

The first principles of the system:

- If a piece of information has a text representation, the system can work with it ([Textuality][TAOUP]).
- Markdown with YAML frontmatter is the chosen representation. One file serves a person, a model, and a PKM tool without conversion ([Obsidian Properties][OBS-PROPS], [MIF][MIF]).
- Metadata travels inside the file it describes ([MIF][MIF]).
- The Markdown-plus-frontmatter shape is the established PKM format ([Obsidian Properties][OBS-PROPS], [Jekyll][JEKYLL], [Hugo][HUGO]).
- Frontmatter stays flat.
- Every architectural decision with alternatives needs a record with a status lifecycle and a fixed shape ([Nygard][NYGARD], [MADR][MADR], [Structured MADR][SMADR]).
- Every required behavior needs a specification requirement ([OpenSpec][OPENSPEC], [RFC 2119][RFC-2119]).
- Directories direct. A directory name is a routing decision.
- Instructions read configuration from environment variables. Templates instantiate from placeholders. Modules work from committed defaults with user overrides merged over them.
- One validation path runs every check, locally and in CI, with one chosen checker per concern.

Current-generation models change what good instruction looks like ([context engineering][CTX], [persona study][PERSONA]), and some principles stay constant:

- A lean instruction set keeps measured results: removing over 80 percent of a production system prompt lost no performance ([context engineering][CTX]).
- A way to verify output outranks another paragraph of guidance (CORE-0013).
- One home per statement: a duplicated statement requires maintenance and eventually drifts (CORE-0013).

Every commitment above must be checkable, not only stated. Instructions say what gets done, not how it should feel. Compliance comes from four levers, strongest first:

1. **Architecture** removes the cause: better structure, better data. One canonical tree ends mirror drift.
2. **Lint or test** catches every recurrence mechanically. A Vale rule flags a banned word on write.
3. **Skill or rule** makes the practice an artifact models load. The ScenarioTitles rule fixes titles at authoring.
4. **Human review** catches what nothing else did, the weakest net.

## What Changes

We work with LLMs through a controlled environment: we specify, lint, and version every instruction. No vendor, harness, or model locks us in. This change makes the foundations enforceable:

- A plain-text-wins capability: everything a model reads has an authoritative plain-text representation.
- A markdown-first-authoring capability: the chosen representation, the metadata home, the frontmatter shape, and the supporting conventions.
- A harness-independent-authoring capability: artifacts author once and assemble per provider into one instance with known provenance.
- A lint-enforced-foundations capability: the checker map names, for every foundation requirement, its check or a declared gap that closes warning-first.

## Capabilities

This change carries deltas for:

- plain-text-wins: plain text as the universal representation.
- markdown-first-authoring: Markdown with flat YAML frontmatter as the system language.
- harness-independent-authoring: author once, assemble per provider, no lock-in.
- lint-enforced-foundations: a lint rule, a validator, or a declared gap for every requirement.

The full planned capability map. A tag marks what exists: (*) a delta in this change, (+) a delta in an active change, (=) canonical already. No tag means a later intake:

```text
representation                       discipline
  plain-text-wins           (*)        architecture-decision-records  (+)
  markdown-first-authoring            (*)        change-lifecycle               (+)
  directories-direct                   context-economy                (+)
  declared-world            (+)        idea-intake                    (+)
                                       draft-gating                   (+)
artifacts                              declared-constraints           (+)
  skills-agents-rules
  adoption-session-state    (=)      enforcement
  artifact-extraction       (+)        lint-enforced-foundations               (*)
  artifact-lifecycle        (+)        artifact-benchmarking          (+)
  mif-alignment             (+)        workflow-security              (=)
  model-assembly
                                     independence
                                       harness-independent-authoring           (*)
```

The model-assembly intake extends the provider-edge contract of artifact-lifecycle rather than starting from zero.

## Impact

- The four delta capabilities in this change, the capability map above, and later the checker configurations the gap list names.

## Glossary

- **rune**: one instruction artifact: a skill, an agent, or a rule.
- **artifact**: any file the system tracks: runes, records, specifications, and their companions.
- **capability**: one named area of required behavior with its canonical specification.
- **requirement**: one testable MUST statement inside a capability, with at least one scenario.
- **change**: one proposal directory that carries requirement deltas until archive merges them.
- **delta**: the openspec term for a change-local specification: ADDED, MODIFIED, or REMOVED requirements.
- **checker map**: the table binding each requirement to its lint rule, validator, or declared gap.
- **declared gap**: a requirement with no mechanical check yet, recorded instead of pretended.

## Sources

- [The Art of Unix Programming, chapter 5: Textuality][TAOUP]
- [Obsidian Properties][OBS-PROPS]
- [MIF][MIF], the modern statement of metadata inside files
- [Jekyll][JEKYLL] and [Hugo][HUGO] front matter, the static-site lineage
- [Documenting Architecture Decisions][NYGARD], Michael Nygard's original post
- [MADR][MADR] and the [MADR Template Primer][MADR-PRIMER]
- [Structured MADR][SMADR], the machine-readable extension runeADR builds on
- [OpenSpec][OPENSPEC], the change lifecycle this tree implements
- [RFC 2119][RFC-2119], the MUST vocabulary of requirements
- [The new rules of context engineering for Claude 5 generation models][CTX] and the [persona study][PERSONA]

[TAOUP]: https://www.catb.org/~esr/writings/taoup/html/ch05s01.html
[OBS-PROPS]: https://help.obsidian.md/properties
[MIF]: https://github.com/modeled-information-format/MIF
[JEKYLL]: https://jekyllrb.com/docs/front-matter/
[HUGO]: https://gohugo.io/content-management/front-matter/
[NYGARD]: https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions
[MADR]: https://adr.github.io/madr/
[MADR-PRIMER]: https://www.ozimmer.ch/practices/2022/11/22/MADRTemplatePrimer.html
[SMADR]: https://smadr.dev
[OPENSPEC]: https://github.com/Fission-AI/OpenSpec
[RFC-2119]: https://www.rfc-editor.org/rfc/rfc2119
[CTX]: https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models
[PERSONA]: https://arxiv.org/abs/2311.10054
