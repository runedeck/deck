---
title: Idea-to-Merge Flywheel
description: One loop turns a raw idea into a merged change and extracted artifacts that enter the context of every later pass
type: adr
category: architecture
tags:
    - architecture
    - pipeline
    - extraction
status: proposed
created: 2026-08-19
updated: 2026-08-19
author: "@N4M3Z"
project: deck
related:
    - "DECK-0004 Routine Environment Matrix"
    - "DECK-0005 Artifact Lifecycle and Evidence Tokens"
    - "DECK-0006 State Stores and Provider Edges"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: []
informed: []
upstream: []
---

# Idea-to-Merge Flywheel

## Context and Problem Statement

Agents are the owner's primary computer interface, across terminals, phone remote control, remote desktops, and local infrastructure. Ideas arrive in any medium and enter the stack ad hoc: some become specifications, some become direct edits, and many evaporate. Finished work leaves the same way: a change merges and the lessons inside it stay unmined. The stack has every middle stage (specification, isolation, swarm delegation, local gates, review lanes, babysitting). No named loop connects a raw thought to a merged change and back into context.

## Decision Drivers

- The entry seam and the exit seam are the two unowned seams. Everything between them already runs.
- An idea transcribed without challenge produces specification noise. Pushback against existing contracts must precede scaffolding.
- Deliveries that extract nothing keep the next prompt as expensive as the last one. The loop must compound.
- The pipeline must stay cross-harness: the future pi host is an edge, not a rewrite target.
- Rules extracted without measurement fill every later context with unpaid cost.

## Considered Options

1. **A linear pipeline** — prompt to merge, extraction stays a habit.
2. **A monolithic orchestrator** — one tool owns intake through merge.
3. **A named loop over existing instances** — contracts for intake and extraction, existing tools for every middle stage, enforcement added later.

## Decision Outcome

Option 3. The loop is: prompt, pushback, specify, isolate, swarm, local gates, human skim, CI and review lanes, babysit, approve, extract, recycle. Intake challenges every idea against specifications, decision records, and advisory memory before scaffolding, and sizes the change by blast radius. Every pass closes with the extraction question. Extracted artifacts rejoin the standard lifecycle, rules pay rent through a bench verdict, and shipped extractions reach later passes through the normal install path. Four placement decisions complete the loop. Memory stays advisory and never authoritative. Obsidian leaves the flow and the vault stays an archive. pi joins as a provider edge, and the eventual pi integration is a thin extension that wraps the rune binary. Copy-on-write workspaces are an acceptable isolation instance because they copy whole trees and never touch git refs, while bookmark and push discipline stay with jj.

## Consequences

- The IntakeIdea skill instantiates the entry seam now. The extraction gate is a named follow-up, not folklore.
- The flywheel gives the deck a growth mechanism: the stack's own development mines the artifacts that improve the stack.
- The pi decision keeps rune harness-independent while leaving a concrete integration path.
- The loop adds one more standing question to every pass, which costs a sentence and pays a rule.
