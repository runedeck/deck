# Design

## Approach

Condense, do not port. Each forge source is read for its contract and its failure modes, and the skill states those in Simplified Technical English for a frontier model: constraints, inputs, outputs, verification. Tutorials, intensity dials, team tooling, and AskUserQuestion loops that a workflow child cannot run are cut. Sources and cuts are recorded per skill in its References section. This beat a verbatim port through AdoptArtifact, which would carry forge's harness assumptions, and beat keeping the workflows as pi prompt templates, which rune cannot deploy.

ForgeCycle uses the DECK-0008 vocabulary. `Stages.md` maps each stage to one owner, and the extraction question closes every pass rather than waiting for the end:

```text
 prompt ─▶ pushback ─▶ specify ─▶ isolate ─▶ swarm ─▶ local gates ─▶ human skim
   │        IntakeIdea  IntakeIdea  VersionCtl  AgentTeam  VersionCtl    Storyboard
   │                                              ▲  ▲          │
   │                       AdversaryReview ───────┘  └──────────┘ red
   ▼
 ci and review lanes ─▶ babysit ─▶ approve ─▶ extract ─▶ recycle
   runeseer              MergeTrain  owner      LearnFrom  rune install
        └── changes requested ──▶ swarm        closed ──▶ stop
```

Storyboard is the human skim seam. One frame before the first write of a stage, one frame after, confirmation in between.

## Structure

```text
runes/development/skills/
├─ ForgeCycle/      SKILL.md  Stages.md
├─ Storyboard/      SKILL.md  ChangeMap.md PlanGraph.md FanOut.md TreeDelta.md StateBox.md SeatMap.md
├─ MergeTrain/      SKILL.md  workflow.js  Triage.md  Review.md
├─ AgentTeam/       SKILL.md  workflow.js  Split.md   (reads MergeTrain/Review.md)
├─ AdversaryReview/ SKILL.md  workflow.js  Attack.md
└─ ResearchGrid/    SKILL.md  workflow.js  Track.md
runes/core/rules/RemoteWrites.md
```

- A workflow skill's `SKILL.md` names the inputs the model reads from the user's sentence, the caps, and the models by class. It tells the model to read `workflow.js` from the skill's directory and pass it to the workflow tool verbatim with `args`. Companions are read by the child from the same directory, named by absolute path in the child brief.
- ForgeCycle keeps no state of its own. It reads `tasks.md` and `rune spec context <id>`, prints the stage strip, names the next stage and its owner, and ends the turn. The next turn invokes that skill. When the owner is absent in the harness, ForgeCycle says so and stops.
- Storyboard writes each confirmed frame to `docs/changes/<id>/storyboard/<nn>-<stage>.txt`. The question uses AskUserQuestion in Claude Code and a plain question elsewhere. `ask-user` in pi is a later package change.
- AdversaryReview applies the CORE-0016 method: a hit survives only when the refutation fails. It runs the refutation lenses and does not replace a future AdversarialReviewer agent.

## Risks

- Nested runs blow the 32-agent cap. Guard: ForgeCycle never invokes a workflow, and each script enforces `meta.caps` before spawning.
- The next stage's owner is absent in the harness. Guard: ForgeCycle says so and stops.
