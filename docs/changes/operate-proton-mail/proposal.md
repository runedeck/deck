---
adr: docs/changes/operate-proton-mail/adr.md
status: proposed
decisions: ["Operate Proton Mail on Proton's own model"]
---

# Operate Proton Mail

## Why

Mail content is private. An agent session on a hosted model sends its context to that model's vendor. Mailbox work therefore needs a session whose model the mail owner accepts for mail: a Lumo model or a local model. Other sessions need a rule that stops mailbox work before it starts.

## What Changes

- The `proton` domain at `runes/proton/` with two skills.
- ProtonMail reads, searches, and sorts the mailbox through the `mail_*` tools of a local mail connector plugin over Proton Mail Bridge. It deploys to opencode.
- ProtonMailBoundary hands mailbox requests off to the mail project and asks before it touches pasted mail. It deploys to Claude Code.

## Capabilities

- operate-proton-mail (new)

## Impact

- `runes/proton/` (new). No other file changes.
- The record in `adr.md` moves to `docs/decisions/` at archive.
