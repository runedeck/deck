---
title: Context Economy
description: Every instruction earns its resident tokens, each fact lives in one artifact, and judgment replaces rulebooks for Claude 5 generation models
type: adr
category: architecture
tags:
    - architecture
    - context
    - rules
status: proposed
created: 2026-08-27
updated: 2026-08-27
author: "@N4M3Z"
project: deck
related:
    - "CORE-0014 No Performance Personas"
    - "CORE-0015 Positive Instruction"
upstream:
    - "https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: []
informed: []
---

# Context Economy

## Context and Problem Statement

Anthropic removed over 80 percent of the Claude Code system prompt for the Claude 5 generation with no measured loss. The deck was authored under the older assumption that more instruction means more control. The audit at main `34b08e54` counts 2232 words across sixteen core rules and 101 duplicated sentences across runes. Every deployed session pays for this text, and every duplicate is a future conflict.

## Considered Options

1. Keep long rules and rely on review to prune them.
2. Adopt context economy as a decided norm with deterministic gates.

## Decision Outcome

Chosen option: context economy as a decided norm.

- Every instruction earns its resident tokens. A rule states one imperative instruction within 50 words.
- One home per fact. Enforcement lives in hooks and CI. Knowledge lives in skills. Constraints live in rules. Identity and gotchas live in the repository brief. Transient state lives in memory. A fact in two layers is a defect.
- Judgment over rulebooks. Trust the model with context and intent. Reserve hard constraints for invariants and safety.
- Progressive disclosure. Situational content loads on demand through skills and companions, never up front.
- Interfaces over examples. An expressive tool or schema teaches use better than a usage example.
- Verification beats instruction. A way to check output outranks another paragraph of guidance.

### Consequences

- [+] The rule corpus shrinks toward a 900-word budget with gates that keep it there.
- [+] Duplicated guidance retires instead of drifting.
- [-] Compression can drop a real constraint, so displaced content moves to a skill before deletion.

## More Information

Compatibility of the forge-core decisions with this norm:

| Record | Verdict | Note |
| --- | --- | --- |
| CORE-0001 Markdown as System Language | affirmed | unchanged |
| CORE-0002 Metadata Inside Files | affirmed | deck sidecars for sealed evidence stay a recorded exception |
| CORE-0003 YAML Frontmatter | affirmed | unchanged |
| CORE-0004 Adopt ADRs | affirmed | this pass exercises it |
| CORE-0005 ADR Template Choice | affirmed | compact bodies preferred under this norm |
| CORE-0006 Directories Direct | affirmed | naming as configuration matches interfaces over examples |
| CORE-0007 Forge MADR Extensions | affirmed | unchanged |
| CORE-0008 Variables in Markdown | affirmed | unchanged |
| CORE-0009 YAML Configuration | affirmed | unchanged |
| CORE-0010 Unified Module Validation | amended | gains the chosen linter set on migration: one linter per surface, single binary, offline on the commit path, changes by record |
| CORE-0011 Verified Remote Execution | affirmed | deck CI pins actions by commit and verifies release binaries by SHA-256. Package installs remain a compliance gap |
| CORE-0012 Fixture-Based Canary Testing | affirmed | the ontology smoke fixture follows it |
| ARCH-0001 Skills Agents and Rules | amended | agents are containers, never personas, per CORE-0014 |
| ARCH-0002 Skills Companion Files | affirmed | progressive disclosure in practice |
| ARCH-0004 Rules as Shared Conventions | amended | shared stays, shape changes to one instruction within 50 words |
| ARCH-0011 Hook Design Principles | affirmed | strengthened: prose demotes to hooks wherever a check can be code |
| ARCH-0014 Per-Tool Memory Files | diverged | the deck authors once and assembles per tool, so accepted duplication ends |
