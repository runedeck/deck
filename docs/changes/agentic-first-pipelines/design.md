# Design: The Idea-to-Merge Flywheel

The pipeline is a loop, not a line. One pass delivers a product change and extracts reusable artifacts. The extracted artifacts enter the context of every later pass, so each delivery makes the next prompt cheaper.

## The loop

```text
prompt -> pushback -> specify -> isolate -> swarm -> local gates -> human skim
   ^                                                                   |
   |                                                                   v
extracted skills / rules / agents <- extract <- merged <- babysit <- CI + review lanes
```

Two outputs leave every pass:

1. **The product**: the merged change.
2. **The extraction**: skills, rules, and agents mined from the pass. Each extracted artifact enters the standard lifecycle (Author, Prove, Measure, Review, Ship) and then sits in context for future prompts. Extraction is a required output, not a cleanup habit.

## Stage map

Each stage names its contract and its instance today. The stack architecture change (`docs/changes/stack-architecture/`) defines the underlying lifecycle. This pipeline is its operating procedure.

| Stage | Contract | Instance today | Status |
|---|---|---|---|
| Prompt | a raw idea in any medium: voice transcript, sketch note, written text | none — ideas arrive ad hoc | **gap: the IntakeIdea skill in this change** |
| Pushback | the agent challenges the idea against existing specs, decision records, and memory before any scaffold. The output is a sharpened intent or a rejection with reasons | openspec-explore skill, informally | partial |
| Specify | `rune spec propose` scaffolds the change. Blast radius decides depth: micro-changes skip the specification, machinery changes carry one, decisions carry a decision record | rune spec, docs/decisions, spec/presence check | exists |
| Isolate | each implementing agent works in a disposable workspace. Colocated repositories use jj workspaces. Copy-on-write snapshots (anomalyco/rift) are an acceptable isolation instance because they copy the whole tree and never touch git refs | jj workspaces | exists, rift optional |
| Swarm | agents parallelize by role (research, implement, review), never as several agents on one change's files | multi-agent delegation | exists |
| Local gates | prek, mdschema, rune validate, kind-specific linters | .githooks, .pre-commit-config.yaml | exists |
| Human skim | a fast owner pass before CI spends review rounds | manual owner pass | **gap: no skill encodes the skim yet** |
| CI + review lanes | ceremony checks plus bot lanes in turns | seer lanes, attestations, quality | exists |
| Babysit | automated round recovery, label toggles, fault triage until merge-ready | babysitting routines, PR #44 | exists |
| Approve | the owner merges, and nothing merges itself | branch rulesets | exists |
| Extract | after merge, the pass is mined: repeated corrections become rules, repeated procedures become skills, repeated roles become agents. The priority ladder picks the form | LearnFrom, CaptureOnTouch | partial: habit, not gate |
| Recycle | extracted artifacts ship through the lifecycle and appear in the context of the next prompt | rune install | exists once extraction happens |

## Placement decisions

- **Memory is advisory, never authoritative.** A memory system plugs into Pushback (recall related decisions) and Extract (store pass learnings). Specifications and decision records stay the only sources of truth. Adoption of cognee waits until the intake seam works. A third memory system needs a named replacement target first.
- **Obsidian leaves the flow.** Its holding-pen role belongs to intake plus workshop capture. The vault stays an archive.
- **pi is an edge, not a rewrite target.** pi joins as a provider edge like the other harnesses. The eventual "rune inside pi" is a thin pi extension that wraps the rune binary. Rewriting rune as a pi module would bind the artifact layer to one harness and break the provider-independence contract (DECK-0006).
- **rift is isolation only.** It creates copy-on-write workspaces with detached state and manages no branches, so bookmark and push discipline stay with jj. It is experimental and serves disposable workspaces only.
- **Measure stays in the loop.** Extracted rules pay rent through BenchArtifact before they ship. A pipeline that extracts unmeasured rules fills every future context with unpaid cost.

## Declared constraints

The pipeline's enforcement layer follows the neurosymbolic split: agents propose what is likely, a declared ontology states what is permitted, deterministic checkers decide. The stack's schemas are the ontology's first layer. The graph of artifacts, stages, evidence, and permitted relations is the second (DECK-0009). Lifecycle folklore becomes axioms with checkers: a rule ships only with a bench verdict, an adoption carries exactly one sealed review, a proposal may reference only entities that exist. Metadata maps to public vocabularies (schema.org, Dublin Core, SKOS, FOAF) before new terms enter.

## Ceremony fit

Ceremony matches the task, and the babysitter enforces the fit:

- Open every proposal and pull request with the problem in the prompter's terms. Implementation never leads.
- Before filing, check whether a pull request for the intent already exists. Read the recently merged ones for register and shape.
- A pull request title is a future commit message and follows that grammar.
- Review does not expand the pull request: a finding outside the change's intent becomes an intake item, not a new commit.
- A review-bot finding not worth addressing gets an explicit mark through the ceremony's waiver labels, never silence.
- Prose that no gate measures does not ship: unmeasured always-in-context Markdown is the slop the bench gate exists to reject.

## Gap register

1. No intake instance: this change adds the IntakeIdea skill as the first one.
2. Pushback has no contract: openspec-explore exists, but nothing requires a challenge pass before scaffolding.
3. Extraction is unenforced: no gate asks "what did this pass teach" before a change closes.
4. No blast-radius rule in writing: when a change may skip Specify is folklore. This design states the rule, and enforcement is future work.
5. The voice and sketch capture surface does not exist. Until it does, transcripts arrive as pasted text.
