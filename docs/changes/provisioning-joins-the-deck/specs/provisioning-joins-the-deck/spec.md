## ADDED Requirements

### Requirement: Provisioning Runes Share One Module

The *[deck][DECK]* MUST keep every provisioning *[rune][RUNE]* in one *[module][MODULE]* called `provisioning`. The module contains *[skills][SKILL]* and *[rules][RULE]* only. Scripts, package lists, and install steps stay outside it, so reading the module cannot change a machine.

#### Scenario: Machine setup skill joins the deck

- **WHEN** a change adds a skill about setting up a machine
- **THEN** the skill is in the provisioning module, and no other module contains a copy

### Requirement: The Validator Rejects Executable Files in the Module

The *[validator][VALIDATOR]* MUST report every executable file in the provisioning module as an error. An executable file has an execute permission, or its first line calls an interpreter. Scripts that change a machine belong to the provisioning codebase, which the deck never deploys.

#### Scenario: Install script enters the module

- **WHEN** a change adds a shell script under the provisioning module
- **THEN** the validator reports the file, and the change fails its checks

### Requirement: The Default Deployment Omits the Module

The *[deployer][DEPLOYER]* MUST NOT deploy the provisioning module when a consumer selects every module of the deck. A consumer receives provisioning runes only after it selects the module by its name. A machine gets setup instructions only on its owner's request.

#### Scenario: Consumer installs the whole deck

- **WHEN** a consumer selects every module of the deck
- **THEN** the deployer leaves every *[harness][HARNESS]* tree without a provisioning rune

### Requirement: A Provisioning Rune Shows That It Helps

The *[archiver][ARCHIVER]* MUST refuse a change that adds or rewrites a provisioning rune without a recorded comparison. The comparison runs the same cases with the rune and without it on at least two *[models][MODEL]*. It shows that at least one model answers at least one case correctly only when the rune is present. A rune that leaves every answer unchanged repeats what the models already know.

#### Scenario: Rune arrives without a comparison

- **WHEN** a change adds a provisioning rune and its change directory contains no comparison
- **THEN** the archiver refuses the change and reports the rune that lacks the comparison

### Requirement: Provisioning Runes Point at Scripts Inside the Provisioning Codebase

A provisioning rune that tells the model to run a script MUST give the script's path inside the provisioning codebase. The module's defaults MUST give the location of that codebase on the machine. A deployed rune then resolves the path in every harness tree, and no link points back into the deck.

#### Scenario: Deployed skill points at an install script

- **WHEN** the model reads a deployed provisioning skill that points at a script
- **THEN** the path resolves against the codebase location from the module's defaults

### Requirement: Provisioning Runes Contain No Personal Data

A provisioning rune MUST NOT contain a personal name, an email address, a host name, an account name, or a secret. The owner's own configuration keeps those values. The deck is public, and every consumer reads the same text.

#### Scenario: Skill contains the owner's host name

- **WHEN** a change adds a provisioning rune that contains the host name of the owner's machine
- **THEN** review rejects the change before it merges

[DECK]: ../../../../specs/glossary/deck.md
[RUNE]: ../../../../specs/glossary/rune.md
[MODULE]: ../../../../specs/glossary/module.md
[SKILL]: ../../../../specs/glossary/skill.md
[RULE]: ../../../../specs/glossary/rule.md
[VALIDATOR]: ../../../../specs/glossary/validator.md
[DEPLOYER]: ../../../../specs/glossary/deployer.md
[HARNESS]: ../../../../specs/glossary/harness.md
[ARCHIVER]: ../../../../specs/glossary/archiver.md
[MODEL]: ../../../../specs/glossary/model.md
