Use the efficient CLI tools.

When the `rtk` binary is installed, prefix every shell command with `rtk` (Rust Token Killer: <https://github.com/rtk-ai/rtk>). This is a hard requirement, not a preference. RTK compresses command output before it reaches the model. RTK passes unknown commands through unchanged, so the prefix is always safe. Prefix each command in a chain. RTK calls binaries directly and bypasses aliases. When `rtk` is not installed, run the plain command.

Search selectively. Use `fd` to find files. Use `rg` to search content. Use `ast-grep` to search code structure: a structural match returns fewer and more precise results than a regex over code. Ask GitHub for fields, not pages: `gh ... --json <fields>`, with `--jq` to select. Read only what the task needs. Never load whole directories or repositories into context.

For the rtk command tables and verification, use the RTK skill.
