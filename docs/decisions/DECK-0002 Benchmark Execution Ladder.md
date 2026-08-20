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
updated: 2026-08-19
author: "@N4M3Z"
project: deck
related: ["DECK-0001 Artifact Benchmarking Skill"]
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: []
informed: []
upstream: []
---

# Benchmark Execution Ladder

## Context and Problem Statement

The Simplified Technical English benchmark exposed a spread of execution costs. A full cross-harness matrix with six models, clean harness state, and blind judging takes hours and demands provider credentials, sandbox carve-outs, and a local proxy. An author who wants a first signal on a new rule needs an answer in minutes, inside the harness that is already running. One fixed procedure cannot serve both, and an unordered menu of procedures invites incomparable results.

## Decision Drivers

- The method must stay constant while the execution mechanics vary, or results stop being comparable across setups
- The calibration targets are Claude and Codex; other harnesses are secondary evidence
- Weaker harnesses confuse easily and need tailored treatment; that work must not block the primary loop
- The eventual home for heavyweight evaluation is runedeck/bench, which does not exist yet

## Considered Options

1. **Always maximal** — every benchmark runs the full cross-harness matrix, hours per iteration
2. **Always native** — every benchmark runs inside the current harness, single-vendor evidence only
3. **Execution ladder** — ordered setups that share one manifest, one grading path, and one verdict rule

## Decision Outcome

Chosen option: **Execution ladder**. Each rung buys more isolation and more models for more time, and every rung reads the same manifest, the same assertions, the same checker, and the same verdict rule.

1. **Minimal.** The current harness runs the cases through its own agent tool. No subprocesses, no route registry. This is the NativeBench procedure and the default.
2. **Value for time.** Claude and Codex run through `claude -p` and `codex exec`, through `rune run` when it is available. A scratch run on two cases with grading only returns a first table in about five minutes.
3. **Maximal.** The explicit cross-harness matrix: every configured harness, clean state, context canaries, raw output retention, and blind cross-vendor judging. This produced the iteration-4 verdict.
4. **runedeck/bench.** The best evaluations will run from runedeck/bench once it exists. The configuration files are the migration unit; the interim wrapper retires.

### Consequences

- [+] A new rule gets a five-minute first table without any infrastructure
- [+] The cross-harness rung stays behind an explicit flag, so nobody pays its cost by accident
- [+] The ladder gives runedeck/bench a defined intake: configurations, not scripts
- [-] A quick scratch table is low confidence and must label itself as such
- [-] Harness-specific treatment prompts for weaker models remain future work on the maximal rung

## More Information

- [DECK-0001 Artifact Benchmarking Skill](DECK-0001%20Artifact%20Benchmarking%20Skill.md) — the extraction this ladder executes
- `runes/core/skills/BenchArtifact/NativeBench.md` — the minimal rung
- `runes/core/skills/BenchArtifact/RuneBench.md` — the maximal rung
