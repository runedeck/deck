---
name: ClarifyTask
description: "Ask the owner clarifying questions as question cards before a large or ambiguous task: one standalone question per card, two to four plain-word options with the recommended one first, then read the answers back as prose by topic, record them where the work lives, and proceed. USE WHEN ask me clarifying questions, ask before you start, interview me first, what do you need to know from me, ask me what is unclear, or the task is large or ambiguous and a wrong guess would waste the work. NOT FOR checking expectations against how a workflow behaves (WorkflowInterface), turning a raw idea into a spec change (IntakeIdea), attacking a draft or a design (AdversaryReview), or walking a change's requirements to verdicts (ReviewChange)."
compatibility: "Uses the harness's question tool when one exists and falls back to a plain question. Workflow children cannot ask and therefore never run this skill."
metadata:
    version: 0.1.0
---

# ClarifyTask

Before a large or ambiguous task, or whenever the owner asks, stop and ask what you cannot find out yourself. The owner answers on question cards, not a numbered list in the reply. A card is one question with a few options the owner picks in one keystroke or overrides in their own words. The owner asked for this form on 2026-11-02, when eight questions went out as two sets of four.

## Constraints

- Ask no question whose answer is in the code, the docs, the configuration, or the conversation. Read first. A question the owner already answered tells them you did not look.
- Ask only what changes the work. When a choice is cheap to reverse and one answer is clearly reasonable, take it and name it in the readback instead.
- One question per card. The question names its subject, because the owner reads the card apart from the reply above it, and the recorded decision must make sense later without either.
- Two to four options per card, each described in plain words. Never "item 3", "batch 2", or "the second approach". See the SelfContainedQuestionOptions rule.
- The recommended option comes first and its label ends with `(Recommended)`. Give the reason in its description. Mark no option when you have no reason to prefer one.
- Every option carries one line that says what it changes in the work.
- The owner can always answer in their own words. A free answer is either the decision or a question to answer before the next set.
- After the cards, write nothing else and wait for the answers. Text sent after a card can dismiss it.
- A workflow child or a background job cannot ask. It puts the open questions in its report and stops at the first one that blocks the work.

## Instructions

1. Read the task, then the code and docs it touches. List what is still unknown and would change the result. Drop every item you answered by reading.
2. Order the questions by how much work each one gates: scope and direction first, details last. Keep related questions in the same set.
3. Write each card from this template:

```text
Question: <a full question that names its subject>?
Header: <a short topic label>
Options:
- <recommended choice> (Recommended): <what it changes in the work>
- <alternative>: <what it changes in the work>
```

4. Ask in sets no larger than one call of the question tool takes. When an answer changes a later question, rewrite or drop that question before you ask the next set. Without a question tool, send the same cards as plain text and end the message at the last card.
5. Read the decisions back as prose, one paragraph per topic, not per card: what the owner chose and what it means for the work. Name the defaults you took without asking. Open items come last.
6. Record the decisions where the work lives: the change's proposal or design, the spec, the brief, or the task's tracking file. When the work has no such file, the readback in the reply is the record.
7. Proceed. Ask again only when two answers conflict, or an answer conflicts with a rule. Then say which ones and why.

This card is wrong, because the owner must scroll back to learn what "batch 2" and the options mean:

```text
Question: Which way for batch 2?
Options:
- Option A
- Option B
```

This card is right, because it reads alone and every option says what it costs:

```text
Question: Should the new export keep the old CSV column names?
Header: Columns
Options:
- Keep the old names (Recommended): existing spreadsheets keep working, new fields go at the end
- Rename to match the API: a cleaner schema, every consumer updates its import
- Ship both layouts: a flag picks one, and the tests cover two code paths
```

## Verification

- No question asked had its answer in the code, the docs, or the conversation.
- Every card names its subject and has two to four plain-word options, each with a line of effect, and a marked recommendation first when one was made.
- The readback is prose grouped by topic, names the defaults taken, and lists open items last.
- The decisions were written where the work lives before the first write that depends on them.

## References

- The SelfContainedQuestionOptions rule: describe each option's change in plain words.
- The ReviewChange skill: the same readback discipline for a change's requirements.
