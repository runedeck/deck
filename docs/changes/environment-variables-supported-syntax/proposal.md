---
status: proposed
---

# Environment variable support

## Why

An *[instruction][INSTRUCTION]* often needs a value that differs for each user or machine: a path, an account, a host. The foundations say the [instruction][INSTRUCTION] refers to it as a shell variable, `$NAME` or `${NAME}`, and never spells the value out. Nothing says where the value comes from when the [instruction][INSTRUCTION] runs. Each author improvises: a hardcoded fallback, a note to the user, or nothing. The user has to guess which variable to set. A *[skill][SKILL]* that needs a value fails without a word when none is set.

This *[change][CHANGE]* defines the sources of a value, their order, and how each *[harness][HARNESS]* runs the step that loads them. It absorbs the foundations requirement The Shell Resolves the Variable, so resolution is described in one place.

## What Changes

- A value comes from the first of four sources that sets it:
    1. an argument given when the [instruction][INSTRUCTION] is invoked
    2. the user's own configuration file, which git ignores
    3. the defaults file that comes with the [instruction][INSTRUCTION]'s domain
    4. the fallback written in the *[state file][STATEFILE]* with the shell's default form
- A loader merges the sources and exports the result as environment variables.
- The *[assembler][ASSEMBLER]* gives each [harness][HARNESS] its own way to run the loader. For Claude Code, the *[basis parameters][BASISPARAMETERS]* add an argument hint and a dynamic context line that runs the loader when the [skill][SKILL] loads. Codex and OpenCode inject nothing, so their *[instance][INSTANCE]* opens with a step that runs the loader in the shell.
- The *[provenance record][PROVENANCERECORD]* of each [instance][INSTANCE] names the [basis parameters][BASISPARAMETERS] that produced it.
- The Shell Resolves the Variable moves here from the foundations. A value resolves when the *[model][MODEL]* runs a shell command and never when the [harness][HARNESS] loads the file.

## Capabilities

### New Capabilities

- environment-variables-supported-syntax: where a configurable value comes from, in which order, and how each [harness][HARNESS] loads it.

## Impact

- The foundations specification user-values-and-variables loses The Shell Resolves the Variable.
- The [assembler][ASSEMBLER], its Claude Code, Codex, and OpenCode [basis parameters][BASISPARAMETERS], and the [provenance record][PROVENANCERECORD].
- Every [skill][SKILL] that reads a configurable value. The worked example in the design is a presentation [skill][SKILL] that reads its images from an assets directory variable.
- Configuration Defaults in the [change][CHANGE] one-domain-one-plugin describes the same defaults file, the same git-ignored user file, and the same export. That requirement is undecided and probably merges here. Until then both stand.

[INSTRUCTION]: ../../specs/glossary/instruction.md
[SKILL]: ../../specs/glossary/skill.md
[CHANGE]: ../../specs/glossary/change.md
[HARNESS]: ../../specs/glossary/harness.md
[STATEFILE]: ../../specs/glossary/state-file.md
[ASSEMBLER]: ../../specs/glossary/assembler.md
[BASISPARAMETERS]: ../../specs/glossary/basis-parameters.md
[INSTANCE]: ../../specs/glossary/instance.md
[PROVENANCERECORD]: ../../specs/glossary/provenance-record.md
[MODEL]: ../../specs/glossary/model.md
