---
title: No Performance Personas
description: Personas do not improve task performance, so runes frame capability through context and tools, and voice guidance stays a register choice
type: adr
category: architecture
tags:
    - architecture
    - agents
    - personas
status: proposed
created: 2026-08-27
updated: 2026-08-27
author: "@N4M3Z"
project: deck
related:
    - "CORE-0013 Context Economy"
upstream:
    - "https://arxiv.org/abs/2311.10054"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: []
informed: []
---

# No Performance Personas

## Context and Problem Statement

A controlled study (Zheng et al., EMNLP 2024 Findings, 162 personas, 4 model families, 2410 questions) shows personas in system prompts do not improve performance over a no-persona control. The best role per question is idiosyncratic, and follow-up work finds persona framing can reduce factual accuracy. Forge-core ARCH-0001 defines agents as specialist personas, so the record needs an amendment for the deck.

## Considered Options

1. Keep persona framing in agents and skills as harmless flavor.
2. Ban performance personas and define agents as execution containers.

## Decision Outcome

Chosen option: ban performance personas.

- A rune frames capability through context, tools, and verifiable procedure. A rune does not claim expertise as capability.
- An agent is an execution container: a fresh context window, a tool allowlist, and a model choice. The container is the value. The persona text is not.
- Voice guidance for outward-facing text is a register choice and stays permitted. It carries no capability claim.
- An exception needs a bench verdict, never a preference.

### Consequences

- [+] The persona lint becomes a deterministic gate at warning severity.
- [+] Agent definitions shrink to the fields that change behavior.
- [-] Existing avatar and voice artifacts need a review against the carve-out.
