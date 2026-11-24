# Evals

Each rune that has an eval suite keeps it here, one directory per rune. A suite proves that the rune changes what a model does: every case runs twice, once with the rune loaded and once without it, and the record keeps both scores.

## Layout

```text
evals/<RuneName>/
├── <case-name>/
│   ├── prompt.md          the task, with max_turns and allowed_tools in frontmatter
│   └── graders/*.md       one grader per file
└── records/               written by scripts/eval-rune, one JSON file per run
```

The case format is the one `claude plugin eval` reads. The runner builds a throwaway plugin around the rune's assembled Claude instance, so a case tests what Claude Code actually loads. A plugin cannot hold a rule file. The runner therefore injects a rule at session start through a hook, and only the run with the rune gets that hook.

## Writing a case

- Give each rune two or three cases. One case asks for the behavior head-on. One case is a near miss, where the rune should hold even though the task does not mention it.
- Use deterministic graders only: `regex`, `tool_used`, `tool_order`, and `file_exists`. A model judge cannot sign in from the eval's child sessions on this machine, and a pattern either matches or it does not.
- Shape a forbidden pattern as real usage, for example a command at the start of a line. A model that follows a rule often quotes the thing the rule forbids, and a bare word would fail it.
- A case must be able to fail. Run it once before you trust it: the run without the rune must score lower. When both runs pass a case, it proves nothing, so rewrite it or drop it.
- Keep `max_turns` at four or fewer and `allowed_tools` read-only. A skill whose procedure reads companion files may use six. The cases test what the model says and plans. They leave the disk alone.
- Never edit a rune to make its own case pass. When a rune fails its case, either the rune is weak or the case is wrong. Say which in the change that fixes it.

## Running a suite

```sh
scripts/eval-rune <RuneName> [--model <id>] [--runs <n>] [--record <dir>] [--canon]
```

`--canon` removes a skill's harness and model variants before assembly. Run it beside a normal run to see whether a variant beats the canon alone.

The runner launches Claude Code through a `rune launch` profile, `main` by default, so the profile supplies the model route and its credential. The eval starts full Claude Code sessions, so it runs outside the command sandbox. `--record <dir>` records the run with asciinema and renders a GIF that shows each case's scores and the answers with and without the rune.

## Records

A record holds the rune's name and kind, the layer it tested (`assembled` or `canon`), the SHA-256 digest of the assembled instance, the model, the run count, the time, the Claude Code version, the overall score, the mean difference that the rune makes, and each case's scores with and without the rune. A record is evidence of one run. A new run adds a record and never rewrites an old one.

A harness or model variant beside a canon earns its place only when its record beats the canon's record on the same cases and the same model.
