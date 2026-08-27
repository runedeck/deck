---
title: The Inference Turn
description: Records what loads into a session at start, per turn, and after compaction, so authoring decisions target the layer that actually pays
type: adr
category: architecture
tags:
    - architecture
    - context
    - pipeline
status: proposed
created: 2026-08-27
updated: 2026-08-27
author: "@N4M3Z"
project: deck
related:
    - "CORE-0013 Context Economy"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: []
informed: []
---

# The Inference Turn

## Context and Problem Statement

Authoring decisions argue about token cost without a shared model of when each artifact reaches the model. The deck needs one record of the inference pipeline, so every artifact discussion can name the layer it changes and the price it pays.

## Considered Options

1. Leave the pipeline as folk knowledge in session transcripts.
2. Record the pipeline as a decision with the layer map.

## Decision Outcome

Chosen option: record the pipeline.

Session start loads the resident set once: the harness system prompt, the settings cascade as behavior, the memory chain (user memory, user rules, the repository brief, deployed rules), the auto-memory index, and the skill listing as names with descriptions. Deferred tools cost nothing until a search loads them.

Each turn adds the event layer: prompt-submit hooks, pre-tool gates (dispatcher parts, the destructive-command guard, the rewrite proxy), sandboxed execution, post-tool feedback, and stop hooks.

Compaction rebuilds the context from a summary. Critical constraints need re-injection at that boundary, and a PostCompact hook is the mechanism.

The layer map from CORE-0013 assigns each fact its home. The resident set is the expensive layer, the event layer is deterministic and near free, and the on-demand layer is paid only when used.

### Consequences

- [+] Every authoring debate can name the layer and its price.
- [+] The compaction boundary is a recorded gap with a named mechanism.
- [-] The record needs an update when the harness changes its loading model.
