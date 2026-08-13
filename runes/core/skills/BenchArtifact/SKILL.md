---
name: BenchArtifact
description: "Benchmark a skill, rule, or agent against a baseline across models: run test cases with and without the artifact, grade, aggregate per model, and render one comparison report. USE WHEN benchmarking an artifact, evaluating a rule, measuring whether a skill helps, comparing model behavior with and without an artifact, or deciding whether an adoption earns its context cost. NOT FOR authoring artifacts (BuildSkill, BuildRule) or reviewing imports (AdoptArtifact)."
metadata:
    version: 0.1.0
allowed-tools: Bash(python3 *), Bash(mkdir *), Bash(cp *), Read, Write, Edit, Grep, Glob, Agent
---

# BenchArtifact

Measure whether an artifact changes model behavior enough to earn its place. Every benchmark runs the same test cases in two configurations, with the artifact and without it, grades both against the same assertions, and reports the delta per model. The loop ends with a human reading the comparison, not with a number.

Results live in the benchmarks working layer outside the repository, `~/Data/Benchmarks/<deck>/<artifact-name>/`, organized by iteration (`iteration-1/`, `iteration-2/`), one directory per test case named `eval-<ID>-<descriptive-name>`. Each configuration directory is named `<config>@<model>` (for example `with_rule@claude-opus-5`) and holds `run-<R>/` subdirectories containing `outputs/`, `grading.json`, and `timing.json`. The aggregator discovers only `eval-*` directories and `run-*` subdirectories; files placed elsewhere are ignored. Create directories as you go, not upfront.

## Prerequisites

- The artifact under test: a skill directory, a rule file, or an agent definition.
- The configuration pair for its kind:
    - **Skill**: `with_skill` runs with the skill loaded; `without_skill` runs bare.
    - **Rule**: `with_rule` runs with the rule text prepended to the task context as a project rule; `without_rule` runs the identical prompt without it.
    - **Agent**: `with_agent` runs the agent definition; `without_agent` runs a general-purpose baseline.
    - Improving an existing artifact: snapshot it first (`cp -r <artifact> <workspace>/artifact-snapshot/`) and use `new_artifact` against `old_artifact`.
- The model list. One model is a valid benchmark; several models answer how the artifact behaves down the capability curve. Name each model by an identifier the harness resolves. State the total run count (cases × configurations × models × repeats) before spawning, and get the user's go-ahead when it is large.

## Constraints

- Both configurations of a pair run the same prompts, the same assertions, and the same model; only the artifact differs. A delta computed across different models is meaningless, and the aggregator never averages across models.
- Spawn every evaluation subagent (runners, graders, comparators, analyzers) on the model that configuration names, never the session's frontier model by default.
- Grade with the exact schema the tooling depends on: `grading.json` carries an `expectations` array with `text`, `passed`, `evidence` fields and a `summary` object with `passed`, `failed`, `total`, `pass_rate`. Check programmatically verifiable assertions with a script, not by eyeballing.
- Capture `timing.json` (`total_tokens`, `duration_ms`, `total_duration_seconds`, `model`) from each completion notification as it arrives; the notification is the only place this data exists. Record unavailable values as `null`, never estimates.
- The comparison report is generated, never hand-written, and stays self-contained: it renders offline with no external requests.

## Instructions

### Write test cases

Draft 2-3 realistic test prompts, the kind that exercise exactly the behavior the artifact should change, and confirm them with the user before running. For a rule, each case is a task where the rule should alter the output; the baseline reveals what the model does on its own. Save prompts to `evals/evals.json` and one `eval_metadata.json` per case (`eval_id`, `eval_name`, `prompt`, `assertions`, which may start empty).

### Spawn all runs in the same turn

For each test case, model, and configuration, spawn a runner subagent in the same turn so everything finishes together. The run prompt names the task, the input files, and the output directory `<workspace>/iteration-<N>/eval-<ID>-<name>/<config>@<model>/run-<R>/outputs/`. The with-artifact runner gets the artifact (skill path, rule text in context, or agent definition); the baseline runner gets the identical prompt without it. Draft assertions while runs are in progress; good assertions are objectively verifiable and read clearly in the report.

### Grade and aggregate

Spawn a grader per run ([templates/agents/grader.md](templates/agents/grader.md)) writing `grading.json` into each `run-<R>/`. Then aggregate from this skill's directory:

```sh
python3 -m scripts.aggregate_benchmark <workspace>/iteration-<N> --artifact-name <name>
```

This produces `benchmark.json` and `benchmark.md` with per-configuration, per-model statistics and one delta per model. Read the results for patterns the aggregates hide (non-discriminating assertions, high-variance cases, time and token tradeoffs); [templates/agents/analyzer.md](templates/agents/analyzer.md) has the analyst instructions.

### Render the comparison

```sh
python3 -m scripts.build_report <workspace>/iteration-<N>/benchmark.json
```

The report is one self-contained HTML file: the summary matrix by model, the per-model deltas, and per-case grading detail. Put it in front of the user. For interactive per-case feedback on outputs, the bundled viewer serves the run outputs on loopback (`eval-viewer/generate_review.py <workspace>/iteration-<N> --skill-name <name> --benchmark <workspace>/iteration-<N>/benchmark.json`; add `--static <path>` in headless environments). Ask before opening a browser.

### Iterate or conclude

Read the user's feedback. Improving the artifact means generalizing from the feedback, not patching to the test set; rerun everything into `iteration-<N+1>/`, baselines included. Stop when the user is happy, the feedback comes back empty, or progress stalls. A benchmark can also conclude negatively: an artifact whose delta stays at zero on every model it targets does not earn its context cost, and that is a result.

### Blind comparison

For a rigorous "is the new version better" answer, give two outputs to an independent judge without revealing which configuration produced them ([templates/agents/comparator.md](templates/agents/comparator.md)), then analyze why the winner won. Optional; the human review loop is usually sufficient.

## Verification

- Every planned configuration-model pair has the same number of graded runs.
- `benchmark.json` reports one delta per model and no cross-model aggregate.
- The report file renders with the network disabled.
- The user has seen the comparison and their conclusion is recorded in the workspace.

## Troubleshooting

- **No subagents** (for example claude.ai): run cases yourself one at a time; skip baselines and quantitative claims, and present outputs inline.
- **Aggregator finds nothing**: check the directory contract; only `eval-*` directories with `<config>@<model>/run-<R>/grading.json` are discovered.
- **Delta missing for a model**: that model lacks one side of the configuration pair; rerun the missing side.
- **Unknown configuration names**: pass `--primary-config` and `--baseline-config` (base names, without the `@model` suffix).
