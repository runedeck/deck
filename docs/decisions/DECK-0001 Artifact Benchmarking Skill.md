---
title: "Artifact Benchmarking Skill"
description: "Extract the evaluation loop from BuildSkill into a standalone BenchArtifact skill that measures any rune against baselines, per model"
type: adr
category: "architecture"
tags: ["benchmarking", "evaluation", "skills"]
status: proposed
created: 2026-08-13
updated: 2026-08-13
author: "Martin Zeman"
project: "deck"
related: []
responsible: []
accountable: []
consulted: []
informed: []
upstream: []
---

# Artifact Benchmarking Skill

## Context and Problem Statement

The evaluation loop lives inside BuildSkill: test cases, with-artifact and baseline runs, grading, aggregation, and a review viewer. It measures skills only, and it reports one aggregate per configuration with no model dimension. The deck now adopts rules and agents through the same reviewed pipeline as skills, and every adoption raises the same question the loop answers for skills: does this artifact change model behavior enough to earn its context cost? A rule adoption today lands with no measurement at all.

## Decision Drivers

- Every artifact kind needs the same evidence: behavior with the artifact against behavior without it.
- Rules are always in context, so their cost is paid on every turn; the case for measuring them is stronger than for skills.
- Model behavior differs: a rule a frontier model does not need may still earn its place for smaller models. One aggregate across models hides exactly this.
- The comparison must be reviewable by a human in one artifact, not assembled from JSON by hand.
- The rune CLI will eventually own benchmarking, but coupling that migration to this extraction would stall both.

## Considered Options

- Keep the loop inside BuildSkill and teach it about rules and agents.
- Extract the loop into a standalone BenchArtifact skill that BuildSkill defers to.
- Implement benchmarking in the rune CLI now and skip the skill stage.

## Decision Outcome

Extract the loop into a standalone BenchArtifact skill in core. BuildSkill keeps a short pointer where its evaluation companion stood; the scripts, agent templates, and viewer move with the loop. BenchArtifact benchmarks any rune: a skill runs with and without the skill loaded, a rule runs with and without the rule text in context, an agent runs against a general-purpose baseline. Runs carry a model dimension, aggregation reports per configuration and model with no cross-model averaging, and the report is one self-contained HTML in the pattern of proton-ai-security's review reports: structured data inlined into a template, vendored stylesheet, client-side rendering, no external requests.

Keeping the loop inside BuildSkill would grow a skill-authoring guide into a benchmarking product and leave rules and agents reaching into another skill's internals. Starting in the rune CLI would gate a working measurement loop behind a Rust port; the skill form keeps the loop editable while its shape settles, and the CLI import follows once it has.

## Consequences

- Rule and agent adoptions can demand measurement before they land; the ReviewMarkers rule is the first candidate.
- BuildSkill shrinks and gains a dependency on a sibling skill for its evaluation step.
- The per-model matrix multiplies run counts; benchmarks stay affordable only while test sets stay small.
- The viewer and aggregator fork from BuildSkill's copies at extraction; divergence between the two is resolved by the CLI import, which retires the skill-side scripts.
