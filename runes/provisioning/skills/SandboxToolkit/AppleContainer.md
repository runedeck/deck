# Apple container on this Mac

Apple container runs each Linux container in its own lightweight VM through the Virtualization framework. `$PROVISION_ROOT/scripts/install/container.sh` installs it from Homebrew and starts the service. Each failure below was seen on this Mac, and the fix named is the one that worked.

The owner runs the install script and every keg-path start on this page. Their first token is a path, not `container`, so an agent session runs them sandboxed, and the launchd and VM operations fail. An agent runs the bare `container ...` lines and hands the rest to the owner as an exact command.

## Preflight

1. `container system status`. If the service is not running, hand the owner the keg-path start: `/opt/homebrew/opt/container/bin/container system start --enable-kernel-install`. Never the linked `/opt/homebrew/bin/container`, see the plugin failure below.
2. Read stderr. The exit code is 0 on a dead transport. `container image ls 2>&1 | grep -Eqi 'unavailable|transport.*inactive'` means the transport is dead even when the status says running.
3. Recover a dead transport, typical after sleep: `container system stop` (an agent may run it), wait three seconds, then the keg-path start from step 1 (the owner runs it).
4. Run `container` as the first word of the command. The harness sandbox exclusion matches the first token only.

## Service lifecycle

The apiserver starts on demand and does not restart at login unless `brew services start container` is used. `container system stop` shuts down the apiserver and every VM.

## Failures seen on this Mac

- Every CLI command hangs forever with no output. The client blocks on a launchd Mach-service lookup while the apiserver is unregistered or crash-looping. Check `launchctl list | grep com.apple.container`. Fix: the keg-path `container system stop`, then `start`. Last resort: `launchctl bootstrap gui/$UID "$HOME/Library/Application Support/com.apple.container/apiserver/apiserver.plist"`. The decisive diagnostic was `container-apiserver start` in the foreground. It came up clean, so the fault was the launchd registration.
- The apiserver exits 1 with `cannot find any plugins with type network`. The service was started through the linked `/opt/homebrew/bin/container`, which derives an install root whose `libexec/` Homebrew never links. Fix: the owner starts it through `/opt/homebrew/opt/container/bin/container`, the keg-path start in the preflight. The install script does this.
- The service is dead after `brew upgrade container`. The launchd plist stores the resolved Cellar path of the old keg. Fix: the owner re-runs the install script, or the keg-path `container system start`, which rewrites the plist.
- A command "succeeded" but did nothing. A transport error prints `Error: unavailable (14): Transport became inactive` and still exits 0. Grep stderr.
- A VM runs but the CLI cannot see it. It was orphaned when the daemon died. `pgrep -f container-runtime-linux`, then kill the orphans.
- A tool inside the VM crashes, or the kernel kills it. The VM defaults to 1 GiB. Pass `-m 4g` on every run. A build fails the same way: `container builder start -m 4g` before `container build`.
- `node_modules` on a mounted project is slow or flaky. Every mount is virtio-fs, which dislikes deep symlink trees. Use `--tmpfs` over the path, or copy in and push out through git.
- A run must stay offline. Create a host-only network once, `container network create --internal <name>`, and pass `--network <name>` to the run. `container system stop` is the wrong tool: it stops every running VM.
