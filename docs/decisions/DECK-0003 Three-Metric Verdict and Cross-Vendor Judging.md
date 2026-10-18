---
title: Three-Metric Verdict and Cross-Vendor Judging
description: An artifact earns its place when assertions hold, its claimed behavior improves, and blind preference stays acceptable; no model judges its own vendor
type: adr
category: architecture
tags:
    - benchmarking
    - evaluation
    - judging
status: accepted
created: 2026-08-19
updated: 2026-10-19
author: "@N4M3Z"
project: deck
related: ["DECK-0001 Artifact Benchmarking Skill", "DECK-0002 Benchmark Execution Ladder"]
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: []
informed: []
upstream: []
change: benchmark-instructions-per-model
---

# Three-Metric Verdict and Cross-Vendor Judging

## Context and Problem Statement

One score hides the failure modes that matter. A *[model][MODEL]* can bring a style checker to zero by dropping facts, or keep every fact in prose that no reader accepts. Early iterations of Simplified Technical English (STE) showed both failures. They also showed judge self-preference: a judge [model][MODEL] preferred the baselines it had written itself. The benchmark needs a *[verdict][VERDICT]* rule that catches each failure separately, and a judging scheme that removes the self-preference confound.

## Decision Drivers

- Meaning loss, mechanical compliance, and prose damage fail independently of each other
- Only a blind judge catches an output that satisfies the checker and repels readers
- A judge that grades its own vendor's output measures its own taste instead of quality
- Each *[artifact][ARTIFACT]* claims a different measurable behavior, so the bench has to accept a different middle metric per [artifact][ARTIFACT]

## Considered Options

1. **One combined score**: one number per run. It ranks simply and hides every trade-off.
2. **Checker density with validity filter**: the assertions decide validity, the density decides the [verdict][VERDICT], and prose damage stays invisible.
3. **Three metrics, cross-vendor judging**: the bench reads separate signals together and assigns the judges across vendors.

## Decision Outcome

Chosen option: **Three metrics, cross-vendor judging**. The bench reads the three metrics together within one [model][MODEL] and never combines them into one number.

- **Assertions guard meaning.** An assertion is a frozen statement about a fact, a figure, or a restriction, and a checker tests it objectively. A dropped assertion is a regression whatever the other metrics say.
- **The checker measures the claimed behavior.** The [artifact][ARTIFACT] brings its own checker, a domain *[linter][LINTER]* for a large claim or a generic pattern-density configuration for a small one. The density metric counts checker findings per 100 checker words of the same text.
- **Blind preferences guard prose.** A judge compares shuffled pairs for clarity, fluency, and directness separately, and the bench records the reasons for each pair.

The bench accepts an [artifact][ARTIFACT] when its claimed behavior improves, its assertions hold, and the blind preference stays acceptable. The judging is cross-vendor. One judge covers the [models][MODEL] from other vendors. A judge from a second vendor covers the first judge's own [model][MODEL]. The report withholds a [verdict][VERDICT] when fewer than half of the planned pairs are valid.

### Consequences

- [+] Iteration-4 could state a split [verdict][VERDICT]. The STE *[skill][SKILL]* passes on Claude Opus and Sonnet, does nothing for GPT-5.6 Sol, and degrades grok-4.6 and Lumo Max
- [+] The report includes the pair review, because numbers alone cannot show a [model][MODEL] that answers with a plan instead of a deliverable
- [-] The judging costs one provider call per pair. The quick rung skips the judging and must say so
- [-] The bench does not yet accept custom judge dimensions per [artifact][ARTIFACT]. That is a planned manifest extension

## More Information

- [DECK-0002 Benchmark Execution Ladder](DECK-0002%20Benchmark%20Execution%20Ladder.md): where each metric runs
- `runes/core/skills/BenchArtifact/references/schemas.md`: the structure of the judgment record
- Rewritten on 2026-10-19 in the plain spoken register. The decision is unchanged.

[MODEL]: ../specs/glossary/model.md
[VERDICT]: ../specs/glossary/verdict.md
[ARTIFACT]: ../specs/glossary/artifact.md
[LINTER]: ../specs/glossary/linter.md
[SKILL]: ../specs/glossary/skill.md
