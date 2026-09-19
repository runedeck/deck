---
name: Storyboard
description: "Draw an ASCII frame of what is about to happen, wait for the owner to confirm it, and close each stage with a frame of what changed. USE WHEN starting work inside a change, before the first file write of a task, before a fan-out or a workflow run, when the plan changes, when the owner asks to see the plan, the schematic, or where things stand, and at the end of a stage. NOT FOR diagrams inside documentation (AsciiDiagrams rule) or progress narration without a decision to confirm."
compatibility: "Uses the harness's question tool when one exists and falls back to a plain question. Workflow children cannot ask and therefore never run this skill."
metadata:
    version: 0.1.0
    decisions: DECK-0016
---

# Storyboard

A frame before you act, a confirmation, a frame after. The owner glances at the frame and confirms the direction or points at the wrong box. Frames accumulate per change, so the change carries its own visual log.

## Prerequisites

- The change id when one exists. Frames are stored under `docs/changes/<id>/storyboard/`.
- Read access to `tasks.md`, the workflow script, or the diff the frame describes.

## Constraints

- One frame before the first write of a stage. No write until the owner confirms.
- The first frame inside a change is the change map. Other kinds follow.
- Width 78 columns or less. Box drawing characters for structure, `──▶` for flow, `×n` for fan-out, `[ ]` around the current node, `+ ~ −` for a delta, `✓ ✗ ↑ ~ ·` for states. No color, no emoji.
- One question after the frame, with three answers: confirm, edit a box, stop. Wait for the answer.
- A correction produces a redrawn frame and a second question before any write.
- Save a frame only after confirmation, as `docs/changes/<id>/storyboard/<nn>-<stage>.txt`, numbered from `01`. Outside a change, show the frame and save nothing.
- Draw from data when data exists: `tasks.md` for the stage strip, the script's `meta.phases` for a plan graph, `jj diff --summary` or `git diff --stat` for a delta. Judgment fills only what data cannot.

## Instructions

Pick the kind from what is about to happen. One kind per frame.

- change map, the first frame inside a change: [ChangeMap.md](ChangeMap.md).
- plan graph, before a workflow or a multi-step edit: [PlanGraph.md](PlanGraph.md).
- fan-out, before parallel agents: [FanOut.md](FanOut.md).
- tree delta, after a stage that wrote files: [TreeDelta.md](TreeDelta.md).
- state box, when behavior has states or options: [StateBox.md](StateBox.md).
- seat map, before an adversarial or research fan-out: [SeatMap.md](SeatMap.md).

Then:

1. Fill the template from data first, then from the plan. Mark the current node with brackets.
2. Show the frame in a `text` fence. Ask: does this match your intent, with the three answers.
3. On confirm, save the frame when inside a change, then proceed with the stage.
4. On edit, redraw and ask again. On stop, end the turn with the frame as the record.
5. When the stage ends, draw the delta frame, show it, and ask the same question. Save it as the next number after the owner confirms. A delta that differs from the plan gets the difference named above the question.

## Verification

- A frame preceded the first write of the stage, and the owner's confirmation preceded the write.
- Saved frames are numbered without gaps and each names its stage.
- Every frame is 78 columns or less and uses only the glyph set.

## References

- Templates: [ChangeMap.md](ChangeMap.md), [PlanGraph.md](PlanGraph.md), [FanOut.md](FanOut.md), [TreeDelta.md](TreeDelta.md), [StateBox.md](StateBox.md), [SeatMap.md](SeatMap.md).
- Deck rule AsciiDiagrams: draw structure when the surface is a terminal. This skill adds the checkpoint and the confirmation.
- Condensed from forge-core `PreviewChoices` and `StagedReview`. Cut: the choice-preview format, replaced by the frame, and the review staging, which ForgeCycle owns.
