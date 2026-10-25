---
name: HomebrewToolkit
description: "Homebrew best practices: bottle vs cask vs mas (when to use each), Brewfile authorship (grouping, tombstones for intentionally-excluded apps, Brewfile.optional split for evaluation installs), destruction semantics (brew uninstall removes the .app), tap management, pinning. USE WHEN authoring or editing a Brewfile, debugging brew install/upgrade behavior, choosing between brew and mas and manual install, adding a third-party tap, or detaching Homebrew from a cask without losing the app."
metadata:
    version: 0.1.0
---

# HomebrewToolkit

Homebrew is the macOS package manager: bottle / cask / mas under one Brewfile. This skill is the
best-practice playbook for using brew without surprises, especially the destruction semantics of
`brew uninstall --cask` that catch people the first time.

## Prerequisites

List the active taps once before you add or remove one:

```sh
brew tap 2>/dev/null | paste -sd' ' - || echo "(brew not installed)"
```

Resolve the provisioning codebase root once before any script step:

```sh
PROVISION_ROOT="${PROVISION_ROOT:-$HOME/Developer/runedeck/provision}"
```

## Constraints

- `brew uninstall --cask <name>` removes the `.app` from `/Applications`. Read
  [Destruction.md](Destruction.md) before you detach or remove a cask.
- Casks cannot be pinned. To block a cask from auto-upgrade, remove the declaration and install it
  through `$PROVISION_ROOT/scripts/install/<name>.sh`.
- Every intentionally absent app keeps a tombstone comment in the Brewfile.
- Run `brew info <name>` before committing a formula or cask name to a script.
- Install custom-built binaries to `~/.local/bin/`, never to `/opt/homebrew/bin/`.

## Instructions

### Choose a channel

Bottles carry CLI tools, casks carry GUI apps whose upstream cadence you trust, and `mas` carries
App Store apps tied to an Apple ID. Pick by the constraint, not the convenience.
[Channels.md](Channels.md) covers each channel, why some apps bypass cask or bottle, and when not to
use Homebrew at all.

### Author the Brewfile

Group entries by topic, give every entry a why-comment, tombstone intentionally absent apps in
place, keep evaluation installs in `manifests/Brewfile.optional`, and put each `tap` line next to
its consumers. [Brewfile.md](Brewfile.md) has the example, pinning, and the reload commands. Taps,
including authoring a tap for a binary-only upstream, are in [Taps.md](Taps.md).

### Run lifecycle commands

```sh
brew install <name>                     # install bottle
brew install --cask <name>              # install cask
brew bundle install --file=manifests/Brewfile     # apply a Brewfile
brew bundle dump --file=manifests/Brewfile        # regenerate Brewfile from installed state
brew bundle cleanup --file=manifests/Brewfile     # show what's installed but not in Brewfile
brew bundle check --file=manifests/Brewfile       # verify Brewfile matches installed
brew upgrade                            # upgrade everything (bottles + casks)
brew upgrade <name>                     # upgrade one
brew pin <name>                         # prevent upgrade until unpin
brew unpin <name>                       # release the pin
brew outdated                           # list upgradable
brew uninstall <name>                   # uninstall (DESTRUCTIVE for casks, see Destruction.md)
brew uninstall --zap --cask <name>      # also remove preferences/caches
brew autoremove                         # remove unused dependencies (run after uninstall)
brew cleanup                            # remove old versions, stale downloads
```

### Keep custom builds out of Homebrew's way

Homebrew owns `/opt/homebrew/bin/`: `brew upgrade` re-symlinks entries from the Cellar and any
manually placed file is silently overwritten or orphaned. If the Homebrew formula provides an older
version of the same binary, `brew unlink <formula>` removes the symlink so `~/.local/bin/` takes
precedence in PATH. Verify which binary is running with `type -a <name>`: shell functions and
aliases may shadow the expected path.

## Troubleshooting

[Pitfalls.md](Pitfalls.md) maps symptoms to fixes: sudo prompts during `brew bundle install`, a
deleted `.app`, `mas` sign-in and purchase errors, "already installed" errors, Brewfile drift, and
an upgrade that overwrote a manual install.

## References

- <https://docs.brew.sh>
- <https://docs.brew.sh/Manpage>
- <https://docs.brew.sh/Cask-Cookbook>
- <https://github.com/Homebrew/homebrew-bundle>
- <https://github.com/mas-cli/mas>
- <https://docs.brew.sh/Taps>
