---
title: Directories Direct
description: Directory names as routing decisions with functional consequences
type: adr
category: architecture
tags:
    - architecture
    - naming
status: accepted
created: 2026-03-19
updated: 2026-09-20
author: "@N4M3Z"
project: deck
related: []
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5", "gpt-5.6-sol"]
informed: []
upstream: []
change: core-foundation-principles
---

# Directories Direct

## Context and Problem Statement

Directory names are the primary navigation mechanism for both humans and AI tools. In an assembly pipeline where directory names drive variant resolution, provider targeting, and model selection, every directory name is a routing decision with functional consequences. A directory named `claude/` immediately tells you "this content is for Claude." A directory named `misc/` tells you nothing.

## Considered Options

1. **Categorization-first**: group by type (`config/`, `docs/`, `scripts/`). Familiar, but it tells you what something is, not where it goes or what it does.
2. **Function-first**: name by routing purpose (`claude/`, `user/`, `rules/`). Every name is a decision with functional consequences.

## Decision Outcome

Directories are navigation, not categorization. Every directory name is a routing decision. It tells the user and the AI where to find things and where new things belong.

Principles:

- Optimize for discoverability over categorization: "where would someone look for it?"
- A well-named directory removes the need for documentation about where each thing goes
- Directory names in qualifier paths (`claude/`, `opus-4-6/`, `user/`) have functional consequences. A typo silently disables content.
- Use `directories`, not `folders`, in docs, commit messages, and conversation

A directory name MUST state a routing purpose. A directory that groups by type alone, such as `misc/`, MUST NOT be added.

## Consequences

- The directory tree is self-documenting
- No separate "where to put things" guide
- Qualifier directories double as routing labels: naming is configuration
