---
name: RTK
description: "RTK (Rust Token Killer), a token-optimized CLI proxy. USE WHEN rtk, token savings, optimize tokens, reduce tokens, compress command output, run builds or tests or git with less output."
metadata:
    version: 0.1.0
    upstream: https://github.com/rtk-ai/rtk
---

# RTK

RTK is a CLI proxy that compresses command output before it reaches the model. It saves 60 to 90 percent of the tokens on common development operations.

## Constraints

- Prefix every shell command with `rtk`. If RTK has a filter for the command, it uses the filter. If not, it passes the command through unchanged, so the prefix is always safe.
- Prefix each command in a chain. `rtk git add . && rtk git commit` needs `rtk` on both sides of `&&`.
- RTK calls binaries directly and bypasses shell aliases. Use `command` only for alias-prone commands that RTK does not cover (`cd`, `cp`, `mv`, `rm`).
- If `rtk` is not installed, run the plain command. Do not fail the task over a missing proxy.

## Instructions

### Build and compile (80-90% savings)

```bash
rtk cargo build         # Cargo build output
rtk cargo check         # Cargo check output
rtk cargo clippy        # Clippy warnings grouped by file (80%)
rtk tsc                 # TypeScript errors grouped by file/code (83%)
rtk lint                # ESLint/Biome violations grouped (84%)
rtk prettier --check    # Files needing format only (70%)
rtk next build          # Next.js build with route metrics (87%)
```

### Test (90-99% savings)

```bash
rtk cargo test          # Cargo test failures only (90%)
rtk vitest run          # Vitest failures only (99.5%)
rtk playwright test     # Playwright failures only (94%)
rtk test <cmd>          # Generic test wrapper, failures only
```

### Git and GitHub (26-87% savings)

```bash
rtk git status          # Compact status
rtk git log             # Compact log (works with all git flags)
rtk git diff            # Compact diff (80%)
rtk git add             # Compact confirmations (59%)
rtk git commit          # Compact confirmations (59%)
rtk gh pr view <num>    # Compact PR view (87%)
rtk gh pr checks        # Compact PR checks (79%)
rtk gh run list         # Compact workflow runs (82%)
```

Git passthrough works for all subcommands, including subcommands this list omits.

### JavaScript and TypeScript tooling (70-90% savings)

```bash
rtk pnpm list           # Compact dependency tree (70%)
rtk pnpm install        # Compact install output (90%)
rtk npm run <script>    # Compact npm script output
rtk prisma              # Prisma without ASCII art (88%)
```

### Files, search, and analysis (60-90% savings)

```bash
rtk ls <path>           # Tree format, compact (65%)
rtk read <file>         # Code reading with filtering (60%)
rtk grep <pattern>      # Search grouped by file (75%)
rtk err <cmd>           # Errors only, from any command
rtk log <file>          # Deduplicated logs with counts
rtk json <file>         # JSON structure without values
rtk summary <cmd>       # Smart summary of command output
```

### Infrastructure and network (65-85% savings)

```bash
rtk docker ps           # Compact container list
rtk docker logs <c>     # Deduplicated logs
rtk kubectl get         # Compact resource list
rtk curl <url>          # Compact HTTP responses (70%)
```

### Meta commands

```bash
rtk gain                # Show token savings analytics
rtk gain --history      # Command usage history with savings
rtk discover            # Find missed optimization opportunities
rtk proxy <cmd>         # Execute the raw command without filtering
```

### Install the harness integrations

Each harness has its own integration path. All rewrite logic lives in the rtk binary.

- Claude Code: `rtk init --global` registers a `PreToolUse` hook (`rtk hook claude`) in `~/.claude/settings.json`. The hook rewrites eligible commands before execution. Do not add manual prefixes where the hook is active.
- OpenCode: `rtk init --opencode` writes `~/.config/opencode/plugins/rtk.ts`. OpenCode auto-loads that directory; the plugin disables itself when the binary is absent.
- Antigravity: project-scoped only. `rtk init --agent antigravity` writes `.agents/rules/antigravity-rtk-rules.md` into the current project and ignores `--global`.
- Codex has no hook mechanism. The UseRTK rule is the codex path: the model adds the prefix itself.

## Verification

```bash
rtk --version         # shows: rtk X.Y.Z
rtk verify            # checks the hook registration and the data directory
rtk gain              # works (not "command not found")
which rtk             # the correct binary
```

If `rtk gain` fails with "command not found", the machine may have reachingforthejack/rtk (Rust Type Kit) instead. If it fails on the tracking database, the process cannot write `~/Library/Application Support/rtk/`; the rewrites still work and only the accounting is lost.

A compact two-line `git status` is the live proof that a rewrite hook is active.

## References

- <https://github.com/rtk-ai/rtk>
