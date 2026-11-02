---
mode: append
compatibility: "Asks through AskUserQuestion. Workflow children cannot ask and therefore never run this skill."
---

## Claude Code

Ask with the `AskUserQuestion` tool. One call takes up to four questions, so eight questions go out as two calls of four, and the second call waits for the first call's answers. Map each card onto one question: the full question in `question`, the topic label in `header` (at most twelve characters), and two to four `options`, each with a `label` and a one-line `description` of what it changes. Put the recommended option first with `(Recommended)` at the end of its `label`. Set `multiSelect` only when the options do not exclude each other. The tool adds `Other` for the owner's own words, so do not add an option for it.
