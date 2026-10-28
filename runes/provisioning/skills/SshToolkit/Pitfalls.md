# Pitfalls

Symptom, then the fix that worked on this machine.

- `Too many authentication failures` from GitHub: `IdentitiesOnly yes` is missing from the host block. ssh offered every loaded key.
- `provider is not an OpenSSH FIDO library`, or an `ed25519-sk` key that fails to load: Apple's `/usr/bin/ssh-keygen` ran. Use `/opt/homebrew/bin/ssh-keygen`.
- `agent refused operation` on `git commit`: the launchd `ssh-agent` got the signing request. Run `$PROVISION_ROOT/scripts/configure/git-ssh-sign.sh`, which installs the wrapper and sets `gpg.ssh.program`. Check with `git config --global --get gpg.ssh.program`.
- ssh waits forever for a passphrase or PIN, with no dialog: `SSH_ASKPASS` is not in this process. Launch from a terminal, or `launchctl setenv SSH_ASKPASS_REQUIRE force` together with the askpass path.
- `User cancelled. (-128)` from the commit of a coding agent: the command sandbox cannot open the dialog. Commit from the owner's terminal.
- The first clone on a fresh Mac fails with `Host key verification failed` and then `ssh_askpass not found`: `~/.ssh/config` and the askpass formula are not in place yet. Run the dotfiles apply and the Brewfile first, then clone.
- `ssh-add -K` does nothing: the YubiKey is not plugged in, or it holds no resident credential. `ssh-keygen -K` in a scratch directory shows what the key holds.
- `$PROVISION_ROOT/scripts/configure/git-ssh-sign.sh` prints a skip: its wrapper source clone is absent. Install the wrapper from the `scripts/` directory of the VersionControl skill at `~/.local/bin/git-ssh-sign-macos`. The chezmoi git template already points `gpg.ssh.program` there.
