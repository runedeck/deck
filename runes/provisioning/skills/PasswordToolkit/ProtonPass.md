# Proton Pass CLI

`pass-cli` is the official Proton client for Proton Pass. Verified: Proton Pass CLI 2.5.1. It needs a paid Pass plan. The Homebrew formula is `proton-pass-cli` from homebrew-core, listed in the Brewfile beside the `proton-pass` cask. PROV-0010 is the decision that keeps Proton keys in Proton, so this tool reads vaults and never exports a key.

## Login

- `pass-cli login` hands off to the browser. `pass-cli info` shows the session.
- CI and scripts use a scoped personal access token: `pass-cli personal-access-token create`, then `pass-cli personal-access-token access` limits it to the one vault the job needs. The store for the token is `pass`.

Log in with the token in the environment of that one process:

```sh
PROTON_PASS_PERSONAL_ACCESS_TOKEN="$(pass show <path> | head -1)" pass-cli login
```

The `--pat` flag of 2.5.1 puts the token into the argument list, where `ps` shows it to every local user while the login runs. The environment of a process is readable by its own user only. The [login documentation][PASSLOGIN] specifies the variable. A token session lasts 2 hours.

## Secret references

- A reference is `pass://<vault>/<item>/<field>`, by name or by id. A TOTP field takes `?totp=code` (the default) or `?totp=uri`. `pass-cli inject --help` and `pass-cli run --help` of 2.5.1 omit the syntax. The [secret references documentation][PASSREFS] gives it.
- `pass-cli run -- <command>` resolves every reference it finds in the environment of the child (`export VAR='pass://...'` first) and masks the values on stdout and stderr.
- `pass-cli inject -i <template> -o <file>` resolves `{{ pass://... }}` in a template and writes the file with mode 0600.
- `pass-cli ssh-agent` serves keys stored in Pass. The SSH keys of this machine stay on the YubiKey (SshToolkit), so it is unused here.

## Limits

- Every export, from `pass-cli export` or from the apps, gives decrypted data, never a key (PROV-0010). Treat an export as a manual backup.
- An unofficial community client exists that scripts the full account credentials. Proton does not endorse it. Use it only for a Proton service that `pass-cli` does not cover, and keep `pass-cli` as the Pass tool.
- Commands fail with no vault access on the free tier, or when the token scope is too narrow.

[PASSLOGIN]: https://protonpass.github.io/pass-cli/commands/login/
[PASSREFS]: https://protonpass.github.io/pass-cli/commands/contents/secret-references/
