# RTK command reference

Read this file only when you select an RTK filter, meta command, or harness integration.

Each example starts an external program. Do not prefix the surrounding shell syntax or shell builtins.

## Build and compile

These filters typically reduce output by 80 to 90 percent.

```bash
rtk cargo build         # Compress Cargo build output.
rtk cargo check         # Compress Cargo check output.
rtk cargo clippy        # Group Clippy warnings by file. Typical savings: 80 percent.
rtk tsc                 # Group TypeScript errors by file and code. Typical savings: 83 percent.
rtk lint                # Group ESLint or Biome violations. Typical savings: 84 percent.
rtk prettier --check    # List only files that need formatting. Typical savings: 70 percent.
rtk next build          # Show compact route metrics. Typical savings: 87 percent.
```

## Test

These filters typically reduce output by 90 to 99 percent.

```bash
rtk cargo test          # Show only Cargo test failures. Typical savings: 90 percent.
rtk vitest run          # Show only Vitest failures. Typical savings: 99.5 percent.
rtk playwright test     # Show only Playwright failures. Typical savings: 94 percent.
rtk test <cmd>          # Wrap another test command and show only failures.
```

## Git and GitHub

These filters typically reduce output by 26 to 87 percent.

```bash
rtk git status          # Show compact status.
rtk git log             # Show compact logs with all Git flags.
rtk git diff            # Show a compact diff. Typical savings: 80 percent.
rtk git add             # Show compact confirmations. Typical savings: 59 percent.
rtk git commit          # Show compact confirmations. Typical savings: 59 percent.
rtk gh pr view <num>    # Show a compact pull request. Typical savings: 87 percent.
rtk gh pr checks        # Show compact checks. Typical savings: 79 percent.
rtk gh run list         # Show compact workflow runs. Typical savings: 82 percent.
```

Git passthrough supports all subcommands.

## JavaScript and TypeScript

These filters typically reduce output by 70 to 90 percent.

```bash
rtk pnpm list           # Show a compact dependency tree. Typical savings: 70 percent.
rtk pnpm install        # Compress installation output. Typical savings: 90 percent.
rtk npm run <script>    # Compress script output.
rtk prisma              # Remove Prisma ASCII art. Typical savings: 88 percent.
```

## Files, search, and analysis

These filters typically reduce output by 60 to 90 percent.

```bash
rtk ls <path>           # Show a compact tree. Typical savings: 65 percent.
rtk read <file>         # Read code with filtering. Typical savings: 60 percent.
rtk grep <pattern>      # Group matches by file. Typical savings: 75 percent.
rtk err <cmd>           # Show only errors from another command.
rtk log <file>          # Deduplicate log lines and show counts.
rtk json <file>         # Show JSON structure without values.
rtk summary <cmd>       # Summarize command output.
```

## Infrastructure and network

These filters typically reduce output by 65 to 85 percent.

```bash
rtk docker ps           # Show a compact container list.
rtk docker logs <c>     # Deduplicate container logs.
rtk kubectl get         # Show a compact resource list.
rtk curl <url>          # Compress HTTP responses. Typical savings: 70 percent.
```

## Meta commands

```bash
rtk gain                # Show token savings data.
rtk gain --history      # Show command history with savings.
rtk discover            # Find external commands that missed RTK.
rtk proxy <cmd>         # Run an external command without filtering.
```

## Harness integrations

- Claude Code: `rtk init --global` registers the `rtk hook claude` `PreToolUse` hook in `~/.claude/settings.json`.
- The Claude Code hook rewrites eligible external commands. Do not add manual prefixes when this hook is active.
- OpenCode: `rtk init --opencode` writes `~/.config/opencode/plugins/rtk.ts`.
- OpenCode loads that directory automatically. The plugin disables itself when RTK is absent.

- Antigravity: `rtk init --agent antigravity` writes `.agents/rules/antigravity-rtk-rules.md` in the current project.
- Antigravity ignores `--global` because this integration is project-scoped.
- Codex: `rtk init --codex` installs `AGENTS.md` and `RTK.md` without a command rewrite hook.
- The UseEfficientCLI rule tells Codex to add each required prefix.

All rewrite logic stays in the RTK binary.
