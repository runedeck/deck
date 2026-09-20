# proton

## Description

Two skills for operating Proton Mail from an agent session while the mail stays on Proton's own model.

- `ProtonMail` teaches an opencode session on a Lumo model to read, search, and sort the mailbox through the `mail_*` tools of a local mail connector plugin.
- `ProtonMailBoundary` tells a Claude Code session that mailbox work does not belong there, hands off to the opencode mail project, and asks before it touches pasted mail.

The boundary skill is advisory. It warns and asks. It does not block a tool call.

## Compatibility

- `ProtonMail` deploys to opencode only. It needs Proton Mail Bridge and a mail connector plugin with the `mail_*` tools, registered in the project `opencode.json`.
- `ProtonMailBoundary` deploys to Claude Code only.

## Installation

Select the domain in the consumer's `.rune` file, then run `rune install` from the mail project.

## Usage

Open the mail project with `opencode` and ask about the inbox. Mutations ask for permission in the interactive session. `opencode run` is for read-only questions.

## Requirements

- [rune-cli](https://github.com/runedeck/rune)
- [Proton Mail Bridge](https://proton.me/mail/bridge)

## License

[EUPL-1.2](LICENSE)
