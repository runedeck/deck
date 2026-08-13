# Bench Artifact Design

## Approach

Move BuildSkill's evaluation machinery into a new BenchArtifact skill and generalize at the configuration boundary: the loop already compares a with-artifact run to a baseline run, so kinds differ only in how each configuration is assembled. The alternative, teaching BuildSkill about rules and agents, was rejected in DECK-0001 because it grows an authoring guide into a benchmarking product.

The runner gains a model parameter passed to the harness invocation, and every run directory records its model in `timing.json` alongside tokens and duration. The aggregator keys results by configuration and model instead of configuration alone. The report follows proton-ai-security's pattern: `benchmark.json` inlined into a template rendered client side with a vendored stylesheet, so one file carries the whole comparison.

## Structure

- `runes/core/skills/BenchArtifact/SKILL.md`: the loop, restated for any artifact kind.
- `BenchArtifact/scripts/`: runner, grader helpers, aggregator with the model dimension, report builder.
- `BenchArtifact/templates/agents/`: grader, comparator, analyzer, unchanged in role.
- `BenchArtifact/assets/`: the comparison report template.
- `runes/core/skills/BuildSkill/EvalLoop.md`: replaced by a pointer to BenchArtifact; `scripts/`, `templates/agents/`, `eval-viewer/` removed from BuildSkill.

## Risks

- The moved scripts carry BuildSkill-shaped assumptions (workspace naming, `skill_name` fields); the tasks rename these to artifact-neutral terms and keep the directory contract explicit so the aggregator still discovers runs.
- Per-model matrices multiply runs; the skill instructs small test sets and states the run count before spawning.
- BuildSkill references could dangle after extraction; a task greps BuildSkill for paths into the removed directories.
