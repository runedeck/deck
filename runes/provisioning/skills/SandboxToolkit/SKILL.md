---
name: SandboxToolkit
description: "Run a workload at the isolation tier the owner chose: Apple container, one VM per container, for agents and experiments, the claude-box image that runs Claude Code behind a VM wall, and its redaction variant. Holds the install script, the image definitions, the token handoff, and the service traps found on this Mac. USE WHEN run untrusted code, disposable container, autonomous agent run, claude in a container, --dangerously-skip-permissions, container build, the container CLI hangs or the apiserver exits, claude-box, redaction box. NOT FOR the host harness sandbox (HarnessSecurity) or general Docker usage."
compatibility: "macOS 26 on Apple Silicon with Apple container 1.6 (check with `container --version`). Scripts and image definitions live in the provisioning codebase at $PROVISION_ROOT."
metadata:
    version: 0.2.0
---

# SandboxToolkit

Each workload runs at the weakest tier that still contains its threat. ARCH-0031, in `$PROVISION_ROOT/docs/decisions/`, fixes the ladder: the coding harness in the Seatbelt process sandbox, agents and Linux experiments in Apple container with one VM per container (VIRT-0002), untrusted native GUI apps in a full Parallels VM (ARCH-0016). OrbStack is installed for Compose and the Docker socket only. It shares one kernel inside one VM, so it is a convenience layer with no place on the ladder. Never pick it for hostile code.

## Prerequisites

- macOS 26 on Apple Silicon. The Homebrew formula installs on macOS 15, but container networking works only on 26, so the install script skips older systems.
- Apple container installed, and its service started by the install script below.
- The preflight in [AppleContainer.md](AppleContainer.md) before any run.

## Constraints

- Never run `claude --dangerously-skip-permissions` on the host. The flag belongs inside a container or VM, where the VM wall replaces the permission system.
- Mount exactly one host directory per run, by absolute path. A bare `$PWD` from the home directory hands the box the whole home at `/work`.
- The token never appears in argv, a Containerfile, or a tracked file. Pass it with a bare `-e CLAUDE_CODE_OAUTH_TOKEN` or with `--env-file`.
- The harness sandbox excludes a command line whose first token is `container`, and nothing else. The install script, the keg-path service start, the `redact` wrapper, and `make redact` start with another token. In an agent session they run sandboxed and fail on the launchd and VM operations, and the wrapper also fails on `gpg`, whose `~/.gnupg` the sandbox denies. Run bare `container ...` lines yourself. Hand every other one to the owner with the exact command, and say that it runs outside the sandbox.
- A container has network access by default. For an offline run, create a host-only network once with `container network create --internal <name>`, and attach the run with `--network <name>`. Do not stop the service for that: `container system stop` stops every VM on the Mac.

## Instructions

### Install the runtime

The owner runs the install script outside an agent sandbox. Resolve the codebase root and hand over the command:

```sh
PROVISION_ROOT="${PROVISION_ROOT:-$HOME/Developer/runedeck/provision}"
"$PROVISION_ROOT/scripts/install/container.sh"
```

The script installs the formula and starts the service through the keg path, `/opt/homebrew/opt/container/bin/container system start --enable-kernel-install`. The flag skips the interactive kernel prompt. The owner re-runs the script after every `brew upgrade container`: the launchd plist records the old keg path, and the service dies with it. An agent session checks the result with `container system status` and reads stderr, because the CLI exits 0 on a dead transport.

### Run an experiment

```sh
container run --rm -it -m 4g -v "/absolute/path/experiment:/work" -w /work docker.io/library/debian:stable-slim bash
```

For untrusted code add `--read-only --tmpfs /tmp`, and `--network <name>` with the host-only network from the constraints when the run must stay offline. Always pass `-m 4g`: a VM defaults to 1 GiB, and the size is fixed at creation.

### Run Claude Code in the box

The image definition is `$PROVISION_ROOT/scripts/sandbox/claude-box/Containerfile`. Build it from that directory after `container builder start -m 4g`, because the builder VM defaults to 2 GiB and npm runs out of memory. A variant is a build arg (`BASE_IMAGE`, `APT_PACKAGES`). Do not edit the file for a variant. The image runs as `USER node` because the CLI rejects skip-permissions as root. [ClaudeBox.md](ClaudeBox.md) gives the token handoff, the three run modes, the home volumes, and the redaction variant.

## Verification

- `container system status` reports running, and `container image ls 2>&1` prints no `unavailable` or `transport` line. The CLI exits 0 on a dead transport, so read stderr.
- A test run shows the mounted directory and nothing from the host environment: `container run --rm -v "/absolute/path:/work" docker.io/library/alpine env`.

## Troubleshooting

[AppleContainer.md](AppleContainer.md) holds the service failures seen on this Mac and the fix for each: a CLI that hangs forever, an apiserver that exits with `cannot find any plugins with type network`, a dead transport after sleep, orphaned VMs, and a service stranded by a Homebrew upgrade.

## References

- `$PROVISION_ROOT/docs/decisions/ARCH-0031 Workload isolation tier model.md`
- `$PROVISION_ROOT/docs/decisions/VIRT-0002 Linux workload isolation Apple container.md`
- `$PROVISION_ROOT/docs/decisions/VIRT-0003 In-sandbox PII redaction.md`
- <https://apple.github.io/container/documentation/>
- <https://code.claude.com/docs/en/sandbox-environments>
