## ADDED Requirements

### Requirement: Ceremony Matches The Task

The weight of the process MUST match the size of the task.
A fix that changes no requirement takes a plain commit. A behavior change takes a change directory. A decision with alternatives takes a record.
Ceremony the task does not need is complexity, and we remove it.

#### Scenario: Small fix arrives with full ceremony

- **WHEN** a change directory contains only a fix that alters no requirement
- **THEN** review turns it into a plain commit and removes the directory

### Requirement: Semantic Density

A line an instruction loads into a model's context MUST state a fact, a constraint, or an action.
A line the model could drop without losing anything is filler. Filler that stays in context costs tokens on every turn.

#### Scenario: Filler enters an instruction

- **WHEN** an instruction gains a sentence that states no fact, constraint, or action
- **THEN** the prose analysis tool reports it, and the author removes the sentence

### Requirement: Verbs Name Actions

A heading, a step, or the name of an action MUST use a verb, not a noun made from one.
Write `accepting a specification`, not `specification acceptance`, and `exploring a decision`, not `decision exploration`.

#### Scenario: Nominalization enters a heading

- **WHEN** a heading or step describes an action as a noun phrase
- **THEN** the prose analysis tool reports it, and the author rewrites it with the verb
