## ADDED Requirements

### Requirement: Agent declares each secret

The deck MUST hold a rule about secrets. The rule MUST tell an agent to declare every secret a repository reads in that repository's secret declaration, with a description of its purpose.

#### Scenario: Script needs a new token

- **WHEN** an agent adds a script that reads a token the repository did not use before
- **THEN** the agent adds the token to the repository's secret declaration with a description

### Requirement: Secret values stay out of the conversation

The rule MUST tell an agent to read a secret only through the secret manager. It MUST forbid printing a value or reading one into the conversation. It MUST tell the agent to pass a value to a program on stdin and to give every read a reason.

#### Scenario: Command needs a credential

- **WHEN** an agent runs a command that needs a credential
- **THEN** the agent runs the command under the secret manager and reports only its result
- **AND** no credential value appears in the transcript or in a process argument
