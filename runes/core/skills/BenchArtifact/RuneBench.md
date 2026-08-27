# Cross-harness Rune benchmark

Read this companion only when the user requests cross-harness execution.

## Purpose

Use Rune for explicit provider routes, clean harness state, timeouts, and structured output parsing.

The native procedure remains the default. Cross-harness mode keeps the wider model and harness matrix available.

## Requirements

- Install Python 3.11 or later.
- Install Rune and verify its path with `rune --version`.
- Define every model route in a JSON route registry.
- Configure CLIProxyAPI credentials through Rune environment references.
- Keep credentials out of the route registry.

## CLIProxyAPI routes

Route Grok and Antigravity models through CLIProxyAPI. Do not use official Grok or Antigravity login state.

Use Claude as the compatible harness for these two model routes:

- `grok@claude` selects `grok-4.6`.
- `antigravity@claude` selects `gemini-3.6-flash-high`.

Define both profiles under `launch.profiles.claude` in the Rune configuration.

Set `ANTHROPIC_BASE_URL` to the CLIProxyAPI endpoint. Resolve `ANTHROPIC_AUTH_TOKEN` from `CLIPROXY_API_KEY`.

The route registry invokes Rune, not `grok` or `agy`:

```json
{
  "routes": {
    "grok-cliproxy": {
      "binary": "rune",
      "model": "grok-4.6",
      "vendor": "xai",
      "argv": [
        "--json", "run", "grok@claude", "--model", "grok-4.6",
        "--repo", "{scratch}", "--mode", "read-only",
        "--prompt-file", "{prompt_file}", "--clean-harness-state"
      ],
      "artifact_argv": ["--system-prompt-file", "{artifact}"],
      "response": "json",
      "context_canary": "List visible artifact rules. Reply CLEAN when none are visible.",
      "forbidden_context_markers": ["artifact-name"]
    }
  }
}
```

Use the same structure for `antigravity@claude`.

## Execution

The cross-harness flag is mandatory. It prevents accidental provider launches from the native workflow.

Use `scripts/bench.py` when one configuration must drive all cross-harness steps.
All configured paths resolve from the configuration file directory.

The common matrix keys are `manifest`, `routes`, `comparison`, `iteration`, `seed`, and `artifact_name`.
The optional `repeats` and `timeout` keys default to one and 600 seconds.
Set `approve` only after the user approves the exact provider-call count.

The snapshot step also needs `artifact_source`, `snapshot`, and `treatment_arm`.
Use `manifest_template` when the step must preserve an unchanged manifest template.
The snapshot directory must be below the generated manifest directory.
The driver stores `artifact_path` relative to the generated manifest.

The grade step needs `grader` and `checker`.
The optional `checker_config` key supplies checker configuration.

The judge step needs `judge_script` and a `judges` list.
Each judge entry names one `route`, a `models` list, and an optional approved call count.

The quick step needs nonempty `quick.routes` and `quick.cases` lists.
It accepts an optional `quick.iteration` value and defaults to 999.
Set `quick.approve` only after the user approves the exact call count.
The quick step never calculates its own approval.

Validate the call count without a provider call:

```sh
python3 scripts/run_benchmark.py --cross-harness --plan \
  --workspace <workspace> --iteration <N> --manifest <evals.json> \
  --routes <routes.json> --repeats 1 --seed <seed>
```

Run only route checks when required:

```sh
python3 scripts/run_benchmark.py --cross-harness --preflight-only \
  --workspace <workspace> --iteration <N> --manifest <evals.json> \
  --routes <routes.json> --repeats 1 --seed <seed>
```

Run an approved matrix:

```sh
python3 scripts/run_benchmark.py --cross-harness \
  --workspace <workspace> --iteration <N> --manifest <evals.json> \
  --routes <routes.json> --repeats 3 --seed <seed> --approve <provider-call-count>
```

The runner prints progress for each route check and matrix run.

It stores raw stdout in `outputs/provider-output.txt` before response parsing.

It stores the parsed final response in `outputs/response.md`.

## Grading

Run the same deterministic grader that native mode uses:

```sh
python3 scripts/grade_iteration.py --iteration <workspace>/iteration-<N> \
  --manifest <workspace>/iteration-<N>/manifest.json --checker <checker.py>
```

Add `--checker-config <rules.json>` when the checker needs a configuration.

## Blind judging

State the judgment call count before execution. One judge call covers one matched pair.

Each judge route also uses one preflight call and one context-canary call.

Assign each model to a judge route from another vendor.

Plan each judge assignment without provider calls:

```sh
python3 scripts/judge_preferences.py --cross-harness --plan \
  --iteration <workspace>/iteration-<N> \
  --manifest <workspace>/iteration-<N>/manifest.json \
  --routes <routes.json> --judge-route <route> --seed <seed> \
  --model <model>
```

Repeat `--model` for each model assigned to the same judge route.

Remove `--plan` to run the assignment. Add `--approve <provider-call-count>` when the total is more than 20.

## Boundaries

- The runner executes argument vectors without a shell.
- Each invocation uses a unique scratch directory.
- Each route receives only declared inputs and treatment resources.
- A context canary must pass before matrix execution.
- A model mismatch stops the matrix.
- A reused iteration with matrix data is invalid.
- Cross-harness execution uses the network.
- The runner writes only to the selected benchmark workspace.

## Result

The runner freezes routes, models, cases, arms, comparisons, paths, and digests in `manifest.json`.

Each completed invocation retains its raw provider output. Failed routes remain explicit records.
