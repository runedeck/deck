---
adr: docs/changes/writing-and-conduct-rules/adr.md
status: proposed
decisions: ["Writing and conduct rules in core"]
---

# Writing and conduct rules

## Why

The owner runs these rules in every session from a deployed copy. Their source lived only on an unpushed stack, so a fresh machine could not rebuild the deployment. A rule that is in use and absent from the deck breaks the reproducibility the deck exists for.

## What Changes

- Rules for writing: CiteSources, LessIsMore, NoEmDash, NoItemCounts, NoAgenticAttribution, AsciiDiagrams, ScenarioTitles.
- Rules for conduct: OnePurpose, AvoidDuplication.
- Each rule enters with the text that is deployed today. No rule carries a provenance sidecar, because each is first-party content.
- The `prose`, `authoring`, and `delivery` casts select the rules that fit them.

## Capabilities

- writing-and-conduct-rules (new)

## Impact

- `runes/core/rules/` gains the rule files. `casts/` gains the entries.
- The record in `adr.md` moves to `docs/decisions/` at archive.
