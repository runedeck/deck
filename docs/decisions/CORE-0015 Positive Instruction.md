---
title: Positive Instruction
description: Instructions state the wanted behavior, because negative phrasing can prime the behavior it names, and negation stays reserved for true prohibitions
type: adr
category: architecture
tags:
    - architecture
    - rules
    - prompting
status: proposed
created: 2026-08-27
updated: 2026-08-27
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
---

# Positive Instruction

## Context and Problem Statement

Anthropic guidance recommends stating the wanted behavior, because a model continues the conversation it is given, and a forceful prohibition can prime the behavior it names. The deck audit counts twenty negative constructions across the sixteen core rules, many of which restate a preference rather than a prohibition.

## Considered Options

1. Leave phrasing to each author's taste.
2. Decide positive instruction as the norm with a negation-density gate.

## Decision Outcome

Chosen option: positive instruction as the norm.

- An instruction states the wanted behavior: `write plain prose` rather than a markdown prohibition.
- Negation stays reserved for true prohibitions: safety boundaries, security invariants, and destructive actions.
- The negation-density lint fires at warning severity when a changed rune exceeds the threshold, so real prohibitions survive and habitual negation retires.

### Consequences

- [+] Rules read as direction instead of a minefield.
- [+] The rewrite in the context-economy change has a measurable target.
- [-] Some prohibitions need careful positive rewording to keep their exact scope.
