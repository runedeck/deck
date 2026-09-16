# Forge Adoption Design

## Approach

Condense, do not port. Each forge source is read for its contract and its failure modes, and the skill states those in Simplified Technical English for a frontier model: constraints, inputs, outputs, verification. Tutorials, intensity dials, team tooling, and AskUserQuestion loops that a workflow child cannot run are cut. Sources and cuts are recorded per skill in its References section. This beat a verbatim port through AdoptArtifact, which would carry forge's harness assumptions, and beat keeping the workflows as pi prompt templates, which rune cannot deploy.

A three-model adversarial pass (astra, grok, lumo, receipts in the workshop) bound seven fixes into the design, and a second pass by astra and grok on these documents bound six more. All are requirements in the delta specs:

- The prohibitions stay an always-on rule, written as a command list so "review" the verb does not block review lanes.
- Workflow skills deploy only where a workflow tool exists, and the filter is verified before merge.
- The script is a file with a 32-agent ceiling and a finite loop ceiling, and no child calls a workflow.
- ForgeCycle names the next stage and ends its turn. It never invokes a workflow or a workflow skill.
- AgentTeam owns files per parallel package, starts dependent packages from the integrated tree, and integrates on trunk.
- AdversaryReview attacks the original and every hit ends fixed or rejected with reason. There is no "accepted".
- ResearchGrid verifies with a different model and an excerpt, rejects unfound claims, and marks single-source numbers unsupported.
- MergeTrain binds every verdict to the surveyed head SHA.

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
- AdversaryReview applies the CORE-0016 method: a hit survives only when the refutation fails. It orchestrates refutation lenses and does not replace a future AdversarialReviewer agent.

## Risks

- A workflow skill reaches a harness with no workflow tool. Guard: `targets`, plus a first line in the body that stops and says so. Task 3.4 verifies the filter and blocks the merge if it does not hold.
- Companion paths resolve against the child's cwd instead of the skill. Guard: the absolute skill path in every child brief. A `rune validate` check is a follow-up.
- Nested runs blow the 32-agent cap. Guard: ForgeCycle never invokes a workflow, and each script enforces `meta.caps` before spawning.
- The prohibitions rule gets stretched, so "one named label" becomes any label. Guard: command-shaped wording, the exception limited to the invoking agent, and child briefs carry the list without the exception.
- pi and codex have no rules path yet. Guard: the pi package `AGENTS.md` carries the same command list until task 4.4 lands.
- No bench and no proof yet, so the only evidence is the adversarial passes on the text. Guard: tasks 4.1 and 4.2 stay open and the ADR status stays proposed.
