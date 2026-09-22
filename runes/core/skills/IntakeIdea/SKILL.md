---
name: IntakeIdea
description: Turn a raw idea into a challenged, scaffolded spec change. USE WHEN intake an idea, capture a thought, voice transcript to spec, sketch to proposal, new idea for the stack, propose from a prompt, or triage a feature thought. NOT FOR implementing an existing change (use the change's tasks), session retrospectives (LearnFrom), or adopting third-party artifacts (AdoptArtifact).
---

# IntakeIdea

## Instructions

Take the raw idea in the form it arrives. Every medium is optional and one is enough: a transcript of a recording, a link to a drawing in the owner's vault, a short written prompt, or several at once. Do not clean it before understanding it. A transcript arrives pasted, or as a link to its file. A link into the vault, for a transcript as for a drawing, is read through the Obsidian CLI and snapshotted with `scripts/sync-idea`, and the record's `upstream` lists the link. [Canvas.md](Canvas.md) says how to read a drawing and what the change keeps of it.

### Step 1: Push back before anything exists

1. Extract the intent: what should be different after this idea lands, and for whom.
2. Search existing state selectively: `rune spec list`, the capability specifications under `docs/specs/`, the decision records under `docs/decisions/`, and advisory memory when available.
3. Challenge the idea against what exists. End in exactly one outcome:
    - **Duplicate**: an existing capability already requires this. Point at it. Stop.
    - **Extension**: an active change already covers this ground. Propose merging the intent into it. Stop.
    - **Survivor**: the idea stands. State the sharpened intent in one sentence and continue.
4. Disagree openly. A weak idea rejected at intake costs one message. The same idea rejected in review costs rounds.

### Step 2: Interview the owner

Before any file exists, ask the owner about the feature. At most seven questions in one round, each one answerable in one sentence:

1. Who is this for, and what is different for them afterwards?
2. What must hold every time? These become MUST statements.
3. What must never happen? These become MUST NOT statements.
4. How will you see that it works? Each answer is one WHEN and THEN.
5. What existing record, capability, or rune does this touch?
6. What is out of scope?
7. What is the smallest version you would accept?

Stop when the answers state every requirement and its scenarios. Do not fill a gap with a guess. A drawing or a transcript answers some questions already, so ask only the open ones.

### Step 3: Size the blast radius

- **Micro**: prose or a single artifact, no contract changes. Route as a direct change without a specification.
- **Machinery**: behavior, checks, workflows, or contracts change. Scaffold with `rune spec propose <change-id> --capability <name>`.
- **Decision**: alternatives exist and the choice will bind later work. Add `--design` and draft a decision record in `docs/decisions/` with the next free DECK number.

### Step 4: Scaffold and fill

1. Create an isolated workspace from the repository root.
2. Use a Jujutsu workspace in a Jujutsu-colocated repository.
3. Use a Git worktree in a Git-only repository.
4. Run the sized scaffold from the isolated workspace.
5. Fill the proposal: why, what changes, capabilities, impact. Keep the sharpened intent as the first line of Why.
6. Write delta requirements with MUST and MUST NOT, one scenario per requirement minimum.
7. Record open questions as tasks, not as vague prose.
8. Set the record's `upstream` to what the idea came from: the link to the drawing or the transcript, or nothing for a bare prompt.

### Step 5: Review the MUST statements and the scenarios with the owner

Before the change counts as proposed, hand the delta specification to the owner as one list: every MUST statement and every scenario, one line each, numbered. Ask for a verdict on each line: keep, change, or drop. Rewrite a changed line and its scenarios and ask again for that line only. The accepted lines stay as they are. A change with a line that has no verdict does not proceed to implementation.

### Step 6: Hand off to the pipeline

1. Run the local gates: `mdschema check` on new documents and `rune validate`.
2. Commit with the proper model identity through the VersionControl flow.
3. Use the gated `jj push` in a Jujutsu-colocated repository.
4. Use the normal Git commit and push flow in a Git-only repository.
5. Open the pull request with the ceremony labels.
6. Report the outcome in one line: the outcome class, the change id or the pointer to existing work, and the pull request link when one exists.

## Verification

- The pushback outcome is explicit: duplicate, extension, or survivor.
- The interview's open questions are answered by the owner, not by a guess.
- A survivor has a scaffolded change whose proposal names the sharpened intent.
- Every MUST statement and every scenario in the delta has the owner's verdict before implementation starts.
- No specification exists for a micro-change, and one exists for machinery.
- `rune spec validate <change-id>` passes for scaffolded changes.
