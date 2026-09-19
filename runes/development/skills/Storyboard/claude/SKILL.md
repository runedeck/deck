---
mode: append
compatibility: "Asks through AskUserQuestion. Workflow children cannot ask and therefore never run this skill."
---

## Claude Code

Ask the confirmation question with the `AskUserQuestion` tool, one question, three options in this order: confirm, edit a box, stop. Put the frame in the question text inside a `text` fence so the owner sees it beside the options. A free-text answer counts as edit a box.
