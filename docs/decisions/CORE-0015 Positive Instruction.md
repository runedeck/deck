---
title: Positive Instruction
description: Instructions state the wanted behavior, because negative phrasing can prime the behavior it names, and negation stays reserved for true prohibitions
type: adr
category: architecture
tags:
    - architecture
    - rules
    - prompting
status: accepted
created: 2026-08-27
updated: 2026-10-19
author: "@N4M3Z"
project: deck
related:
    - "CORE-0013 Context Economy"
upstream:
    - "https://claude.com/blog/best-practices-for-prompt-engineering"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: []
informed: []
change: economy-measure-context-efficiency
---

# Positive Instruction

## Context and Problem Statement

Anthropic's guidance recommends stating the wanted behavior. It does so because a *[model][MODEL]* continues the conversation in front of it, and a forceful prohibition can prime the behavior it names. An audit of the *[deck][DECK]* counted twenty negative constructions across its sixteen core *[rules][RULE]*. Many of them restate a preference and prohibit nothing.

## Considered Options

1. Leave phrasing to each author's taste.
2. Make positive instruction the norm, and add a lint that measures negation density.

## Decision Outcome

Option 2. Positive instruction is the norm.

- Each directive states the wanted behavior, as in `write plain prose`, in place of a prohibition of markdown.
- The author reserves negation for a true prohibition: a safety boundary, a security invariant, or a destructive action.
- The negation-density lint reports a warning when a changed *[rune][RUNE]* exceeds the threshold, so a real prohibition survives and habitual negation leaves the [rune][RUNE].

### Consequences

- [+] A [rule][RULE] tells the [model][MODEL] what to do instead of listing what to avoid.
- [+] The rewrite in the economy-measure-context-efficiency *[change][CHANGE]* has a measurable goal.
- [-] Some prohibitions need a careful rewording in positive form to keep their exact scope.

## More Information

- Rewritten on 2026-10-19 in the plain spoken register. The decision is unchanged.

[MODEL]: ../specs/glossary/model.md
[DECK]: ../specs/glossary/deck.md
[RULE]: ../specs/glossary/rule.md
[RUNE]: ../specs/glossary/rune.md
[CHANGE]: ../specs/glossary/change.md
