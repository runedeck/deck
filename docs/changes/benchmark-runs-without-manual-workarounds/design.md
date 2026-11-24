# Benchmark runs without manual workarounds design

## Approach

The run step already writes the frozen manifest to `iteration-<N>/manifest.json`. The wrapper gets one helper that returns this path, and the grade, judge, report, and quick steps call it. The matrix step keeps the source manifest, because it is the step that freezes the plan. The alternative was a `frozen_manifest` key in the configuration file. A second key could point at a different file than the one the run step wrote, so the wrapper derives the path instead.

The aggregator checks the checker fields only when the checker reports a reliable density. An unreliable run must still have a grading file with finite assertion totals, so a run with no grading stays `missing_grading`. The corpus and verdict code already skip null densities. The verdict of such a pair is "No checker data", or a failure label when assertions regress or fail. The alternative was a density computed from fewer than 40 words. The checker sets that threshold so that one finding in a one-word answer does not read as 100 findings per 100 words.

The example route drops `--clean-harness-state` for `--clean`. The owner's working route registries already use `--clean`.

The owner chose regular-expression kinds on 2026-10-24. The alternative was an any-of group: a `patterns` entry that is a list of literal wordings. It reads more easily, but a literal forbidden string still fails on a warning that quotes it. A regular expression can anchor the forbidden match to a line that starts with the command. The grader searches with `re.IGNORECASE | re.MULTILINE`, and `validate_manifest` compiles each pattern with the same flags. The grader and the validator take the flags from one constant in `run_benchmark.py`.

## Commands

| Role | Command |
|---|---|
| Run the matrix and freeze the plan | `python3 scripts/bench.py run <config.json>` |
| Grade, judge, and report from the frozen plan | `python3 scripts/bench.py grade\|judge\|report <config.json>` |
| Script tests | `python3 -m unittest discover -s scripts -p 'test_*.py'` from the BenchArtifact directory |

## Risks

- A reader of an old `benchmark.json` sees `missing_grading` for short answers. The report step regenerates the file from the run records, which this change does not touch.
- A verdict that was "Not comparable" can now be "Fails required meaning". The graded assertions of the matched pairs support that label.
