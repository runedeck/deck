---
name: Chezmoi
description: "The owner's chezmoi setup: the engine decision, the bootstrap script in the provisioning codebase, the live files that are template renders, and the traps found on this machine. USE WHEN bootstrapping dotfiles on a fresh machine, changing a chezmoi-managed file such as the Claude settings or the rune config, a value vanished after chezmoi apply, a placeholder appeared in a target, or adding a private value to a template. NOT FOR general chezmoi documentation or choosing a dotfiles tool."
compatibility: "Verified with chezmoi 2.73 on macOS. Scripts live in the provisioning codebase at $PROVISION_ROOT."
metadata:
    version: 0.2.0
---

# Chezmoi

chezmoi is the dotfiles engine on this machine. This skill holds the facts a model cannot know without the owner: the decision behind the engine, the script that bootstraps it, the live files that are template renders, and the traps found here. The upstream reference covers the rest.

## Prerequisites

- `chezmoi` on `PATH`. The Brewfile of the provisioning codebase installs it.
- The provisioning codebase at `$PROVISION_ROOT`, with `DOTFILES_REPO` set in its `.env` before the bootstrap.
- [Gotchas.md](Gotchas.md), before an edit to a file that chezmoi renders.

## Constraints

- Edit the chezmoi source. The next `chezmoi apply` replaces a live edit of a rendered target.
- Do not run `chezmoi apply` from an agent sandbox. The sandbox cannot write the chezmoi state database, and the harness policy allows read-only chezmoi commands only. The owner applies.
- A template never calls `pass`. Every harness policy denies the password store, so a per-apply lookup fails inside an agent sandbox. Private values enter through the chezmoi config at `chezmoi init`, see [Gotchas.md](Gotchas.md).
- Do not write an account name, a host name, or a secret into a source file. The public repository carries placeholders.

## Instructions

### Apply the owner's decision

ARCH-0005, in `$PROVISION_ROOT/docs/decisions/`, chose chezmoi with the traditional `pass` store as the secret backend. The owner chose it because a day-to-day apply must not need a cloud round trip, and because chezmoi has a built-in `pass` template function. Practice replaced that second reason: a template calls no `pass` function, because every harness sandbox denies the store. Instead, `.chezmoi.toml.tmpl` reads the private values once, at `chezmoi init`, into `[data.private]` of the chezmoi config. `passage` is the escape hatch if GPG key management costs too much.

Plugins and sub-repositories come through `.chezmoiexternal.toml`, never git submodules or `run_onchange_` scripts. Each third-party external is an archive pinned at a release with a SHA-256, and a weekly workflow opens a pull request when a pin moves. The conventions of the source tree are in [Attributes.md](Attributes.md).

### Bootstrap a machine

The owner runs the configure script outside an agent sandbox. It ends in `chezmoi apply`, which writes the chezmoi state database and the targets under `$HOME`, and both fail under Seatbelt. An agent prepares the `.env` and hands over the command:

```sh
PROVISION_ROOT="${PROVISION_ROOT:-$HOME/Developer/runedeck/provision}"
"$PROVISION_ROOT/scripts/configure/dotfiles.sh"
```

The script skips when `DOTFILES_REPO` is unset and refuses the placeholder from `.env.example`. It probes the repository with `git ls-remote`, so a private repository fails with a `gh auth login` hint instead of a clone error. Without a source it runs `chezmoi init --apply`, with one it runs `chezmoi apply`. The source lives at the chezmoi default, which `chezmoi source-path` prints.

### Change a rendered file

Find the source with `chezmoi source-path <target>`. These live files on this machine are template renders, and the next apply replaces a live edit:

- `~/.claude/settings.json`: rendered by `dot_claude/modify_private_settings.json.tmpl`, with the permission rules from `.chezmoidata/harness/claude.json`. The script prints the template and copies back only three keys from the live file: `hooks`, `model`, and `outputStyle`. An apply replaces every other key the app wrote, plugins and marketplaces included, and registers no hook.
- `~/.config/rune/config.yaml`: rendered by `dot_config/rune/modify_config.yaml.tmpl`. An apply replaces every key except `.setup`.
- `~/.gitconfig`: rendered by `dot_gitconfig.tmpl`. An apply rewrites the file.

Edit the source, then hand the apply to the owner. [Commands.md](Commands.md) gives the drift check for a `modify_` template that works inside the sandbox.

### Capture a GUI change

Apps such as Zed write their own config. chezmoi owns the live file, and `$PROVISION_ROOT/scripts/configure/zed.sh` seeds it only when absent. After a change in the app, capture it with `chezmoi re-add <target>`. This works because those sources are plain files. `re-add` skips a template.

## Verification

- `chezmoi verify` exits 0, or `chezmoi diff` shows only the intended change.
- `chezmoi managed` lists the new target after an add.

## Troubleshooting

[Gotchas.md](Gotchas.md) lists the traps found on this machine with the fix that worked: a vanished rune profile, a settings diff of hundreds of lines, a plugin that stops after an apply, a placeholder written into a target, a silent `re-add`, an apply blocked in the sandbox, and a missing dcg hook entry.

## References

- `$PROVISION_ROOT/docs/decisions/ARCH-0005 Dotfiles engine chezmoi.md`: the engine and secret store decision.
- `$PROVISION_ROOT/docs/decisions/ARCH-0008 Config home dotfiles vs provisioning.md`: what belongs in dotfiles.
- <https://www.chezmoi.io/reference/>: the upstream reference.
