---
name: AgentDesktop
description: "Drive a desktop GUI inside a disposable box: create a cua Space or a Parallels agent VM, run commands in it, click, type, take screenshots, read the accessibility tree, then throw the box away. USE WHEN computer use in a sandbox, GUI or browser testing, a Linux box for an agent, a throwaway VM, cua Spaces, Parallels agent VMs, the STC base image, or resuming the agent VM work. NOT FOR the owner's own desktop (use the computer-use tool), cloud browsers (BrowserbaseToolkit), or shell work that needs no GUI."
compatibility: "macOS on Apple silicon. cua needs its MCP server or its CLI. Parallels needs Parallels Desktop Pro or higher for prlctl and linked clones. prlctl must run outside the agent's command sandbox."
metadata:
    version: 0.1.0
---

# AgentDesktop

Gives an agent a desktop it can wreck. The box is the security boundary, so an agent inside it may run with bypassed permissions.

## Prerequisites

- cua: the `cua` MCP server, or the cua CLI. Version 0.9.0 of the CLI ships in `/Applications/Cua Spaces.app/Contents/MacOS/cua` and is not on `PATH`.
- Parallels: Parallels Desktop 27 Pro or higher, and the stopped base VM `STC`.
- The helper scripts in [scripts/](scripts/), [guest/](guest/) and [seed/](seed/).

## Constraints

- Run agents with bypassed permissions only inside a box. Copy files in. Never mount a host directory, and keep host sharing off.
- Never type a password, key or token into a box. The `agent` user has no password and no sudo. Root work goes through `prlctl exec` or `space_bash`.
- A box is disposable: delete it after its task. Start `STC` only to update it, then take a new snapshot.
- Name each Parallels VM with [scripts/new-agent-vm.sh](scripts/new-agent-vm.sh). It picks a free Warhammer 40,000 title and never adds a number.

## Instructions

### Choose a backend

Capabilities, as cua Space then Parallels agent VM:

- **New Linux box:** `create_space` on `local`, about 73 s cold. A linked clone of `STC`, about 1 s, with `exec` after about 12 s.
- **Shell:** `space_bash`. `prlctl exec` as root, with `runuser -l agent` for the desktop.
- **Files in and out:** `upload`, `download`, `space_write`. [scripts/run-in-guest.sh](scripts/run-in-guest.sh).
- **Screenshot:** `computer_screenshot`. `prlctl capture` on the host, or `scrot` in the guest.
- **Mouse and keyboard:** `computer_click`, `computer_type`, `computer_hotkey`, `computer_scroll`. `xdotool` in the guest, and `prlctl send-key-event` for the console.
- **Accessibility tree:** `computer_get_accessibility_tree`. `pyatspi` in the guest.
- **Browser:** `sandbox_open_browser` with Chromium. Firefox from Mozilla's deb, with the terms accepted by policy.
- **Snapshot and fork:** checkpoint and fork. `prlctl snapshot` and linked clones.
- **Coding agent inside:** `agent_start`. Claude Code and Codex are installed and signed out.
- **Reach from another device:** the relay, or direct over Tailscale. The Parallels window.

Prefer cua. Use Parallels for a full VM with a real Xorg display, or when cua's faults block the task.

### cua Spaces

Create, use and delete Spaces as [Cua.md](Cua.md) describes. Read its fault list before a long task.

### Parallels agent VMs

Create a VM with `scripts/new-agent-vm.sh <purpose>`, start it, wait with `scripts/wait-exec.sh <vm> 120`, and work through `prlctl exec`. [Parallels.md](Parallels.md) covers the base image, updates and traps.

### Drive the desktop

Run GUI commands as `agent` on display `:0`. [Desktop.md](Desktop.md) gives the commands for clicks, typing, screenshots and the accessibility tree.

## Verification

- `prlctl exec <vm> hostname` prints the VM name. For cua, `space_bash` with `uname -a` answers.
- A screenshot shows the window the task expects.
- The accessibility tree lists the application under test.

## Troubleshooting

- `prlctl` fails with `/bin/ps: Operation not permitted`: it ran inside the command sandbox. Run it as the whole command line or from a script outside the sandbox.
- `prlctl exec` fails with `PrlJob_GetResult` or `Unable to open new session`: retry. A long command line fails every time, so use `run-in-guest.sh`.
- A Space is slow: it has 2 CPUs. See the CPU note in [Cua.md](Cua.md).
- More traps: [Parallels.md](Parallels.md#traps) and [Cua.md](Cua.md#faults-seen).

## References

- [cua Spaces reference](https://cua.ai/docs/spaces/reference/spaces), [cua lifecycle](https://cua.ai/docs/cua-sdk/guides/lifecycle), [cua MCP tools](https://cua.ai/docs/cua-cli/reference/mcp-tools).
- [Parallels command-line reference](https://docs.parallels.com/landing/parallels-desktop-developers-guide/command-line-interface-utility), [linked clones, KB 122669](https://kb.parallels.com/en/122669).
- The cua skills `cua-spaces`, `cua-sandboxes`, `cua-driver` and `gui-automation` cover the cua tools in more depth.
