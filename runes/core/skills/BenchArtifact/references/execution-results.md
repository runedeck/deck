# Benchmark execution results

## Execution result

Write `result.json` in each run directory. Write the final response to `outputs/response.md`.

The JSON response and word count must match `response.md` exactly.

Cross-harness mode also writes unparsed stdout to `outputs/provider-output.txt`.

```json
{
  "schema_version": 2,
  "eval_id": 1,
  "eval_name": "concise-rewrite",
  "arm": "with_artifact",
  "model": "reported-model-name",
  "repeat": 1,
  "state": "valid",
  "duration_seconds": 12.4,
  "response": "Final response.",
  "word_count": 2,
  "usage": {
    "input_tokens": null,
    "cache_creation_input_tokens": null,
    "cache_read_input_tokens": null,
    "output_tokens": null,
    "total_tokens": null
  },
  "notes": []
}
```

Use these executor states:

- `valid`
- `provider_failure`
- `timeout`
- `invalid_output`
- `preflight_failure`
- `context_failure`
- `model_mismatch`

The aggregator can add `missing_execution` and `missing_grading`.

## Timing result

Native mode writes `timing.json` from the harness completion notification.

Record `duration_seconds`, `total_tokens`, and `model`. Use `null` for unavailable values.

## Grading result

Write `grading.json` beside `result.json`.

```json
{
  "expectations": [
    {
      "text": "The response keeps the stated limit.",
      "passed": true,
      "evidence": "The response states 25 jobs."
    }
  ],
  "summary": {"passed": 1, "failed": 0, "total": 1, "pass_rate": 1.0},
  "lint": {"total": 2, "total_per100w": 1.6, "words": 125},
  "notes": []
}
```

Preferences remain separate from assertions and checker findings.
