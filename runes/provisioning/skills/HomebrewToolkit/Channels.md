# Bottle vs cask vs mas

- **`brew "<name>"` (bottle):** CLI tools, libraries, daemons. Installs to
  `/opt/homebrew/{bin,lib,Cellar}`. Updates with `brew upgrade <name>`.
- **`cask "<name>"` (cask):** GUI .app bundles (and some CLIs in disguise). Installs to
  `/Applications/<name>.app`. Updates with `brew upgrade --cask <name>` (often unattended-unsafe).
- **`mas "<name>", id: <N>`:** Mac App Store apps (entitlement-bound). Installs to
  `/Applications/<name>.app`. Updates through the App Store's own update path.

**Pick a channel by the constraint, not the convenience**:

- **Bottle** for CLI tools: easiest to update, easiest to scope-limit (`brew leaves`, `brew uses`).
  Most things go here.
- **Cask** for GUI apps where you trust the upstream's release cadence and want unattended
  `brew upgrade` to apply updates. NOT for apps that publish breaking changes weekly without semver
  discipline (see "Why not cask" below).
- **mas** for App Store apps where the Apple ID purchase / entitlement is the source of truth.
  Requires being signed into the same Apple ID that owns / purchased the app. `mas signin` is
  **deprecated since macOS 10.15**: sign in via System Settings instead.

## Why not cask (for some apps)

Some rapid-ship apps publish breaking changes between releases, treat semver as decorative, or push
critical hotfixes through cask faster than a human can review them. Examples in this user's setup
that intentionally bypass cask:

- **cmux**: manaflow-ai/cmux. Migrated from cask to manual DMG via `$PROVISION_ROOT/scripts/install/cmux.sh` after
  `brew upgrade` was identified as a risk. See the Brewfile tombstone comment for the rationale.

For these, the canonical install path is a `$PROVISION_ROOT/scripts/install/<app>.sh` that curls the
GitHub-canonical-latest DMG (`releases/latest/download/<asset>`) and a Brewfile tombstone comment
explaining why the cask is *intentionally absent*. The tombstone is load-bearing: without it, a
future session sees a missing cask and "fixes" it by adding it back.

## Why not bottle (for some tools)

Same logic in reverse. Tools whose Homebrew bottle lags behind upstream (Rust nightly, language
version managers with their own self-update, polyglot dev-environment shells) install better via
their own canonical installer. Document the choice with a tombstone in the same place a
`brew "<name>"` would have gone.

## When NOT to use Homebrew

- Apps with critical update-cadence concerns (cmux today, possibly others). Use
  `$PROVISION_ROOT/scripts/install/<name>.sh` + Brewfile tombstone.
- Tools whose canonical installer self-updates (rustup, mise, nvm, etc.). Their built-in update
  mechanism is the right path.
- Apple-platform first-party apps that come from the App Store with App Store entitlements (iWork,
  Final Cut Pro, Logic Pro). Use `mas`.
- Apps with paid licenses that Homebrew has no way to track (1Password 7 Mac, Microsoft Office
  standalone). Brewfile entries that require manual activation are OK with a tombstone-style comment
  explaining the post-install step.
