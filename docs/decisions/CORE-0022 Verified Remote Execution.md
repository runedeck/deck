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
updated: 2026-10-19
author: "@N4M3Z"
project: deck
related:
    - "CORE-0021 Unified Module Validation"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: []
informed: []
upstream:
    - "https://github.com/N4M3Z/forge-core/blob/main/docs/decisions/CORE-0011%20Verified%20Remote%20Execution.md"
change: one-domain-one-plugin
---

# Verified Remote Execution

## Context and Problem Statement

Continuous integration (CI) and hooks fetch tools from the network. A plain `curl | bash` runs whatever the remote server sends, on every run. So a compromised upstream alters what executes, and nothing reports it. The fetch is not the problem. The problem is execution without verification.

## Decision Drivers

- A fetched tool is current, and nobody maintains a local copy.
- A committed digest is a trust anchor. The upstream can alter a file, and execution of that file then needs an explicit digest update.
- A supply chain attack targets the gap between a fetched file and a verified one. The [SLSA threats][SLSA-THREATS] page lists those attacks, where SLSA is Supply-chain Levels for Software Artifacts.

## Considered Options

1. Fetch the file and run it without verification.
2. Do not fetch at all. Commit every tool to the *[repository][REPOSITORY]* and update it by hand.
3. Fetch the file, compare its SHA-256 digest (Secure Hash Algorithm, 256 bits) with a committed digest, and run it only when they match.

## Decision Outcome

Option 3. A file that CI or a hook fetches from the network MUST match a SHA-256 digest committed to the [repository][REPOSITORY] before it runs. A mismatch MUST stop the run.

The installer in the [repository][REPOSITORY] is `scripts/install-tools`. The file `scripts/tool-versions` stores one digest for each tool, system, and machine. The installer downloads the archive and checks the digest. It installs only when the digest matches.

A digest update is an explicit act. The author reads the upstream revision, updates the committed digest, and commits. Each edit to executed code then passes through review.

### Consequences

- [+] The installer finds a compromised upstream at once, because the digest does not match.
- [-] Each tool upgrade needs a new digest for every system and machine the [repository][REPOSITORY] supports. The owner wants that friction.
- [-] A network failure stops the install. The [repository][REPOSITORY] does not keep a committed copy of the tools as a fallback.

## More Information

- [SLSA levels][SLSA-LEVELS]
- Rewritten on 2026-10-19 in the plain spoken register. The decision is unchanged.

[SLSA-THREATS]: https://slsa.dev/spec/v1.0/threats "SLSA v1.0, Threats and mitigations"
[SLSA-LEVELS]: https://slsa.dev/spec/v1.0/levels "SLSA v1.0, Security levels"
[REPOSITORY]: ../specs/glossary/repository.md
