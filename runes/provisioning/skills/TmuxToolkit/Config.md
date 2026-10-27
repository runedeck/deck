# Config snippets

## Baseline config

Drop these into the chezmoi source at `dot_config/tmux/tmux.conf` (deploys to
`~/.config/tmux/tmux.conf`):

```tmux
# True color + tmux-256color terminfo
set -g default-terminal "tmux-256color"
set -as terminal-overrides ",*-256color:Tc"

# Kitty keyboard protocol — accept extended sequences from the outer terminal
# and advertise extended-keys support to the inner TUI.
set -g extended-keys on
set -as terminal-features 'xterm*:extkeys'

# OSC 52 clipboard — copy in tmux propagates to the macOS clipboard.
set -g set-clipboard on

# Focus events — inner editors auto-reload when files change outside.
set -g focus-events on

# Mouse on — drag-resize, click-to-focus, scroll.
set -g mouse on

# No vim escape lag.
set -g escape-time 10

# Large scrollback per pane.
set -g history-limit 100000

# 1-indexed windows + panes, contiguous renumber on close.
set -g base-index 1
set -g pane-base-index 1
set -g renumber-windows on
```

The `Tc` capability + `terminal-features 'xterm*:extkeys'` pair is the canonical incantation. Both
halves are needed (the outer→tmux hop *and* the tmux→inner hop) for modifier-rich keystrokes to
survive.

## Session persistence

`tmux-resurrect` + `tmux-continuum` is the persistent-session pair:

```tmux
# tmux-resurrect — save / restore the session graph
set -g @resurrect-strategy-vim 'session'
set -g @resurrect-strategy-nvim 'session'
set -g @resurrect-processes 'ssh helix nvim "git log" "git diff"'

# tmux-continuum — auto-save every 15 min, auto-restore on server start
set -g @continuum-restore 'on'
set -g @continuum-save-interval '15'
```

Resurrect captures sessions, windows, panes, pane CWDs, and pane processes from
`@resurrect-processes`. vim/nvim/helix are first-class via the `-strategy-*` options. Ad-hoc REPLs
come back as bare shells unless added to the processes list. `prefix+Ctrl-s` saves now,
`prefix+Ctrl-r` restores last save.

Snapshots are written under `~/.local/share/tmux/resurrect/`. Audit growth periodically: resurrect
keeps every snapshot.

## Catppuccin theming

```tmux
set -g @catppuccin_flavor 'mocha'                    # latte | frappe | macchiato | mocha
set -g @catppuccin_window_status_style 'rounded'     # basic | rounded | slanted | custom | none

# Module-driven status-right composition.
set -g @catppuccin_status_modules_right 'application session date_time'
```

The `@plugin 'catppuccin/tmux'` line MUST come before any `@catppuccin_*` option that references
module files. The include logic resolves only after the plugin is sourced. Wrong order → status-line
modules render as raw `#{...}` strings.

## OSC 52 clipboard

`set-clipboard on` enables tmux to honor OSC 52 escapes: copies inside tmux propagate to the macOS
clipboard without `pbcopy`. The terminal also has to permit OSC 52 writes. Ghostty defaults are
sane.

For copy-mode vi keys with a belt-and-braces `pbcopy` fallback:

```tmux
set -g mode-keys vi
bind-key -T copy-mode-vi v send-keys -X begin-selection
bind-key -T copy-mode-vi y send-keys -X copy-pipe-and-cancel "pbcopy"
```

The explicit `pbcopy` pipe rescues clients that do not honor OSC 52 (legacy iTerm2 profiles, some
headless setups).
