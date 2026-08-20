---
name: RTK
description: "Use RTK to reduce external-command output. USE WHEN rtk, token savings, compact builds, tests, Git, GitHub, logs, or command output. NOT FOR shell builtins, shell syntax, or RTK installation."
compatibility: "Verified with RTK 0.45.0. Plain external commands remain valid without RTK."
metadata:
    version: 0.1.0
    upstream: https://github.com/rtk-ai/rtk
---

# RTK

RTK is a CLI proxy that compresses command output before it reaches the model. It reduces output by 60 to 90 percent for common development commands.

## Constraints

- If RTK is installed, prefix each external command with `rtk`.
- Do not prefix shell builtins, shell keywords, assignments, redirections, control operators, or other shell syntax.
- Prefix each external command in a chain. Leave the shell syntax unchanged.
- RTK starts external binaries directly and bypasses shell aliases.

- RTK returns the external command exit status.
- A wrapped command keeps its file, network, GUI, and external-state effects.
- If RTK is absent, run the external command without the prefix.

## Instructions

### Prefix an external command

Place `rtk` before the external program and its arguments.

This form is incorrect because RTK cannot start the `cd` shell builtin:

```bash
rtk cd repo && rtk git status
```

This form lets the shell process `cd` and lets RTK start Git:

```bash
cd repo && rtk git status
```

Use the same rule for `export`, `source`, `set`, `if`, `for`, assignments, redirections, and control operators.

### Select an RTK command

Use normal external-command syntax after the `rtk` prefix. RTK passes an unknown external command through unchanged.

Read [CommandReference.md](CommandReference.md) when you need a filter, raw output, meta command, or harness integration.

### Configure a harness

Read [CommandReference.md](CommandReference.md#harness-integrations) when a harness must add RTK automatically.

Do not add manual prefixes where an active hook already rewrites eligible external commands.

## Verification

```bash
command -v rtk       # The shell finds the intended binary.
rtk --version        # RTK prints its version.
rtk verify           # RTK checks its integration and data directory.
rtk gain             # RTK prints token savings data.
```

A compact `git status` result proves that an RTK filter or rewrite hook is active.

## Troubleshooting

If `rtk gain` reports `command not found`, `reachingforthejack/rtk` (Rust Type Kit) can be installed instead.

If RTK cannot write `~/Library/Application Support/rtk/`, accounting stops. Command filtering continues.

## References

- [CommandReference.md](CommandReference.md): command filters, meta commands, and harness integrations.
- <https://github.com/rtk-ai/rtk>
