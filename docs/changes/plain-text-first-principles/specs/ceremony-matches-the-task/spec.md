## ADDED Requirements

### Requirement: Ceremony Matches The Task

The weight of the process MUST match the size of the task. A fix that *[changes][CHANGE]* no requirement takes a plain commit. A behavior [change][CHANGE] takes a [change][CHANGE] directory, and a decision with alternatives takes a record. Unneeded ceremony is complexity, and we remove it.

#### Scenario: Small fix arrives with full ceremony

- **WHEN** a [change][CHANGE] directory contains only a fix that alters no requirement
- **THEN** review turns it into a plain commit and removes the directory

### Requirement: A Check Challenges The Small Mark

The author marks a commit as small. The *[validator][VALIDATOR]* MUST challenge that mark whenever the commit touches anything that defines behavior. The author then takes the full process, or overrides the challenge with a reason.

#### Scenario: Small mark touches a specification

- **WHEN** a commit marked small touches a specification, the ontology, a decision record, or a test's expected result
- **THEN** the [validator][VALIDATOR] challenges the mark, and the author takes the full process or overrides the challenge with a reason

### Requirement: Semantic Density

A line an *[instruction][INSTRUCTION]* loads into a *[model][MODEL]*'s context MUST state a fact, a constraint, or an action.
A line the [model][MODEL] could drop without losing anything is filler. Filler that stays in context costs tokens on every turn.

#### Scenario: Filler enters an instruction

- **WHEN** an [instruction][INSTRUCTION] gains a sentence that states no fact, constraint, or action
- **THEN** the prose *[analysis tool][ANALYSISTOOL]* reports it, and the author removes the sentence

### Requirement: Verbs Name Actions

A heading, a step, or the name of an action MUST use a verb. A noun made from a verb MUST NOT name an action.
Write `accepting a specification`, not `specification acceptance`, and `exploring a decision`, not `decision exploration`.

#### Scenario: Nominalization enters a heading

- **WHEN** a heading or step describes an action as a noun phrase
- **THEN** the prose [analysis tool][ANALYSISTOOL] reports it, and the author rewrites it with the verb

[CHANGE]: ../../../../specs/glossary/change.md
[VALIDATOR]: ../../../../specs/glossary/validator.md
[INSTRUCTION]: ../../../../specs/glossary/instruction.md
[MODEL]: ../../../../specs/glossary/model.md
[ANALYSISTOOL]: ../../../../specs/glossary/analysis-tool.md
