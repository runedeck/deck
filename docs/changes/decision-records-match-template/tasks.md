# Tasks

## 1. Implementation

- [x] 1.1 Require `### Consequences` under `## Decision Outcome` in `docs/decisions/.mdschema` and drop the `## Consequences` entry
- [x] 1.2 Add `scripts/check-decision-shape`: signed consequences, `consulted` as `@handle` or `<model-id>@<harness>`, `upstream` and `related` that resolve
- [x] 1.3 Register the check as a prek hook on `docs/`, and `authors.yaml`
- [x] 1.4 Convert every record: Consequences under the outcome with signs, `consulted` with the harness suffix
- [x] 1.5 Restore CORE-0001: source dates, `### Consequences` with signs, `upstream` naming the forge-core record, the rule, and the seven requirement references
- [x] 1.6 Correct the CORE-0011 outcome sentence and date the amendment under More Information
- [x] 1.7 Repair the rotten references: DECK-0019 `related`, DECK-0006 `related`, CORE-0003 and CORE-0005 `upstream`
- [x] 1.8 Add the `opencode` harness domain to `authors.yaml`
- [x] 1.9 Record the decision in `adr.md`
- [x] 1.10 Add `supersedes`, `archived`, `status`, `rune:Canvas`, and the lifecycle classes to `rune.ttl`, and map every record key in `ontology/context.jsonld`
- [x] 1.11 Add the asserted-status and supersession shapes with named smoke findings (`scripts/check-ontology`, `ontology/smoke/expected.tsv`)
- [x] 1.12 Add `scripts/sync-idea`: snapshot a vault drawing through the Obsidian CLI into `docs/ideas/` with a provenance sidecar, and check it against the source
- [x] 1.13 Add the IntakeIdea `Canvas.md` companion: read a drawing by its `obsidian://` link, origin on the left, what the change keeps
- [x] 1.14 CORE-0001 names its canvas by `obsidian://` link, and `docs/ideas/Markdown First.md` is its checked snapshot

## 2. Verification

- [x] 2.1 `tests/test_check_decision_shape.py`: a passing record, an unsigned consequence, a bare model id, an unknown harness, a dangling upstream, a requirement reference
- [x] 2.2 `mdschema check` on every record with the new schema, and the four decision checks
- [x] 2.3 `rune spec validate decision-records-match-template`, Vale, rumdl, typos on the changed files
- [x] 2.4 Recorded proof under `docs/proofs/decision-records-match-template/`, one scene per scenario

## 3. Follow-up

- [ ] 3.1 Copy the corrected schema to `runedeck/adr/adr.mdschema` (that repository)
- [ ] 3.2 The `gpt-5.6-sol@codex` suffix on seven adopted records comes from the delegation runbook, and no commit confirms it. Confirm or change the harness
- [ ] 3.3 `rune spec archive decision-records-match-template` assigns the record its DECK id (cli)
- [ ] 3.4 Flip the status shapes from Warning to Violation once `rune graph export` emits `rune:status` (cli #70, #71)
- [ ] 3.5 Re-record the proof: two new scenarios (canvas link accepted, drawing changed after the snapshot) have no scenes yet
