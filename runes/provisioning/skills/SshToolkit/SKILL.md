---
name: SshToolkit
description: "SSH keys and git SSH signing on this machine: the YubiKey FIDO2 key scripts, the decisions on signing format and key names, the Homebrew OpenSSH and askpass plumbing, and the traps met on this Mac. USE WHEN generating or rotating an SSH key, ed25519-sk, agent refused operation, provider is not an OpenSSH FIDO library, SSH_ASKPASS or User cancelled, naming a second YubiKey, allowed_signers, editing ~/.ssh/config. NOT FOR OpenPGP signing (GpgToolkit) or the password store (PasswordToolkit)."
compatibility: "macOS with Homebrew openssh. The scripts live in the provisioning codebase that PROVISION_ROOT names."
metadata:
    version: 0.2.0
---

# SshToolkit

One YubiKey-resident FIDO2 key (`ed25519-sk`, resident, verify-required) serves SSH authentication and git SSH signing. GPG is the default commit-signing format on this machine, and SSH signing is the per-repository alternative (ARCH-0006). This skill keeps the scripts, the decisions, and the traps. [Config.md](Config.md) holds the `~/.ssh/config` facts, [Fido2.md](Fido2.md) the key, agent, and askpass facts, and [Pitfalls.md](Pitfalls.md) the symptom-to-fix list.

## Prerequisites

Resolve the provisioning codebase before the first script step:

```sh
PROVISION_ROOT="${PROVISION_ROOT:-$HOME/Developer/runedeck/provision}"
```

The provisioning order on a fresh Mac. Each script is idempotent:

1. `brew install openssh`. The Brewfile holds it. Apple's build lacks the FIDO2 middleware.
2. `$PROVISION_ROOT/scripts/install/ssh-yubikey-key.sh` generates the resident key with Homebrew's `ssh-keygen`. It reads `SSH_KEY_NAME`, `SSH_YUBIKEY_APPLICATION`, and `GIT_EMAIL` from `$PROVISION_ROOT/.env`. Set a lasting value in that file. A value you export for one run wins over the file, except `SCOPE`, which always comes from the file.
3. `gh auth login`, then `gh ssh-key add ~/.ssh/<key>.pub --title "<host> (a)"`, and the same file again with `--type signing --title "<host> (s)"`.
4. `$PROVISION_ROOT/scripts/configure/git-identity.sh` writes `user.name` and `user.email` from `.env` and refuses the example placeholders (PROV-0008).
5. `$PROVISION_ROOT/scripts/configure/git-ssh-sign.sh` installs the `git-ssh-sign-macos` wrapper into `~/.local/bin` and sets `gpg.ssh.program` to it. The chezmoi git template already renders that key with the same value, so the write changes nothing, and git reads `gpg.ssh.program` only when `gpg.format` is `ssh`. The script skips when its source clone is absent. When it skips, install the copy that the VersionControl skill includes under `scripts/` by hand at `~/.local/bin/git-ssh-sign-macos`, the path the template already names.
6. Opt one repository in, inside that repository: `git config gpg.format ssh` and `git config user.signingkey ~/.ssh/<key>.pub`. For local verification, append `<email> <key-type> <key>` to `~/.config/git/allowed_signers`. The chezmoi git template already points `gpg.ssh.allowedSignersFile` at that file.

`$PROVISION_ROOT/scripts/configure/git-signing-ssh.sh` skips by default and prints the per-repository commands. Never pass it `--global` on this machine. With that flag it writes `gpg.format ssh`, `user.signingkey <pub>`, `commit.gpgsign true`, `tag.gpgsign true`, and `gpg.ssh.allowedSignersFile` to the global config. That makes SSH the default signing format and overwrites the OpenPGP `user.signingkey` that GpgToolkit set, against ARCH-0006. The writes go into `~/.gitconfig`, which is chezmoi output, and the next `chezmoi apply` reverts them. The flag fits only a machine that has no GPG toolchain and no chezmoi.

`chezmoi apply` writes `~/.ssh/config`. The private host inventory arrives as `~/.ssh/hosts` and `~/.ssh/vendor`, linked from the private dotfiles tree.

## Constraints

- Do not edit `~/.ssh/config` by hand. Edit the chezmoi source and apply.
- `~/.gitconfig` is chezmoi output of `dot_gitconfig.tmpl`. Send a signing-key or format change to that template and apply, never to `git config --global`.
- Generate and sign with FIDO2 keys through `/opt/homebrew/bin/ssh-keygen`, never `/usr/bin/ssh-keygen` (PROV-0003).
- Keep `IdentitiesOnly yes` on the GitHub host block. Without it ssh offers every loaded key, and GitHub refuses after about six.
- Keep GPG as the signing default. Opt one repository into SSH signing with `git config gpg.format ssh` and `git config user.signingkey ~/.ssh/<key>.pub` (ARCH-0006).

## Instructions

### Apply the decisions

- ARCH-0006: GPG with the YubiKey OpenPGP slot and pinentry-mac is the default. SSH with FIDO2 is the alternative for a repository that prefers it.
- PROV-0003: a key file is `~/.ssh/yubikey_<model>_<year-or-context>`, one per physical YubiKey, such as `yubikey_5c_nano_2026` or `yubikey_5_nfc_work`. The `IdentityFile` order in `~/.ssh/config` sets the role (primary, backup). The file name carries no role. GitHub titles are `<host> (a)` for authentication and `<host> (s)` for signing: the same `.pub`, a different `--type`. The FIDO2 application string is `ssh:<github-user>`. PIN entry on signing goes through the `ssh-askpass` LaunchAgent and `SSH_ASKPASS_REQUIRE=force` in `~/.zshenv`.
- PROV-0008: the global author uses the GitHub `noreply` address. A repository on another forge gets a per-repository alias with `git config --local user.email`.

### Name and register a second YubiKey

A FIDO2 credential is bound to its hardware. Each YubiKey gets its own `ssh-keygen` run. Set `SSH_KEY_NAME` in `$PROVISION_ROOT/.env` to the new file name, then run `$PROVISION_ROOT/scripts/install/ssh-yubikey-key.sh`. Then register the `.pub` twice on GitHub, with the `(a)` and `(s)` titles. Read [Fido2.md](Fido2.md) for the re-import on a fresh machine.

### Check the resolved config

`ssh -G <host>` prints the effective settings after every `Host` and `Match` block, with no connection. Use it before and after an edit of the chezmoi source.

## Verification

- `git commit --allow-empty -m "test: signed commit"` in a repository that opted into SSH signing shows the askpass dialog, then the key blinks.
- `git log --show-signature -1` reports a good signature against `~/.config/git/allowed_signers`.

## Troubleshooting

Read [Pitfalls.md](Pitfalls.md). The two traps that cost the most time on this machine:

- `agent refused operation` on commit: the launchd `ssh-agent` of macOS refuses FIDO2 keys. The wrapper from `$PROVISION_ROOT/scripts/configure/git-ssh-sign.sh` strips `SSH_AUTH_SOCK`, so `ssh-keygen` talks to the key directly.
- `User cancelled. (-128)` when a coding agent commits: the command sandbox of the agent cannot show the askpass dialog. Stage and draft in the agent, then commit from the owner's terminal.
