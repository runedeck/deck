---
title: "Artifact Benchmarking Skill"
description: "Extract the evaluation loop from BuildSkill into a standalone BenchArtifact skill that measures any rune against baselines, per model"
type: adr
category: "architecture"
tags: ["benchmarking", "evaluation", "skills"]
status: accepted
created: 2026-08-13
updated: 2026-10-19
author: "Martin Zeman"
project: "deck"
related: []
responsible: []
accountable: []
consulted: []
informed: []
upstream: []
change: benchmark-instructions-per-model
---

# Artifact Benchmarking Skill

## Context and Problem Statement

The evaluation loop is inside the BuildSkill *[skill][SKILL]*: test cases, with-artifact and baseline runs, grading, aggregation, and a review viewer. It measures [skills][SKILL] only. It reports one aggregate per configuration, with no *[model][MODEL]* dimension. The owner now adopts *[rules][RULE]* and *[agents][AGENT]* into the *[deck][DECK]* through the same reviewed pipeline as [skills][SKILL]. Every adoption asks the question the loop answers for [skills][SKILL]: does this *[artifact][ARTIFACT]* alter [model][MODEL] behavior enough to justify its context cost? Today the owner adopts a [rule][RULE] with no measurement at all.

## Decision Drivers

- Every [artifact][ARTIFACT] kind needs the same evidence: behavior with the [artifact][ARTIFACT] against behavior without it.
- A [rule][RULE] is always in context, so the session pays its cost on every turn. The case for measuring a [rule][RULE] is stronger than for a [skill][SKILL].
- [Model][MODEL] behavior differs: a [rule][RULE] a frontier [model][MODEL] does not need may still help a smaller [model][MODEL]. One aggregate across [models][MODEL] hides exactly this.
- A person must be able to review the comparison in one [artifact][ARTIFACT]. A comparison built from JSON by hand does not count.
- The `rune` command-line interface (CLI) will own benchmarking one day, but tying that migration to this extraction would stall both.

## Considered Options

- Keep the loop inside BuildSkill and extend it to [rules][RULE] and [agents][AGENT].
- Extract the loop into a standalone BenchArtifact [skill][SKILL] that BuildSkill defers to.
- Build benchmarking in the `rune` CLI now and skip the [skill][SKILL] stage.

## Decision Outcome

The owner extracts the loop into a standalone BenchArtifact [skill][SKILL] in core. BuildSkill keeps a short pointer where its evaluation *[companion][COMPANION]* stood. The scripts, [agent][AGENT] *[templates][TEMPLATE]*, and viewer move with the loop.

BenchArtifact benchmarks any *[rune][RUNE]*. A [skill][SKILL] runs with and without the [skill][SKILL] loaded. A [rule][RULE] runs with and without the [rule][RULE] text in context. An [agent][AGENT] runs against a general-purpose baseline. Each run records a [model][MODEL] dimension. Aggregation reports per configuration and [model][MODEL], with no cross-model averaging.

The report is one self-contained HTML (HyperText Markup Language) file in the pattern of proton-ai-security's review reports. That pattern inlines structured data into a [template][TEMPLATE], vendors the stylesheet, renders on the client, and makes no external request.

Keeping the loop inside BuildSkill would grow a skill-authoring guide into a benchmarking product. [Rules][RULE] and [agents][AGENT] would then reach into another [skill][SKILL]'s internals. Starting in the `rune` CLI would block a working measurement loop behind a Rust port. The [skill][SKILL] form keeps the loop editable while its structure settles. The CLI import comes after that.

### Consequences

- [+] Adopting a [rule][RULE] or an [agent][AGENT] can demand a measurement before the merge. The ReviewMarkers [rule][RULE] is the first candidate.
- [-] BuildSkill shrinks and gains a dependency on a sibling [skill][SKILL] for its evaluation step.
- [-] The per-model matrix multiplies the run count. A benchmark is affordable only while the test set is small.
- [-] The viewer and the aggregator fork from BuildSkill's copies at extraction. The CLI import resolves the divergence and retires the skill-side scripts.

## More Information

- Rewritten on 2026-10-19 in the plain spoken register. The decision is unchanged.

[SKILL]: ../specs/glossary/skill.md
[MODEL]: ../specs/glossary/model.md
[RULE]: ../specs/glossary/rule.md
[AGENT]: ../specs/glossary/agent.md
[DECK]: ../specs/glossary/deck.md
[ARTIFACT]: ../specs/glossary/artifact.md
[COMPANION]: ../specs/glossary/companion.md
[RUNE]: ../specs/glossary/rune.md
[TEMPLATE]: ../specs/glossary/template.md
