---
title: The Inference Turn
description: Records what loads into a session at start, per turn, and after compaction, so authoring decisions target the layer that actually pays
type: adr
category: architecture
tags:
    - architecture
    - context
    - pipeline
status: accepted
created: 2026-08-27
updated: 2026-10-19
author: "@N4M3Z"
project: deck
related:
    - "CORE-0013 Context Economy"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: []
informed: []
upstream: []
change: economy-measure-context-efficiency
---

# The Inference Turn

## Context and Problem Statement

The *[repository][REPOSITORY]* needs one record of the inference pipeline, so every *[artifact][ARTIFACT]* discussion can state the layer it alters and the price it pays. Authoring decisions argue about token cost without a shared account of when each [artifact][ARTIFACT] reaches the *[model][MODEL]*.

## Considered Options

1. Leave the pipeline as folk knowledge in session transcripts.
2. Record the pipeline as a decision with the layer map.

## Decision Outcome

Chosen option: record the pipeline.

Session start loads the resident set once. The resident set contains the *[harness][HARNESS]* system prompt, the settings cascade as behavior, and the memory chain. The memory chain is user memory, user *[rules][RULE]*, the [repository][REPOSITORY] brief, and deployed [rules][RULE]. The resident set also contains the auto-memory index and the *[skill][SKILL]* listing as *[names][NAME]* with *[descriptions][DESCRIPTION]*. Deferred tools cost nothing until a search loads them.

Each turn can invoke the event layer: prompt-submit *[hooks][HOOK]*, pre-tool checks, sandbox enforcement, post-tool feedback, and stop [hooks][HOOK]. Prompt-submit [hooks][HOOK] and post-tool feedback can add payloads that the [model][MODEL] sees. The other entries perform runtime work and add tokens only when they emit a diagnostic that the [model][MODEL] sees.

Compaction rebuilds the context from a summary. Critical constraints need re-injection at that boundary, and a PostCompact [hook][HOOK] is the mechanism.

The layer map from [CORE-0013 Context Economy](CORE-0013%20Context%20Economy.md) assigns each fact its home. The resident set adds tokens to every inference turn. The event layer always incurs its runtime cost, and it adds input tokens only for payloads that the [model][MODEL] sees. The on-demand layer adds cost only when the session loads it.

### Consequences

- [+] Every authoring debate can state the layer and its price.
- [+] The compaction boundary is a recorded gap with a named mechanism.
- [-] The record needs an update when the [harness][HARNESS] alters its loading behavior.

## More Information

- Rewritten on 2026-10-19 in the plain spoken register. The decision is unchanged.

[ARTIFACT]: ../specs/glossary/artifact.md
[MODEL]: ../specs/glossary/model.md
[HARNESS]: ../specs/glossary/harness.md
[RULE]: ../specs/glossary/rule.md
[REPOSITORY]: ../specs/glossary/repository.md
[SKILL]: ../specs/glossary/skill.md
[HOOK]: ../specs/glossary/hook.md
[NAME]: ../specs/glossary/name.md
[DESCRIPTION]: ../specs/glossary/description.md
