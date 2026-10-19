---
title: Artifact Lifecycle and Evidence Tokens
description: Seven flow stages move every artifact from capture to operation, and each stage issues one evidence token the next stage requires
type: adr
category: architecture
tags:
    - architecture
    - lifecycle
    - evidence
status: accepted
created: 2026-08-19
updated: 2026-10-19
author: "@N4M3Z"
project: deck
related:
    - "DECK-0001 Artifact Benchmarking Skill"
    - "DECK-0004 Temporary Adoption State"
    - "DECK-0003 Three-Metric Verdict and Cross-Vendor Judging"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: []
informed: []
upstream: []
change: lifecycle-stages-and-evidence
---

# Artifact Lifecycle and Evidence Tokens

## Context and Problem Statement

The stack needs one named sequence of stages, so that each hand-off between tools has an owner and each promotion has a condition. The stack grew one tool at a time: build *[skills][SKILL]*, an adoption state machine, the bench, *[agentic review lanes][AGENTICREVIEWLANE]*, an installer, and *[harness][HARNESS]* *[routines][ROUTINE]*. Each tool works, but no document states the pipeline they form, so the hand-offs between the tools belong to nobody. The drift report in issue #45 is the symptom. A step that a person carries by hand from one tool to the next fails, and no check notices.

## Decision Drivers

- Every *[artifact][ARTIFACT]* kind ([skill][SKILL], *[rule][RULE]*, *[agent][AGENT]*, *[hook][HOOK]*, [routine][ROUTINE]) moves through the same states. Only the tools differ.
- A promotion without evidence is an assertion. The ceremony already rejects an assertion everywhere else.
- A [rule][RULE] is in context on every turn, so its promotion condition must be the highest and the most explicit.
- The feedback loop from operation back to capture exists informally, and it loses a lesson when a session ends.

## Considered Options

1. Tool-centric documentation. The owner describes each tool well and leaves the pipeline implicit.
2. One monolithic pipeline tool. The owner builds one program that runs every step.
3. Named stages with evidence tokens. The owner keeps the tools, names each stage, and defines one token for each stage as its promotion condition.

## Decision Outcome

Option 3. The stages are Capture, Author, Prove, Measure, Review, Ship, Operate. Each stage issues one evidence token:

- Capture: a dated capture note.
- Author: a schema-validation pass.
- Prove: a provenance identity.
- Measure: a bench *[verdict][VERDICT]* for each *[model][MODEL]*.
- Review: an exact-head clean review.
- Ship: a deploy-manifest digest.
- Operate: [routine][ROUTINE] coverage.

A stage MUST NOT consume an [artifact][ARTIFACT] without the token of the previous stage. Evidence is append-only, and it survives retirement. Operate feeds Capture: a drift report, an audit finding, or a bench regression becomes a captured note.

The workshop's order of repairs, from architecture down to human review, selects the stage that takes a repeated problem. An architecture repair goes into Author. A lint goes into Review. A [rule][RULE] goes into Author, and Measure makes the [rule][RULE] prove its value. Human review is the floor.

### Consequences

- [+] An existing tool fills a stage, and the stage, never the tool, is the definition. The owner replaces a tool without moving a contract.
- [+] The gap register in the lifecycle-stages-and-evidence *[change][CHANGE]* lists every hand-off that is manual today. Each one is now a named defect instead of background noise.
- [+] A future check that blocks a promotion (a [rule][RULE] without a [verdict][VERDICT], an adoption without a sealed record) has a specification to cite.
- [+] The evidence tokens give retirement a clean principle: the owner removes the [artifact][ARTIFACT] and keeps the tokens.

## More Information

- Rewritten on 2026-10-19 in the plain spoken register. The decision is unchanged.

[ROUTINE]: ../specs/glossary/routine.md
[ARTIFACT]: ../specs/glossary/artifact.md
[SKILL]: ../specs/glossary/skill.md
[RULE]: ../specs/glossary/rule.md
[AGENT]: ../specs/glossary/agent.md
[HOOK]: ../specs/glossary/hook.md
[VERDICT]: ../specs/glossary/verdict.md
[AGENTICREVIEWLANE]: ../specs/glossary/agentic-review-lane.md
[HARNESS]: ../specs/glossary/harness.md
[MODEL]: ../specs/glossary/model.md
[CHANGE]: ../specs/glossary/change.md
