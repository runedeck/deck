# Brewfile authorship

A Brewfile is read by `brew bundle install --file=<path>`. Conventions that pay off long-term:

```ruby
# manifests/Brewfile — grouped by topic, every entry has a why-comment.

# Proton suite (the owner defaults to Proton-native apps).
cask "proton-drive"
cask "proton-mail"
cask "proton-vpn"

# Local LLM runner.
cask "lm-studio"

# AI coding agent (CLI). Configured locally with lm-studio + Proton Lumo as providers.
# Config TBD — capture as $PROVISION_ROOT/scripts/configure/<tool>.sh once provider files settle.
brew "opencode"
```

Best practices:

1. **Group by topic, not channel.** Brewfile readability comes from "what cluster does this app
   belong to" (proton suite, dev tools, editors) not "is it a brew or a cask".
2. **Every entry has a why-comment.** A bare `brew "foo"` rots: no one remembers why `foo` was added
   six months later. Even `# bundled with X` is enough.
3. **Tombstone intentionally-absent apps in place.** When you remove a cask but want future sessions
   to NOT re-add it, leave a comment block at the entry's original sort position explaining why.
   Example: the `cmux` block in `manifests/Brewfile` after the `cmux` cask was migrated to manual
   DMG.
4. **Brewfile.optional for evaluation installs.** Apps you tried and did not adopt as daily drivers
   (Warp, Wave) live in `manifests/Brewfile.optional`. Same `brew bundle install --file=...`
   invocation, separate file. Keeps the primary Brewfile lean while preserving the evaluation
   history.
5. **Reference taps explicitly.** When a tap is needed, add the `tap "<owner>/<repo>"` line near the
   dependent entries, not at the top. Grouping the tap with its consumers makes the dependency
   visible.

## Pinning

```sh
brew pin <name>                         # block this formula from `brew upgrade`
brew unpin <name>                       # release
brew list --pinned                      # what's pinned
```

Pin sparingly. The reason to pin should be documented in the Brewfile next to the entry:

```ruby
# Pinned at 1.4.x — 1.5 breaks the <foo> integration; revisit after <upstream-issue>.
brew "name@1.4"
```

Casks cannot be pinned (the API has no `--cask` flag on `brew pin`). The cask equivalent is
**manual install via DMG**: the migration described in [Channels.md](Channels.md). If you need to
block a cask from auto-upgrade, the right tool is to remove the cask declaration entirely and
capture the install in `$PROVISION_ROOT/scripts/install/<name>.sh`.

## Reload after editing the Brewfile

```sh
brew bundle install --file=manifests/Brewfile      # apply added entries (idempotent)
brew bundle check --file=manifests/Brewfile        # verify match
brew bundle cleanup --file=manifests/Brewfile      # list installed but absent from Brewfile
```

`bundle install` is idempotent: re-running with no changes is a no-op. Use it freely.
