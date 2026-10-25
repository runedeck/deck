# Common pitfalls

- **`brew bundle install` hangs at an sudo prompt:** a cask requires a `sudo` install (rare, e.g.
  system-extension installs). Re-run from a TTY where you can type the password.
- **`brew uninstall --cask` deleted the .app you wanted to keep:** see "Detaching Homebrew from a
  cask" in [Destruction.md](Destruction.md). Move the .app aside first, or skip the uninstall
  command.
- **`mas install <id>` fails with "Not signed in":** `mas signin` is deprecated since macOS 10.15.
  Sign in via System Settings → Apple ID, then re-run.
- **`mas install <id>` fails with "An item could not be purchased":** the Apple ID does not own the
  app. Buy/get it in the App Store first, THEN `mas install <id>` works on subsequent machines.
- **`brew install` says "Error: Cannot install <name> because it is already installed":** an older
  `brew link --overwrite <name>` is needed, or the formula was relocated between taps.
- **Brewfile drift between machines:** run `brew bundle dump --file=manifests/Brewfile --describe`
  to regenerate. Sort and groom by hand afterward.
- **`brew upgrade` overwrote a manually-installed version:** the cask was still declared. Either
  remove the cask declaration and add the manual install script, OR pin (bottles only).
