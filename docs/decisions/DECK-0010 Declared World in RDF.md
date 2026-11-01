---
title: Declared World in RDF
description: The deck declares its artifact world in RDF with established vocabularies, and SHACL shapes validate the extracted graph as a deterministic check
type: adr
category: architecture
tags:
    - architecture
    - ontology
    - validation
status: accepted
created: 2026-08-26
updated: 2026-10-19
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
change: ontology-keeps-agents-honest
---

# Declared World in RDF

## Context and Problem Statement

The *[repository][REPOSITORY]* needs a deterministic layer that decides which proposed *[artifact][ARTIFACT]* it permits, and this record chooses the semantic-web stack for that layer. *[Models][MODEL]* propose [artifacts][ARTIFACT]. The first draft was a custom checker with a custom world file. A custom checker grows into a private standard that nobody else maintains.

The semantic-web stack already solves this problem. Established vocabularies define the concepts, the Resource Description Framework (RDF) stores the facts, and the Shapes Constraint Language (SHACL) validates them. The [repository][REPOSITORY] needs a decision on namespaces, vocabulary reuse, the validation semantics, and the toolchain.

## Decision Drivers

- The [repository][REPOSITORY] reuses established vocabularies. It invents no term that schema.org, PROV-O, Dublin Core, SKOS, FOAF, or DOAP already defines. PROV-O is the provenance ontology of the World Wide Web Consortium (W3C). The other abbreviations are the Simple Knowledge Organization System (SKOS), Friend of a Friend (FOAF), and Description of a Project (DOAP).
- The check that admits or blocks an [artifact][ARTIFACT] must be deterministic: one boolean conformance result with a machine-readable report.
- The toolchain must run locally as single binaries. The owner prefers Rust, excludes Java, and excludes Python from the path of the blocking check.
- A namespace choice is permanent. A later rename costs as much as a history rewrite.
- The blocking check must grow one shape at a time from observed failures, as the OBO (Open Biological and Biomedical Ontologies) Foundry does.

## Considered Options

1. A custom checker with a custom world file. The owner has full control, no standard, and a private format to maintain forever.
2. OWL (Web Ontology Language) constraints with a reasoner. OWL is a standard, but it operates under the open-world assumption. A cardinality axiom makes the reasoner infer that two refunds are one refund. It never fails the data.
3. An RDF ontology for description plus SHACL shapes for validation. RDFS (RDF Schema) and OWL describe and infer. SHACL validates under the closed-world assumption and fails deterministically.

## Decision Outcome

Option 3. The decisions in detail:

- **Namespaces.** The product vocabulary has the namespace `https://runedeck.ai/ns#` and the prefix `rune:`. The owner's personal vocabulary has the namespace `https://martinzeman.net/ns#` and the prefix `n4m3z:`. An entity gets an IRI (Internationalized Resource Identifier) under `/id/`, apart from the terms under `/ns#`. The personal graph imports the product graph, and never the reverse.
- **Vocabulary reuse.** PROV-O is the backbone: an [artifact][ARTIFACT] is a `prov:Entity`, work is a `prov:Activity`, and a person or a [model][MODEL] is a `prov:Agent`. Dublin Core terms hold the generic metadata. The [repository][REPOSITORY] creates a term only where a verified search does not find an established term. Every created class declares `rdfs:subClassOf` to an established class. The first created terms are `rune:DecisionRecord`, `rune:Rule`, and `rune:Verdict`.
- **Kinds from the first-generation survey.** The taxonomy says "kind" and never "ontology", because the first generation used that word for filesystem roots. `rune:Rune` is the umbrella class over the five kinds. *[Canon][CANON]*, *[Sidecar][SIDECAR]*, *[Companion][COMPANION]*, *[Template][TEMPLATE]*, *[Variant][VARIANT]*, and *[StructureSchema][STRUCTURESCHEMA]* are classes, because the first generation proved that each one is necessary. Provider and *[Target][TARGET]* remain separate. A drift state is a query over digests and never a stored fact.
- **Identity.** A record identifier such as DECK-0010 is the identity. The extractor creates the IRI from the identifier and never from the file path. When two files claim one identifier, they merge into one node, and the shapes report the collision as a cardinality violation.
- **Validation semantics.** OWL and RDFS never block an [artifact][ARTIFACT]. The SHACL shapes in `ontology/shapes.ttl` are the check that blocks. The first scope is three shapes: a unique identifier on each record, a resolvable reference, and a *[verdict][VERDICT]* pointer on every *[rule][RULE]*.
- **Toolchain.** `rudof shacl-validate`, a Rust program, validates the extracted graph. The extractor is a `rune` subcommand in the cli clone. The prose and hygiene checks are rumdl, typos, Vale, lychee, actionlint, and zizmor.
- **Change ceremony.** A new class or a new namespace requires a *[decision record][DECISIONRECORD]*. A new shape on an existing class is a normal reviewed *[change][CHANGE]*. A shape's severity starts at Warning, and the owner moves it to Violation in a recorded follow-up.

### Consequences

- [+] The world file is in Turtle, a W3C standard. Any RDF tool reads it, and nobody maintains a custom parser.
- [+] The blocking check grows through the extraction flywheel: an observed failure becomes a permanent shape.
- [+] The instance graph answers provenance queries at no extra cost once commits and [verdicts][VERDICT] enter it.
- [-] The rudof dependency is young (0.x). The shapes are standard SHACL, so pySHACL or Apache Jena can cross-check the same files outside the blocking path.
- [-] The [repository][REPOSITORY] takes on nomenclature debt. A contributor must learn five terms: *[triple][TRIPLE]*, ontology, shape, IRI, and closed world. The design document in the ontology-keeps-agents-honest [change][CHANGE] contains the primer.

## More Information

- 2026-09-23: the owner moved the namespace from `runedeck.dev` to `runedeck.ai`, the domain the project owns. No external data referenced the old IRIs, so this was the last cheap moment. The owner updated the cli exporter, the two ontology files, and the smoke *[fixture][FIXTURE]* together.
- Rewritten on 2026-10-19 in the plain spoken register. The decision is unchanged.

[REPOSITORY]: ../specs/glossary/repository.md
[ARTIFACT]: ../specs/glossary/artifact.md
[MODEL]: ../specs/glossary/model.md
[CANON]: ../specs/glossary/canon.md
[SIDECAR]: ../specs/glossary/sidecar.md
[COMPANION]: ../specs/glossary/companion.md
[TEMPLATE]: ../specs/glossary/template.md
[VARIANT]: ../specs/glossary/variant.md
[STRUCTURESCHEMA]: ../specs/glossary/structure-schema.md
[TARGET]: ../specs/glossary/target.md
[DECISIONRECORD]: ../specs/glossary/decision-record.md
[CHANGE]: ../specs/glossary/change.md
[TRIPLE]: ../specs/glossary/triple.md
[VERDICT]: ../specs/glossary/verdict.md
[RULE]: ../specs/glossary/rule.md
[FIXTURE]: ../specs/glossary/fixture.md
