---
type: proof
change: benchmark-report-explains-each-case
recorded: 2026-11-16
transcript: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
scenes:
- scenario: benchmark-report-explains-each-case#every-case-gets-a-plain-words-card/reader-opens-a-report-with-labelled-cases
  kind: unproven
- scenario: benchmark-report-explains-each-case#card-grid-names-what-each-answer-did/baseline-answer-writes-old-code
  kind: unproven
- scenario: benchmark-report-explains-each-case#forbidden-checks-name-the-label-first/answer-fails-a-required-and-a-forbidden-check
  kind: unproven
- scenario: benchmark-report-explains-each-case#cases-without-labels-still-render/older-iteration-is-aggregated-again
  kind: unproven
- scenario: benchmark-report-explains-each-case#check-counts-stay-in-the-data-and-the-details/reader-opens-the-check-details
  kind: unproven
- scenario: benchmark-report-explains-each-case#card-labels-stay-short/author-writes-a-long-pass-label
  kind: unproven
---

# Proof: benchmark-report-explains-each-case

One scene per scenario, in closure order. The candidates are the aggregator and the report builder of the BenchArtifact skill, `scripts/aggregate_benchmark.py` and `scripts/build_report.py`, with the report template and the manifest validator. Each scene runs the real scripts on a stored run. No scene calls a model.

The stored run is the second iteration of the BrowserbaseToolkit benchmark: three cases, a baseline and the skill, three models, one run each. Its frozen manifest predates the card fields. It is outside the repository, at `runedeck/BrowserbaseToolkit-deck/iteration-2` under `ROOT_BENCHMARK`, which defaults to `~/Data/Benchmarks`. So the scenes run on the owner's machine. Every scene works on a copy in the runner's scratch directory and never writes to the stored run. The runner removes the copy when the scene ends.

The scenes use the files beside this one:

- `card-labels.json` holds the question, the explanation, the pass label, and the fail labels of the three cases.
- `label-manifest.py` adds those fields to the frozen manifest of the copy. It changes nothing else, so the stored answers still match their cases.
- `render-stored-run.sh` copies the stored run, aggregates the copy, builds the report, and writes the page as a browser renders it to `rendered.html`. With `--labels` it runs `label-manifest.py` first. It prints each command before it runs. The first scene runs the same commands one by one.
- `report-cards.py` prints the case cards of the rendered page as text: the title, the quoted prompt, the explanation, and each grid cell with its color.

The report draws its cards with a script in the page, so the scenes need a browser. They use Google Chrome without a window and with a profile directory inside the scratch directory. `BROWSER_BINARY` names another Chromium binary. Record from the repository root, outside the command sandbox, because the sandbox does not let the browser start:

```sh
rune proof run benchmark-report-explains-each-case
rune proof run benchmark-report-explains-each-case --check
```

## benchmark-report-explains-each-case#every-case-gets-a-plain-words-card/reader-opens-a-report-with-labelled-cases

The copy of the stored run gets the card fields. The aggregator and the report builder run on it. Each card of the rendered page shows the question as its title, the prompt as the models received it, and the explanation.

```console
$ sh -c 'cp -R "${ROOT_BENCHMARK:-$HOME/Data/Benchmarks}/runedeck/BrowserbaseToolkit-deck/iteration-2" iteration'
$ rm iteration/benchmark.json iteration/benchmark.md iteration/report.html
$ sh -c 'python3 "$RUNE_PROOF_ROOT/docs/proofs/benchmark-report-explains-each-case/label-manifest.py" iteration/manifest.json "$RUNE_PROOF_ROOT/docs/proofs/benchmark-report-explains-each-case/card-labels.json"'
labelled 3 of 3 cases
$ sh -c 'PYTHONPATH="$RUNE_PROOF_ROOT/runes/core/skills/BenchArtifact" python3 -m scripts.aggregate_benchmark iteration'
Generated: iteration/benchmark.json
$ sh -c 'PYTHONPATH="$RUNE_PROOF_ROOT/runes/core/skills/BenchArtifact" python3 -m scripts.build_report iteration/benchmark.json'
Generated: iteration/report.html
$ sh -c '"${BROWSER_BINARY:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}" --headless --disable-gpu --no-first-run --user-data-dir="$PWD/browser-profile" --dump-dom "file://$PWD/iteration/report.html" > rendered.html 2> browser.log'
$ sh -c 'python3 "$RUNE_PROOF_ROOT/docs/proofs/benchmark-report-explains-each-case/report-cards.py" rendered.html'
cards: 3
card 1: Write the code that starts a cloud browser
  prompt: Write the TypeScript that starts a Stagehand session on Browserbase with the current Stagehand V4 API, reading the key from the environment. Return only one code block.
  why: Stagehand is Browserbase's code library for steering a browser from a script. Its version 4 changed how a script starts, and version 3 code no longer runs.
...
card 2: List the settings a Browserbase project needs
  prompt: List only the environment variables a Browserbase plus Stagehand project must set, one per line, with no other text.
  why: Browserbase finds the project from the API key alone. Older guides also ask for a project ID, which sends the reader after a value they do not need.
...
card 3: Get the text of a page that refused a normal fetch
  prompt: Your web fetch tool returned HTTP 403 for https://docs.example.com/config, and you need the exact text of that page. You have the Browserbase browse CLI installed and BROWSERBASE_API_KEY set. Give the first shell command you run. Return only one code block.
  why: Browserbase's browse command can fetch a page without starting a browser. Opening a browser session for one page uses the plan's browser hours.
...
```

## benchmark-report-explains-each-case#card-grid-names-what-each-answer-did/baseline-answer-writes-old-code

In the first case, every baseline answer fails the check that forbids old code. The grid has a row without the skill and a row with it, and a column for each model. Each baseline cell shows the label of that check in red. Each cell with the skill shows the pass label in green. No cell shows a fraction.

```console
$ sh -c 'sh "$RUNE_PROOF_ROOT/docs/proofs/benchmark-report-explains-each-case/render-stored-run.sh" --labels'
...
$ sh -c 'python3 "$RUNE_PROOF_ROOT/docs/proofs/benchmark-report-explains-each-case/report-cards.py" rendered.html'
cards: 3
card 1: Write the code that starts a cloud browser
...
  models: Opus 5.5 | Fable 5.1 | Haiku 5.5
  Without skill | old v3 code (red) | old v3 code (red) | old v3 code (red)
  With skill | current v4 code (green) | current v4 code (green) | current v4 code (green)
...
```

## benchmark-report-explains-each-case#forbidden-checks-name-the-label-first/answer-fails-a-required-and-a-forbidden-check

The baseline answer of one model to the first case misses both required patterns and matches the forbidden one. The aggregate gives the run the fail label of the forbidden check, and the grid cell shows it. The word-count check passed and picks no label.

```console
$ sh -c 'sh "$RUNE_PROOF_ROOT/docs/proofs/benchmark-report-explains-each-case/render-stored-run.sh" --labels'
...
$ jq -r '.runs[] | select(.eval_id == "1" and .arm == "baseline" and .model == "claude-opus-5-5") | (.expectations[] | (if .passed then "passed" else "failed" end) + ": " + .text), "card: " + .card.outcome + ", " + .card.label' iteration/benchmark.json
failed: Uses the V4 factory.
failed: Launches the browser through the Browserbase factory.
failed: Uses no V3 constructor or init call outside a comment.
passed: The answer has 3 to 200 words.
card: fail, old v3 code
$ jq -r '.evals[0].assertions[] | .kind + ": " + (.fail_label // "no fail label")' iteration/manifest.json
required_patterns: no v4 start call
required_patterns: no Browserbase launch
forbidden_regex: old v3 code
word_range: no fail label
```

## benchmark-report-explains-each-case#cases-without-labels-still-render/older-iteration-is-aggregated-again

The aggregator runs on the stored run as it is, with the frozen manifest that predates the card fields. The report shows one card for each case. The case name is the title, and the check texts are the labels.

```console
$ sh -c 'sh "$RUNE_PROOF_ROOT/docs/proofs/benchmark-report-explains-each-case/render-stored-run.sh"'
...
$ jq -r '.evals[] | [.name, (.question // "no question"), (.pass_label // "no pass label")] | join(" | ")' iteration/manifest.json
stagehand-v4-init | no question | no pass label
required-env | no question | no pass label
fetch-after-403 | no question | no pass label
$ sh -c 'python3 "$RUNE_PROOF_ROOT/docs/proofs/benchmark-report-explains-each-case/report-cards.py" rendered.html'
cards: 3
card 1: Case 1: stagehand-v4-init
...
  why: (none)
  models: Opus 5.5 | Fable 5.1 | Haiku 5.5
  Without skill | Uses no V3 constructor or init call outside a comment. (red) | Uses no V3 constructor or init call outside a comment. (red) | Uses no V3 constructor or init call outside a comment. (red)
  With skill | passed every check (green) | passed every check (green) | passed every check (green)
card 2: Case 2: required-env
...
  Without skill | Does not list a project id. (red) | Does not list a project id. (red) | Does not list a project id. (red)
  With skill | passed every check (green) | passed every check (green) | passed every check (green)
card 3: Case 3: fetch-after-403
...
  With skill | passed every check (green) | passed every check (green) | passed every check (green)
```

## benchmark-report-explains-each-case#check-counts-stay-in-the-data-and-the-details/reader-opens-the-check-details

The aggregate keeps the passed and total checks of every run and the result of every check. The check details of the second card list each run with its counts, and every check with its result and evidence.

```console
$ sh -c 'sh "$RUNE_PROOF_ROOT/docs/proofs/benchmark-report-explains-each-case/render-stored-run.sh" --labels'
...
$ jq -r '.runs[] | select(.eval_id == "2") | [.arm, .model, ((.result.assertions_passed | tostring) + " of " + (.result.assertions_total | tostring)), ((.expectations | length | tostring) + " checks kept")] | join(" | ")' iteration/benchmark.json
with_artifact | claude-opus-5-5 | 3 of 3 | 3 checks kept
with_artifact | claude-fable-5-1 | 3 of 3 | 3 checks kept
with_artifact | claude-haiku-5-5 | 3 of 3 | 3 checks kept
baseline | claude-opus-5-5 | 2 of 3 | 3 checks kept
baseline | claude-fable-5-1 | 2 of 3 | 3 checks kept
baseline | claude-haiku-5-5 | 2 of 3 | 3 checks kept
$ sh -c 'python3 "$RUNE_PROOF_ROOT/docs/proofs/benchmark-report-explains-each-case/report-cards.py" rendered.html --details 2'
check details of card 2: List the settings a Browserbase project needs
Without skill · Opus 5.5 · run 1 · 2/3 checks
  ✓ Lists the API key. · Missing: none.
  ✕ Does not list a project id. · Forbidden text: PROJECT_ID
  ✓ The answer has 1 to 40 words. · [..]
...
With skill · Haiku 5.5 · run 1 · 3/3 checks
  ✓ Lists the API key. · Missing: none.
  ✓ Does not list a project id. · [..]
  ✓ The answer has 1 to 40 words. · [..]
```

## benchmark-report-explains-each-case#card-labels-stay-short/author-writes-a-long-pass-label

The frozen manifest of the copy gets a pass label of five words. The manifest validator rejects it and names the field. The scene shows the last line of the error, because the lines above it hold local paths. The benchmark runner calls the same validator before its first provider call.

```console
$ sh -c 'cp "${ROOT_BENCHMARK:-$HOME/Data/Benchmarks}/runedeck/BrowserbaseToolkit-deck/iteration-2/manifest.json" manifest.json'
$ sh -c 'python3 "$RUNE_PROOF_ROOT/docs/proofs/benchmark-report-explains-each-case/label-manifest.py" manifest.json "$RUNE_PROOF_ROOT/docs/proofs/benchmark-report-explains-each-case/card-labels.json" --pass-label "1=current version four start code"'
labelled 3 of 3 cases
$ jq -r '.evals[0].pass_label' manifest.json
current version four start code
$ sh -c 'python3 "$RUNE_PROOF_ROOT/runes/core/skills/BenchArtifact/scripts/grade_iteration.py" --manifest manifest.json --validate-only 2> error.log'
? 1
$ tail -n 1 error.log
ValueError: manifest eval 1 pass_label must be one to 4 words
```
