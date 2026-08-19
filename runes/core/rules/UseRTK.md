When the `rtk` binary is installed, prefix every shell command with `rtk` (Rust Token Killer: <https://github.com/rtk-ai/rtk>). This is a hard requirement, not a preference. RTK compresses command output before it reaches the model. RTK passes unknown commands through unchanged, so the prefix is always safe. Prefix each command in a chain.

RTK calls binaries directly and bypasses aliases. When `rtk` is not installed, run the plain command. For the command tables and verification, use the RTK skill.
