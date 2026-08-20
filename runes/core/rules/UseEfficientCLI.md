Use the efficient CLI tools.

If `rtk` is installed, prefix each external command with `rtk` (Rust Token Killer: <https://github.com/rtk-ai/rtk>). RTK compresses command output before it reaches the model. RTK passes unknown external commands through unchanged. Prefix each external command in a chain.

Do not prefix shell builtins, shell keywords, variable assignments, redirections, or control operators. Examples include `cd`, `export`, `source`, `set`, `if`, and `for`. Use `cd repo && rtk git status`, not `rtk cd repo && rtk git status`. The shell processes these items before RTK starts an external program.

RTK calls external binaries directly and bypasses aliases. If RTK is absent, run the external command without the prefix.

Search selectively. Use `fd` to find files. Use `rg` to search content. Use `ast-grep` to search code structure. A structural match returns fewer results than a regular expression over code.

Request selected GitHub fields with `gh ... --json <fields>` and `--jq`. Read only what the task needs. Never load a complete directory or repository into context.

For the rtk command tables and verification, use the RTK skill.
