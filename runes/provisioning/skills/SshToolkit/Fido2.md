# FIDO2 key, agents, and askpass

## The key

`$PROVISION_ROOT/scripts/install/ssh-yubikey-key.sh` runs Homebrew's `ssh-keygen` with `-t ed25519-sk -O resident -O verify-required -O application="ssh:<github-user>" -C "<email>" -f ~/.ssh/<key>`. Resident means `ssh-keygen -K` re-derives the handle files from the YubiKey on another machine. Verify-required means PIN plus touch on every use. The application string lets one YubiKey hold several resident SSH credentials. The private blob never leaves the YubiKey, so `~/.ssh/<key>` and its `.pub` need no backup.

Apple's `/usr/bin/ssh-keygen` knows the algorithm but lacks the `libsk-libfido2` wrapper. Pointing it at the raw `libfido2.dylib` through `SSH_SK_PROVIDER` fails with `provider is not an OpenSSH FIDO library` (PROV-0003 tried it). Homebrew's `openssh` formula pulls `libfido2` and works. The script hard-codes `/opt/homebrew/bin/ssh-keygen`.

## Re-import on a fresh machine

`ssh-add -K` imports every resident key into the agent, and `ssh-keygen -K` writes the handle files into the current directory under its own names. Both need the YubiKey plugged in and Homebrew's binaries. Move the extracted files to the PROV-0003 name afterwards.

## Two agents

The launchd `ssh-agent` of macOS lacks the libfido2 middleware. It loads ordinary keys with Keychain passphrases and refuses `ed25519-sk` with `agent refused operation`. Keep it for Keychain-cached keys. For signing, `$PROVISION_ROOT/scripts/configure/git-ssh-sign.sh` installs the `git-ssh-sign-macos` wrapper, which strips `SSH_AUTH_SOCK` so Homebrew's `ssh-keygen` reaches libfido2 and the YubiKey directly. `gpg.ssh.program` points at the wrapper. SSH login and agent forwarding keep Apple's agent.

## Askpass

`ssh-askpass` (Homebrew, from a third-party tap in the Brewfile) is the Cocoa PIN dialog. Its LaunchAgent exports `SSH_ASKPASS=/opt/homebrew/opt/ssh-askpass/bin/ssh-askpass`, `SUDO_ASKPASS`, and a placeholder `DISPLAY` for GUI sessions. `~/.zshenv` exports `SSH_ASKPASS_REQUIRE=force`, so ssh always tries the dialog instead of a TTY prompt.

The trap: a process that inherits launchd's environment without the LaunchAgent misses `SSH_ASKPASS` and hangs, or fails with `agent refused operation` and no dialog. Launch the app from a terminal, or export through launchd with `launchctl setenv SSH_ASKPASS /opt/homebrew/opt/ssh-askpass/bin/ssh-askpass` and `launchctl setenv SSH_ASKPASS_REQUIRE force`. That survives until reboot.

Outside a sandbox, an inline `SSH_ASKPASS=/opt/homebrew/opt/ssh-askpass/bin/ssh-askpass SSH_ASKPASS_REQUIRE=force` before the git command makes the dialog appear. Inside the command sandbox of a coding agent the dialog cannot open, and the failure reads `User cancelled. (-128)`. The owner then commits from a terminal with GUI access.

## Allowed signers

The file git reads here is `~/.config/git/allowed_signers`, not `~/.ssh/allowed_signers`: `gpg.ssh.allowedSignersFile` in the chezmoi git template points at it. One entry is `<email> <key-type> <key>`, the email in front of the first two fields of the `.pub`. Append it by hand. `$PROVISION_ROOT/scripts/configure/git-signing-ssh.sh` appends the same line, but every other write of that script is global and switches the machine to SSH signing (SKILL.md). The file enables `git verify-commit` and `git log --show-signature` locally. GitHub keeps its own list.
