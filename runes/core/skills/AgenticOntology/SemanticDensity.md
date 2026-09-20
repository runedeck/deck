# Semantic density

The measure the drift audit reports. It answers one question about a vocabulary: does each word carry exactly one meaning, and does each meaning have exactly one word?

## Definition

For a corpus and an ontology:

- A **label** is an `rdfs:label` or `skos:prefLabel` in `rune.ttl`.
- A **term** is a word or short phrase the corpus uses as a name for a concept: it appears in backticks, in a heading, in a frontmatter field, or capitalized as a proper noun.
- The **density** of a label is the number of concepts it names in the corpus. The target is one.
- The **density** of a concept is the number of terms the corpus uses for it. The target is one.

A label with density above one is **overloaded**: one word, several meanings. `verdict` would be overloaded if the bench verdict and a review verdict both used it. A concept with density above one is **diluted**: several words, one meaning. `receipt`, `proof`, `attestation`, and `evidence` naming the same prove-stage record is dilution.

## Procedure

1. List the labels: `rg -o 'rdfs:label "[^"]+"|skos:prefLabel "[^"]+"' ontology/rune.ttl`.
2. For each label, count distinct meanings in the corpus. Read the sentences `rg -n -w '<label>' docs runes --glob '!.workspaces'` returns and group them by meaning.
3. For each concept, list the terms the corpus uses for it. Start from the label's `rdfs:comment` and search for the nouns it contains.
4. Report a table: concept, surviving label, other terms found, files.

## Why density matters for an agent

A rule or a skill sits in context on every turn, so every word in it is paid for repeatedly. A vocabulary with density one lets an instruction say `Proof` and mean one thing in every harness, so the instruction can be short. A diluted vocabulary forces every instruction to list the synonyms or risk being read as naming something else, and an overloaded one forces qualifiers on every use. The shortest exact instruction set is the one written against a vocabulary at density one.

The same holds for the model reading a diagnostic. A CLI error that says `proof` when the skill said `receipt` costs a turn of reconciliation. Density one is what makes the ontology, the skill text, and the tool output one language.

## Limits

The count is by hand. The procedure gives the searches and the grouping rule, and a person or an agent does the grouping. No tool computes density from the corpus yet. The follow-up in the agentic-ontology-stack tasks names the extractor as the place that could.
