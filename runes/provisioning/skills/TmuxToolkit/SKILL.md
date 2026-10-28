---
name: TmuxToolkit
description: "Tmux setup as a toolkit of best-practice config, plugins, and gotchas-with-fixes. Covers baseline config (true color, kitty protocol pass-through, OSC 52 clipboard, focus events, mouse), plugin management via chezmoi externals, TPM bootstrap, tmux-resurrect + tmux-continuum for session persistence, catppuccin theming. USE WHEN configuring tmux, adopting tmux plugins, fixing kitty-protocol passthrough into helix or neovim, restoring sessions across reboots, debugging tmux behavior under Ghostty or cmux, or tuning the status line."
metadata:
    version: 0.1.0
---

# TmuxToolkit

Best-practice tmux configuration for the persistent-session layer beneath Ghostty / cmux. Concrete
config, plugins worth adding, and the kitty-protocol + OSC 52 + truecolor plumbing that lets modern
TUIs work cleanly inside a multiplexed session.

For invocation, keybindings, and save/quit semantics see `docs/tldrs/tmux.md`.

## Constraints

- Keep the TPM `run '~/.config/tmux/plugins/tpm/tpm'` line last in `tmux.conf`.
- Put `@plugin 'catppuccin/tmux'` above every `@catppuccin_*` option.
- Do not restart the tmux server unless changing init-only settings (`default-terminal`, terminfo):
  `kill-server` drops every session that is not restored by continuum on next start.

## Instructions

### Configure tmux

The config lives in the chezmoi source at `dot_config/tmux/tmux.conf` (deploys to
`~/.config/tmux/tmux.conf`). [Config.md](Config.md) holds the baseline (true color, kitty protocol,
OSC 52, focus events, mouse, scrollback, indexing), session persistence with tmux-resurrect and
tmux-continuum, Catppuccin theming, and the OSC 52 copy-mode bindings.

### Install plugins

chezmoi externals clone the plugins declaratively, so a fresh Mac does not wait for `prefix + I`.
TPM still loads them from the `@plugin` lines. The externals file and the TPM bootstrap are in
[Plugins.md](Plugins.md).

### Align the kitty keyboard protocol

Three sides have to agree:

- **Ghostty (outer):** kitty-protocol on (default in recent versions). `macos-option-as-alt`
  consistent.
- **tmux (middle):** `extended-keys on` + `terminal-features 'xterm*:extkeys'` (in the baseline).
- **helix / nvim (inner):** `keyboard-protocol = "kitty"` (helix) or the equivalent `:set` lines
  (neovim).

When all three agree, Alt+Arrow, Shift+Tab, Ctrl+Tab survive into the inner editor with the correct
modifier flags. When one disagrees, modifier-rich keystrokes get downgraded silently.

### Reload after edit

```sh
tmux source-file ~/.config/tmux/tmux.conf      # reload running server, preserve sessions
```

## Troubleshooting

[Pitfalls.md](Pitfalls.md) maps symptoms to fixes: Cmd+click on URLs, Alt+Arrow, bare-shell
restores, plugins that do not load, raw `#{...}` status modules, the `default-terminal` warning,
hjkl navigation, and a silent `prefix+I`.

## References

- <https://github.com/tmux/tmux/wiki>
- <https://github.com/tmux-plugins/tpm>
- <https://github.com/tmux-plugins/tmux-resurrect>
- <https://github.com/tmux-plugins/tmux-continuum>
- <https://github.com/catppuccin/tmux>
- <https://www.chezmoi.io/reference/special-files-and-directories/chezmoiexternal-format/>
- <https://sw.kovidgoyal.net/kitty/keyboard-protocol/>
- <https://invisible-island.net/xterm/ctlseqs/ctlseqs.html#h3-Operating-System-Commands>
