---
adr: "docs/decisions/DECK-0001 Artifact Benchmarking Skill.md"
status: proposed
---
# Bench Artifact

## Why

See the linked ADR for the decision rationale. This proposal records the change in scope.

## What Changes

- A new BenchArtifact skill lands in `runes/core/skills/`, owning the evaluation loop: test cases, with-artifact and baseline runs, grading, aggregation, and the comparison report.
- The loop generalizes across artifact kinds: skills, rules, and agents each get a defined with-artifact configuration and baseline.
- Runs gain a model dimension. Aggregation reports per configuration and model; the report renders the matrix as one self-contained HTML with no external requests.
- BuildSkill's `EvalLoop.md`, `scripts/`, `templates/agents/`, and `eval-viewer/` move to BenchArtifact; BuildSkill keeps a pointer to the extracted loop.
- The rune CLI is untouched; importing the loop into `rune` is a later change.

## Capabilities

- artifact-benchmarking (new)

## Impact

- `runes/core/skills/BenchArtifact/` (new), extracted from BuildSkill with adapted scripts and templates.
- `runes/core/skills/BuildSkill/`: evaluation companion becomes a reference to BenchArtifact.
- Adoption practice: AdoptArtifact's uncertain-value path points at BenchArtifact instead of BuildSkill's loop.
