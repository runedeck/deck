---
name: AgenticOntology
description: "Govern the deck's vocabulary: admit a term into the declared world, name an artifact from its lifecycle stage, audit the corpus for synonyms and overloaded words, and retire a term through deprecation. USE WHEN a new concept needs a name, a skill or class needs a name, two words mean one thing, one word means two things, a term enters a spec or decision record, or the ontology or its shapes change. NOT FOR validating instance data in CI (the shapes hook does that), authoring runes (BuildSkill), or prose style (SimplifiedTechnicalEnglish)."
compatibility: "Requires rudof for shape validation and rg for the corpus audit."
metadata:
    version: 0.1.0
---

# AgenticOntology

The deck declares what exists once, in `ontology/rune.ttl`, and every other artifact uses those names. This skill keeps that true: a term enters the ontology before it enters prose, an artifact takes its name from the stage it serves, and a word that drifts gets merged or retired. [Lifecycle.md](Lifecycle.md) holds the stage table, [SemanticDensity.md](SemanticDensity.md) the measure the audit reports, and [Vocabularies.md](Vocabularies.md) which established vocabulary to reuse.

## Constraints

- One name for one thing across the ontology, the specs, the decision records, the skill names, and the CLI diagnostics. A synonym is a defect, not a style choice.
- A term enters `ontology/rune.ttl` before any spec, record, or skill uses it. Prose cites the ontology. The ontology never cites prose.
- Reuse before minting. A minted class declares `rdfs:subClassOf` to an established class, and a minted scheme uses SKOS. [Vocabularies.md](Vocabularies.md) lists the search order.
- A new class or namespace needs a decision record (DECK-0010). A new shape on an existing class is a normal reviewed change.
- Derived states are queries over stored facts, never stored facts.
- A rename is a migration: deprecate, keep the old label as an alternative label for one release, then remove. Never edit a label in place.
- The ontology describes and the shapes decide. Do not put a constraint in `rune.ttl`, and do not put a definition in `shapes.ttl`.

## Instructions

### Admit a term

1. State the concept in one sentence and the stage it belongs to.
2. Search the corpus for an existing label: `rg -n -i '<concept words>' ontology docs runes --glob '!.workspaces'`. A hit means reuse, not a new term.
3. Search the established vocabularies in the order [Vocabularies.md](Vocabularies.md) gives. Reuse the term when one fits.
4. Otherwise mint it: class or concept, `rdfs:label`, `rdfs:comment` of one sentence, and the superclass. Add one shape in `shapes.ttl` at Warning severity, and one seeded instance in `ontology/smoke/instances.ttl` that the shape reports. Raise the expected counts in the fixture's header comment and in the `ontology-syntax` hook in `.pre-commit-config.yaml`, which asserts the exact Violation and Warning totals.
5. Add the term to the glossary that the consuming spec or record cites, and open the change that uses it.

### Name an artifact

1. Find the lifecycle stage the artifact serves in [Lifecycle.md](Lifecycle.md), and the entity it consumes and the entity it produces.
2. Compose the name as the stage verb, or an established discipline noun, plus the object: `BenchArtifact`, `AdoptArtifact`, `ContinuousIntegration`, `VersionControl`.
3. Reject a name that names the category instead of the act, a name that a philosophy or product already owns, and a name whose first word is a marketing adjective.
4. Record the name and its stage in the lifecycle table.

### Audit drift

1. For every label in `rune.ttl`, list its synonyms from the corpus with `rg`, and for every corpus word that looks like a term, list the labels it maps to.
2. Compute the density in [SemanticDensity.md](SemanticDensity.md). Report each word below or above one with the files that use it.
3. Propose one merge per finding: which label survives, which files change, which shape catches a recurrence.

### Retire a term

1. Mark the term `owl:deprecated true` and move its label to `skos:altLabel` on the surviving term.
2. Replace every corpus use in one change, with the audit as its receipt.
3. Remove the term one release later, with the decision record that admitted it updated to say so.

## Verification

- `rudof data ontology/rune.ttl` parses, and the `ontology-syntax` hook passes: the fixture's Violation and Warning totals equal the counts the hook asserts.
- The drift audit reports a density of one for every label the change touched.
- Every skill name in the lifecycle table parses as stage verb or discipline noun plus object.
- The decision record for a new class exists before the class does.

## Troubleshooting

- `rudof` reports zero findings on a fixture that should fail: rudof exits zero on violations, so read the report for `sh:Violation`, never the exit status.
- A term has an established home and a minted twin: keep the established term, deprecate the twin, and run the retire route.
- Two skills want the same name: the stage table decides. The artifact that serves the earlier stage keeps the verb, and the other takes the object it produces.

## References

- `ontology/rune.ttl`, `ontology/shapes.ttl`, `ontology/smoke/instances.ttl`
- DECK-0010 Declared World in RDF, DECK-0014 Vocabulary Governance
