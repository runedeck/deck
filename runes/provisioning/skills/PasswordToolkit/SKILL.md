---
name: PasswordToolkit
description: "Secrets on this machine: pass (the GPG password store, encrypted to the YubiKey key) and pass-cli (Proton Pass). The install script, the decisions on custody, sync, and backup, and the traps met on this Mac. USE WHEN storing or reading a secret, password, API key, license, or TOTP from the CLI, pass init or a store migration to a new YubiKey, pass show hangs or No secret key, Proton Pass CLI, pass-cli login or a personal access token, deciding where a credential lives. NOT FOR GPG key custody itself (GpgToolkit) or SSH keys (SshToolkit)."
compatibility: "macOS with Homebrew. Verified with pass 1.7.4 and Proton Pass CLI 2.5.1. pass-cli needs a paid Proton Pass plan."
metadata:
    version: 0.2.0
---

# PasswordToolkit

Two tools, two stores. `pass` keeps each secret as a GPG file under `~/.password-store`, encrypted to the YubiKey key, so every read needs the card (GPG-0001). `pass-cli` is Proton's official client for Proton Pass vaults. They are different binaries with different stores. One never replaces the other. [Pass.md](Pass.md) holds the store rules and the migration to a new key. [ProtonPass.md](ProtonPass.md) holds the Proton facts.

## Prerequisites

Resolve the provisioning codebase before the first script step:

```sh
PROVISION_ROOT="${PROVISION_ROOT:-$HOME/Developer/runedeck/provision}"
```

- `$PROVISION_ROOT/scripts/install/pass.sh` installs `pass` and `pass-otp` from Homebrew. It skips on a work-scoped machine (`SCOPE=work`). The extension is installed at `/opt/homebrew/lib/password-store/extensions/otp.bash`.
- `brew install proton-pass-cli` installs the `pass-cli` binary. The formula is in homebrew-core and in the Brewfile. It needs a paid Proton Pass plan.
- `pass init <key-id>` with the YubiKey key id, so entries encrypt to the card. `.gpg-id` in the store records it.

## Constraints

- Never put a secret in a command argument, in `echo`, or in a tracked file. Pipe it: `printf '%s' "$secret" | pass insert -e <path>`.
- The store never gets a networked remote (GPG-0006). Entries are encrypted to an ECC subkey, ECC falls to a quantum computer, so harvested ciphertext is a decrypt-later target. The backup is a dated copy of the whole store, `.git` included, in the `pass/` directory of the encrypted vault.
- Store commits are bookkeeping only: `git -C ~/.password-store config commit.gpgsign false` keeps them out of global signing.
- Proton keys stay in Proton (PROV-0010). A Proton Pass export gives decrypted data, never a key, and the Proton role of the YubiKey is FIDO2 account 2FA.
- The personal access token for `pass-cli` lives in `pass`, never in a tracked file, scoped to the one vault it needs. It reaches `pass-cli login` through the `PROTON_PASS_PERSONAL_ACCESS_TOKEN` variable, never through `--pat`.

## Instructions

### Choose the tool

- A secret under your own key, readable offline, or machine-local: `pass`. The default when unsure.
- A secret that already lives in a Proton Pass vault, a shared vault, or a CI job without interactive login: `pass-cli`, with a personal access token in CI.
- A TOTP code: `pass otp <path>` for store entries, `pass-cli item totp <item>` for Proton items.

### Use the store

Read [Pass.md](Pass.md) for the commands, the first-commit rules, and the migration of the store to a new YubiKey key.

### Use Proton Pass

Read [ProtonPass.md](ProtonPass.md) for login, tokens, and secret injection with `pass-cli run` and `pass-cli inject`.

## Troubleshooting

- `pass show` hangs: pinentry needs a terminal. `export GPG_TTY=$(tty)`, and check that `gpg-agent` runs. The command sandbox of a coding agent cannot show the PIN dialog, so read the entry from the owner's terminal.
- `No secret key` or `decryption failed`: the card is not inserted, or the store is encrypted to another key id. Compare `.gpg-id` with `gpg --card-status`.
- Reads fail after a card swap although the card is in: `gpg-connect-agent "scd serialno" "learn --force" /bye` rebinds the stubs.
- `pass otp` not found: `pass-otp` is missing. Run the install script.
- Completions missing right after the install: a stale compinit cache. Find it with `zsh -ic 'echo $_comp_dumpfile'`, remove that file, then `exec zsh`.
