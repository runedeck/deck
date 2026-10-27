---
name: DotfilesScope
description: "Where a setting lives on this machine: per-user runtime configuration in the chezmoi dotfiles source, and the path from a fresh machine to that state in the provisioning codebase at $PROVISION_ROOT."
---

# DotfilesScope

Per-user runtime configuration that follows the owner to every machine lives in the chezmoi dotfiles source. Find it with `chezmoi source-path`, or `chezmoi source-path <target>` for one file. A source name follows the `dot_` convention: `dot_config/<app>/config` deploys to `~/.config/<app>/config`. Examples: the shell, git, ssh, tmux, ghostty, starship, and the Claude and Codex settings.

What gets a fresh machine to that state lives in the provisioning codebase at `$PROVISION_ROOT`, default `~/Developer/runedeck/provision`: the Brewfile and the other manifests, `scripts/install/*.sh`, `scripts/configure/*.sh`, `scripts/verify/*.sh`, and the decision records. A configure script may run `chezmoi apply`, or seed a file that chezmoi does not manage yet, but the canonical content of a config stays in the dotfiles source, never under the codebase's `manifests/`.

The boundary test (ARCH-0008): "what should my machine look like once it is set up?" goes to dotfiles. "How do I get a fresh machine to that state?" goes to the provisioning codebase. When in doubt, the config belongs in dotfiles.

Capture a touched config in the same session: edit the chezmoi source, let the owner run `chezmoi apply`, because the agent sandbox cannot write the chezmoi state database, then verify with `chezmoi diff`. A live file that chezmoi renders from a template loses a direct edit at the next apply. When a configure script and a dotfile write the same target, the dotfile is canonical, and the script becomes redundant.
