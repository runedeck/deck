---
status: proposed
---

# Model specific assembly

## Why

No *[harness][HARNESS]* solves model-specific *[instructions][INSTRUCTION]*. The *[model][MODEL]* can *[change][CHANGE]* in the middle of a session. Build time alone cannot know which [model][MODEL] reads the [instruction][INSTRUCTION]. The foundations promise an [instruction][INSTRUCTION] reusable across [harnesses][HARNESS] and [models][MODEL]. One *[Instance][INSTANCE]* per [Harness][HARNESS] keeps one [instance][INSTANCE] for each [harness][HARNESS]. This [change][CHANGE] backs both. The *[assembler][ASSEMBLER]* builds a *[variant][VARIANT]* for each known [model][MODEL]. A *[hook][HOOK]* puts the active [model][MODEL]'s [variant][VARIANT] in place at runtime.

## What Changes

- The [assembler][ASSEMBLER] builds a [variant][VARIANT] of each [instruction][INSTRUCTION] for every [model][MODEL] it knows.
- A [hook][HOOK] runs at session start and when the [model][MODEL] [changes][CHANGE]. It reads the active [model][MODEL] and swaps in the matching [variant][VARIANT], or injects that [variant][VARIANT]'s difference as context.
- The [variant][VARIANT] resolution order is the user's own [variant][VARIANT], then the [harness][HARNESS] and [model][MODEL] [variant][VARIANT], then the [harness][HARNESS] [variant][VARIANT], then the base *[rune][RUNE]*.
- One [Instance][INSTANCE] per [Harness][HARNESS] stays as written. The [harness][HARNESS] tree holds one [instance][INSTANCE] for each [instruction][INSTRUCTION], and the [hook][HOOK] swaps one [variant][VARIANT] for another and deploys no second [instance][INSTANCE].

## Capabilities

### New Capabilities

- one-instance-per-model: a [variant][VARIANT] for each [model][MODEL] at build time, and the [hook][HOOK] that activates one at runtime.

## Impact

- The [assembler][ASSEMBLER], the *[deployer][DEPLOYER]*, the [hook][HOOK] of each [harness][HARNESS], and the *[provenance record][PROVENANCERECORD]* of a [variant][VARIANT].
- The foundations requirements Reusable Across [Harnesses][HARNESS] and [Models][MODEL] and One [Instance][INSTANCE] per [Harness][HARNESS], which rest on this [change][CHANGE].
- Companions Earn Their Place in the foundations. A [model][MODEL] [variant][VARIANT] stays when it beats the *[canon][CANON]* alone on an evaluation for its [harness][HARNESS] and [model][MODEL].

[INSTRUCTION]: ../../specs/glossary/instruction.md
[MODEL]: ../../specs/glossary/model.md
[HARNESS]: ../../specs/glossary/harness.md
[INSTANCE]: ../../specs/glossary/instance.md
[CHANGE]: ../../specs/glossary/change.md
[ASSEMBLER]: ../../specs/glossary/assembler.md
[VARIANT]: ../../specs/glossary/variant.md
[HOOK]: ../../specs/glossary/hook.md
[RUNE]: ../../specs/glossary/rune.md
[DEPLOYER]: ../../specs/glossary/deployer.md
[PROVENANCERECORD]: ../../specs/glossary/provenance-record.md
[CANON]: ../../specs/glossary/canon.md
