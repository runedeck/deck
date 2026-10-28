# Source conventions on this machine

The source tree uses the `dot_` convention: `dot_config/<app>/config` deploys to `~/.config/<app>/config`. An earlier layout kept plain names and copied them to dotted targets with a `run_onchange_` install script. It was replaced because it reimplemented `dot_` in bash and needed every plain file in `.chezmoiignore`. Do not reintroduce it.

## Prefixes in use

- `private_dot_ssh`, `private_dot_gnupg`, `private_dot_codex-cliproxy`: credential directories deploy with owner-only modes. Their secret content stays outside the source.
- `dot_claude/modify_private_settings.json.tmpl`: a `modify_` script for `~/.claude/settings.json`. It receives the live file on stdin, prints the template, and copies back only three live keys: `hooks`, `model`, and `outputStyle`. An apply replaces every other key the app wrote, such as the plugin list, the marketplaces, and UI state. The permission rules it inlines come from `.chezmoidata/harness/claude.json`.
- `dot_config/rune/modify_config.yaml.tmpl`: a `modify_` script for `~/.config/rune/config.yaml`. Its last step keeps only the live `.setup` block and replaces every other key.
- `dot_gitconfig.tmpl`: a template, so `chezmoi re-add` skips it.
- `create_dot_p10k.zsh`: creates the prompt config only when absent, so a local edit survives.
- `run_after_verify_harness_config.sh.tmpl`: a verification that runs after every apply.
- `run_onchange_after_<tool>.sh.tmpl`: a step that reruns when its rendered content changes. Under the Claude Code sandbox a `brew` call inside such a script runs sandboxed and fails, one more reason the owner applies.

## Special files

- `.chezmoiexternal.toml`: third-party content as archives pinned at a release with a SHA-256. The first-party shell framework stays `git-repo`, because it pulls submodules and chezmoi has no revision pin for that type. A weekly workflow opens a pull request when a pin moves, so a refresh stays reviewable.
- `.chezmoi.toml.tmpl`: at `chezmoi init` it reads the private values from `pass` (or from Proton Pass on request) into `[data.private]` of the chezmoi config. `promptChoiceOnce` picks the store at the first init, and `chezmoi init --prompt` asks again. A template reads `.private.<name>`, never `pass`.
- `.chezmoidata/private.yaml`: the public placeholder for each private value, such as `@GITLAB_HOST@`. The placeholder reaches a target when `chezmoi init` did not run after a change, see [Gotchas.md](Gotchas.md).
- `.chezmoidata/harness/claude.json`: the Claude permission rules (allow, ask, deny) as data.

## Upstream reference

- <https://www.chezmoi.io/reference/source-state-attributes/>
- <https://www.chezmoi.io/reference/special-files-and-directories/chezmoiexternal-format/>
