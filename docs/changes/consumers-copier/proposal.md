---
adr: "docs/decisions/DECK-0012 Consumer Ceremony Synchronization.md"
status: proposed
---

# Consumers Copier

## Why

The deck's checks and the skeleton template disagreed in every shared file, its Copier pin was two months stale, and the weekly ceremony audit reported the same intentional rows each week (deck#45). The deck's prose failed the generated Vale style the template now carries (deck#18). [DECK-0012](../../decisions/DECK-0012%20Consumer%20Ceremony%20Synchronization.md) records how a diverged consumer converges.

## What Changes

- `answers.yaml` records the current skeleton commit. Copier merged the template from the old pin, and the deck's own hooks, targets, excludes, and Quality steps sit on top of the template's.
- The deck installs the shared toolchain through `scripts/install-tools` and runs its provenance digest tests in Quality.
- Semicolons and contractions in prose are corrected at the reported positions. Every sealed file the corrections touched is resealed. The Simplified Technical English samples keep their deliberate errors through a path-scoped Vale override.
- Nested lists indent four spaces under rumdl, and the flagged files are formatted.
- `.ceremony-divergences.yaml` is seeded empty. The deck declares no whole-file divergence.

## Capabilities

- template-composition (new)
- adoption-session-state (modified)

## Impact

- Root check configuration, hooks, workflows, and tool pins.
- Sealed sidecars under `runes/core/rules/.provenance`, `runes/core/skills/BuildSkill/.provenance`, and `runes/core/skills/BenchArtifact/templates/agents/.provenance`.
- Prose across `runes/core`, `docs/decisions`, and `docs/changes`.
