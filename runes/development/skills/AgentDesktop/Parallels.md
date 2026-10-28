# Parallels

`STC` (Standard Template Construct) is the base VM. Every agent VM is a linked clone of its newest snapshot. Parallels Desktop 27 supports Ubuntu 26.04 LTS on Apple silicon ([KB 124223][PDREQ]).

## The base image

- Ubuntu 26.04.1 LTS arm64, Xfce on X11, LightDM auto-login for `agent` (no password, no sudo).
- The X11 and AT-SPI stack from cua's image: `xdotool`, `wmctrl`, `xclip`, `scrot`, ImageMagick, `python3-pyatspi`. Accessibility turns on at login.
- Firefox from Mozilla's APT repository, with a policy that turns off telemetry and sets `SkipTermsOfUse`. The owner accepted the Firefox terms on 2026-10-26.
- Node, npm, Claude Code, Codex, `gh`, `jj`, `uv`, `fd`, tmux, ffmpeg, bubblewrap and socat.
- No screen lock or blanking. Clipboard, application, SmartMount, cloud, location and camera sharing are off.
- An empty `/etc/machine-id`, so each clone gets its own ID and its own DHCP address.

## Use an agent VM

- **Create:** `scripts/new-agent-vm.sh <purpose words>` prints the new name.
- **Start:** `prlctl start <vm>`.
- **Wait:** `scripts/wait-exec.sh <vm> 120`.
- **Run as root:** `prlctl exec <vm> "<command>"`.
- **Run a script:** `scripts/run-in-guest.sh <vm> <script> <guest-log>`.
- **Screenshot:** `prlctl capture <vm> --file shot.png`.
- **Check the image:** `scripts/run-in-guest.sh <vm> guest/verify-agent.sh /var/log/verify.log`.
- **Remove:** `prlctl delete <vm>`, or `prlctl unregister <vm>` and move the `.pvm` directory to the trash.

A clone takes about 1 s to create and 1.4 MB of disk at first. `prlctl exec` answers 11 to 12 s after start.

## Update the base

1. `prlctl start STC`, then `scripts/wait-exec.sh STC 300`.
2. Edit [guest/provision-base.sh](guest/provision-base.sh). Rerun it with `scripts/run-in-guest.sh STC guest/provision-base.sh /var/log/provision-base.log`. It is safe to rerun and ends by emptying the machine ID.
3. `prlctl stop STC`, then `prlctl snapshot STC -n clean-<next>`. `new-agent-vm.sh` uses the newest snapshot.

## Rebuild the base from scratch

1. Download `ubuntu-26.04.1-live-server-arm64.iso` from cdimage.ubuntu.com and check its SHA-256 against `SHA256SUMS`.
2. Build the seed disk: `hdiutil makehybrid -o seed.iso seed -iso -joliet -default-volume-name cidata`.
3. `prlctl create STC --distribution ubuntu`, set `--memsize 8192 --cpus 4`, and attach three CDs: the installer, `seed.iso`, and the Linux Tools ISO from the `Contents/Resources/Tools` directory of the Parallels Desktop app. Boot from the CD first.
4. Start the VM. At "Continue with autoinstall? (yes|no)", send `prlctl send-key-event STC --scancode N` for 21, 18, 31 and 28 (y, e, s, Enter).
5. After the install powers off (about 30 min), disconnect the installer and seed CDs, boot from disk, and run `guest/provision-base.sh`.

## Traps

- `prlctl` leaves the sandbox only as the whole command line. A pipe, `&&` or `$(...)` runs it inside the sandbox, where it fails.
- `prlctl exec` joins its arguments into one guest shell line, runs as root with `HOME=/`, a `PATH` without `/usr/local` and umask 077, and fails on a line of a few KB. `run-in-guest.sh` handles all of this.
- `prlctl exec` fails now and then with `PrlJob_GetResult` or `PrlJob_GetRetCode`, mostly in the first minute after boot. Retry.
- `--isolate-vm on` blocks `prlctl exec`. Turn the sharing switches off one by one instead.
- `prlctl set --name` works only on a stopped VM and renames the `.pvm` directory. Renaming the base through `prlctl` rewrites every clone's parent path. Moving the directory by hand breaks the clones.
- A linked clone needs a snapshot of a stopped base ([KB 122669][PDKB]). Several clones can run at once.
- `prlctl` has no mouse input. The vendor MCP server `Parallels/pdfm-mcp` has no mouse or accessibility tool either ([README][PDMCP]). Use `xdotool` in the guest.

[PDREQ]: https://kb.parallels.com/en/124223
[PDKB]: https://kb.parallels.com/en/122669
[PDMCP]: https://raw.githubusercontent.com/Parallels/pdfm-mcp/main/README.md
