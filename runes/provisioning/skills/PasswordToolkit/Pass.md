# Pass

The store inherits the YubiKey custody model (GPG-0001): decrypting any entry needs the card, with one PIN per insertion (ARCH-0006). Verified: `pass` 1.7.4 at `/opt/homebrew/bin/pass`, with `pass-otp` from the install script.

## Store rules

- Line 1 of an entry is the secret. Later lines are metadata: `login:`, `url:`, an `otpauth://` URI for `pass otp`. Write such an entry from a variable, never from a literal on the command line: `printf '%s\nlogin: <login>\n' "$secret" | pass insert -m -f <path>`. Read line 1 in a script with `pass show <path> | head -1`.
- `pass git init` turns on history, and every change then auto-commits. Add a `.gitignore` with `.DS_Store` and `._*` before the first commit, or the init commit sweeps Finder files into history. For files already tracked: `git ls-files -z | grep -zE '(^|/)\.DS_Store$|(^|/)\._' | xargs -0 git rm --cached --`.
- No remote (GPG-0006). Entry names are plaintext paths even though contents are encrypted, and the ciphertext is a decrypt-later target. The backup is a dated copy of the whole store in the `pass/` directory of the vault, refreshed when the vault is.
- `git -C ~/.password-store config commit.gpgsign false`: store commits are bookkeeping.

## Migrate the store to a new key

The migration is one `pass init` with both keys reachable: the old card decrypts, the new key encrypts.

1. `cat ~/.password-store/.gpg-id` shows the old id, often a subkey id.
2. The old public key must be in the keyring, with no trust setting needed. If it left, recover it from GitHub as the GitHubKeyEndpoints companion of GpgToolkit describes.
3. Insert the old YubiKey. Run `gpg-connect-agent "scd serialno" "learn --force" /bye`, then `gpg --card-status` binds the old stubs to the card.
4. Take the safety copy first: `cp -a ~/.password-store <backup-copy>`, where `<backup-copy>` does not exist yet. The live store stays where it is. The other direction, `cp -a <copy> ~/.password-store` onto an existing store, nests the copy inside it as `~/.password-store/<name>/`, and the next step then keeps a duplicate of every entry under the old key.
5. `pass init <new-key-id>` decrypts each entry with the old card, encrypts it to the new key, and rewrites `.gpg-id`. A touch per entry happens only when the old card has an encryption touch policy. A subdirectory with its own `.gpg-id` needs `pass init -p <subdir> <new-key-id>` as well.
6. Insert the new YubiKey and run the `learn --force` line again. `pass show <entry>` and `pass otp <otp-entry>` must both succeed before the backup copy goes.
