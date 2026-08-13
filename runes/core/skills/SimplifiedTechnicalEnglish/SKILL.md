---
name: SimplifiedTechnicalEnglish
description: "Write or rewrite prose as Simplified Technical English (ASD-STE100). USE WHEN deslop a text, STE rewrite, simplified technical english, plain-language rewrite, controlled-language rewrite, make docs read human, remove AI slop, review text for STE violations, write error messages, tool descriptions, or agent instructions that cannot be misread. NOT FOR code, identifiers, command syntax, or creative and marketing copy where voice is the point."
metadata:
    version: 0.1.0
    spec: ASD-STE100 Issue 9 (January 2025)
allowed-tools: Bash(python3 *), Read, Write, Edit, Grep, Glob
---

# SimplifiedTechnicalEnglish

Write prose that one reading cannot misread. ASD-STE100 is the aerospace controlled-language standard that stops a technician with basic English from misreading a maintenance instruction. The same discipline stops an AI agent, a translation layer, or a tired reviewer from misparsing your text. It applies to documentation, READMEs, pull-request text, commit messages, error messages, release notes, comments, tool descriptions, and agent-to-agent messages. It never applies to code, identifiers, or command syntax.

Three ways to use it: **write** new text in STE, **rewrite** existing text and keep every fact, or **review** without a rewrite, one violation for each row.

## Prerequisites

Pick a mode before you write. When the user does not say which, infer it from the text type.

- **Strict**: procedures, runbooks, error messages, tool and function descriptions, inter-agent instructions, safety text. Apply every rule and the two length caps.
- **STE-flavored**: READMEs, PR descriptions, changelogs, explanatory prose. Apply the structural rules in full. Treat the dictionary rules as a direction of travel, because prose needs some range.

## Constraints

Structural rules, numbered per ASD-STE100 Issue 9:

- Use the active voice. Passive is correct only when the actor is unknown or irrelevant (3.6). A past participle used as an adjective is not passive (3.3): `the field is required` is correct.
- Use simple tenses only (3.2): no present perfect, no stacked auxiliaries (3.4), no `-ing` main verb where a simple tense works (3.5).
- Write one instruction for each sentence (5.2). Instructions stay within 20 words (5.1) and descriptive sentences within 25 (6.3).
- Put a comma between a condition and its command (5.4): `If the test fails, read the log.`
- Do not drop words to compress (4.2): `Remove the bolts from the panel`, never `Remove bolts from panel`. Do not use contractions.
- Use a verb for an action (3.7): `analyze the log`, not `perform an analysis of the log`.
- Do not use phrasal verbs (9.3): write `start`, not `spin up`, and `contact`, not `reach out`.
- Do not use semicolons (8.1). Every other standard mark is permitted. Keep multi-word nouns within three words (2.1). Write one topic for each paragraph (6.5), at most six sentences (6.6).
- Use one name for one thing (1.11, 9.4). Pick one verb for one action and reuse it. Never rotate `check`, `verify`, and `confirm`.
- Use the short common word: `use`, not `utilize` or `leverage`, and `before`, not `prior to`. Do not use marketing adjectives. [references/recurring-errors.md](references/recurring-errors.md) carries the standard's own list of the most frequent writer errors.

Guards that outrank every rule above:

- Never drop a fact, number, condition, hedge, or scope qualifier to satisfy a length cap. Keep the longer sentence and flag it.
- Modality is content. `May have failed` never becomes `failed`. When the tense rule and the modality rule conflict, modality wins.
- Never add a cause, frequency, or mechanism that the source did not state. That is a different claim, not a rewrite.
- Keep code identifiers, part numbers, units, error strings, and safety wording exact.
- Change the smallest span that repairs a violation. If the input already complies, return it unchanged and say so.
- This skill repairs the form of a text, not its substance. A hollow paragraph rewritten under these rules is still hollow. Say so instead of polishing it.
- The official dictionary of approximately 900 words is not reproduced here, because ASD restricts redistribution. Apply its principle and do not claim dictionary compliance.

## Instructions

### Rewrite or write

Read the input once for meaning before you change anything. Walk it sentence by sentence, flag each violation, and rewrite the flagged spans with the meaning kept exact. Output the finished text alone: no preamble, no mode announcement, no summary of changes. When you keep a longer phrasing on purpose, add one line with the prefix `Kept as-is:` that names the phrase and the precision it protects.

### Review

On a review request (`show the diff`, `which rules did it break`, `before/after`), output a table with one row per violation, `Rule | Original | Simplified`. Then add one line on anything you left alone and why.

### Lint

When commands are available, lint the draft with the bundled checker. Repair the reported categories and lint again, at most two passes:

```sh
# <skill-dir> is this skill's directory; the draft path is your own.
python3 <skill-dir>/scripts/ste-lint.py <draft>            # flavored target: under 2.5 per 100 words
python3 <skill-dir>/scripts/ste-lint.py --strict <draft>   # strict target: under 1.5 per 100 words
```

Report the final score with the text. Do not present text as clean without a lint run. Without command access, walk the checklist instead: long sentences, semicolons, contractions, complex tenses, passive with a known actor, nominalizations, phrasal verbs, four-word noun stacks, dropped articles, rotated names.

## Verification

- The lint score meets the mode's target, or each remaining violation is a flagged, deliberate keep.
- Every fact, number, hedge, and qualifier of the source survives in the output.
- The output contains only the requested text.

## References

- [references/writing-rules.md](references/writing-rules.md): the rule categories with citations and the standard's history.
- [references/recurring-errors.md](references/recurring-errors.md): the standard's own 39 most frequent writer errors, with the software-relevant subset.
- [examples/before-after.md](examples/before-after.md): official-rule illustrations and agent-output rewrites, with the reason modality wins.
- [examples/rewrite-samples.md](examples/rewrite-samples.md): measured baseline-versus-STE model outputs with lint scores.
- The full standard is free at [asd-ste100.org](https://www.asd-ste100.org) via the request form. This skill is unofficial and not affiliated with ASD. ASD-STE100 is a registered EU trademark.
