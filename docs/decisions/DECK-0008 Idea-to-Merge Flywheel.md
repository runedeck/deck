---
title: Idea-to-Merge Flywheel
description: One loop turns a raw idea into a merged change and extracted artifacts that enter the context of every later pass
type: adr
category: architecture
tags:
    - architecture
    - pipeline
    - extraction
status: accepted
created: 2026-08-19
updated: 2026-10-19
author: "@N4M3Z"
project: deck
related:
    - "DECK-0005 Artifact Lifecycle and Evidence Tokens"
    - "DECK-0006 State Stores and Provider Edges"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: []
informed: []
upstream: []
change: agentic-first-pipeline-rules
---

# Idea-to-Merge Flywheel

## Context and Problem Statement

The owner uses *[harnesses][HARNESS]* as the primary computer interface: in terminals, through remote control from a phone, on remote desktops, and on local infrastructure. An *[idea][IDEA]* arrives in any medium and enters the stack without a procedure. Some [ideas][IDEA] become specifications, some become direct edits, and many evaporate. Finished work leaves the same way: a *[change][CHANGE]* merges, and the lessons inside it stay unmined. The stack has every middle stage: specification, isolation, swarm delegation, local checks, each *[agentic review lane][AGENTICREVIEWLANE]*, and babysitting. No named loop connects a raw thought to a merged [change][CHANGE] and back into context.

## Decision Drivers

- The entry step and the exit step have no owner. Everything between them already runs.
- An [idea][IDEA] transcribed without challenge produces specification noise. The intake must challenge the [idea][IDEA] against the existing contracts before it creates the [change][CHANGE].
- A delivery that extracts nothing keeps the next prompt as expensive as the last one. Each pass must leave the next pass cheaper.
- The pipeline must work on every [harness][HARNESS]. The future pi host joins as one more edge and forces no rewrite.
- A *[rule][RULE]* extracted without measurement adds cost to every later context without a measured benefit.

## Considered Options

1. **A linear pipeline**: from prompt to merge, with extraction left as a habit.
2. **A monolithic orchestrator**: one tool owns intake through merge.
3. **A named loop over existing implementations**: a contract for intake, a contract for extraction, the existing tools for every middle stage, and enforcement added later.

## Decision Outcome

Option 3. The loop is: prompt, pushback, specify, isolate, swarm, local checks, human skim, continuous integration and each [agentic review lane][AGENTICREVIEWLANE], babysit, approve, extract, recycle. The intake challenges every [idea][IDEA] against the specifications, the *[decision records][DECISIONRECORD]*, and the advisory memory before it creates the [change][CHANGE]. It sizes the [change][CHANGE] by how much the [change][CHANGE] can break.

Every pass closes with the extraction question. An extracted *[artifact][ARTIFACT]* rejoins the standard *[lifecycle][LIFECYCLE]*. A [rule][RULE] pays for its context cost with a bench *[verdict][VERDICT]*. A released extraction enters a later pass through the normal install path.

Four placement decisions complete the loop. Memory stays advisory and never authoritative. Obsidian leaves the flow, and the vault stays an archive. pi joins as a provider edge, and the eventual pi integration is a thin extension that wraps the rune binary. A copy-on-write workspace is an acceptable isolation method, because it copies a whole tree and never touches a git ref. Bookmark and push discipline stay with jj.

### Consequences

- [+] The IntakeIdea *[skill][SKILL]* fills the entry step now. The extraction check is a named follow-up task.
- [+] The loop gives the *[repository][REPOSITORY]* a growth mechanism: the development of the stack mines the [artifacts][ARTIFACT] that improve the stack.
- [+] The pi decision keeps rune independent of any [harness][HARNESS] and leaves a concrete integration path.
- [-] The loop adds one more standing question to every pass. The question costs a sentence and yields a [rule][RULE].

## More Information

Amendment on pull request delivery. The middle stages need observable evidence of completion beyond named tools and procedures.
The [pull-request delivery contract](../changes/merge-ready-needs-evidence/specs/merge-ready-needs-evidence/spec.md) defines that evidence for the existing babysitting stage.
This amendment keeps VersionControl as the procedure owner and preserves the existing publication-authorization contract.
It adds no pipeline stage, no orchestration service, and no acceptance step that a council decides.

The [design](../changes/merge-ready-needs-evidence/design.md) assigns source contradictions to [skill][SKILL] repairs and mechanical defects to their existing tooling owners.
This separation stops a repeated review failure from producing a duplicate rulebook or an unrelated edit in a pull request.

- Rewritten on 2026-10-19 in the plain spoken register. The decision is unchanged.

[IDEA]: ../specs/glossary/idea.md
[CHANGE]: ../specs/glossary/change.md
[HARNESS]: ../specs/glossary/harness.md
[RULE]: ../specs/glossary/rule.md
[DECISIONRECORD]: ../specs/glossary/decision-record.md
[ARTIFACT]: ../specs/glossary/artifact.md
[VERDICT]: ../specs/glossary/verdict.md
[SKILL]: ../specs/glossary/skill.md
[REPOSITORY]: ../specs/glossary/repository.md
[AGENTICREVIEWLANE]: ../specs/glossary/agentic-review-lane.md
[LIFECYCLE]: ../specs/glossary/lifecycle.md
