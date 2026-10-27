# Claude Code in the box

The whole harness runs inside the VM: file tools, hooks, MCP servers, settings, and history. Anthropic documents this as the isolation boundary for unattended runs, and it also runs the harness day to day as a security layer.

## Image

`$PROVISION_ROOT/scripts/sandbox/claude-box/Containerfile`: `node:22-slim`, `git` and `ca-certificates` from the `APT_PACKAGES` build arg, Claude Code from npm, `USER node`, workdir `/work`. Build from that directory, after the builder VM has memory:

```sh
container builder start -m 4g
container build -t claude-box -f Containerfile .
container build -t claude-box-py --build-arg APT_PACKAGES="git ca-certificates python3" -f Containerfile .
```

Rebuild to refresh the pinned Claude Code version. Inside, a project-local install succeeds and `apt-get` fails on purpose. Put a recurring toolchain into a build arg.

## Auth

Interactive: log in on the first run. The OAuth URL prints in the terminal, and the credential stays inside the box. Headless: `claude setup-token` makes a one-year token. The owner keeps it in `pass` under `anthropic/claude-oauth-token`, the path the redact launcher reads (`FORGE_REDACT_TOKEN_PASS` overrides it).

The pass store lives on a YubiKey and asks for a touch per read, so the owner caches the token once a year in an env file with mode 600 and hands it to runs with `--env-file`:

```sh
umask 077
mkdir -p ~/.config/containers
printf 'CLAUDE_CODE_OAUTH_TOKEN=%s\n' "$(pass show anthropic/claude-oauth-token)" >| ~/.config/containers/claude-box.env
```

`umask 077` makes the file owner-only from its first byte, where a later `chmod` leaves a window in which another local user can read the token. The `>|` redirect overwrites the file on the yearly refresh: the owner's shell sets `noclobber`, and a plain `>` fails there with `file exists` and leaves the old token in place.

`~/.config/containers` is in the harness sandbox's `denyRead`, so a host Bash subprocess cannot read the cache. The directory stays out of dotfiles, because the content regenerates from `pass`.

## Run modes

Mount an explicit absolute project path. Supervised and disposable:

```sh
container run --rm -it -m 4g --env-file ~/.config/containers/claude-box.env -v "/path/to/project:/work" -w /work claude-box claude
```

Persistent harness. Login, settings, and history survive in a named volume, and the host still exposes only the project:

```sh
container volume create claude-home-<project>
container run --rm -it -m 4g -v claude-home-<project>:/home/node -v "/path/to/project:/work" -w /work claude-box claude
```

Autonomous, where the VM wall replaces the permission system:

```sh
container run --rm -m 4g --env-file ~/.config/containers/claude-box.env -v "/path/to/project:/work" -w /work claude-box claude --dangerously-skip-permissions -p "<prompt>" --output-format stream-json
```

Review the result with `git diff` in the project. With `--rm` the VM leaves nothing behind.

## Home volumes

One volume per project, named `claude-home-<project>`. Claude Code keys its state by project path, and every box mounts the project at `/work`, so a shared volume mixes histories. A fresh volume mounts root-owned while the image runs as `node`. Without a one-time ownership fix, login saves and settings writes fail with permission denied:

```sh
container run --rm -u root -v claude-home-<project>:/home/node claude-box sh -c 'chown -R node:node ~node'
```

Retire a volume with `container volume rm claude-home-<project>`. Never `container volume prune`: a `--rm` box detaches its volume on exit, so prune deletes every idle home volume at once.

## Redaction variant

VIRT-0003, in `$PROVISION_ROOT/docs/decisions/`, adds `claude-box-redact`. The box's Claude routes through the forge-redact proxy on loopback inside the VM, a secret gets a 403, and personal data becomes consistent surrogates before anything leaves the VM. The agent's own boundary is Claude Code's native sandbox, copied into the image at `/etc/claude-code/managed-settings.json` from `$PROVISION_ROOT/scripts/sandbox/claude-box/managed-settings.json`: `denyRead` on `/seed` and `/capture`, an egress allowlist, `enableWeakerNestedSandbox`, and `failIfUnavailable`. Apple container cannot run a network firewall (one network per container, no `CAP_NET_ADMIN`), so the boundary sits one layer up.

The owner runs both `redact` commands outside an agent sandbox. The wrapper's first token is a path, so an agent session runs it sandboxed, where the `container` calls fail on VM operations and `gpg` fails on the denied `~/.gnupg`. An agent hands over the exact command.

Build the base image first, then the variant. `$PROVISION_ROOT/scripts/sandbox/claude-box/redact build [<gpg-recipient>]` uses that directory as the build context, adds the forge-redact wheel and the operator's GPG public key, builds, and removes both. The recipient defaults to the default secret key, and the build fails if it does not resolve. The Presidio and spaCy layer is large, so the first build is slow.

`redact run [claude args]` mounts the current directory at `/work`, so start it from the project: `cd /absolute/path/project`, then `$PROVISION_ROOT/scripts/sandbox/claude-box/redact run`. From the home directory it hands the box the whole home, which the constraint in [SKILL.md](SKILL.md) forbids. The script decrypts the master vault at `~/.local/state/forge/presidio/vault.gpg` (one YubiKey touch) into a seed mounted read-only at `/seed`, runs the box with a capture directory at `/capture`, then moves the re-encrypted vault back to the master. The private key never enters the VM. `make redact build` in the codebase calls the same script. `make redact run` works only from the codebase root, because the Makefile resolves `scripts/sandbox/claude-box` relative to itself, and so it mounts the codebase root at `/work`. For a project, call `$PROVISION_ROOT/scripts/sandbox/claude-box/redact run` from the project directory. The entrypoint fails closed: it sends a planted secret and refuses to start Claude without a 403.

The variant is disposable mode only. A `claude-home-<project>` volume mounted over the home directory of the `node` user would shadow the copied policy, the sandbox settings, the public key, and the certificate authority of the proxy.
