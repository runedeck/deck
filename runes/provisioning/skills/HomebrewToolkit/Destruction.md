# Destruction semantics

**`brew uninstall --cask <name>` removes the `.app` from `/Applications`, not just the Homebrew
metadata.** This catches people the first time. The intuition is "uninstall = remove the package
manager's tracking, leave my apps alone". That is not how casks work.

## What gets deleted by `brew uninstall --cask`

- **`/Applications/<name>.app` (the app itself):** removed by bare uninstall and by `--zap`.
- **`/opt/homebrew/Caskroom/<name>/` (metadata):** removed by bare uninstall and by `--zap`.
- **`/opt/homebrew/bin/<name>` (CLI symlink):** removed by bare uninstall and by `--zap`.
- **`~/Library/Preferences/<bundle-id>.plist`:** kept by bare uninstall, removed by `--zap`.
- **`~/Library/Caches/<bundle-id>/`:** kept by bare uninstall, removed by `--zap`.
- **`~/Library/Application Support/<name>/`:** kept by bare uninstall, removed by `--zap`.

`--zap` is for "I'm done with this app forever, clear all traces". Bare `uninstall` is "I no longer
want this app installed but keep my settings if I reinstall".

## Detaching Homebrew from a cask without losing the app

Two safe patterns:

1. **Move the .app aside first**, uninstall, move it back:

   ```sh
   mv /Applications/<Name>.app /tmp/
   brew uninstall --cask <name>
   mv /tmp/<Name>.app /Applications/
   ```

   The brew metadata is gone. The app stays. Subsequent `brew upgrade` no longer touches it.

2. **Skip uninstall entirely**: delete the Caskroom directory and the symlink directly:

   ```sh
   rm -rf /opt/homebrew/Caskroom/<name>
   rm /opt/homebrew/bin/<name>     # if the cask shipped a CLI symlink
   ```

   Faster, fewer moves. brew has no record of the cask after this. The app is untouched.

Either pattern leaves you in a state where the next `brew bundle install` (without the
`cask "<name>"` line) is a no-op. Add the tombstone comment in the Brewfile so the absence is
intentional.
