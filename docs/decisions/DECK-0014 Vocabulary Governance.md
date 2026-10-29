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
updated: 2026-10-19
author: "@N4M3Z"
project: deck
related:
    - "DECK-0010 Declared World in RDF"
    - "DECK-0013 Local Checks Before Publication"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5-1@claude"]
informed: []
upstream: []
change: terms-enter-ontology-first
---

# Vocabulary Governance

## Context and Problem Statement

DECK-0010 declared the world of the *[repository][REPOSITORY]* in RDF (the Resource Description Framework) and made a *[decision record][DECISIONRECORD]* the price of a new class. It did not say who admits a term, how an *[artifact][ARTIFACT]* gets its name, or what happens when the corpus drifts.

On 2026-09-15 a search looked for the name of the prove-stage *[skill][SKILL]*. The search went through catalogs of agent [skills][SKILL], continuous integration (CI) vendors, philosophy, and governance vocabularies. The answer came from the [repository][REPOSITORY]'s own lifecycle scheme, which already states the stage name. The same session found four words for one prove-stage record: receipt, *[proof][PROOF]*, *[attestation][ATTESTATION]*, evidence. The ontology has a class for measure-stage evidence, `rune:Verdict`, and none for the prove stage.

## Decision Drivers

- A term that prose uses before the ontology defines it invites a synonym. The next author picks another word for the same thing.
- An [artifact][ARTIFACT] that the author names by taste gets renamed later. A name derived from the stage table is stable.
- The owner pays for a *[rule][RULE]* or a [skill][SKILL] on every turn. A vocabulary at density one, one word for each concept, shortens the [rule][RULE] or the [skill][SKILL].
- The prove stage produces evidence, and no class in the graph can store it.

## Considered Options

1. A [skill][SKILL], AgenticOntology, owns admission, naming, drift audit, and retirement. The class `rune:Proof` with its shape stores the prove-stage evidence.
2. The owner adds a naming [rule][RULE] alone, loaded on every turn, and leaves the ontology untouched.
3. The owner keeps naming ad hoc and adds a class when a *[change][CHANGE]* needs one.

## Decision Outcome

Chosen option: the [skill][SKILL] and the class.

AgenticOntology routes four acts. To admit a term, the author searches the corpus and then the established vocabularies in a fixed order. The author then creates the term with a superclass, a Warning shape, and a seeded smoke instance. To name an [artifact][ARTIFACT], the author joins the stage verb or the discipline noun to the entity the stage consumes. To audit drift, the [skill][SKILL] counts synonyms per label and labels per word and reports the result as a density, with a target of one. To retire a term, the author deprecates it, keeps an alternative label for one release, and then removes it.

The lifecycle table, the density measure, and the vocabulary search order are *[companions][COMPANION]* of the [skill][SKILL].

`rune:Proof` is a `prov:Entity`. It `proves` a candidate commit and has one `proofKind` from a SKOS (Simple Knowledge Organization System) scheme. The first kinds are `checks` and `behavior`. A candidate counts as proven when a [proof][PROOF] exists for its commit. A query answers that question, and no stored state does. The ContinuousIntegration receipt is the first [Proof][PROOF].

Option 2 puts the [rule][RULE] in every context window and still leaves the ontology behind the prose. Option 3 is the state this decision replaces.

### Consequences

- [-] The author pays for a new concept with one ontology edit and one shape before writing any prose.
- [-] The owner runs the density audit by hand until the extractor computes it. That extractor is a recorded follow-up.
- [-] The [skill][SKILL] names two tools, `rudof` and `rg`. A checkout without rudof cannot run the shape check. The hook reports that under `REQUIRE_GATES`.
- [-] The smoke *[fixture][FIXTURE]* states four Violations and thirteen Warnings, and the hook asserts those counts. A missing property that a shape also constrains by value reports twice. The [fixture][FIXTURE] comment says so. The shape lists the permitted [proof][PROOF] kinds, because the hook validates the instance graph without the ontology loaded.

## More Information

- Rewritten on 2026-10-19 in the plain spoken register. The decision is unchanged.

[REPOSITORY]: ../specs/glossary/repository.md
[DECISIONRECORD]: ../specs/glossary/decision-record.md
[ARTIFACT]: ../specs/glossary/artifact.md
[SKILL]: ../specs/glossary/skill.md
[COMPANION]: ../specs/glossary/companion.md
[PROOF]: ../specs/glossary/proof.md
[FIXTURE]: ../specs/glossary/fixture.md
[RULE]: ../specs/glossary/rule.md
[CHANGE]: ../specs/glossary/change.md
[ATTESTATION]: ../specs/glossary/attestation.md
