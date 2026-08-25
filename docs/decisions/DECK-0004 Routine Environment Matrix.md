---
title: Routine Environment Matrix
description: "Assign a routine environment by the sensitivity of the data the session reads, never mount a private repository beside general egress, and treat the prompt register as the control layer"
type: adr
category: architecture
tags:
    - routines
    - scanners
    - security
status: accepted
created: 2026-08-25
updated: 2026-08-25
author: "@N4M3Z"
project: deck
related: []
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: []
informed: []
upstream: []
---

# Routine Environment Matrix

## Context and Problem Statement

Provider routines run the deck scanner and awareness prompts in cloud sessions. Each session combines three grants: repository mounts, network egress, and connectors. The first installs produced every failure class in one evening: an audit with no repository mounts, a web scanner behind an allowlist proxy, and a repository scanner whose trust preconditions the provider cannot satisfy. The open question was how to assign environments so that a prompt-injection compromise stays bounded.

## Decision Drivers

- The routine prompts read untrusted data by design: repository content, pull request text, issue comments, and public web pages.
- A compromised session is bounded by its grants, not by its instructions.
- Exfiltration needs two legs in one session: readable private data and general egress.
- The GitHub proxy works at every network level, so repository work needs no general egress.
- Fewer environments are easier to reason about than one environment per routine.

## Considered Options

- One dedicated environment per routine, least privilege everywhere.
- One environment for everything with full network.
- Three environments assigned by the sensitivity of the readable data.

## Decision Outcome

Three environments, selected by what the session reads:

| Environment | Network | Mounts | Routines |
|---|---|---|---|
| AirGap | none | private content | repository exposure scanner |
| Default | GitHub proxy only | repository chips, private chips permitted | ceremony audit, repository digest |
| WebScan | full | none | GitHub exposure, online mentions |

Two rules complete the matrix. A private repository never mounts in a session with general egress: that combination recreates both exfiltration legs. The prompt register (authority section, permitted and prohibited operations, counts, loud canary) stays the control layer inside every environment; the matrix bounds the damage when that layer fails.

## Consequences

- The public-data scanners run with full web access at near-zero stakes: everything they read is already public.
- Repository work runs with no egress at all, so a compromised audit can at most write GitHub comments under its own identity.
- The full-trust repository scanner stays blocked on providers without per-run trusted preparation; its canary reports CONFIGURATION_FAILURE instead of degrading silently, and a separately documented degraded variant trusts the platform clone.
- Convenience grants (extra chips, connectors) are owner decisions recorded in the routine, not defaults.
