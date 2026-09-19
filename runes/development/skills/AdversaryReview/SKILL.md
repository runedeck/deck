---
name: AdversaryReview
description: "Attack a draft or a design from three disjoint hostile angles in parallel, bind every hit to a quoted line, and settle each hit as fixed or rejected with reason. USE WHEN attack this, find the holes, hostile read, adversary pass, refute my claims, review this post before it goes out, stress-test the design. NOT FOR code diff review inside a workflow (MergeTrain Review.md), consensus panels, or rewriting for style alone (SimplifiedTechnicalEnglish)."
compatibility: "Requires a workflow tool: the pi workflow extension or Claude Code Workflow. Attack children need no network. Stops with one sentence where no workflow tool exists."
targets: [claude, agentskills]
metadata:
    version: 0.1.0
    decisions: DECK-0016, CORE-0016
---

# AdversaryReview

The CORE-0016 method as a workflow: a claim survives only when the refutation fails. Three seats attack the original text from disjoint angles. A settle step then gives every hit one of two dispositions, fixed or rejected with reason. There is no accepted, and there is no vote.

## Prerequisites

- A workflow tool. Without one, reply "AdversaryReview needs a workflow tool" and stop.
- The path of the text under attack, from the user's sentence. Optional: the audience.
- The absolute path of this skill's directory, for [Attack.md](Attack.md).

## Constraints

- The attack targets the original. No rewrite, tightening, or translation happens before the attack.
- Angles are fixed and disjoint: facts, logic, reception. A hit from another angle arrives from that seat.
- Every hit quotes a line copied from the text. A paraphrased hit is discarded.
- Fatal means publishing as written would embarrass the author. Style alone is never fatal.
- Settle disposes of every hit, fatal or not: fixed, or rejected with a reason the owner can read. A hit neither fixed nor refuted stays open in the report.
- Attack children cite no external source and fetch nothing. The text is the evidence.
- Caps: 3 attacks, 1 settle. Total 4 agents, one loop.

## Instructions

Read `workflow.js` from this skill's directory and pass it to the workflow tool verbatim. Set `args`:

```json
{ "draft": "/abs/path/to/text.md", "audience": "<who reads it>", "skillDir": "/abs/AdversaryReview",
  "changeId": "<id or omit>", "models": { "review": "...", "code": "..." } }
```

Every hit carries an id. Settle closes a hit as fixed or rejected with reason, or leaves it out, in which case the result lists it as open. A run with a failed seat returns `complete: false` and must not be read as a clean review.

In pi, attacks on grok and settle on sol, `cliproxy/` ids only. In Claude Code, omit to inherit. Never name an Anthropic model inside pi.

Phases, as the script runs them:

1. Attack: three children, one angle each, apply [Attack.md](Attack.md) to the original and return hits with quote, objection, and fatal.
2. Settle: one child receives the original and every hit, applies the fixes that survive its own refutation, rejects the rest with a reason, and returns the revised text plus the disposition table.

When Storyboard is installed, show its seat map before the run.

## Verification

- Every hit's quote appears verbatim in the original.
- Every hit has a disposition of fixed or rejected with reason.
- The revised text changes only lines that a fixed hit names.
- No child fetched a page or cited an external source.

## References

- [workflow.js](workflow.js), [Attack.md](Attack.md).
- Deck decision CORE-0016 Adversarial Review over Councils: the method. This skill orchestrates refutation seats and does not replace a future reviewer agent.
- Condensed from forge-core `TheOpponent` and forge-dev `ReceiveReview`. Cut: intensity levels (the angles are fixed), the steel-man essay (the settle child consumes hits), and web lookups (unverified in the child).
