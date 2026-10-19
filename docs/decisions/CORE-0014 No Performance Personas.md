---
title: No Performance Personas
description: Personas do not improve task performance, so runes frame capability through context and tools, and voice guidance stays a register choice
type: adr
category: architecture
tags:
    - architecture
    - agents
    - personas
status: accepted
created: 2026-08-27
updated: 2026-10-19
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
change: economy-measure-context-efficiency
---

# No Performance Personas

## Context and Problem Statement

A controlled study shows that personas in system prompts do not improve performance over a no-persona control. The study is Zheng et al., Empirical Methods in Natural Language Processing (EMNLP) 2024 Findings, with 162 personas, 4 *[model][MODEL]* families, and 2410 questions. The best role per question is idiosyncratic, and follow-up work finds that persona framing can reduce factual accuracy. Forge-core ARCH-0001 defines *[agents][AGENT]* as specialist personas, so the record needs an amendment for the *[deck][DECK]*.

## Considered Options

1. Keep persona framing in [agents][AGENT] and *[skills][SKILL]* as harmless flavor.
2. Ban performance personas and define [agents][AGENT] as execution containers.

## Decision Outcome

Chosen option: ban performance personas.

- A *[rune][RUNE]* frames capability through context, tools, and verifiable procedure. It does not claim expertise as capability.
- An [agent][AGENT] is an execution container: a fresh context window, a tool allowlist, and a [model][MODEL] choice. The container is the value. The persona text adds none.
- Voice guidance for outward-facing text is a register choice and remains permitted. It makes no capability claim.
- An exception needs a bench *[verdict][VERDICT]*. A preference never justifies one.

### Consequences

- [+] The persona lint becomes a deterministic check at warning severity.
- [+] [Agent][AGENT] definitions shrink to the fields that alter behavior.
- [-] Existing avatar and voice *[artifacts][ARTIFACT]* need a review against the carve-out.

## More Information

- Rewritten on 2026-10-19 in the plain spoken register. The decision is unchanged.

[MODEL]: ../specs/glossary/model.md
[AGENT]: ../specs/glossary/agent.md
[DECK]: ../specs/glossary/deck.md
[SKILL]: ../specs/glossary/skill.md
[RUNE]: ../specs/glossary/rune.md
[VERDICT]: ../specs/glossary/verdict.md
[ARTIFACT]: ../specs/glossary/artifact.md
