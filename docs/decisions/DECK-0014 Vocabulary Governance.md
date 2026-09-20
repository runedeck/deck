---
title: "Vocabulary Governance"
description: "One skill governs the deck's vocabulary: a term enters the ontology before prose uses it, an artifact takes its name from its lifecycle stage, and the prove stage gets its evidence class"
type: adr
category: architecture
tags:
    - ontology
    - naming
    - evidence
status: accepted
created: 2026-09-15
updated: 2026-09-15
author: "@N4M3Z"
project: deck
related:
    - "DECK-0010 Declared World in RDF"
    - "DECK-0013 Local Checks Before Publication"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5-1"]
informed: []
upstream: []
change: agentic-ontology-stack
---

# Vocabulary Governance

## Context and Problem Statement

DECK-0010 declared the deck's world in RDF and made a decision record the price of a new class. It did not say who admits a term, how an artifact gets its name, or what happens when the corpus drifts. Naming the prove-stage skill on 2026-09-15 took a survey of agent-skill catalogs, CI vendors, philosophy, and governance vocabularies before the answer came from the deck's own lifecycle scheme, which already names the stage. The same session found four words for one prove-stage record: receipt, proof, attestation, evidence. The ontology has a class for measure-stage evidence, `rune:Verdict`, and none for the prove stage.

## Decision Drivers

- A term used in prose before it exists in the ontology is a synonym waiting to happen.
- An artifact named by taste is renamed later. A name derived from the stage table is stable.
- A rule or skill is paid for on every turn, and a vocabulary at density one is what keeps it short.
- The prove stage produces evidence that nothing in the graph can hold.

## Considered Options

1. A skill, AgenticOntology, that owns admission, naming, drift audit, and retirement, plus `rune:Proof` as the prove-stage evidence class with a shape.
2. A naming rule alone, loaded on every turn, with the ontology untouched.
3. Keep naming ad hoc and add classes when a change needs one.

## Decision Outcome

Chosen option: the skill and the class.

AgenticOntology routes four acts. Admit a term: corpus search, established-vocabulary search in a fixed order, then mint with a superclass, a Warning shape, and a seeded smoke instance. Name an artifact: stage verb or discipline noun plus the entity the stage consumes. Audit drift: synonyms per label and labels per word, reported as a density with the target one. Retire a term: deprecate, alternative label for one release, remove. The lifecycle table, the density measure, and the vocabulary search order are companions.

`rune:Proof` is a `prov:Entity` that `proves` a candidate commit and carries one `proofKind` from a SKOS scheme, with `checks` and `behavior` as the first kinds. A candidate is proven when a proof exists for its commit, a query and not a stored state. The ContinuousIntegration receipt is the first Proof.

Option 2 puts the rule in every context window and still leaves the ontology behind the prose. Option 3 is the state this decision replaces.

## Consequences

- A new concept costs one ontology edit and one shape before it costs any prose.
- The density audit is manual until the extractor computes it, which is a recorded follow-up.
- The skill names `rudof` and `rg`. A checkout without rudof cannot run the shape check, and the hook says so under `REQUIRE_GATES`.
- The smoke fixture states four Violations and thirteen Warnings, and the hook asserts those counts. A missing property that a shape also constrains by value reports twice, which the fixture comment states. The permitted proof kinds are enumerated in the shape, because the hook validates the instance graph without the ontology loaded.
