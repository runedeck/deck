---
adr: "docs/decisions/DECK-0014 Vocabulary Governance.md"
status: accepted
decisions: ["DECK-0014 Vocabulary Governance"]
---

# Agentic ontology stack

## Why

See the linked ADR for the decision rationale. This proposal records the change in scope.

The deck declares its world in RDF, but nothing says how a term gets in, how an artifact gets its name, or what happens when prose drifts from the ontology. Naming one skill took a day of surveys before the lifecycle scheme answered it. The prove stage has no evidence class.

## What Changes

- The AgenticOntology skill in core: admit a term, name an artifact from its stage, audit the corpus for drift, and retire a term. Companions carry the lifecycle table, the semantic density measure, and the vocabulary search order.
- `ontology/rune.ttl` gains `rune:Proof`, `rune:proves`, the receipt fields (`configurationDigest`, `validatorVersion`, `exitStatus`), and the `rune:proofKinds` scheme with `checks` and `behavior`.
- `ontology/shapes.ttl` gains the proof-covers-a-candidate shape at Warning severity, and the smoke fixture gains the orphan proof it reports.
- DECK-0014 records the decision.

## Capabilities

- agentic-ontology-stack (new)

## Impact

- `runes/core/skills/AgenticOntology/` (new).
- `ontology/rune.ttl`, `ontology/shapes.ttl`, `ontology/smoke/instances.ttl`.
- `.pre-commit-config.yaml`: the shapes smoke hook asserts four Violations and thirteen Warnings.
- `docs/decisions/`: DECK-0014.
