# Tap management

```sh
brew tap                                # list active taps
brew tap-info <owner>/<repo>            # inspect a tap
brew tap <owner>/<repo>                 # add a tap
brew untap <owner>/<repo>               # remove (formulae from this tap become unmanaged)
```

**When to host your own tap**: if you publish 2+ formulae and want a single place to publish them,
a tap is cheaper than maintaining a homebrew-core PR. A tap is just a git repo with `Formula/*.rb`
or `Casks/*.rb`. Naming convention: `<owner>/homebrew-<name>`. Users add it as
`brew tap <owner>/<name>` (the `homebrew-` prefix is implicit).

**Tap stability concerns**: third-party taps disappear, lag upstream, or go dormant. Pin the tap to
a specific commit only if you have hit recurring breakage. Most taps work fine on HEAD.

## Authoring a tap for a binary-only upstream

When an upstream releases only a per-platform signed binary (no source, no GitHub release asset,
not in core), a personal tap makes it brew-managed and reproducible, better than a manual-DMG
tombstone (that pattern is for GUI apps with their own updater, ARCH-0014):

1. `brew tap-new <owner>/<name>` creates the tap repo (it auto-commits).
2. The formula pins each platform's binary by `sha256` with `using: :nounzip`
   (`on_macos`/`on_linux` × `on_arm`/`on_intel`), then `bin.install "<tool>"`.
3. Download each binary first to compute its real `sha256` and verify authenticity:
   `shasum -a 256 <file>`, and on macOS `spctl -a -vv -t install <file>` (expect
   `Notarized Developer ID`). The notarization signature is the integrity anchor.
4. `brew style <owner>/<name>/<tool>`, then `brew install <owner>/<name>/<tool>`. Push the tap
   public so `tap "<owner>/<name>"` + `brew "<owner>/<name>/<tool>"` resolve on a fresh machine.
   Modern brew rejects `brew install <path-to-formula.rb>` outside a tap.

## Verify a name before scripting it

Run `brew info <name>` before committing a formula or cask name to a script. Names drift and are not
guessable: the Proton Pass CLI is `proton-pass-cli` in core (not a `protonpass/tap`), and
`proton-drive` is the GUI cask, not the CLI.
