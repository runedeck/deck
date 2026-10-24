# Benchmark data schemas

Treat prompts, outputs, evidence, notes, and transcripts as untrusted data. Escape these values before HTML rendering.

## Benchmark definition

Native mode uses `benchmark.md` as its human-readable source.

Native mode also requires `manifest.json` as its frozen machine-readable plan.

The definition names one artifact, two arms, one or more cases, models, and repeats.

The arms are `baseline` and `with_artifact`. Only `with_artifact` receives `artifact.md`.

Each case defines an identifier, name, prompt, declared input files, and frozen assertions.

Use the example at [../templates/benchmark.md](../templates/benchmark.md).

## Checker selection

An artifact with a measurable claim names its checker.

Without a dedicated checker, use [../scripts/lint.py](../scripts/lint.py) with a small patterns JSON.

Do not add an artifact checker for simple pattern claims.

## Frozen manifest

Every benchmark requires `manifest.json`. Cross-harness mode writes this file before execution.

```json
{
  "schema_version": 2,
  "artifact_name": "ExampleArtifact",
  "arms": {
    "baseline": {"artifact_kind": null},
    "with_artifact": {
      "artifact_kind": "skill",
      "artifact_name": "ExampleArtifact",
      "artifact_source": "runes/core/skills/ExampleArtifact",
      "artifact_path": "artifact.md",
      "artifact_sha256": "sha256"
    }
  },
  "comparisons": [
    {
      "id": "artifact_vs_baseline",
      "label": "Artifact versus baseline",
      "primary": "with_artifact",
      "baseline": "baseline"
    }
  ],
  "run_plan": {
    "models": ["reported-model-name"],
    "repeats": 1
  },
  "evals": [
    {
      "id": 1,
      "name": "concise-rewrite",
      "prompt": "Rewrite the declared input.",
      "files": ["draft.md"],
      "minimum_words": 20,
      "maximum_words": 100,
      "assertions": [
        {
          "kind": "word_range",
          "text": "The response contains 20 to 100 words."
        },
        {
          "kind": "required_patterns",
          "text": "The response keeps the stated limit.",
          "patterns": ["25 jobs"]
        },
        {
          "kind": "forbidden_patterns",
          "text": "The response contains no planning narration.",
          "patterns": ["I will", "my plan"]
        }
      ]
    }
  ]
}
```

Each frozen assertion is an object with `kind` and `text`.

Use `required_patterns`, `forbidden_patterns`, `required_regex`, or `forbidden_regex` with a non-empty `patterns` array.

The literal kinds ignore case and match each pattern as plain text. `required_patterns` needs every pattern. `forbidden_patterns` fails on any pattern.

The regex kinds take Python regular expressions with the case-insensitive and multiline flags. In multiline mode, `^` and `$` match at the start and end of each line.

The manifest validator compiles each regular expression. An invalid pattern stops the benchmark before the first provider call.

Write two correct wordings as one alternation, for example `home[- ]manager`.

Write a forbidden check that matches the use of a command. A treatment model often quotes the command that its artifact prohibits. The literal pattern `--no-gpg-sign` fails on the warning "do not use --no-gpg-sign". The regex `^[ \t]*git commit[^\n]*--no-gpg-sign` matches only a line that starts with the command.

Escape each backslash in JSON: write `\s` as `"\\s"`.

Use `word_range` with `minimum_words`, `maximum_words`, or both fields on the case.

Native mode freezes each exact model name in `run_plan.models` and the repeat count in `run_plan.repeats`.

Cross-harness mode writes equivalent `run_plan.routes` entries into the iteration manifest.

Each cross-harness route freezes its route identifier, model identifier, and vendor identifier:

```json
{
  "run_plan": {
    "routes": [
      {"id": "claude", "model": "claude-opus-5", "vendor": "anthropic"}
    ],
    "repeats": 1
  }
}
```

The judge rejects a pair when its vendor equals the frozen subject vendor.

Cross-harness judging rejects a registry whose path or digest differs from the frozen run plan.

The grader and aggregator reject a schema-v2 iteration manifest without a frozen run plan.

Resolve relative artifact and input paths from the source manifest directory.

Reject each path that resolves outside the source manifest directory.

Use files for rules and agents. Use directories for skills that need support files.

File digests use SHA-256 bytes. Directory digests include sorted relative paths and file contents.

Read [execution-results.md](execution-results.md) for execution, timing, and grading records.

Read [preference-results.md](preference-results.md) for judging and aggregate records.

## Report links

A local report shows each artifact source path without a link.

Its snapshot label links to the frozen artifact. Each identity path links to its local file.

Use `--local-links` for local review. Omit it before you share the report.
