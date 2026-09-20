---
title: "Verified Remote Execution"
description: "A file fetched from the network in CI or in a hook runs only after its SHA-256 matches a digest committed to the repository."
type: adr
category: security
tags:
    - security
    - ci
    - supply-chain
status: accepted
created: 2026-04-02
updated: 2026-09-20
author: "@N4M3Z"
project: deck
related:
    - "CORE-0007 Unified Module Validation"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: []
informed: []
upstream: []
change: core-foundation-principles
---

# Verified Remote Execution

## Context and Problem Statement

CI and hooks fetch tools from the network. A plain `curl | bash` trusts the remote server on every run, so a compromised upstream changes what executes and nothing reports it. The fetch is not the problem. Execution without verification is.

## Decision Drivers

- A fetched tool is current and costs no local maintenance.
- A committed digest is a trust anchor: the upstream can change, and execution then needs an explicit digest update.
- Supply chain attacks target the gap between fetched and verified ([SLSA threats][SLSA-THREATS]).

## Considered Options

1. Fetch and run with no verification.
2. No network fetch. Commit every tool and update by hand.
3. Fetch, compare the SHA-256 with a committed digest, and run only on a match.

## Decision Outcome

Option 3. A file that CI or a hook fetches from the network MUST be verified against a SHA-256 digest committed to the repository before it runs. A mismatch MUST stop the run.

`scripts/install-tools` is the instance in the deck. `scripts/tool-versions` holds one digest for each tool, system, and machine. The installer downloads the archive, checks the digest, and installs only on a match.

A digest update is an explicit act: read the upstream change, update the committed digest, and commit. Each change to executed code then passes through review.

## Consequences

- A compromised upstream is found at once, because the digest does not match.
- Each tool upgrade needs a digest for every system and machine the deck supports. That friction is intended.
- A network failure stops the install. The deck keeps no committed copy of the tools to fall back on.

## More Information

- [SLSA levels][SLSA-LEVELS]

[SLSA-THREATS]: https://slsa.dev/spec/v1.0/threats "SLSA v1.0, Threats and mitigations"
[SLSA-LEVELS]: https://slsa.dev/spec/v1.0/levels "SLSA v1.0, Security levels"
