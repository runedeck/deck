## ADDED Requirements

### Requirement: Term links in a skill bundle resolve after deployment

A term definition in a skill file MUST point at the term's glossary page by the page's repository URL, and MUST NOT point at it by a relative path that leaves the skill directory. The term link itself, the tag, and the emphasized first use stay as the ontology rule prescribes. A term link MUST NOT be removed to satisfy the source-layer check.

#### Scenario: Skill links a term by relative path

- **WHEN** a skill file defines a term tag with a relative path into the glossary directory
- **THEN** the source-layer check reports the path as leaving the bundle
- **AND** the author rewrites the definition to the repository URL of the same page

#### Scenario: Skill links a term by repository URL

- **WHEN** a skill file defines a term tag with the repository URL of its glossary page
- **THEN** the source-layer check passes the reference as external
- **AND** the term fixer leaves the definition unchanged
