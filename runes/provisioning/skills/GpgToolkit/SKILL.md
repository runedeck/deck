---
name: GpgToolkit
description: "GPG key custody and commit signing on this machine: the toolchain and backup scripts, the decisions that set the key layout, the YubiKey touch and PIN policy, and the traps met on this Mac. USE WHEN setting up GPG signing, gpg signing failed or Timeout, YubiKey OpenPGP, sec# or ssb> stubs, keytocard, ykman hangs, paperkey or the key vault, adding a GPG UID, a commit shows Unverified. NOT FOR SSH keys and FIDO2 signing (SshToolkit) or the password store (PasswordToolkit)."
compatibility: "macOS with Homebrew. The scripts live in the provisioning codebase that PROVISION_ROOT names."
metadata:
    version: 0.2.0
---

# GpgToolkit

The primary key stays offline in an encrypted vault, the three subkeys live on the YubiKey, and git signs with OpenPGP by default. `sec#` for the primary and `ssb>` for the subkeys in `gpg -K` is the correct state. This skill keeps the facts a model cannot know: the scripts to run, the records that set the key layout, and the traps found on this machine. The GitHub-specific facts are in [GitHubKeyEndpoints.md](GitHubKeyEndpoints.md).

## Prerequisites

Resolve the provisioning codebase before the first script step:

```sh
PROVISION_ROOT="${PROVISION_ROOT:-$HOME/Developer/runedeck/provision}"
```

- `$PROVISION_ROOT/scripts/install/gpg-toolchain.sh` installs `gnupg`, `pinentry-mac`, and `ykman` from Homebrew and warns when GPG Suite is present. Idempotent.
- `$PROVISION_ROOT/scripts/install/paperkey.sh` installs `paperkey` and `qrencode`. It skips on a work-scoped machine (`SCOPE=work`).
- `$PROVISION_ROOT/scripts/configure/keyvault-scaffold.sh <mounted-volume> <key-id>` lays out the offline vault on a mounted encrypted volume: documents, markers, empty directories, and a local git repository with signing off. It writes no key material. Run it before you move secrets in, because a re-run overwrites the documents.
- `~/.gnupg/gpg-agent.conf` and `~/.gnupg/scdaemon.conf` come from chezmoi. These scripts do not write them. A `run_onchange` script disables the Keychain PIN storage of pinentry-mac and reloads the agents after each change.

## Constraints

- Install GPG from Homebrew only (GPG-0005). GPG Suite installs gpg 2.2, which fights Homebrew gnupg over `~/.gnupg`. Uninstall it when the toolchain script warns.
- Key material never leaves the vault or the card. The scaffold script moves no secret, and neither does this skill.
- Back up before any `keytocard`, offline (GPG-0004 and GPG-0006). That step replaces the on-disk secret with a stub.
- Never switch the signing format or disable signing to get past a prompt failure. SSH signing is a per-repository opt-in (ARCH-0006).
- Never import a v6 or post-quantum certificate into the daily keyring (GPG-0007). GnuPG rejects v6, and such a certificate is never a root of identity here.
- The revocation certificate never lands on the vault volume. It lives at a third location (GPG-0006).

## Instructions

### Apply the decisions

- GPG-0001: GPG stays, hardware-backed. The sign, encrypt, and auth subkeys live on the YubiKey OpenPGP applet. The host keyring holds public keys and stubs.
- GPG-0002: a new key is Curve25519, ed25519 to certify, sign, and authenticate, cv25519 to encrypt. Not RSA.
- GPG-0003: the key stays classical. Post-quantum is on only where a managed service runs it (Proton mail).
- GPG-0004: generate the key offline in a throwaway keyring, a certify-only primary with sign, encrypt, and auth subkeys. Back up, then `keytocard`.
- GPG-0005: Homebrew `gnupg` plus `pinentry-mac`. GPG Suite stays off the machine.
- GPG-0006: paperkey as a QR code plus its text output, printed on a direct-attached printer. The vault is one AES-256 container and a local git repository with no remote, ever. A restore drill decides whether a copy is trusted.
- ARCH-0006: `gpg.format openpgp`, `commit.gpgsign true`, `tag.gpgsign true`, and `user.signingkey` set to the signing subkey id with a trailing exclamation mark, which pins that subkey. Touch policy `cached` on the signature slot, `on` for encryption and authentication. `forcesig` off, so one PIN per insertion.

### Configure signing on the daily machine

1. Run the two install scripts above.
2. Import the public certificate from the vault with `gpg --import`, then `gpg --card-status` binds the stubs to the inserted card.
3. `gpg -K --keyid-format 0xlong` shows the signing subkey as the `ssb>` line tagged `[S]`. `~/.gitconfig` is chezmoi output of `dot_gitconfig.tmpl`, which renders `user.signingkey`, `gpg.format openpgp`, `commit.gpgsign`, `tag.gpgsign`, and the `gpg "ssh"` section. Set `user.signingkey` in that template to the subkey id with a trailing exclamation mark, which pins the subkey, then `chezmoi apply`. A `git config --global` write goes into `~/.gitconfig`, and the next apply reverts it.
4. Set the touch policy per card: `ykman openpgp keys set-touch sig cached`, then `dec on` and `aut on`. ykman names the encryption slot `dec` and rejects `enc`. Card settings are per card, so repeat them on every YubiKey.
5. Register the certificate with the forge. Read [GitHubKeyEndpoints.md](GitHubKeyEndpoints.md) for GitHub.

jj repositories keep model commits unsigned. Signing happens at push, and only in the owner's attended mode, so a locally unsigned jj commit is the normal state. The VersionControl skill holds that rule.

## Verification

- `gpg --card-status` lists the three subkeys against the inserted card.
- `git commit --allow-empty -m "test: signed commit"` shows the PIN dialog, the key blinks, and `git log --show-signature -1` reports a good signature.

## Troubleshooting

- `gpg: signing failed: Timeout`: pinentry could not prompt from a non-interactive shell. Export `GPG_TTY`, let pinentry-mac raise the dialog, or run the command from the owner's own terminal. The command sandbox of a coding agent cannot show the dialog. Not a method problem.
- A push times out while the LED blinks and no dialog shows: the PIN cache outlived the 15 s touch window. This machine caps it with `default-cache-ttl 12` and `max-cache-ttl 15` in `gpg-agent.conf`, so the dialog returns with each needed touch.
- `ykman` hangs after its PIN prompt, right after a gpg operation: scdaemon holds the card. `gpgconf --kill gpg-agent scdaemon`, replug the key, retry. Close Yubico Authenticator when it runs.
- gpg does not see the card: scdaemon needs `disable-ccid` on macOS. GnuPG 2.3 and later stopped the PC/SC fallback, and CryptoTokenKit owns the USB device. chezmoi writes the line.
- The `ykman` PIN prompt accepts typing but Enter does nothing or echoes `^M`: the terminal sends an untranslated CR to a raw-mode prompt. Observed in cmux, where Shift+Enter submits. Terminal.app needs no workaround.
- After a card swap the stubs still point at the old card: `gpg-connect-agent "scd serialno" "learn --force" /bye`.
- `PIN retry counter: 3 0 3` in `gpg --card-status` is the healthy factory state. The middle counter is the unset Reset Code.
- qrencode refuses the paperkey output: it rejects raw binary. Pipe `paperkey --output-type raw` through `base64` first, and decode with `base64 -d` before `paperkey --pubring` on restore.
- `sec#` in `gpg -K`: the primary is a stub, and the real one is in the vault. Expected. A UID change is an offline ceremony: add it there, re-export, re-import everywhere the key lives.
- A key update is not recognized somewhere: key blocks never sync. Import or paste the updated block into every keyring and every forge that holds it.
