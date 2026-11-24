---
title: "Unified Module Validation"
description: "One check list in .pre-commit-config.yaml runs before a commit, before a push, and in CI, with one chosen checker for each concern."
type: adr
category: process
tags:
    - validation
    - ci
    - pre-commit
status: accepted
created: 2026-04-02
updated: 2026-10-19
author: "@N4M3Z"
project: deck
related:
    - "CORE-0022 Verified Remote Execution"
    - "CORE-0007 Fixture-Based Canary Testing"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5@claude", "gpt-5.6-sol@codex"]
informed: []
upstream:
    - "https://github.com/N4M3Z/forge-core/blob/main/docs/decisions/CORE-0010%20Unified%20Module%20Validation.md"
    - "one-domain-one-plugin#one-checker-per-concern"
    - "one-domain-one-plugin#one-validation-path"
change: one-domain-one-plugin
---

# Unified Module Validation

## Context and Problem Statement

The *[repository][REPOSITORY]* needs one list of checks that every path runs. A check that exists in one place and not in another gives a false pass. The paths are continuous integration (CI), the commit hook, and a session. When each path runs its own list of checks, a commit can be clean in one path and broken in the next.

## Decision Drivers

- The [repository][REPOSITORY] keeps one list of checks, with no copy in a Makefile, a workflow, or a hook script.
- A missing tool must not look like a passed check.
- The [repository][REPOSITORY] keeps one tool for each concern, so two tools never disagree about the same *[analysis rule][ANALYSISRULE]*.

## Considered Options

1. Each path keeps its own checks: a workflow file, a hook script, and a Makefile target.
2. One declarative list in `.pre-commit-config.yaml`, which prek runs in every path.

## Decision Outcome

Option 2. `.pre-commit-config.yaml` MUST be the only list of checks. The commit hook, the push hook, `make validate`, and the CI `quality` job MUST each run that list through prek.

A guarded hook skips when its tool is absent, so a fresh clone remains usable. CI MUST set `REQUIRE_GATES=1`, which turns an absent tool into a failure. A session that reports a stage as clean MUST have every tool present ([DECK-0013 Local Checks Before Publication](DECK-0013%20Local%20Checks%20Before%20Publication.md)).

The [repository][REPOSITORY] keeps one checker for each concern: rumdl for Markdown structure, Vale for prose style, typos for spelling, and lychee for links. It keeps gitleaks for secrets, actionlint and zizmor for workflows, mdschema for document frames, and shellcheck for shell. It keeps ruff for Python and rudof for the declared graph. A tool MUST be one binary that works offline on the commit path. A revision of the tool set MUST arrive through a *[decision record][DECISIONRECORD]*.

### Consequences

- [+] The check list is one file, so a new check is one edit that every path runs.
- [-] CI runs checks that a local run can skip. A local pass with skipped hooks is not a pass, and the hook output is the only place that shows the skip.
- [-] CI builds the rune command-line interface (CLI) from source for the `contract` job, so CI can run a check that the installed CLI lacks. A local pass does not prove that job.
- [-] The commit hook has one fallback: when prek is absent, it runs gitleaks alone and says so.

## More Information

- Rewritten on 2026-10-19 in the plain spoken register. The decision is unchanged.

[REPOSITORY]: ../specs/glossary/repository.md
[ANALYSISRULE]: ../specs/glossary/analysis-rule.md
[DECISIONRECORD]: ../specs/glossary/decision-record.md
