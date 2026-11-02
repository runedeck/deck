---
mode: replace
compatibility: "Uses AskUserQuestion. Workflow children cannot ask and never run this skill."
---

# ClarifyTask

Pause before a large or ambiguous task, or whenever the owner asks. Ask only what you cannot learn yourself.
Use question cards instead of a numbered list in the reply. Each card has one question and a few options.
The owner selects an option with one keystroke or answers in their own words.
The owner requested this form on 2026-11-02: eight questions in two sets of four.

## Constraints

- Read the code, docs, configuration, and conversation before asking. Do not ask for an answer those sources contain. Repeating an answered question shows the owner you did not read.
- Ask only questions that change the work. Use a clear, reasonable default when the choice is cheap to reverse. Name that default in the readback.
- Put one question on each card. Name its subject so the card and recorded decision make sense without earlier text.
- Give each card two to four options in plain words. Do not use labels such as "item 3", "batch 2", or "the second approach". Follow the SelfContainedQuestionOptions rule.
- Put the recommended option first. End its label with `(Recommended)`. Explain the recommendation in its description. Mark no recommendation without a reason to prefer an option.
- Give each option one line that states what it changes in the work.
- Always let the owner answer in their own words. Treat a free answer as the decision or a question to answer before the next set.
- After sending cards, write nothing else. Wait for the answers. Later text can dismiss the cards.
- A workflow child or background job cannot ask. It reports open questions and stops at the first question that blocks the work.

## Instructions

### Map cards to the tool

Use `AskUserQuestion` for the cards.
Send one to four questions per call.
For eight questions, send two calls of four.
Wait for the first call's answers before sending the second call.
Map each card's full question to `question`.
Use a topic label of at most twelve characters for `header`.
Give each question two to four `options`.
Map each option to a `label` and a one-line `description` of its effect.
Put the recommended option first, with `(Recommended)` at the end of its `label`.
Set `multiSelect` only when the options do not exclude each other.
The tool adds `Other` for the owner's own words.
Do not add an option for `Other`.

### Ask and record decisions

1. Read the task, then the code and docs it affects. List what remains unknown and would change the result. Remove every item you answered by reading.
2. Order questions by how much work depends on each answer. Put scope and direction first, then details. Group related questions.
3. Write each card from this template:

```text
Question: <a full question that names its subject>?
Header: <a short topic label>
Options:
- <recommended choice> (Recommended): <why this is recommended and what it changes in the work>
- <alternative>: <what it changes in the work>
```

4. Keep each set within the question tool's limit for one call. If an answer changes a later question, rewrite or remove that question before the next set. Without a question tool, send the same cards as plain text. End the message at the last card.
5. Read the decisions back as prose, with one paragraph per topic instead of per card. State what the owner chose and what it means for the work. Name defaults you used without asking. Put open items last.
6. Record decisions before the first write that depends on them. Use the change's proposal or design, the spec, the brief, or the task's tracking file. If no such file exists, use the readback in the reply as the record.
7. Proceed. Ask again only when answers conflict with each other or with a rule. State which answers or rules conflict and why.

This card fails because its subject and options need earlier text:

```text
Question: Which way for batch 2?
Options:
- Option A
- Option B
```

This card works because it names its subject and each option's effect:

```text
Question: Should the new export keep the old CSV column names?
Header: Columns
Options:
- Keep the old names (Recommended): Existing spreadsheets still work. New fields go at the end.
- Rename to match the API: A simpler schema requires every consumer to update its import.
- Offer both layouts: A flag selects one layout. Tests cover both code paths.
```

## Verification

- No answer to an asked question exists in the code, docs, configuration, or conversation.
- Every card names its subject and has two to four options in plain words. Each option has one line of effect. Any marked recommendation comes first and states its reason.
- The readback uses prose grouped by topic, names the defaults, and lists open items last.
- The decision record exists where the work lives before the first write that depends on it.

## References

- The SelfContainedQuestionOptions rule: describe each option's change in plain words.
- The ReviewChange skill: the same readback discipline for a change's requirements.
