## ADDED Requirements

### Requirement: A Variant per Known Model

The *[assembler][ASSEMBLER]* MUST build one *[variant][VARIANT]* of an *[instruction][INSTRUCTION]* for each *[model][MODEL]* it knows, from the *[canon][CANON]* and that [model][MODEL]'s *[sidecar][SIDECAR]*, at build time. A [model][MODEL] without a [sidecar][SIDECAR] gets no [variant][VARIANT] and reads the next [variant][VARIANT] in the resolution order. The differences are known before a session, so building them early keeps the runtime step to a swap.

#### Scenario: Model sidecar exists

- **WHEN** an [instruction][INSTRUCTION] has a [sidecar][SIDECAR] for one [model][MODEL]
- **THEN** the [assembler][ASSEMBLER] writes that [model][MODEL]'s [variant][VARIANT] with its own *[provenance record][PROVENANCERECORD]*, and the *[harness][HARNESS]* tree still holds one *[instance][INSTANCE]* of the [instruction][INSTRUCTION]

### Requirement: Variant Resolution Has One Order

The [assembler][ASSEMBLER] MUST pick the [variant][VARIANT] for one [harness][HARNESS] and [model][MODEL] in this order, and the first that exists wins:

1. the user's own [variant][VARIANT]
2. the [harness][HARNESS] and [model][MODEL] [variant][VARIANT]
3. the [harness][HARNESS] [variant][VARIANT]
4. the base *[rune][RUNE]*

#### Scenario: Harness variant and model variant both exist

- **WHEN** an [instruction][INSTRUCTION] has a [harness][HARNESS] [variant][VARIANT] and a [variant][VARIANT] for the active [model][MODEL] on that [harness][HARNESS]
- **THEN** the [harness][HARNESS] and [model][MODEL] [variant][VARIANT] wins, and the user's own [variant][VARIANT] wins over both when it exists

### Requirement: A Runtime Hook Activates the Variant

A *[hook][HOOK]* MUST run at session start and when the [model][MODEL] changes. It reads the active [model][MODEL] and swaps in that [model][MODEL]'s [variant][VARIANT]. Where the [harness][HARNESS] cannot swap a file, it injects the [variant][VARIANT]'s difference as context. The [harness][HARNESS] tree keeps one [instance][INSTANCE] per [instruction][INSTRUCTION], so the [hook][HOOK] swaps and never adds. The [model][MODEL] can change in a session, so build time cannot know it.

#### Scenario: Model changes in a session

- **WHEN** the user switches the [model][MODEL] after the session started
- **THEN** the [hook][HOOK] reads the new [model][MODEL] and swaps in its [variant][VARIANT], or injects its difference, before the next turn

[ASSEMBLER]: ../../../../specs/glossary/assembler.md
[VARIANT]: ../../../../specs/glossary/variant.md
[INSTRUCTION]: ../../../../specs/glossary/instruction.md
[MODEL]: ../../../../specs/glossary/model.md
[CANON]: ../../../../specs/glossary/canon.md
[SIDECAR]: ../../../../specs/glossary/sidecar.md
[PROVENANCERECORD]: ../../../../specs/glossary/provenance-record.md
[HARNESS]: ../../../../specs/glossary/harness.md
[INSTANCE]: ../../../../specs/glossary/instance.md
[RUNE]: ../../../../specs/glossary/rune.md
[HOOK]: ../../../../specs/glossary/hook.md
