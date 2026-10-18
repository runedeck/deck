---
title: Rune Fills the Tool Roles
description: The specifications name roles instead of programs. One program, rune, fills every role and has the capabilities each role needs.
type: adr
category: architecture
tags:
    - architecture
    - specifications
    - roles
    - rune
status: proposed
created: 2026-10-18
updated: 2026-10-19
author: "@N4M3Z"
project: deck
related:
    - "CORE-0019 Spec-Driven Change Lifecycle"
    - "CORE-0021 Unified Module Validation"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5-1@claude"]
informed: []
upstream: []
change: plain-text-first-principles
---

# Rune Fills the Tool Roles

## Context and Problem Statement

This record says which program fills the *[tool roles][TOOLROLE]*, and what it has to do for each one. The specifications leave that question open. The foundation specifications describe an *[instruction][INSTRUCTION]* kept as an *[artifact][ARTIFACT]*. The [tool roles][TOOLROLE] check it, assemble it for each *[harness][HARNESS]*, generate it from its source, deploy it, repair it, sign it, and archive it.

A *[requirement][REQUIREMENT]* states the [tool role][TOOLROLE] that does each job. It states no command and no flag, because the owner renames a command while the behavior stays the same. The foundations are a philosophy for treating [instructions][INSTRUCTION] as [artifacts][ARTIFACT]. A manual for one tool is a different document.

The roles are ontology terms: the *[validator][VALIDATOR]*, the *[assembler][ASSEMBLER]*, the *[generator][GENERATOR]*, the *[deployer][DEPLOYER]*, the *[fixer][FIXER]*, the *[signer][SIGNER]*, and the *[archiver][ARCHIVER]*.

## Decision Drivers

- A [requirement][REQUIREMENT] outlives a command name, so the specifications stay true when the owner renames a command
- One install and one version put the commit hook, the push hook, and continuous integration on one path ([CORE-0021](CORE-0021%20Unified%20Module%20Validation.md))
- Each role reads the same ontology, the same *[structure schemas][STRUCTURESCHEMA]*, and the same manifest, so one program needs one parser for each
- A role is replaceable. Another program that passes the same *[scenarios][SCENARIO]* may fill it

## Considered Options

1. One program per role. The owner installs and versions a separate [validator][VALIDATOR], [assembler][ASSEMBLER], [generator][GENERATOR], [deployer][DEPLOYER], [fixer][FIXER], [signer][SIGNER], and [archiver][ARCHIVER]. Seven tools then agree on one ontology and one manifest only by discipline.
2. Rune fills every role. One program fills each role as a capability, and rune meets a [requirement][REQUIREMENT] when its behavior matches it.
3. A plugin per [harness][HARNESS]. The extension mechanism of each [harness][HARNESS] fills the roles for that [harness][HARNESS], with no shared program. Each [harness][HARNESS] then has its own copy of the constraints.

## Decision Outcome

Option 2. Rune fills every role. The specifications keep stating roles, and this record binds each role to the capabilities rune MUST have:

- The [validator][VALIDATOR] reads [artifacts][ARTIFACT] against the [structure schemas][STRUCTURESCHEMA], the ontology, the link constraints, and the deployment manifest, and reports findings. It never edits.
- The [assembler][ASSEMBLER] turns a *[canon][CANON]* and its *[sidecars][SIDECAR]* into one *[instance][INSTANCE]* for each [harness][HARNESS] and a *[variant][VARIANT]* for each *[model][MODEL]* it knows. It translates includes and term links for each [harness][HARNESS] and seals the *[provenance record][PROVENANCERECORD]*.
- The [generator][GENERATOR] writes derived files from their source: the root index, the directory indexes, the glossary pages, and the changelog. It regenerates them for the drift check.
- The [deployer][DEPLOYER] copies [instances][INSTANCE] into the [harness][HARNESS] trees and records the deployment manifest.
- The [fixer][FIXER] edits [artifacts][ARTIFACT] to repair a reported finding, as a separate step the author invokes or a hook runs before the [validator][VALIDATOR]. Its first job is a draft term in the ontology.
- The [signer][SIGNER] binds a head to the owner's key.
- The [archiver][ARCHIVER] moves an accepted *[change][CHANGE]* into the canonical specifications and refuses a [change][CHANGE] that links to a draft term.

A role remains replaceable. Another program MAY fill a role when it passes the same [scenarios][SCENARIO]. A [requirement][REQUIREMENT] never states rune by name.

### Consequences

- [+] A [requirement][REQUIREMENT] stays true when the owner renames a rune command, because the specification states the role
- [+] The owner installs one program at one version, with one path through the hooks and continuous integration
- [+] All roles share one reading of the ontology, the [structure schemas][STRUCTURESCHEMA], and the manifests
- [-] Rune is the one dependency for every role. A bug in rune blocks checking, *[assembly][ASSEMBLY]*, and deployment at once. The fallback scripts under `scripts/fallback/` cover only the term check, the term [fixer][FIXER], and the glossary [generator][GENERATOR] today.
- [-] The capability list in this record grows with every new role. A role that a specification adds without a line here is a gap that this record owns.

## More Information

- The voice review of 17 and 18 October 2026 decided that specifications state roles and no program. It listed the [validator][VALIDATOR], the [assembler][ASSEMBLER], the [generator][GENERATOR], the [deployer][DEPLOYER], and the [fixer][FIXER]. The [signer][SIGNER] and the [archiver][ARCHIVER] joined when the ontology gained the roles.
- Rewritten on 2026-10-19 in the plain spoken register. The decision is unchanged.

[INSTRUCTION]: ../specs/glossary/instruction.md
[ARTIFACT]: ../specs/glossary/artifact.md
[HARNESS]: ../specs/glossary/harness.md
[REQUIREMENT]: ../specs/glossary/requirement.md
[VALIDATOR]: ../specs/glossary/validator.md
[ASSEMBLER]: ../specs/glossary/assembler.md
[GENERATOR]: ../specs/glossary/generator.md
[DEPLOYER]: ../specs/glossary/deployer.md
[FIXER]: ../specs/glossary/fixer.md
[SIGNER]: ../specs/glossary/signer.md
[ARCHIVER]: ../specs/glossary/archiver.md
[CANON]: ../specs/glossary/canon.md
[SIDECAR]: ../specs/glossary/sidecar.md
[INSTANCE]: ../specs/glossary/instance.md
[MODEL]: ../specs/glossary/model.md
[PROVENANCERECORD]: ../specs/glossary/provenance-record.md
[CHANGE]: ../specs/glossary/change.md
[TOOLROLE]: ../specs/glossary/tool-role.md
[VARIANT]: ../specs/glossary/variant.md
[STRUCTURESCHEMA]: ../specs/glossary/structure-schema.md
[SCENARIO]: ../specs/glossary/scenario.md
[ASSEMBLY]: ../specs/glossary/assembly.md
