Declare every secret a repository reads in `secretspec.toml` at the repository root, each with a description. Add one with `secretspec add <NAME> --description "<purpose>"`. Read a secret only through `secretspec run -- <command>` or `secretspec get <NAME>`, never from a dotenv file or a shell profile.

Never print a secret value, and never read one into the conversation. When a command needs a secret, run it under `secretspec run` and report the result. Pass a value to a program on stdin, because a process list shows every argument. Store a value with `secretspec set <NAME> --from-file -`.

Give every call a reason with `--reason "<why>"`. SecretSpec refuses an agent session that gives none, and its audit log keeps the reason beside the read.

The harness credentials live in `~/.config/rune/secretspec.toml`. `rune launch` and `rune run` read an unset `from_env` key from it. Do not export a credential in the shell to start a launch.
