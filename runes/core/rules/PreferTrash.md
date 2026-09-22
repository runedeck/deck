Delete a user file or directory with `trash <path...>`, never with `rm`. The command is `scripts/trash` in every runedeck repository and `~/.local/bin/trash` on the owner's machines, the same script. It moves the item into the FreeDesktop trash under `~/.local/share/Trash` on macOS and Linux and records the original path and the time, so every deletion is recoverable. It does not call Finder or Apple Events, so it runs inside the command sandbox like any other command, alone or in a chain.

`rm` stays for scratch and regenerable content only: a `mktemp` directory, `build/` output, a cache. A path that this session did not create, or that cannot be regenerated, goes to the trash.

Recover an item with `mv ~/.local/share/Trash/files/<name> <original path>`. The original path is in `~/.local/share/Trash/info/<name>.trashinfo`.
