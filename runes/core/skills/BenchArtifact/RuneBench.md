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
  --routes <routes.json> --repeats 3 --seed <seed> --approve <run-count>
```

The runner prints progress for each route check and matrix run.

It stores raw stdout in `outputs/provider-output.txt` before response parsing.

It stores the parsed final response in `outputs/response.md`.

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
