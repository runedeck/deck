## ADDED Requirements

### Requirement: Mail content stays on an accepted model

The ProtonMail skill MUST keep subjects, senders, and bodies inside its session. It MUST NOT write them to a file or a note, and MUST NOT hand them to a model outside Proton Lumo and the local model servers.

#### Scenario: User asks for a summary file

- **WHEN** the user asks the session to save message subjects to a file
- **THEN** the session declines and answers in the conversation only

### Requirement: Mutations stay behind the permission prompt

Every mutating tool MUST ask the user for permission. When nobody answers the prompt, the skill MUST stop, MUST NOT retry, and MUST NOT split the call to get past the prompt.

#### Scenario: Mutation runs without an interactive user

- **WHEN** a mutating tool fails with a rejected permission under a non-interactive run
- **THEN** the session reports what it found and the exact call it tried, and makes no further attempt

### Requirement: Nothing is deleted permanently

The ProtonMail skill MUST move a message to Trash and MUST NOT look for a delete or an empty-trash operation.

#### Scenario: User asks to delete messages

- **WHEN** the user asks to delete a set of messages
- **THEN** the session moves them to Trash and says that a move out of Trash restores them

### Requirement: Other sessions hand mailbox work off

The ProtonMailBoundary skill MUST NOT install, configure, or call mailbox tools. It MUST hand a mailbox request off to the mail project. It MUST warn once and ask before it processes pasted mail content.

#### Scenario: Mailbox question reaches a hosted-model session

- **WHEN** the user asks a hosted-model session about their inbox
- **THEN** the session names the mail project, gives the command to open it, and stops

#### Scenario: User pastes a mail body

- **WHEN** the user pastes mail content and asks for work on it
- **THEN** the session warns once, asks whether to continue, and proceeds only on a clear yes
