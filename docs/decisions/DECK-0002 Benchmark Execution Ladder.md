---
title: Benchmark Execution Ladder
description: Ordered benchmark setups from in-harness agents to runedeck/bench, sharing one manifest, grading path, and verdict rule
type: adr
category: architecture
tags:
    - benchmarking
    - execution
    - harness
status: accepted
created: 2026-08-19
updated: 2026-10-19
author: "@N4M3Z"
project: deck
related: ["DECK-0001 Artifact Benchmarking Skill"]
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: []
informed: []
upstream: []
change: benchmark-instructions-per-model
---

# Benchmark Execution Ladder

## Context and Problem Statement

One fixed procedure cannot serve both a quick first signal and a full cross-harness matrix, and an unordered menu of procedures invites incomparable results. The Simplified Technical English benchmark exposed a spread of execution costs. A full cross-harness matrix with six *[models][MODEL]*, clean *[harness][HARNESS]* state, and blind judging takes hours. It demands provider credentials, sandbox carve-outs, and a local proxy. An author who wants a first signal on a new *[rule][RULE]* needs an answer in minutes, inside the [harness][HARNESS] that is already running.

## Decision Drivers

- The method must remain constant while the execution mechanics vary, or results stop being comparable across setups.
- The benchmark calibrates against Claude and Codex. Other [harnesses][HARNESS] are secondary evidence.
- Weaker [harnesses][HARNESS] confuse easily and need tailored treatment. That work must not block the primary loop.
- The eventual home for heavyweight evaluation is runedeck/bench, which does not exist yet.

## Considered Options

1. **Always maximal**: every benchmark runs the full cross-harness matrix, hours per iteration.
2. **Always native**: every benchmark runs inside the current [harness][HARNESS], single-vendor evidence only.
3. **Execution ladder**: ordered setups that share one manifest, one grading path, and one [verdict rule](../BenchArtifact%20Anatomy.md).

## Decision Outcome

Chosen option: **Execution ladder**. Each rung gives more isolation and more [models][MODEL] in exchange for more time. Every rung reads the same manifest, the same assertions, the same checker, and the same [verdict rule](../BenchArtifact%20Anatomy.md).

1. **Minimal.** The current [harness][HARNESS] runs the cases through its own subagent tool, with no subprocess and no route registry. This rung is the NativeBench procedure and the default.
2. **Value for time.** Claude and Codex run through `claude -p` and `codex exec`, through `rune run` when it is available. A scratch run on two cases with grading only returns a first table in about five minutes.
3. **Maximal.** The explicit cross-harness matrix runs every configured [harness][HARNESS] with clean state, context canaries, raw output retention, and blind cross-vendor judging. This rung produced the iteration-4 *[verdict][VERDICT]*.
4. **runedeck/bench.** The best evaluations will run from runedeck/bench once it exists. The configuration files are the migration unit. The interim wrapper retires.

### Consequences

- [+] A new [rule][RULE] gets a five-minute first table without any infrastructure.
- [+] An explicit flag guards the cross-harness rung, so nobody incurs its cost by accident.
- [+] The ladder gives runedeck/bench a defined intake of configurations rather than scripts.
- [-] A quick scratch table is low confidence and must label itself as such.
- [-] Harness-specific treatment prompts for weaker [models][MODEL] remain future work on the maximal rung.

## More Information

- [DECK-0001 Artifact Benchmarking Skill](DECK-0001%20Artifact%20Benchmarking%20Skill.md): the extraction this ladder executes
- `runes/core/skills/BenchArtifact/NativeBench.md`: the minimal rung
- `runes/core/skills/BenchArtifact/RuneBench.md`: the maximal rung
- Rewritten on 2026-10-19 in the plain spoken register. The decision is unchanged.

[MODEL]: ../specs/glossary/model.md
[HARNESS]: ../specs/glossary/harness.md
[RULE]: ../specs/glossary/rule.md
[VERDICT]: ../specs/glossary/verdict.md
