---
title: Declared Constraints over Proposed Changes
description: Agents propose what is likely, a declared ontology states what is permitted, and deterministic checkers decide
type: adr
category: architecture
tags:
    - architecture
    - ontology
    - verification
status: proposed
created: 2026-08-19
updated: 2026-08-19
author: "@N4M3Z"
project: deck
related:
    - "DECK-0005 Artifact Lifecycle and Evidence Tokens"
    - "DECK-0008 Idea-to-Merge Flywheel"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: []
informed: []
upstream: []
---

# Declared Constraints over Proposed Changes

## Context and Problem Statement

Agents hallucinate entities and then everyone verifies by hand. Comments go out of date, documentation duplicates code, and unmeasured Markdown sits in every context window. The stack already has the primitive answer — mdschema constrains structure, JSON schemas constrain fields, the ceremony constrains process — but the constraints stop at single files. Nothing declares the permitted relations between artifacts, stages, and evidence, so lifecycle rules like "a rule ships only with a bench verdict" live as folklore that only review rounds enforce.

## Decision Drivers

- The neurosymbolic split is the right division of labor: probabilistic agents propose, symbolic declarations permit, deterministic checkers decide.
- Code is truth; prose drifts. A constraint written as prose decays, and the same constraint written as a checkable declaration does not.
- Public vocabularies (schema.org, Dublin Core, SKOS, FOAF) already name most metadata concepts; inventing parallel terms creates translation debt.
- Inference and constraint are different tools: one suggests missing facts, the other rejects invalid states. The stack needs the rejecting kind first.
- Every checker added below review (the leverage ladder's lint rung) removes a class of review rounds.

## Considered Options

1. **Prose contracts only** — keep lifecycle rules in specifications and enforce them in review.
2. **Full semantic-web stack now** — RDF store, OWL ontology, reasoner, from day one.
3. **Declared constraints, grown from existing schemas** — state the artifact graph and its axioms in the deck, map metadata to public vocabularies, and build small deterministic checkers per constraint; adopt heavier reasoning only when a constraint needs it.

## Decision Outcome

Option 3. The deck declares its world: artifact kinds, lifecycle stages, evidence tokens, and the permitted relations between them, reusing public vocabulary terms where they exist. Lifecycle rules become axioms in the description-logic style — functional properties for one-time facts, domain and range for who may hold what — and each axiom gets a deterministic checker. Proposals that name entities are verified against the declared world, so a hallucinated reference fails a check instead of surviving until review. The existing schemas remain the ontology's first layer; the graph layer grows from them without a platform rewrite.

## Consequences

- The evidence-token gates from DECK-0005 acquire an enforcement mechanism that is neither prose nor review labor.
- Intake pushback gains a deterministic ground: an idea referencing nonexistent capabilities is rejected by check, not by argument.
- The vocabulary mapping keeps deck metadata legible to external tooling at near-zero cost.
- The heavier machinery (RDF serialization, OWL reasoners) stays optional until a constraint demonstrably needs inference, which keeps complexity matched to the task.
