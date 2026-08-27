---
title: Declared World in RDF
description: The deck declares its artifact world in RDF with established vocabularies, and SHACL shapes validate the extracted graph as a deterministic gate
type: adr
category: architecture
tags:
    - architecture
    - ontology
    - validation
status: proposed
created: 2026-08-26
updated: 2026-08-26
author: "@N4M3Z"
project: deck
related:
    - "DECK-0001 Artifact Benchmarking Skill"
    - "DECK-0003 Three-Metric Verdict and Cross-Vendor Judging"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: []
informed: []
upstream: []
---

# Declared World in RDF

## Context and Problem Statement

Agents propose artifacts, and the deck needs a deterministic layer that decides what is permitted. The first draft was a custom checker with a custom world file. Custom checkers grow into a private standard that nobody else maintains. The semantic-web stack already solves this problem: established vocabularies name the concepts, RDF stores the facts, and SHACL validates them. The deck needs a decision on namespaces, vocabulary reuse, the validation semantics, and the toolchain.

## Decision Drivers

- Reuse established vocabularies. Do not invent terms that schema.org, PROV-O, Dublin Core, SKOS, FOAF, or DOAP already define.
- The gate must be deterministic: one boolean conformance result with a machine-readable report.
- The toolchain must run locally as single binaries. Prefer Rust. Exclude Java. Exclude Python from the gate path.
- Namespace choices are permanent. A rename later is as costly as a history rewrite.
- The gate must grow one shape at a time from observed failures, after the OBO Foundry practice.

## Considered Options

1. **Custom checker with a custom world file.** Full control, zero standards, and a private format to maintain forever.
2. **OWL constraints with a reasoner.** Standard, but OWL operates under the open-world assumption. A cardinality axiom infers that two refunds are one refund. It never fails the data.
3. **RDF ontology for description plus SHACL shapes for validation.** RDFS and OWL describe and infer. SHACL validates under the closed-world assumption and fails deterministically.

## Decision Outcome

Option 3. The decisions in detail:

- **Namespaces.** The product vocabulary lives at `https://runedeck.dev/ns#` with prefix `rune:`. The owner's personal vocabulary lives at `https://martinzeman.net/ns#` with prefix `n4m3z:`. Entities get IRIs under `/id/`, separate from terms under `/ns#`. The personal graph imports the product graph, never the reverse.
- **Vocabulary reuse.** PROV-O is the backbone: artifacts are `prov:Entity`, work is `prov:Activity`, people and models are `prov:Agent`. Dublin Core terms carry generic metadata. The deck mints a term only where verified search finds no established term, and every minted class declares `rdfs:subClassOf` to an established class. The first minted terms are `rune:DecisionRecord`, `rune:Rule`, and `rune:Verdict`.
- **Kinds from the first-generation survey.** The taxonomy says "kind", never "ontology", because the first generation spent that word on filesystem roots. `rune:Rune` is the umbrella class over the five kinds. Canon, Sidecar, Companion, Template, Variant, and StructureSchema are classes, because the first generation proved each is load-bearing. Provider and Target stay separate. Drift states are queries over digests, never stored facts.
- **Identity.** A record identifier such as DECK-0010 is the identity. The extractor mints the IRI from the identifier, not from the file path. Two files that claim one identifier merge into one node, and the shapes report the collision as a cardinality violation.
- **Validation semantics.** OWL and RDFS never gate. SHACL shapes in `ontology/shapes.ttl` are the gate. The first scope is three shapes: unique record identifiers, resolvable references, and a verdict pointer on every rule.
- **Toolchain.** `rudof shacl-validate` (Rust) validates the extracted graph. The extractor is a `rune` subcommand in the cli repository. The prose and hygiene row is rumdl, typos, Vale, lychee, actionlint, and zizmor.
- **Change ceremony.** A new class or a new namespace requires a decision record. A new shape on existing classes is a normal reviewed change. Shape severity starts at Warning and moves to Violation in a recorded follow-up.

## Consequences

- The world file format is W3C-standard Turtle. Any RDF tool reads it, and no custom parser exists to maintain.
- The gate grows through the extraction flywheel: an observed failure becomes a permanent shape.
- The instance graph gives provenance queries for free once commits and verdicts enter it.
- The rudof dependency is young (0.x). Mitigation: the shapes are standard SHACL, so pySHACL or Apache Jena can cross-check the same files off the gate path.
- The deck learns nomenclature debt: contributors must learn five terms (triple, ontology, shape, IRI, closed world). The design document in the declared-world change carries the primer.
