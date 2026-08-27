## ADDED Requirements

### Requirement: Description and Validation Separate

The ontology in `ontology/rune.ttl` MUST only describe kinds and relations. Validation MUST come from SHACL shapes in `ontology/shapes.ttl`. A gate MUST NOT depend on OWL or RDFS inference for a pass-or-fail result.

#### Scenario: A constraint is proposed as an OWL axiom

- **WHEN** a change models a cardinality limit as an OWL axiom without a matching shape
- **THEN** review rejects the change and requests a SHACL shape

### Requirement: Established Vocabularies First

A new term MUST reuse an established vocabulary when one fits. A minted term MUST declare `rdfs:subClassOf` to an established class. A new class or namespace MUST carry a decision record.

#### Scenario: A minted term duplicates schema.org

- **WHEN** a change mints a term that an established vocabulary already defines
- **THEN** review rejects the minted term and names the established term

### Requirement: Identifier Is Identity

The extractor MUST mint entity IRIs from record identifiers under `https://runedeck.dev/id/`, never from file paths. Two files that claim one identifier MUST merge into one graph node, and each input file MUST contribute one `rune:sourcePath` value, so the duplicate stays visible.

#### Scenario: Two records claim one identifier

- **WHEN** two files carry the identifier DECK-0002
- **THEN** validation reports cardinality violations on the DECK-0002 node

### Requirement: Severity Ratchet

A new shape MUST start at Warning severity. A move to Violation MUST land as a recorded follow-up change after the existing corpus conforms.

#### Scenario: A shape is added while violations exist on main

- **WHEN** a new shape would fail files that main already contains
- **THEN** the shape ships at Warning severity and a follow-up task records the flip condition

### Requirement: Guarded Hooks

Every lint hook MUST skip when its binary is absent, so a fresh clone commits successfully. CI MUST install every gate binary against a pinned digest and MUST set `REQUIRE_GATES`, which turns a guarded skip into a failure.

#### Scenario: A contributor lacks the tools

- **WHEN** a contributor commits without rumdl, Vale, or typos installed
- **THEN** the guarded hooks skip and the commit proceeds

#### Scenario: CI lacks a gate binary

- **WHEN** a CI run misses one gate binary with `REQUIRE_GATES` set
- **THEN** the corresponding hook fails instead of skipping

### Requirement: CI Checks the Change Range

CI MUST select one commit range for both commit-stage and pre-push checks. Hooks that accept filenames MUST inspect only files in that range. Repository validators MUST run as their hook configuration specifies. CI MUST inspect all files only if no usable base exists.

#### Scenario: A pull request has a usable base

- **WHEN** CI checks a pull request with an available base commit
- **THEN** both stages use the same range and repository validators keep their configured behavior
