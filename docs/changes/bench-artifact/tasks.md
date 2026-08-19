## 1. Extraction

- [x] 1.1 Create `runes/core/skills/BenchArtifact/` and move BuildSkill's `EvalLoop.md` content, `scripts/aggregate_benchmark.py`, `templates/agents/`, `eval-viewer/`, and `references/schemas.md` into it; `assets/eval_review.html` stays with BuildSkill's description-optimization pipeline
- [x] 1.2 Rename BuildSkill-shaped terms to artifact-neutral ones (`skill_name` to `artifact_name`, per-kind configuration names) across the moved scripts and docs
- [x] 1.3 Replace BuildSkill's evaluation companion with a pointer to BenchArtifact and update every BuildSkill reference into the moved directories

## 2. Generalization

- [x] 2.1 Define the with-artifact and baseline configurations per kind (skill, rule, agent) in `SKILL.md`
- [x] 2.2 Add the model parameter to the runner instructions and record the model in each run's `timing.json`
- [x] 2.3 Key the aggregator by configuration and model; no cross-model averaging

## 3. Comparison report

- [x] 3.1 Build the self-contained report: `benchmark.json` inlined into a template with a vendored stylesheet, per-model matrix, per-case grading detail
- [x] 3.2 Verify the report renders offline with no external requests

## 4. Verification

- [ ] 4.1 `rune validate` passes on the deck
- [x] 4.2 No path under BuildSkill references the removed directories
- [ ] 4.3 A rule benchmark runs end to end (ReviewMarkers with and without the rule) and produces the per-model report

## 5. Rebuild (2026-08-19)

- [x] 5.1 Split execution into NativeBench (default) and RuneBench behind `--cross-harness`
- [x] 5.2 Freeze manifests per iteration, refuse re-entry, retain raw provider stdout
- [x] 5.3 Verify each route with a preflight and a context canary before the matrix
- [x] 5.4 Grade with the artifact's checker; correct the corpus density denominator to checker words
- [x] 5.5 Judge pairs blind and cross-vendor; record winners and reasons per dimension
- [x] 5.6 Rebuild the report: verdict first, artifact identity, browsable pair viewer with judgments
- [x] 5.7 Write `benchmark.md` as one compact delta table for pull request bodies
- [x] 5.8 Run the six-model STE matrix (iteration-4) and record the split verdict
