# Vocabularies

The search order before minting a term, from DECK-0010: reuse an established term when one fits, and mint only with a superclass in one of these.

## Search order

- **PROV-O** (`prov:`), for an artifact, an activity, a person or a model: `prov:Entity`, `prov:Activity`, `prov:Agent`, and derivation with `prov:wasDerivedFrom`, `prov:wasGeneratedBy`, `prov:wasAttributedTo`.
- **SKOS** (`skos:`), for a controlled list of values: `skos:ConceptScheme` and `skos:Concept` for stages and kinds of proof, `skos:altLabel` for a retired label.
- **Dublin Core terms** (`dcterms:`), for generic metadata: `dcterms:identifier`, `dcterms:title`, `dcterms:relation`, `dcterms:creator`.
- **schema.org** (`schema:`), for a document or a procedure: `schema:CreativeWork`, `schema:HowTo`.
- **SHACL** (`sh:`), for a constraint: every shape in `shapes.ttl`, never a constraint in `rune.ttl`.
- **in-toto and SLSA**, for a supply-chain attestation: the `.provenance/` sidecars. A `rune:Proof` is the deck-side twin of an in-toto attestation, not a replacement.
- **OWL and RDFS** (`owl:`, `rdfs:`), for a class definition or a deprecation: `rdfs:subClassOf`, `rdfs:label`, `rdfs:comment`, `owl:deprecated`.

## Rules of reuse

- Reuse the established IRI, never a copy of it under `rune:`.
- A minted class declares `rdfs:subClassOf` to an established class. A minted scheme is a `skos:ConceptScheme` and its members are `skos:Concept`.
- OWL and RDFS describe under the open-world assumption and never reject data. SHACL validates under the closed-world assumption and is the only gate.
- The product namespace is `https://runedeck.dev/ns#`. Entities live under `https://runedeck.dev/id/`. A namespace is permanent.

## Where the deck already reuses

`rune:Rune` is a `prov:Entity` and a `schema:CreativeWork`. `rune:Skill` is a `schema:HowTo`. `rune:Provider` is a `prov:Agent`. `rune:Verdict` and `rune:Proof` are `prov:Entity`. `rune:Stage` and `rune:ProofKind` are `skos:Concept`. A decision record is a `prov:Entity` and a `schema:CreativeWork`, minted because no established vocabulary covers architecture decision records.
