# Benchmark preference results

## Blind preference result

The optional manifest `judging` object formalizes the fixed criteria:

```json
{
  "judging": {
    "dimensions": [
      {
        "id": "clarity",
        "label": "Clarity",
        "criterion": "Prefer the text that a reader can understand without resolving ambiguity.",
        "weight": 1
      },
      {
        "id": "fluency",
        "label": "Fluency",
        "criterion": "Prefer natural connected prose. Penalize awkward or staccato wording.",
        "weight": 0.5
      },
      {
        "id": "directness",
        "label": "Directness",
        "criterion": "Prefer the text that states useful information sooner.",
        "weight": 1
      }
    ],
    "guards": [
      "Do not judge factual accuracy or completeness. Deterministic assertions test those requirements."
    ]
  }
}
```

The judge builds its prompt from these dimensions and guards.

The aggregator copies the block into `benchmark.json`. The report shows each criterion beside its scores.

Without the block, the judge uses the default clarity, fluency, and directness criteria.

When present, `dimensions` must contain clarity, fluency, and directness exactly once.

Each dimension needs a non-empty `label` and `criterion`.

Each optional weight must be from 0 through 1. A weight of 0 disables the verdict dimension.

Each optional `trade_off` or `win` threshold must be from 0 through 1.

Each `trade_off` threshold must be less than its effective `win` threshold.

Each dimension accepts an optional `weight`, `trade_off`, and `win` value.

A weight below 1 marks a trade-off as soft. A soft trade-off still produces a warning verdict.

The default weight is 1. Fluency has a default weight of 0.5.

Dimension thresholds replace the report defaults for that dimension.

The optional manifest `metrics` array replaces the report's metric definitions:

```json
{
  "metrics": [
    {"id": "checker", "label": "Checker /100w", "definition": "Checker findings for each 100 checked words.", "example": "4.89 to 1.09 means most findings disappeared."}
  ]
}
```

The aggregator copies the array into `benchmark.json` as `metric_definitions`. The report renders each entry in its Metric definitions section and in the matching column popup. Without the array, the report uses its default definitions.

Store judgments under `preferences/<comparison>/eval-<ID>/<model>/run-<R>.json`.

Record the blind order. Record one winner and one reason for each judging dimension.

Each winner is the primary arm, baseline arm, or `tie`.

The native parent adds arm mappings after the blind judge writes its raw result:

```json
{
  "schema_version": 2,
  "comparison": "artifact_vs_baseline",
  "eval_id": 1,
  "model": "reported-model-name",
  "repeat": 1,
  "judge_model": "other-vendor-model",
  "seed": 123,
  "blind_order": {"A": "with_artifact", "B": "baseline"},
  "state": "valid",
  "clarity_winner": "A",
  "clarity_winner_arm": "with_artifact",
  "clarity_reason": "Output A is easier to understand."
}
```

Add the equivalent winner, arm, and reason fields for fluency and directness.

## Aggregated benchmark

`aggregate_benchmark.py` writes `benchmark.json` and `benchmark.md`.

The aggregate keeps named arms, explicit comparisons, matched pairs, exclusions, notes, and limitations.

Corpus ratios use total findings and total words from matched outputs.

The aggregator calculates each model verdict once. The JSON stores its status, label, and explanation points.

The Markdown and HTML reports render this stored verdict.

The checker density must improve before the verdict can report an improvement.

Each enabled preference dimension needs one judgment for each matched pair.

The preference explanation uses the metric judgment count, not the matched-pair count.

The report calculates missing verdict fields in older schema-v2 aggregates with the same Python implementation.

The aggregate contains no cross-model average.

The report omits a verdict when fewer than half of the planned pairs are valid.
