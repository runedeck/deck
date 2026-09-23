---
title: File over App
description: The work lives in files the person owns, in open formats any tool reads, so it outlives every app that touches it
type: adr
category: architecture
tags:
    - architecture
    - plain-text
    - portability
status: proposed
created: 2026-09-28
updated: 2026-09-28
author: "@N4M3Z"
project: deck
related:
    - "CORE-0001 Markdown as System Language"
    - "CORE-0002 Metadata Inside Files"
    - "CORE-0006 Open Knowledge Format Bundle"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5-1@claude"]
informed: []
upstream:
    - "obsidian://open?vault=Atlas&file=Library%2FCanvas%2FPlain%20Text%20Wins"
    - "https://stephango.com/file-over-app"
    - "plain-text-is-futureproof#plain-text-representation"
    - "markdown-with-yaml-frontmatter#metadata-inside-files"
    - "instructions-stay-vendor-neutral#reusable-across-harnesses-and-models"
change: plain-text-first-principles
---

# File over App

## Context and Problem Statement

Every tool we use, an editor, a vault, a harness, a review bot, is short-lived next to the work it touches. Steph Ango's essay [File over app][FOA] (2023) states the test. A person's work goes into files they own, in open formats any tool reads, and the work outlasts the app.
Plain text, Markdown, metadata inside the file, and one source for every harness are four choices with one reason. This record states the reason, so a new tool has something to be measured against.

## Decision Drivers

- A harness, a vault, and a review bot each come and go, and the instructions and records stay
- A file that only one vendor's app can open is readable only as long as that vendor allows
- Every tool on the roster reads files, so files are the one interface they all share

## Considered Options

1. App over file: keep the work where the tool keeps it, in a memory store, a database, or a vendor format, and export when needed. Fast to start, and every export loses something.
2. File over app: the work is a file the person owns, in an open format, and every tool is a replaceable view over it.

## Decision Outcome

Option 2. Every artifact the deck governs MUST be a file the owner holds in the repository, in a format any tool reads without that tool's vendor. A tool MAY keep its own store, and that store MUST derive from the files and MUST be rebuildable from them. A tool that cannot work from the files does not join the roster.
This record is the reason behind the others: plain text ([CORE-0001](CORE-0001%20Markdown%20as%20System%20Language.md)), metadata inside the file ([CORE-0002](CORE-0002%20Metadata%20Inside%20Files.md)), the Open Knowledge Format bundle ([CORE-0006](CORE-0006%20Open%20Knowledge%20Format%20Bundle.md)), and one source for every harness.

### Consequences

- [+] A tool change is a view change. The files, their history, and their links stay.
- [+] A new tool is judged by one question: does it work from the files.
- [-] A tool-native feature that keeps state elsewhere, memory, a session index, a comment database, is either unused or a rebuildable cache.
- [-] A file can be text and still closed in practice. A compressed drawing payload is text no person reads, so an SVG snapshot sits beside it.

[FOA]: https://stephango.com/file-over-app
