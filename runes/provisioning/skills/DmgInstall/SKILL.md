---
name: DmgInstall
description: "Idempotent macOS .app install from a DMG: curl + hdiutil attach (random mountpoint) + cp -R + detach + codesign verify + CLI symlink. The reusable pattern for rapid-ship AppKit apps that intentionally bypass Homebrew. USE WHEN adding an install script under `$PROVISION_ROOT/scripts/install/` for a DMG-distributed app, deciding whether an app belongs in Brewfile or as a manual install, debugging hdiutil mount failures, or reasoning about idempotency for App-bundle installs."
metadata:
    version: 0.1.0
---

# DmgInstall

The reusable install pattern for `.app` bundles delivered via DMG, outside Homebrew. Used when an
app's release cadence makes unattended `brew upgrade` unsafe (rapid-ship AppKit apps, agents,
channel releases). Pairs with a Brewfile tombstone comment explaining why the app is intentionally
not a cask: see the HomebrewToolkit skill.

Reference implementation: `$PROVISION_ROOT/scripts/install/cmux.sh`. Every new
DMG-installed app should mirror its shape unless there is a specific reason to deviate. The shared
steps live in `$PROVISION_ROOT/scripts/lib/dmg.sh`: the mount-point parse, the detach, the exit
trap, and the copy through a temporary name. Source it, and give the new script a `--dry-run` that
stops before any download, mount, or copy.

## Prerequisites

Resolve the provisioning codebase root once before you open or run a script:

```sh
PROVISION_ROOT="${PROVISION_ROOT:-$HOME/Developer/runedeck/provision}"
```

## Constraints

- Download from the canonical-latest URL. Do not pin a version in the script.
- Skip when the `.app` is present unless `--force` is passed, and always print the skip reason.
- Detach the DMG in the failure path too.
- A failed `codesign --verify` warns. It does not fail the install.
- Every DMG-install script needs a matching Brewfile tombstone.

## Instructions

### Choose DMG-install or a Brewfile cask

- **Upstream releases weekly with breaking changes:** DMG-install.
- **Unattended `brew upgrade` would overwrite a known-good version:** DMG-install.
- **App ships via GitHub Releases (canonical-latest URL exists):** DMG-install is well-suited, a
  cask is possible.
- **App has its own self-update mechanism:** DMG-install.
- **App is stable, semver-disciplined, multi-year maintained:** Brewfile cask. DMG-install is
  overkill.

When in doubt, start with a Brewfile cask. Migrate to DMG-install only if you have been bitten by an
unattended upgrade.

### Write the installer

A DMG installer script in `$PROVISION_ROOT/scripts/install/<app>.sh` should:

1. **Source `$PROVISION_ROOT/scripts/lib/env.sh`** for `FORGE_PROVISION_ROOT`, the `.env` values,
   and `require_scope`.
2. **Skip if already installed** unless `--force` is passed.
3. **Download to a tempfile** via `curl -fL --progress-bar -o <tmp> <url>` with `trap` cleanup.
4. **Mount the DMG** via `hdiutil attach -nobrowse -mountrandom /tmp` and read the mount point
   from the third tab-separated field of its `/dev` line (`/private/tmp/dmg.XXXXXX`, never under
   `/Volumes`). Do not pass `-quiet` here: it closes stdout and stderr, so no mount point is
   printed. Detach when the mount holds no `.app`.
5. **Validate the .app exists** at the mount point before copying.
6. **Remove the old .app** if `--force` and an old version is present.
7. **Copy the .app** to `/Applications/` via `cp -R`.
8. **Detach the DMG** via `hdiutil detach -quiet`.
9. **Verify code signature** via `codesign --verify --quiet` (warning-not-fail).
10. **Create a CLI symlink** if the app ships a CLI (`<App>.app/Contents/Resources/bin/<tool>` →
    `~/.local/bin/<tool>`).
11. **Print next-steps hints** for things the script cannot do (e.g., `cmux hooks setup`).

The code for each step, with the reason for each flag, is in [Steps.md](Steps.md).

### Add the Brewfile tombstone

Every DMG-install script needs a matching tombstone in `manifests/Brewfile` explaining why the app
is *intentionally* not a cask:

```ruby
# <app> — intentionally NOT installed via Homebrew. Reproduced on fresh
# Mac by `$PROVISION_ROOT/scripts/install/<app>.sh`, which curls the canonical-latest DMG
# from <github releases url> and drops <app>.app into /Applications.
# Rationale: <app> ships rapidly; we'd rather opt into upgrades manually
# than have `brew upgrade` overwrite a known-good version.
```

The tombstone is load-bearing. Without it, a future session sees no cask declaration and "fixes" it
by adding `cask "<app>"`, which silently competes with the manual install. The comment makes the
absence intentional and traceable.

## Troubleshooting

[Pitfalls.md](Pitfalls.md) maps symptoms to causes: an empty mount point, bundle merging on copy,
signature checks on notarized apps, a CLI missing from PATH, an HTML download, repeated downloads,
and trap cleanup timing.

## References

- <https://ss64.com/mac/hdiutil.html>
- <https://developer.apple.com/library/archive/documentation/Security/Conceptual/CodeSigningGuide/Procedures/Procedures.html>
- <https://docs.github.com/en/repositories/releasing-projects-on-github/linking-to-releases>
