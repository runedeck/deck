---
adr: docs/changes/draft-artifact-skill-adoption/adr.md
status: proposed
decisions: ["Draft a rune where the harness loads it"]
---

# Draft artifact skill adoption

## Why

A new skill had two bad starts: write it in the deck and wait for a deploy cycle to try it, or write it by hand into `.claude/skills/` where `rune doctor` reports it as an orphan and `rune repair` quarantines it. The cli now has `rune draft` and `rune promote` (cli `4fa850b9`): a draft lives in the provider directories, `.drafts` records it, doctor knows it, and promote moves it into the deck with its change stub. Nothing in the deck told a session to use them.

## What Changes

- Add the DraftArtifact skill at `runes/core/skills/DraftArtifact/SKILL.md`, promoted from a `rune draft` by the same commands it documents.
- The skill routes to BuildSkill after promotion. It does not replace the authoring workflow.

## Capabilities

### New Capabilities

- `draft-artifact-skill-adoption`: a session starts a skill, agent, or rule as a registered draft, checks it with `rune draft --list` and `rune doctor`, and promotes or drops it.

## Impact

- `runes/core/skills/DraftArtifact/SKILL.md` (new).
- The record in `adr.md` moves to `docs/decisions/` at archive.
