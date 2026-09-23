# Model specific assembly design

## Approach

Two halves: variants at build time, activation at runtime. The *[assembler][ASSEMBLER]* builds a *[variant][VARIANT]* for each *[model][MODEL]* it knows, because the differences are known before a session. A *[hook][HOOK]* reads the active [model][MODEL] at session start and on a [model][MODEL] change. The [model][MODEL] is chosen at runtime and can change in a session, so build time cannot know it.

The alternative was one *[instance][INSTANCE]* for each *[harness][HARNESS]* and [model][MODEL], deployed side by side. It lost twice: it breaks One Instance per Harness, and it still cannot change with the [model][MODEL] in a session. The owner chose the swap: the [hook][HOOK] puts the active [model][MODEL]'s [variant][VARIANT] in place of the one [instance][INSTANCE].

## Coverage table

| Capability | Requirement | Check or missed requirement |
|---|---|---|
| one-instance-per-model | A Variant per Known Model | missed requirement: the assembler builds no model variant yet |
| one-instance-per-model | Variant Resolution Has One Order | missed requirement: no fixture holds a user variant, a harness and model variant, and a harness variant of one instruction |
| one-instance-per-model | A Runtime Hook Activates the Variant | missed requirement: no hook reads the active model yet |

## Commands

No command implements this change yet. When the cli change that builds it exists, this table names the command, flags, hook, and diagnostic ids for each requirement.

## Decisions

- Reusable Across Harnesses and Models stays in the foundations, with "and models" backed by this change (voice review, 2026-10-18).
- One Instance per Harness stays as written. The [hook][HOOK] swaps in the [model][MODEL]'s [variant][VARIANT] instead of a second [instance][INSTANCE] for each [model][MODEL].
- The ontology's [variant][VARIANT] term already states the resolution order: user, then [harness][HARNESS] and [model][MODEL], then [harness][HARNESS], then the base *[rune][RUNE]*. This change makes the [assembler][ASSEMBLER] and the [hook][HOOK] apply it.
- Companions Earn Their Place decides whether a [model][MODEL] [variant][VARIANT] stays. It beats the *[canon][CANON]* alone on an evaluation for its [harness][HARNESS] and [model][MODEL], or it goes.

## Risks

- A [harness][HARNESS] may not tell a [hook][HOOK] which [model][MODEL] is active, or may not fire a hook on a model change. Guard: where a swap is impossible, the [hook][HOOK] injects the [variant][VARIANT]'s difference as context. Where neither works, the [harness][HARNESS] gets its [harness][HARNESS] [variant][VARIANT] only, and the coverage table says so.
- A swap in a session leaves the deployment manifest naming the base [instance][INSTANCE]. Guard: the swap is a runtime overlay that the next deployment resets, and the deployment check reads the manifest and ignores the overlay.
- Variants multiply files. Guard: Companions Earn Their Place removes a [variant][VARIANT] that does not beat the canon on an evaluation.

[ASSEMBLER]: ../../specs/glossary/assembler.md
[VARIANT]: ../../specs/glossary/variant.md
[MODEL]: ../../specs/glossary/model.md
[HOOK]: ../../specs/glossary/hook.md
[INSTANCE]: ../../specs/glossary/instance.md
[HARNESS]: ../../specs/glossary/harness.md
[RUNE]: ../../specs/glossary/rune.md
[CANON]: ../../specs/glossary/canon.md
