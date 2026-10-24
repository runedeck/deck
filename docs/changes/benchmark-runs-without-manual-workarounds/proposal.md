---
status: proposed
decisions: []
---

# Benchmark runs without manual workarounds

## Why

The owner evaluated the forge-provision skills on 2026-10-20 and the BrowserbaseToolkit port on 2026-10-22. The records are in `~/Data/Benchmarks/forge-provision/` and `~/Data/Benchmarks/runedeck/BrowserbaseToolkit-deck/`. Each evaluation needed hand fixes before the BenchArtifact pipeline finished, and each fix repeats on the next run:

- The wrapper grade step gave the grader the source manifest, which has no run plan. The grader stopped with "manifest needs a frozen run_plan", the error of the [run plan check][RUNPLAN]. The report step had the same mismatch.
- The example route in the cross-harness companion passes `--clean-harness-state`. The help of `rune run` in rune 0.6.0 lists `--clean` and no `--clean-harness-state`.
- A pattern assertion matches literal text and needs every pattern. One assertion cannot accept "home-manager" and "Home Manager". A forbidden check fails on a warning that quotes the forbidden command.
- The aggregator excludes a run as `missing_grading` when the [generic checker][CHECKER] counts fewer than 40 prose words. The BrowserbaseToolkit iteration had every assertion graded, but its report said "Not comparable" with 0 pairs for all three models.

## What Changes

- The wrapper gives the grade, judge, and report steps the frozen manifest of the iteration. The quick step does the same for its scratch iteration.
- The example route uses `--clean`.
- An unreliable checker density no longer excludes a graded run. The density fields of the run are null, and the run pairs on its assertion results. The verdict then reports missing checker data instead of no pairs.
- New `required_regex` and `forbidden_regex` assertion kinds take case-insensitive, multiline Python regular expressions. The manifest validator compiles them before any provider call. The literal kinds keep their behavior.
- The schema reference tells authors to write two wordings as one alternation, and to shape a forbidden expression as a command line.

## Capabilities

### New Capabilities

- `benchmark-runs-without-manual-workarounds`: the cross-harness pipeline finishes from one configuration file, and short answers keep their assertion results in the comparison.

## Impact

- `runes/core/skills/BenchArtifact/scripts/`: `bench.py`, `aggregate_benchmark.py`, `grade_iteration.py`, and `run_benchmark.py`, with their tests.
- `runes/core/skills/BenchArtifact/`: `RuneBench.md`, `references/schemas.md`, and `references/preference-results.md`.
- The adoption sidecars of `aggregate_benchmark.py` and `schemas.md` get new subject digests.
- An iteration aggregated before this change keeps its old `benchmark.json`. Run the report step again to pair its short answers.

[RUNPLAN]: ../../../runes/core/skills/BenchArtifact/scripts/run_benchmark.py
[CHECKER]: ../../../runes/core/skills/BenchArtifact/scripts/lint.py
