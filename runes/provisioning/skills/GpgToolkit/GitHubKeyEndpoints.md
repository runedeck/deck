# GitHub key endpoints

GitHub publishes every key on an account at unauthenticated endpoints: OpenPGP keys at `github.com/<user>.gpg`, SSH public keys at `github.com/<user>.keys`. Everything inside a key block is public, the UID names and addresses included. A `noreply` author address hides nothing while the key UID carries the real address. PROV-0008 sets the author address per forge for that reason: the GitHub `noreply` address globally, a per-repository alias elsewhere.

## Facts that apply here

- Treat a GPG UID as a public identity statement. Put only a name and an address that may appear on the open web in it.
- Register the public certificate with `gh gpg-key add <cert.asc>`. A key title on GitHub carries the subkey-usage suffix after the host name: `(s)`, `(e)`, `(a)`, or `(c)`, the same convention as the SSH titles `(a)` and `(s)` (PROV-0003).
- Verification needs the committer email to match a UID on the signing key and a verified address on the account. A mismatch shows Unverified with reason `bad_email`, although the signature is valid. Inspect it with `gh api repos/<owner>/<repo>/commits/<sha> --jq '.commit.verification'`. GitHub re-verifies old commits once the key matches.
- Adding a UID needs the certify key, which is offline. Add the UID in the vault keyring, export the block with `gpg --armor --export`, replace the key on GitHub, and import the block into the daily keyring. Key blocks never sync.
- An old public key that left the keyring comes back from GitHub: `gh api user/gpg_keys --jq '.[] | select(.key_id=="<old-key-id>") | .raw_key' | gpg --import`. The password store migration in PasswordToolkit needs it.
