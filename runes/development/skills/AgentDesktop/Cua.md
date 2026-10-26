# Cua

cua runs disposable Linux, macOS and Windows boxes called Spaces, and drives them over MCP. The canonical Linux image `ghcr.io/trycua/linux:24.04` is Ubuntu 24.04 with Xfce on Xvfb, AT-SPI and no snaps ([Dockerfile][CUADF]).

## Work in a Space

1. `list_spaces`, then `create_space` with `on: "local"` and a `name`. A cold create pulled the image and took about 73 s.
2. Run commands with `space_bash`. Set `timeout` for long jobs, or start them with `nohup` and poll a log.
3. Copy a directory in with `upload`. Copy results out with `download`.
4. Drive the GUI with `computer_screenshot`, `computer_click`, `computer_type`, `computer_hotkey` and `computer_scroll`. Coordinates are in screenshot pixels.
5. For a browser, `sandbox_open_browser` starts Chromium with a throwaway profile.
6. Delete the Space with `delete_space` when the task ends.

## Run a test suite in a Space

This worked for the rune CLI on 2026-10-25, with 2370 tests passing:

1. Export a clean tree on the host: `git --git-dir=<repo>/.git archive <commit> | tar -x -C <dir>`.
2. `upload` the directory. Install the toolchain with `space_bash` (`apt-get`, `rustup`).
3. Restore executable bits. `upload` drops them, see the faults below.
4. Run `git init`, `git add -A` and `git commit` in the Space when the tests read the git `HEAD`.
5. Start the suite with `nohup` and read the log in rounds.

## Faults seen

Seen on this Mac on 2026-10-25 and 2026-10-26:

- **runc instead of gVisor.** OrbStack has no gVisor, so cua fell back to runc in OrbStack's shared VM, as its documented rule says ([Spaces reference][CUASPACES]). For one VM per box, try the `vz` microVM runtime that cua 0.9.0 offers.
- **2 CPUs.** A Space got `cpu.max` 200000/100000 on an 18-core host. `sandbox_pool_create` accepts `cpus` and `memory_mb`. This is not tested yet.
- **Relay down.** The daemon could not reach `relay.cua.ai`, and the Cua app showed 0 Spaces. Local work over MCP does not need the relay.
- **Browser state tool.** `get_browser_state` failed with "session is not available to this transport". Use screenshots and clicks instead.
- **Executable bits.** `upload` drops every executable bit. Restore them with `chmod` from a list made on the host.
- **The Space user has passwordless sudo.** For an agent without sudo, add a second user.

## Reach a Space from another device

The relay at `relay.cua.ai` connects your devices to Spaces without an open port. Without it:

- Direct over Tailscale: `cua spaces add <tailnet-name>:3211 --token "$CUA_ENV_TOKEN" --name <name>` registers the Space as `direct:<addr>` ([Add a Space][CUAADD]). Restrict port 3211 with Tailscale access rules.
- Your own relay: the open-source `cua-relay` runs anywhere, and `cua-spacesd join --relay wss://<host> --relay-token <token>` joins it ([cua-spacesd][SPACESD]). Whether the Cua app and CLI can use a custom relay is not verified.

[CUADF]: https://github.com/trycua/cua/blob/de783ee0a6eea707223f3475a4bcee6acd64b38b/libs/images/linux/Dockerfile
[CUASPACES]: https://cua.ai/docs/spaces/reference/spaces
[CUAADD]: https://cua.ai/docs/spaces/guides/add-a-space
[SPACESD]: https://github.com/trycua/cua/blob/main/libs/cua-spacesd/README.md
