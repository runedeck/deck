---
adr: docs/changes/cast-player-in-proofs/adr.md
status: proposed
decisions: ["A proof plays as a cast where a person reads it"]
---

# Proof page handover

## Why

The trusted-key-anchor proof of 2026-09-21 was recorded, rendered, and committed, and the handover named the GIF path. The owner had to ask twice for the page with the player. The rule from `cast-player-in-proofs` said what a page must do, not that a page must exist at the end of every proof. This change makes the page a required step and gives the skill a generator, so the step is one command.

## What Changes

- AcceptanceTesting `SKILL.md`: a new `Hand over the page` step after `File the proof`, and a Verification line for it.
- AcceptanceTesting `Recording.md`: the Embed section states the rule, a new Page section gives the command and the page's home in the workshop.
- AcceptanceTesting `scripts/proof-page.py`: builds the page from casts, captions, facts, and the player script.

## Capabilities

### New Capabilities

- `proof-page-handover`: a finished proof is handed over as a page whose scene list comes from the casts.

## Impact

- One skill in the deck. The player still comes from [html-tools](https://github.com/N4M3Z/html-tools). The workshop page `docs/specs/2026-09-21-proof-set.html` is the first one built this way.
