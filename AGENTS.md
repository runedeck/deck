# AGENTS.md

## Cursor Cloud specific instructions

### What this repo is

`runedeck` is a **content repository ("a deck"), not a runnable application**. There is no
web server, backend, database, or long-running service to start. "Running" the project means
validating the markdown/YAML content and deploying it into AI-harness directories with the
external [`rune`](https://github.com/runedeck/rune) CLI. See `README.md` and `deck.yaml` for the
layout, and `CONTRIBUTING.md` for content conventions (four-space indent, LF, trailing newline).

### Toolchain (baked into the VM snapshot)

The validation toolchain is pre-installed and persists in the environment snapshot:

- `rune` (the deck CLI) — built from source at `github.com/runedeck/rune` and installed to
  `~/.cargo/bin/rune`. It needs **Rust edition 2024 (rustc ≥ 1.85)**; the image's default Rust
  was 1.83, so the snapshot was upgraded with `rustup default stable`. Rebuild with
  `cargo install --path <clone> --locked` if you need a newer `rune`.
- `prek` and `semgrep` — installed via `pip3` (into `~/.local/bin`); these are the only tools the
  update script refreshes.
- `gitleaks` (v8.30.1, pinned to CI) in `/usr/local/bin`; `shellcheck` via apt.

`~/.local/bin` and `~/.cargo/bin` are added to `PATH` in `~/.bashrc`. If a tool "is not found",
confirm the shell sourced `~/.bashrc`.

### Lint / test / validate (there is no build or app to run)

- `rune validate` — validates the deck content against `schemas/*.mdschema` (fast).
- `make validate` — the full gate: runs `.githooks/pre-commit` then `.githooks/pre-push`.
- `make install` — sets `core.hooksPath=.githooks` so commits/pushes run the gate.

Non-obvious gotcha: the **pre-commit** stage only checks *staged* files, while the **pre-push**
stage checks the `origin/main..HEAD` commit range. So on a clean working tree with nothing staged,
`make validate` still exercises shellcheck / rune-validate / semgrep / gitleaks through the
push-range stage rather than skipping everything. Most hooks in `.pre-commit-config.yaml` are
type-gated (Python/Rust/TS) and never fire here because no such source files exist.

The commit/push hooks fail loudly if neither `prek` nor `gitleaks` is on `PATH` — they never
pass silently.

### Consumer / product flow (how the deck is actually used)

```sh
rune config set deck <path-to-this-clone>   # point rune at the deck
rune skill add rune                          # stage a rune into a consumer's .rune manifest
rune install                                 # deploy into .claude/.codex/.gemini/.opencode
rune doctor --target .                       # verify deployment integrity
```
