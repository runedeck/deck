---
title: Portable discovery with a shared guard procedure
description: Separate process evidence from untrusted guard output and keep one shared policy companion.
type: adr
category: architecture
tags:
    - skills
    - safety
    - portability
status: proposed
created: 2026-09-10
updated: 2026-09-11
author: "@N4M3Z"
project: deck
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: []
informed: []
upstream: []
---

# Portable discovery with a shared guard procedure

## Context and Problem Statement

SafetyFirst needs observed guard state on providers that do not execute Claude injection.
Rune already supports provider entrypoints and complete body replacement.
It does not merge provider-specific companions.

## Considered Options

1. Keep Claude injection in canonical content.
   Other providers would receive no discovery evidence.
2. Append portable instructions to the existing procedure.
   Both procedures would remain, with an unclear relationship.
3. Copy the full guard policy into each provider entrypoint.
   Each copy would need separate maintenance.
4. Deploy provider-specific companions.
   This option would depend on unsupported assembly behavior.
5. Use a portable entrypoint, a complete Claude replacement, and shared policy and probe companions.
   The probe helper separates process evidence from child output.

Shell pipelines with final text markers cannot establish process success.
The child can print those markers before a failed exit.
Output truncation can then hide the actual failure marker.

## Decision Outcome

Use the portable base entrypoint for explicit bounded discovery.
Keep automatic invocation in a short Claude entrypoint with explicit `mode: replace`.
Both entrypoints reference one unchanged `Workflow.md` companion.
Both invoke one shared Python helper for bounded guard discovery.
The helper separates actual process status from escaped, untrusted child output in one JSON record.
Printed success markers cannot establish a successful version probe.

Write relative links for the assembled skill root.
The Claude source file therefore uses `Workflow.md`, not `../Workflow.md`.
Assembly relocates that entrypoint beside the shared companion.

Add a source-only `claude/Workflow.md` symlink to `../Workflow.md`.
This alias resolves the same links during source lint without copying the policy.
The existing collector excludes provider qualifier directories from companion collection.
Assembly therefore emits the canonical regular file beside the selected entrypoint.
Keep all source link checks enabled.
The tests must check the source alias and resolve each assembled link to the unchanged regular companion.

## Consequences

- The entrypoints remain small and the guard policy retains one source.
- Both entrypoints need Python 3 and a POSIX process boundary, with missing dependencies reported as unknown.
- Claude also requires `timeout` to bound lookup and runtime startup without an unbounded fallback.
- The source alias supplies no provider-specific content and does not enter the assembled bundle.
- The change adds no Codex variant, new provider, or deployment mechanism.
- Native Claude permission matching and native Codex discovery remain separate acceptance checks.
