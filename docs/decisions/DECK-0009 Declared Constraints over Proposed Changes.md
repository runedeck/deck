---
title: Declared Constraints over Proposed Changes
description: Agents propose what is likely, a declared ontology states what is permitted, and deterministic checkers decide
type: adr
category: architecture
tags:
    - architecture
    - ontology
    - verification
status: accepted
created: 2026-08-19
updated: 2026-10-19
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
change: agentic-first-pipeline-rules
---

# Declared Constraints over Proposed Changes

## Context and Problem Statement

A *[model][MODEL]* hallucinates an entity, and then a person verifies every reference by hand. Comments go out of date. Documentation duplicates code. Unmeasured Markdown sits in every context window.

The stack already has the basic answer. The *[structure schema][STRUCTURESCHEMA]* constrains the structure of a file, a JSON schema constrains its fields, and the ceremony constrains the process. But those constraints stop at single files. No declaration states the permitted relations between *[artifacts][ARTIFACT]*, their stages, and evidence. A stage constraint such as "a *[rule][RULE]* enters the *[deck][DECK]* only with a bench *[verdict][VERDICT]*" therefore lives as folklore. Only a review round enforces it.

## Decision Drivers

- The neurosymbolic split is the right division of labor. A probabilistic [model][MODEL] proposes, a symbolic declaration permits, and a deterministic checker decides.
- A constraint written as prose decays. The same constraint written as a checkable declaration does not.
- Public vocabularies already name most metadata concepts: schema.org, Dublin Core, SKOS (the Simple Knowledge Organization System), and FOAF (Friend of a Friend). An invented parallel term creates translation debt.
- Inference and constraint are different tools. Inference suggests a missing fact, and a constraint rejects an invalid state. The stack needs the rejecting kind first.
- Every checker the owner adds below review, on the lint rung of the ladder, removes a class of review rounds.

## Considered Options

1. **Prose contracts only**: the owner keeps stage constraints in specifications, and a reviewer enforces them in review.
2. **Full semantic-web stack now**: an RDF (Resource Description Framework) store, an OWL (Web Ontology Language) ontology, and a reasoner, from day one.
3. **Declared constraints, grown from existing schemas**: the owner states the [artifact][ARTIFACT] graph and its axioms in the *[repository][REPOSITORY]* and maps the metadata to public vocabularies. Each constraint gets a small deterministic checker. The owner adopts heavier reasoning only when a constraint needs it.

## Decision Outcome

Option 3. The [repository][REPOSITORY] declares its world. The declaration lists the [artifact][ARTIFACT] kinds, their stages, the evidence tokens, and the permitted relations between them. It reuses a public vocabulary term where one exists. Each stage constraint becomes an axiom in the description-logic style. A functional property states a one-time fact, and a domain and a range state who may hold what.

Each axiom gets a deterministic checker. A deterministic check verifies every named entity in a proposal against the declared world. A hallucinated reference therefore fails a check instead of surviving until review. The existing schemas remain the ontology's first layer. The graph layer grows from them without a platform rewrite.

### Consequences

- [+] The evidence-token conditions from [DECK-0005](DECK-0005%20Artifact%20Lifecycle%20and%20Evidence%20Tokens.md) get an enforcement mechanism that is neither prose nor review labor.
- [+] Intake pushback gains a deterministic ground. A check rejects an *[idea][IDEA]* that references a *[capability][CAPABILITY]* that does not exist, and nobody has to argue the point.
- [+] The vocabulary mapping lets external tooling read the [repository][REPOSITORY]'s metadata at low cost.
- [+] The heavier machinery, RDF serialization and OWL reasoners, remains optional until a constraint needs inference. Complexity then matches the task.

## More Information

- Rewritten on 2026-10-19 in the plain spoken register. The decision is unchanged.

[STRUCTURESCHEMA]: ../specs/glossary/structure-schema.md
[MODEL]: ../specs/glossary/model.md
[ARTIFACT]: ../specs/glossary/artifact.md
[DECK]: ../specs/glossary/deck.md
[VERDICT]: ../specs/glossary/verdict.md
[REPOSITORY]: ../specs/glossary/repository.md
[RULE]: ../specs/glossary/rule.md
[IDEA]: ../specs/glossary/idea.md
[CAPABILITY]: ../specs/glossary/capability.md
