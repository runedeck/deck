---
name: IntakeIdea
description: Turn a raw idea into a challenged, scaffolded spec change. USE WHEN intake an idea, capture a thought, voice transcript to spec, sketch to proposal, new idea for the stack, propose from a prompt, or triage a feature thought. NOT FOR implementing an existing change (use the change's tasks), session retrospectives (LearnFrom), or adopting third-party artifacts (AdoptArtifact).
---

# IntakeIdea

## Instructions

Take the raw idea exactly as given: a voice transcript, a sketch description, or written prose. Do not clean it before understanding it.

### Step 1: Push back before anything exists

1. Extract the intent: what should be different after this idea lands, and for whom.
2. Search existing state selectively: `rune spec list`, the capability specifications under `docs/specs/`, the decision records under `docs/decisions/`, and advisory memory when available.
3. Challenge the idea against what exists. End in exactly one outcome:
    - **Duplicate**: an existing capability already requires this. Point at it. Stop.
    - **Extension**: an active change already covers this ground. Propose merging the intent into it. Stop.
    - **Survivor**: the idea stands. State the sharpened intent in one sentence and continue.
4. Disagree openly. A weak idea rejected at intake costs one message. The same idea rejected in review costs rounds.

### Step 2: Size the blast radius

- **Micro**: prose or a single artifact, no contract changes. Route as a direct change without a specification.
- **Machinery**: behavior, checks, workflows, or contracts change. Scaffold with `rune spec propose <change-id> --capability <name>`.
- **Decision**: alternatives exist and the choice will bind later work. Add `--design` and draft a decision record in `docs/decisions/` with the next free DECK number.

### Step 3: Scaffold and fill

1. Create an isolated workspace from the repository root.
2. Use a Jujutsu workspace in a Jujutsu-colocated repository.
3. Use a Git worktree in a Git-only repository.
4. Run the sized scaffold from the isolated workspace.
5. Fill the proposal: why, what changes, capabilities, impact. Keep the sharpened intent as the first line of Why.
6. Write delta requirements with MUST and MUST NOT, one scenario per requirement minimum.
7. Record open questions as tasks, not as vague prose.

### Step 4: Hand off to the pipeline

1. Run the local gates: `mdschema check` on new documents and `rune validate`.
2. Commit with the proper model identity through the VersionControl flow.
3. Use the gated `jj push` in a Jujutsu-colocated repository.
4. Use the normal Git commit and push flow in a Git-only repository.
5. Open the pull request with the ceremony labels.
6. Report the outcome in one line: the outcome class, the change id or the pointer to existing work, and the pull request link when one exists.

## Verification

- The pushback outcome is explicit: duplicate, extension, or survivor.
- A survivor has a scaffolded change whose proposal names the sharpened intent.
- No specification exists for a micro-change, and one exists for machinery.
- `rune spec validate <change-id>` passes for scaffolded changes.
