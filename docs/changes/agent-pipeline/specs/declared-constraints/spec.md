## ADDED Requirements

### Requirement: Agents propose, the ontology permits

The stack MUST separate proposal from permission. An agent proposes what is likely; a declared ontology states what is permitted; a deterministic checker decides. A proposal that names an entity MUST be verifiable against the declared world: hallucinated artifacts, stages, or relations fail the check instead of entering the record.

#### Scenario: A proposal references an artifact that does not exist

- **WHEN** a scaffolded change references a rune, capability, or decision record absent from the declared world
- **THEN** a deterministic check fails and names the missing entity

### Requirement: The ontology reuses existing vocabularies

The declared ontology MUST reuse established vocabularies before inventing terms: schema.org, Dublin Core, SKOS, FOAF, and domain vocabularies where they fit. New terms enter only for stack concepts no public vocabulary covers, and each new term carries a definition.

#### Scenario: A metadata field has a public equivalent

- **WHEN** a new artifact field duplicates a Dublin Core or schema.org term
- **THEN** the ontology maps to the public term instead of minting one

### Requirement: Lifecycle constraints become machine-checkable rules

Evidence-token rules MUST be expressible as declared constraints over the artifact graph, in the style of description-logic axioms: a rule ships only with a bench verdict, an adopted artifact carries exactly one sealed review, a retirement keeps its evidence. Inference suggests; constraints reject. Checkers built on the declarations replace folklore gates.

#### Scenario: A rule ships without a verdict

- **WHEN** the artifact graph shows a rule deployed with no bench verdict linked
- **THEN** the constraint checker reports the violation without any agent judgment

#### Scenario: A one-time property is asserted twice

- **WHEN** a functional property (one sealed review per adoption) receives a second assertion
- **THEN** the checker rejects the second assertion
