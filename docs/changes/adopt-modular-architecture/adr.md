---
title: "A rune is one governed instruction"
description: "A rune is one governed instruction: a Markdown file with frontmatter, a skill, an agent, a rule, or a hook, with one canon, optional companions and variants, and a provenance sidecar."
type: adr
category: architecture
tags:
    - architecture
    - vocabulary
    - runes
status: proposed
created: 2026-09-23
updated: 2026-09-23
author: "@N4M3Z"
project: deck
related:
    - "CORE-0001 Markdown as System Language"
    - "CORE-0002 Metadata Inside Files"
    - "DECK-0014 Vocabulary Governance"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5-1@claude"]
informed: []
upstream:
    - "obsidian://open?vault=Atlas&file=Library%2FCanvas%2FPlain%20Text%20Is%20The%20System"
    - "harness-independent-authoring#reusable-across-harnesses-and-models"
change: adopt-modular-architecture
---

# A rune is one governed instruction

## Context and Problem Statement

A *rune* [RUNE] is the unit the deck is made of, and this record says what one is.
The foundations define the *instruction* [INSTRUCTION], the file a *harness* [HARNESS] loads to steer a *model* [MODEL], and require that one source serves every harness and model.
A governed instruction has three kinds of part: what is written once, what varies by harness and model, and what records where an instance came from.
Anthropic's glossary calls rules instruction files, and says that Claude Code is the harness and Claude the model inside it ([Claude Code glossary][CC-GLOSSARY]).
Its hooks are settings entries, and a hook rune is the Markdown source that assembly renders into such an entry.

## Considered Options

1. Leave the term to the ontology comment. Then nothing records why a rune has these parts and not others.
2. Write one record that defines the parts and the rule for each: one canon, companions for what one harness needs, variants for what one harness or model needs, a sidecar for provenance, and assembly as the only way to make an instance.

## Decision Outcome

Option 2.

- A rune MUST be one instruction: a Markdown file with YAML frontmatter, of kind skill, agent, rule, or hook. A hook rune is the source of a harness's hook configuration, not the configuration itself.
- A rune MUST have exactly one *canon* [CANON], the harness-neutral entrypoint, and the canon MUST NOT contain a harness-specific instruction.
- A harness-specific instruction MUST live in a *companion* [COMPANION].
- A harness-, model-, or user-specific alternative MUST live in a *variant* [VARIANT].
- An instance MUST come from *assembly* [ASSEMBLY], one for each harness and model, and MUST NOT be edited in its *target* [TARGET].
- Provenance MUST live in the *sidecar* [SIDECAR] under `.provenance/`, the one exception to metadata inside the file (CORE-0002).

### Consequences

- [+] Every requirement that says rune now points at one definition, and the term check refuses a prose use with no ontology entry.
- [+] A new harness costs companions and nothing in a canon.
- [-] A canon that contains harness wording fails the rule, and that wording belongs in a companion.
- [-] Model is a second assembly dimension, and resolving it needs the harness to say which model runs.

[INSTRUCTION]: https://runedeck.ai/ns#Instruction
[CC-GLOSSARY]: https://code.claude.com/docs/en/glossary
[RUNE]: https://runedeck.ai/ns#Rune
[HARNESS]: https://runedeck.ai/ns#Harness
[MODEL]: https://runedeck.ai/ns#Model
[CANON]: https://runedeck.ai/ns#Canon
[COMPANION]: https://runedeck.ai/ns#Companion
[VARIANT]: https://runedeck.ai/ns#Variant
[ASSEMBLY]: https://runedeck.ai/ns#Assembly
[TARGET]: https://runedeck.ai/ns#Target
[SIDECAR]: https://runedeck.ai/ns#Sidecar
