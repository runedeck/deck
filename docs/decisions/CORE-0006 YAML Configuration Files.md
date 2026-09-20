---
title: YAML Configuration Files
description: Modules ship defaults.yaml merged with gitignored config.yaml via recursive deep merge
type: adr
category: architecture
tags:
    - architecture
    - config
status: accepted
created: 2026-02-19
updated: 2026-09-20
author: "@N4M3Z"
project: deck
related:
    - "CORE-0005 Variables in Markdown Instructions and Templates"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5", "gpt-5.6-sol"]
informed: []
upstream: []
change: core-foundation-principles
---

# YAML Configuration Files

## Context and Problem Statement

ENV vars in markdown instructions ([CORE-0005](CORE-0005 Variables in Markdown Instructions and Templates.md)) need a source. Each module has configurable values (paths, feature flags, skill rosters) that differ between default and user-specific setups. The configuration system must support committed defaults, user overrides, and ENV var export without requiring users to manage shell profiles.

## Decision Drivers

- Defaults are committed and version-controlled, so the module works out of the box
- User overrides are gitignored, so personal paths and preferences stay out of the repository
- Override granularity is per-field, not per-file: users change one path, not the entire config
- ENV variable export is automatic: `yq` can read individual values, but the export of an entire config subtree as prefixed ENV vars requires a multi-step pipeline

## Considered Options

1. **Flat ENV files**: `.env` with `KEY=VALUE` pairs. No nesting, no merge, no defaults mechanism.
2. **JSON config**: structured and mergeable, but hard to author by hand, with no comment support.
3. **YAML with deep merge**: a committed `defaults.yaml` merged with a gitignored `config.yaml`, recursive so users override only the fields they need.

## Decision Outcome

Chosen option: **YAML with deep merge**. Each module includes `defaults.yaml` with the full schema and working defaults. Users create a gitignored `config.yaml` with only the fields they override. The config loading exports the merged result as ENV vars with a configurable prefix.

A module MUST include a committed `defaults.yaml` that works without user input. A user override MUST live in a git-ignored `config.yaml` and MUST merge over the defaults field by field.

## Consequences

- The module works out of the box with zero user configuration
- Users override one field without knowing the full schema
- The config loading bridges config to ENV vars consumed by skills and shell commands
- Deep merge semantics can surprise: array replacement versus append, null versus missing
