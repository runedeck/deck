---
title: Artifact Lifecycle and Evidence Tokens
description: Seven flow stages move every artifact from capture to operation, and each stage issues one evidence token the next stage requires
type: adr
category: architecture
tags:
    - architecture
    - lifecycle
    - evidence
status: proposed
created: 2026-08-19
updated: 2026-08-19
author: "@N4M3Z"
project: deck
related:
    - "DECK-0001 Artifact Benchmarking Skill"
    - "DECK-0002 Temporary Adoption State"
    - "DECK-0003 Three-Metric Verdict and Cross-Vendor Judging"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: []
informed: []
upstream: []
---

# Artifact Lifecycle and Evidence Tokens

## Context and Problem Statement

The stack grew one tool at a time: build skills, an adoption state machine, a bench harness, review lanes, an installer, and provider routines. Each tool works, but nothing names the pipeline they form, so the seams between them belong to nobody. The drift report in issue #45 is the symptom: hand-carried steps between tools fail without any check noticing. The stack needs one named lifecycle so that every seam has an owner and every promotion has a condition.

## Decision Drivers

- Every artifact kind (skill, rule, agent, hook, routine) moves through the same states; only the tools differ.
- A promotion without evidence is an assertion; the ceremony already rejects assertions everywhere else.
- Rules sit in context on every turn, so their promotion bar must be the highest and the most explicit.
- The feedback loop from operation back to capture exists informally and loses lessons when sessions end.

## Considered Options

1. **Tool-centric documentation** — describe each tool well and leave the pipeline implicit.
2. **One monolithic pipeline tool** — build a single orchestrator that owns every step.
3. **Named stages with evidence tokens** — keep the tools, name the stages, and define one token per stage as the promotion condition.

## Decision Outcome

Option 3. The lifecycle is Capture, Author, Prove, Measure, Review, Ship, Operate. Each stage issues one evidence token: a dated capture note, a schema-validation pass, a provenance identity, a per-model bench verdict, an exact-head clean review, a deploy-manifest digest, and routine coverage. A stage MUST NOT consume an artifact without the previous token. Evidence is append-only and survives retirement. Operate feeds Capture: drift reports, audit findings, and bench regressions are captured notes. The workshop leverage ladder selects the stage that owns a repeated problem: architecture into Author, lints into Review, rules into Author with Measure paying their rent, human review as the floor.

## Consequences

- Existing tools become stage instances, not the definition; a tool can be replaced without moving the contract.
- The gap register in the stack-architecture change lists every hop that is manual today; each is now a named defect, not background noise.
- Future gates (a rule without a verdict, an adoption without a sealed record) have a specification to cite.
- The token model gives retirement a clean rule: remove the artifact, keep the tokens.
