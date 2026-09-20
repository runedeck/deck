---
adr: "docs/decisions/DECK-0001 Artifact Benchmarking Skill.md"
status: implemented
---

# Bench Artifact

## Why

See the linked ADR for the decision rationale. This proposal records the change in scope.

## What Changes

- A new BenchArtifact skill lands in `runes/core/skills/`, owning the evaluation loop: test cases, with-artifact and baseline runs, grading, aggregation, and the comparison report.
- The loop generalizes across artifact kinds: skills, rules, and agents each get a defined with-artifact configuration and baseline.
- Runs gain a model dimension. Aggregation reports per configuration and model. The report renders the matrix as one self-contained HTML with no external requests.
- BuildSkill's `EvalLoop.md`, `scripts/`, `templates/agents/`, and `eval-viewer/` move to BenchArtifact. BuildSkill keeps a pointer to the extracted loop.
- The rune CLI is untouched. The import of the loop into `rune` is a later change.

## Capabilities

- artifact-benchmarking (new)

## Impact

- `runes/core/skills/BenchArtifact/` (new), extracted from BuildSkill with adapted scripts and templates.
- `runes/core/skills/BuildSkill/`: evaluation companion becomes a reference to BenchArtifact.
- Adoption practice: AdoptArtifact's uncertain-value path points at BenchArtifact instead of BuildSkill's loop.

## Rebuild (2026-08-19, retroactive record)

The Simplified Technical English benchmark drove a rebuild inside this change. The shipped shape differs from the original extraction:

- Execution follows the ladder in `DECK-0002 Benchmark Execution Ladder`: native in-harness agents by default, direct Claude and Codex CLIs for a fast first table, and a full cross-harness matrix behind the explicit `--cross-harness` flag.
- The verdict follows `DECK-0003 Three-Metric Verdict and Cross-Vendor Judging`: assertions, checker density, and blind cross-vendor preferences, read together within one model.
- The cross-harness runner freezes the manifest per iteration, refuses re-entry, retains raw provider stdout, and verifies each route with a preflight and a context canary.
- The report opens with a verdict, names the tested artifact and digest, and provides a browsable pair viewer with the blind judgment beside each pair.
- `benchmark.md` is one compact delta table for pull request bodies. A bench table accompanies every PR that adds a skill, rule, or agent.
- Artifacts ship one version only: the manifest and snapshot carry no version suffix, and iteration records stay immutable instead.
