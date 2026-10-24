# Benchmark report explains each case design

## Approach

The aggregator computes the label, and the report only draws it. The constraint "generate each report from `benchmark.json`" holds, and `benchmark.json` stays the one record of what each cell says. `run_card` matches each graded expectation to its frozen assertion by text, drops word-count checks, and picks a label. The report groups the runs of each case by baseline or treatment and by model, and draws one label for each group. Repeats with the same label show once, with a count.

The owner proposed the label of the first failed assertion. This change takes a failed forbidden check before a failed required check, and keeps the order inside each group. A forbidden match names what the answer did, such as "old v3 code" or "opened a browser". A missing required pattern only says what the answer lacked. With the first-failed rule, case 1 of the BrowserbaseToolkit benchmark would need its required check to carry the label "old v3 code", which is wrong for an answer that writes neither version.

Matching by text keeps the label right when an author reorders assertions between a run and a later aggregate. A check whose text has no frozen assertion counts as a content check and gives its own text.

## Commands

| Requirement | Command |
|---|---|
| Every case gets a plain-words card | `python3 -m scripts.build_report <iteration>/benchmark.json` |
| Card grid names what each answer did | the same report, the "What each case asked" section |
| Forbidden checks name the label first | `python3 -m scripts.aggregate_benchmark <iteration>` |
| Cases without labels still render | the aggregate and report commands on an older iteration |
| Check counts stay in the data and the details | the "Check details" fold under each card |
| Card labels stay short | `python3 scripts/grade_iteration.py --manifest <manifest> --validate-only` |

## Risks

- A label that reads well for one answer can mislead for another. The fold under each card keeps the evidence for every check.
- Model column names come from a pattern for Claude model ids. Any other id shows as it is.
