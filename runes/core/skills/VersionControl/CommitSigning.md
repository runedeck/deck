# Commit Signing

The runedeck specification keeps model commits unsigned. This companion covers repositories that do sign, with a hardware key. Two valid options exist. On macOS, prefer GPG with the YubiKey OpenPGP slot and `pinentry-mac`. SSH with FIDO2 (`sk-ssh-ed25519`) is the alternative. GitHub and GitLab accept both, but on macOS the SSH path needs a wrapper around Apple's `ssh-agent`.

## GPG (preferred)

Configure git to sign with the YubiKey's OpenPGP signing subkey:

```sh
git config --global gpg.format openpgp
git config --global user.signingkey <KEY-ID>!         # trailing ! pins to the signing subkey
git config --global commit.gpgsign true
git config --global tag.gpgsign true
```

`pinentry-mac` (brew cask `pinentry-mac`) handles the PIN entry GUI through `~/.gnupg/gpg-agent.conf`:

```
pinentry-program /opt/homebrew/bin/pinentry-mac
```

Set the cache TTL values to match your touch policy. A cache shorter than the touch window makes the pinentry dialog reappear together with each needed touch, so the dialog cues the touch. `gpg-agent` finds the YubiKey on the first signing operation. Touch the YubiKey when the LED blinks.

## Batch re-signing: the `-c` config leak

You need a re-signing rewrite when the commit email does not match the signing key. Prevent it: set `user.email` to the key's email in every colocated repo and every submodule before the first commit. The recovery:

```sh
git -c commit.gpgsign=false rebase --root --force-rebase \
    --exec 'git commit --amend --no-edit -S'
```

The `-S` is load-bearing. `git -c` exports the override through `GIT_CONFIG_PARAMETERS`, which every child process inherits. Without an explicit `-S`, the amend sees `commit.gpgsign=false` and silently produces unsigned commits. The absence of hardware prompts during a signing rebase is the tell. Verify after any batch rewrite:

```sh
git log --format='%h %G? %ae %s'    # expect G on every line
```

## SSH with FIDO2 (alternative)

```sh
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/<keyname>.pub
git config --global commit.gpgsign true
```

### Apple's bundled `ssh-agent` refuses FIDO2

**Symptom**: `git commit` fails immediately with `agent refused operation`, although `ssh-add -L` shows the SK key and the YubiKey is present.

**Root cause**: the launchd `ssh-agent` on macOS has no FIDO2 support. When git signs, `ssh-keygen` consults `SSH_AUTH_SOCK`, hits Apple's agent, and gets the refusal.

**Verification**:

```sh
ssh-add -T ~/.ssh/<keyname>.pub                                   # agent path: expect "agent refused operation"
env -u SSH_AUTH_SOCK ssh-keygen -Y sign -f ~/.ssh/<keyname>.pub \
    -n git <<< test                                               # direct path: expect a valid signature
```

**Fix**: install the one-line wrapper shipped with this skill and point git at it:

```sh
install -m 0755 ./scripts/git-ssh-sign-macos ~/.local/bin/git-ssh-sign-macos
git config --global gpg.ssh.program ~/.local/bin/git-ssh-sign-macos
```

The wrapper strips `SSH_AUTH_SOCK` so `ssh-keygen` talks to libfido2 and the YubiKey directly. SSH login and agent forwarding keep Apple's agent. Reverse with `git config --global --unset gpg.ssh.program`.

### `SSH_ASKPASS` is per-shell, not per-user

The PIN-entry dialog fires only when the signing process's environment exports `SSH_ASKPASS`. GUI-launched processes inherit launchd's environment and miss a `~/.zshenv` export. Either launch the app from a terminal, or export through launchd:

```sh
launchctl setenv SSH_ASKPASS /opt/homebrew/bin/ssh-askpass
launchctl setenv SSH_ASKPASS_REQUIRE force
```

`launchctl setenv` survives until reboot; persist it with a LaunchAgent plist.

### Verify signatures

```sh
git log --show-signature -1
git verify-commit HEAD
```

Local verification of SSH signatures needs `~/.ssh/allowed_signers` and `git config --global gpg.ssh.allowedSignersFile ~/.ssh/allowed_signers`, one `email key namespace="git"` entry per line.
