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
updated: 2026-08-19
author: "@N4M3Z"
project: deck
related: ["DECK-0001 Artifact Benchmarking Skill", "DECK-0002 Benchmark Execution Ladder"]
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: []
informed: []
upstream: []
---

# Three-Metric Verdict and Cross-Vendor Judging

## Context and Problem Statement

A single score hides the failure modes that matter. A model can drive a style checker to zero by dropping facts, or keep every fact in prose no reader would accept. Early Simplified Technical English iterations showed both failures, and they also showed judge self-preference: a judge model preferred baselines written by itself. The benchmark needs a verdict rule that catches each failure separately and a judging scheme that removes the self-preference confound.

## Decision Drivers

- Meaning loss, mechanical compliance, and prose damage are independent failure modes
- Blind judgment is the only defense against outputs that satisfy the checker and repel readers
- A judge that grades its own vendor's output measures taste, not quality
- Each artifact claims a different measurable behavior, so the middle metric must be pluggable

## Considered Options

1. **One combined score** — a single number per run, simple to rank, hides every trade-off
2. **Checker density with validity filter** — assertions gate validity, density decides, prose damage invisible
3. **Three metrics, cross-vendor judging** — separate signals read together, judges assigned across vendors

## Decision Outcome

Chosen option: **Three metrics, cross-vendor judging**, read together within one model and never combined into one number.

- **Assertions guard meaning.** Frozen, objectively checkable statements about facts, figures, and restrictions. A drop is a regression regardless of the other metrics.
- **The checker measures the claimed behavior.** The artifact brings its checker: a domain linter for a large claim, or a generic pattern-density configuration for a small one. Density uses checker findings per 100 checker words from the same text.
- **Blind preferences guard prose.** A judge compares shuffled pairs for clarity, fluency, and directness separately, with reasons recorded per pair.

An artifact earns its place when its claimed behavior improves, assertions hold, and blind preference stays acceptable. Judging is cross-vendor: one judge covers the models from other vendors, and a second vendor's judge covers the first judge's own model. The report withholds a verdict when fewer than half of the planned pairs are valid.

### Consequences

- [+] Iteration-4 could state a split verdict: the STE skill earns its place on Claude Opus and Sonnet, does nothing for GPT-5.6 Sol, and degrades grok-4.6 and Lumo Max
- [+] Pair review is a first-class report feature, because numbers alone cannot show a model answering with a plan instead of a deliverable
- [-] Judging costs one provider call per pair; the quick rung skips it and must say so
- [-] Custom judge dimensions per artifact are a planned manifest extension, not yet built

## More Information

- [DECK-0002 Benchmark Execution Ladder](DECK-0002%20Benchmark%20Execution%20Ladder.md) — where each metric runs
- `runes/core/skills/BenchArtifact/references/schemas.md` — the judgment record shape
