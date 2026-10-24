# Tasks

## 1. Data

- [x] 1.1 The manifest validator accepts `question`, `why`, `pass_label`, and `fail_label`, and keeps each label to four words
- [x] 1.2 The aggregator writes a `card` for each run, the case headers, and the planned model order

## 2. Report

- [x] 2.1 The template draws one card for each case with the question, the prompt, the explanation, the grid, and the check details
- [x] 2.2 `references/schemas.md` documents the fields and the authoring guidance

## 3. Verification

- [ ] 3.1 Script tests, `rune validate --skill-layers`, `rune validate`, `rune spec validate`, and `vale --no-global` on changed prose
- [x] 3.2 The BrowserbaseToolkit iteration-2 report, rendered from a labelled scratch copy, shows three cards in light and dark themes, and the pre-change aggregate renders cards titled by case name
