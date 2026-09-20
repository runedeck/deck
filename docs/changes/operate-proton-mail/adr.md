---
title: "Operate Proton Mail on Proton's own model"
description: "Mailbox work runs in a session on a Lumo or local model through a local mail connector, and every other session hands mailbox requests off."
type: adr
category: architecture
tags:
    - runedeck
    - domain
    - proton
    - privacy
status: proposed
created: 2026-09-20
updated: 2026-09-20
author: "@N4M3Z"
project: deck
related: []
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5-1"]
informed: []
upstream: []
change: operate-proton-mail
---

# Operate Proton Mail on Proton's own model

## Context and Problem Statement

An agent that reads a mailbox puts mail content into its context, and a hosted model sends that context to its vendor. The mail owner accepts Proton Lumo and local models for mail, and no other.

## Considered Options

1. One mail skill for every harness.
2. A mail skill for the accepted models only, with no guidance elsewhere.
3. A mail skill for the accepted models, and a boundary skill for every other session.

## Decision Outcome

Option 3. The mail skill MUST run only where the model is a Lumo model or a local model. The boundary skill MUST hand mailbox requests off and MUST ask before it touches pasted mail. Every mutation MUST stay behind a permission prompt, and nothing is deleted permanently.

## Consequences

- The boundary skill is advisory. It warns and asks, and it blocks no tool call.
- A user who pastes mail into a hosted-model session can still continue after one warning.
- Neither skill has a bench verdict or a proof yet. Both are open tasks.
