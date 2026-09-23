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
updated: 2026-10-18
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

The foundation specifications describe how an *[instruction][INSTRUCTION]* is kept as an *[artifact][ARTIFACT]*. It is checked, assembled for each *[harness][HARNESS]*, generated from its source, deployed, repaired, signed, and archived.
A *[requirement][REQUIREMENT]* names the *[tool role][TOOLROLE]* that does each job. It names no command and no flag, because a command gets renamed while the behavior stays. The foundations are a philosophy for treating [instructions][INSTRUCTION] as [artifacts][ARTIFACT]. A manual for one tool is a different document.
The roles are ontology terms: the *[validator][VALIDATOR]*, the *[assembler][ASSEMBLER]*, the *[generator][GENERATOR]*, the *[deployer][DEPLOYER]*, the *[fixer][FIXER]*, the *[signer][SIGNER]*, and the *[archiver][ARCHIVER]*.
This record answers the question the specifications leave open: which program fills the roles, and what it has to do for each.

## Decision Drivers

- A [requirement][REQUIREMENT] outlives a command name, so the specifications stay true when a command is renamed
- One install and one version keep the commit hook, the push hook, and continuous integration on one path ([CORE-0021](CORE-0021%20Unified%20Module%20Validation.md))
- Every role reads the same ontology, the same structure schemas, and the same manifest, so one program needs one parser for each
- A role stays replaceable: another program that passes the same scenarios may fill it

## Considered Options

1. One program per role: a separate [validator][VALIDATOR], [assembler][ASSEMBLER], [generator][GENERATOR], [deployer][DEPLOYER], [fixer][FIXER], [signer][SIGNER], and [archiver][ARCHIVER], each installed and versioned alone. Seven tools agree on one ontology and one manifest only by discipline.
2. Rune fills every role: one program fills each role as a capability, and a [requirement][REQUIREMENT] is met when rune's behavior matches it.
3. A plugin per [harness][HARNESS]: each harness's own extension mechanism fills the roles for that harness, with no shared program. Every harness then carries its own copy of the rules.

## Decision Outcome

Option 2. Rune fills every role. The specifications keep naming roles, and this record binds each role to the capabilities rune MUST have:

- The [validator][VALIDATOR] reads [artifacts][ARTIFACT] against the structure schemas, the ontology, the link rules, and the deployment manifest, and reports findings. It never edits.
- The [assembler][ASSEMBLER] turns a *[canon][CANON]* and its *[sidecars][SIDECAR]* into one *[instance][INSTANCE]* for each [harness][HARNESS] and a *[variant][VARIANT]* for each *[model][MODEL]* it knows. It translates includes and term links for each [harness][HARNESS] and seals the *[provenance record][PROVENANCERECORD]*.
- The [generator][GENERATOR] writes derived files from their source: the root index, the directory indexes, the glossary pages, and the changelog. It regenerates them for the drift check.
- The [deployer][DEPLOYER] copies [instances][INSTANCE] into the harness trees and records the deployment manifest.
- The [fixer][FIXER] edits [artifacts][ARTIFACT] to repair a reported finding, as a separate step the author invokes or a hook runs before the validator. Its first job is a draft term in the ontology.
- The [signer][SIGNER] binds a head to the owner's key.
- The [archiver][ARCHIVER] moves an accepted *[change][CHANGE]* into the canonical specifications and refuses a change that links to a draft term.

A role stays replaceable. Another program MAY fill a role when it passes the same scenarios, and a [requirement][REQUIREMENT] never names rune.

### Consequences

- [+] A requirement stays true when a rune command is renamed, because the specification names the role
- [+] One install, one version, and one path through the hooks and continuous integration
- [+] Every role shares one reading of the ontology, the structure schemas, and the manifests
- [-] Rune is the one dependency for every role. A bug in rune blocks checking, assembly, and deployment at once. The fallback scripts under `scripts/fallback/` cover only the term check, the term fixer, and the glossary generator today.
- [-] The capability list in this record grows with every new role. A role a specification adds without a line here is a gap this record owns.

## More Information

- The voice review of 17 and 18 October 2026 decided that specifications name roles and no program. It named the validator, the assembler, the generator, the deployer, and the fixer. The signer and the archiver joined when the ontology gained the roles.

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
