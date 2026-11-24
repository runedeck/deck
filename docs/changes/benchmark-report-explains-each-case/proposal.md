---
status: proposed
decisions: []
---

# Benchmark report explains each case

## Why

The owner could not read the BrowserbaseToolkit iteration-2 report. Its case names, such as "stagehand-v4-init", and a grid of fractions such as "0 / 3" say nothing to a reader who does not know Stagehand or Browserbase. A redrawn version with one card for each case worked: a plain question, the prompt, one or two sentences on what a right answer does, and a grid that names what each answer did.

## What Changes

- A case can carry `question`, `why`, and `pass_label`. An assertion can carry `fail_label`. All four are optional.
- The aggregator gives each run a `card` with an outcome and a label, and writes the cases and the planned model order into `benchmark.json`.
- The report opens with a "What each case asked" section: one card for each case, with baseline and treatment rows, a column for each model, and a folded section with the check details.
- The manifest validator keeps each label to four words or fewer.
- `references/schemas.md` tells authors to write the question and the explanation for a reader who does not know the product.

## Capabilities

### New Capabilities

- `benchmark-report-explains-each-case`: the report shows each case as a plain-words card that names what each answer did.

## Impact

- `runes/core/skills/BenchArtifact/scripts/`: `aggregate_benchmark.py` and `run_benchmark.py`, with their tests.
- `runes/core/skills/BenchArtifact/assets/report-template.html` and `references/schemas.md`.
- The adoption sidecars of `aggregate_benchmark.py` and `schemas.md` get new subject digests.
- A manifest without the new fields renders as before, plus cards titled by case name.
