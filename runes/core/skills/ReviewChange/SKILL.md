---
name: ReviewChange
description: "Walk a change's requirements with the owner one at a time: the heading, one line of context, the real tension, then a verdict of keep, change, drop, split, or merge, explained in four parts and read back as prose. USE WHEN review the change with me, walk the requirements, verdict walk, decide the open requirements, read back the decisions, the owner reviews a specification by voice or in the terminal. NOT FOR a hostile read of a draft (AdversaryReview), implementing a change (openspec-apply-change), or a review bot loop on a pull request (VersionControl)."
metadata:
    version: 0.1.0
---

# ReviewChange

The owner decides a specification one *[requirement][REQUIREMENT]* at a time. You bring the [requirement][REQUIREMENT], its tension, and concrete ways to *[change][CHANGE]* it. The owner answers in one word or in their own words. The walk ends in a readback that the implementing session works from. The owner asked on 2026-10-17 to keep this pattern as the way specifications get reviewed.

## Prerequisites

- The [change][CHANGE] directory with its specifications, the `design.md` coverage table, the *[decision records][DECISIONRECORD]* it cites, and any reviewer verdicts.
- The glossary pages, so you can explain a term inside a [requirement][REQUIREMENT] from its definition.
- One channel, either the terminal with `AskUserQuestion` or voice through a project built from voice-safe files.

## Constraints

- One [requirement][REQUIREMENT] at a time. Short turns. The owner's attention is the scarce resource.
- Name a [requirement][REQUIREMENT] by its heading, never by an index letter or number, in the walk and in the readback.
- Numbers are words in anything spoken or read back.
- Never skip past "I do not understand" or "I have no idea what you just said". Re-explain with the four-part template first, then ask again.
- Before the next [requirement][REQUIREMENT], discuss the owner's answers and answer the owner's questions. The owner's words: "always before you move on, I need you to discuss with me and answer my questions".
- A verdict binds to the [requirement][REQUIREMENT]'s current text. When the owner [changes][CHANGE] the text, say what the new text claims before you move on.
- When a decision [changes][CHANGE] during the walk, the readback states only the final decision and marks the reversal where it matters.

## Instructions

### Present one requirement

Say three things, then stop:

1. The heading.
2. One line of context: what the [requirement][REQUIREMENT] asks for, in everyday words.
3. The real tension, usually the gap between the [requirement][REQUIREMENT] and the check or the record behind it. An example: "The statement says a projection never stands in for its source. The only scenario tests a snapshot without its sidecar. So the core claim has no failing case."

Ask for a verdict: keep, [change][CHANGE], drop, split, or merge with another [requirement][REQUIREMENT]. Offer concrete proposals instead of an open question: "Rename plus that new scenario, sidecar rule kept as is. Does that work?"

### Explain on request

When the owner asks what a [requirement][REQUIREMENT] means, or says they do not understand, use the four-part template in this order and add nothing:

1. The rule in everyday words. "Do not use the full process for small stuff."
2. A concrete example. "If you fix a typo, you just commit it."
3. What goes wrong without the rule. "Every typo drags a week of paperwork behind it."
4. The open question. "Does a person decide what counts as small, or a check?"

Explain a concept by its effect, the failure it prevents, and one example. Its name explains nothing. Borrow from the owner's world where it helps.

### Rename when the explanation is clearer

When a [requirement][REQUIREMENT] or a term has an arcane name, rewrite it in plain words and offer both, the name and the rewrite. The owner picks. When the plain words win, the name was wrong, and the rename goes into the readback as a decision. The name `harness-neutral` became "the main file works without any vendor's extras", and the heading became Canon Stays Vendor-Neutral.

### Read back as prose

At the end, or when the owner asks, read every decision back as prose. Write one paragraph per [requirement][REQUIREMENT], named by heading, that says what the owner decided and why, in the plain register. Rules that apply to every specification, new [requirements][REQUIREMENT], new [changes][CHANGE], and ontology [changes][CHANGE] get their own sections. Open items come last. Write the readback to a dated file that the implementing session reads first. The first one was `runedeck-review-decisions-2026-10-17.md` in the workshop.

## Verification

- Every [requirement][REQUIREMENT] in scope has one verdict in the readback, or sits under open items with the question that blocks it.
- No item is named by a letter or a number anywhere in the walk or the readback.
- Each explanation the owner asked for has all four parts.
- The owner confirmed the readback, or its unconfirmed parts carry a mark.

## References

- The terminal form: `AskUserQuestion` with four [requirements][REQUIREMENT] per call and a header such as `N/32`. Each item gets one summary line. Do not copy the [requirement][REQUIREMENT] over. The options are `Keep` plus three concrete proposed [changes][CHANGE], and `Other` for the owner's own words. Keep the state in a `state.json` in the workshop's spec directory so the walk resumes. Discuss after every batch before the next one.
- The voice form: a project built from voice-safe files. Such a file has no index ids and reads as narrative under headings. It has no tables, lists, code, paths, extensions, or abbreviations. Each section is self-contained, and the file stays under twelve kilobytes.
- The SelfContainedQuestionOptions rule: describe each option's [change][CHANGE] in plain words.

[REQUIREMENT]: ../../../../docs/specs/glossary/requirement.md
[CHANGE]: ../../../../docs/specs/glossary/change.md
[DECISIONRECORD]: ../../../../docs/specs/glossary/decision-record.md
