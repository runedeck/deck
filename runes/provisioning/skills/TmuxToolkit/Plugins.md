# Plugin management via chezmoi externals

TPM's `prefix + I` to install plugins is imperative: a fresh Mac would have no plugins until you
press the key. chezmoi externals make plugin clones declarative:

```toml
# dotfiles/.chezmoiexternal.toml
[".config/tmux/plugins/tpm"]
    type = "git-repo"
    url = "https://github.com/tmux-plugins/tpm.git"
    refreshPeriod = "168h"

[".config/tmux/plugins/tmux-resurrect"]
    type = "git-repo"
    url = "https://github.com/tmux-plugins/tmux-resurrect.git"
    refreshPeriod = "168h"

[".config/tmux/plugins/tmux-continuum"]
    type = "git-repo"
    url = "https://github.com/tmux-plugins/tmux-continuum.git"
    refreshPeriod = "168h"

[".config/tmux/plugins/catppuccin/tmux"]
    type = "git-repo"
    url = "https://github.com/catppuccin/tmux.git"
    refreshPeriod = "168h"
```

`chezmoi apply` clones each repo at first run and refreshes weekly. TPM still parses the `@plugin`
lines in `tmux.conf` to register and load its plugins. Catppuccin loads directly. Pin a plugin by
setting `refreshPeriod = "8760h"` (one year) until you bump it.

Append TPM bootstrap to the *end* of `tmux.conf`:

```tmux
run '~/.config/tmux/plugins/catppuccin/tmux/catppuccin.tmux'

set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-resurrect'
set -g @plugin 'tmux-plugins/tmux-continuum'

run '~/.config/tmux/plugins/tpm/tpm'
```

The TPM `run` line must be last. TPM reads the `@plugin` declarations above it and sources each
plugin's entry script.
