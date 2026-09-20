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
updated: 2026-09-20
author: "@N4M3Z"
project: deck
related:
    - "CORE-0008 Verified Remote Execution"
    - "CORE-0018 Fixture-Based Canary Testing"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5", "gpt-5.6-sol"]
informed: []
upstream: []
change: core-foundation-principles
---

# Unified Module Validation

## Context and Problem Statement

A check that exists in one place and not in another gives a false pass. When CI, the commit hook, and a session each run their own list of checks, a change can be clean in one and broken in the next. The deck needs one list that every path runs.

## Decision Drivers

- One list of checks. No copy in a Makefile, a workflow, and a hook script.
- A missing tool must not look like a passed check.
- One tool for each concern, so two tools never disagree about the same rule.

## Considered Options

1. Each path keeps its own checks: a workflow file, a hook script, and a Makefile target.
2. One declarative list in `.pre-commit-config.yaml`, run by prek in every path.

## Decision Outcome

Option 2. `.pre-commit-config.yaml` MUST be the only list of checks. The commit hook, the push hook, `make validate`, and the CI `quality` job MUST each run that list through prek.

A guarded hook skips when its tool is absent, so a fresh clone stays usable. CI MUST set `REQUIRE_GATES=1`, which turns an absent tool into a failure. A session that reports a stage as clean MUST have every tool present ([DECK-0013](DECK-0013 Local Checks Before Publication.md)).

The deck keeps one checker for each concern: rumdl for Markdown structure, Vale for prose style, typos for spelling, lychee for links, gitleaks for secrets, actionlint and zizmor for workflows, mdschema for document frames, shellcheck for shell, ruff for Python, and rudof for the declared graph. A tool MUST be a single binary that works offline on the commit path. A tool change MUST arrive through a decision record.

## Consequences

- The check list is one file, so a new check is one edit and reaches every path.
- CI runs checks that a local run can skip. A local pass with skipped hooks is not a pass, and the hook output is the only place that shows the skip.
- CI builds the rune CLI from source for the `contract` job, so CI can run a check that the installed CLI lacks. A local pass does not prove that job.
- The commit hook has one fallback: when prek is absent it runs gitleaks alone and says so.
