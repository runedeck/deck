---
name: GhosttyToolkit
description: "Ghostty configuration best practices: appearance + window chrome, macOS-native integration (quick terminal, option-as-alt, titlebar style), kitty keyboard protocol, OSC 8 hyperlink hover, shell integration features, multi-line input for Claude Code, the three known Ghostty+tmux trap zones. USE WHEN configuring Ghostty, debugging key reporting under tmux, wiring the macOS quick terminal, restoring sessions across relaunch, tuning URL hover cost, or aligning option-as-alt and extkeys."
metadata:
    version: 0.1.0
---

# GhosttyToolkit

Best-practice Ghostty configuration. macOS-native, GPU-accelerated, kitty-protocol-native.
libghostty is the substrate cmux is built on, so settings carry across both apps for the
appearance/key-reporting subset.

Config lives at `~/.config/ghostty/config` (canonical source: `dot_config/ghostty/config` under
chezmoi). Reload binding: `cmd+shift+r` (overridden from default `cmd+shift+,` to free that chord
for cmux). For a quick reference of invocation and keybindings, see `docs/tldrs/ghostty.md` (when
authored).

## Constraints

- Put config comments on their own line. Ghostty reads a trailing `# comment` as part of the value.
- Global keybinds (`keybind = global:...`) require a full app restart, not just config reload, to
  take effect.
- A global binding also needs Ghostty toggled on under Privacy & Security → Accessibility.

## Instructions

### Configure Ghostty

[Appearance.md](Appearance.md) holds the appearance baseline (theme, font, cursor, thickening),
window chrome (padding, save state, opacity, colorspace), and macOS-native integration (titlebar,
fullscreen, option-as-alt). [Behavior.md](Behavior.md) holds the quick terminal, shell integration
and SSH, OSC 8 hyperlink hover, mouse and clipboard, notifications, and custom keybinds over the
1.3+ defaults.

### Align the kitty keyboard protocol

Three layers must agree to forward modifier-rich keystrokes (Alt+Arrow, Shift+Tab, Ctrl+Tab) into
the inner editor:

- **Ghostty (outer):** kitty protocol on by default in 1.x. `macos-option-as-alt` must stay
  consistent.
- **tmux (middle):** `extended-keys on` + `terminal-features 'xterm*:extkeys'` (see TmuxToolkit).
- **Inner editor:** helix `keyboard-protocol = "kitty"`, neovim equivalent `:set`.

Any disagreement collapses modifier reporting silently. See the trap zones in
[Troubleshooting.md](Troubleshooting.md) for the macos-option-as-alt + extkeys clash.

### Extend Ghostty

Ghostty has no plugin system. The extension points:

- **Themes**: `~/.config/ghostty/themes/<name>` (same syntax as the main config).
- **Custom shaders**: `custom-shader = /path/to/file.glsl` (repeat to stack). Catalogues:
  [0xhckr/ghostty-shaders](https://github.com/0xhckr/ghostty-shaders),
  [thijskok/ghostty-shaders](https://github.com/thijskok/ghostty-shaders).
- **Config includes**: `config-file = path` (`?path` for silent-if-absent, useful for machine-local
  overrides).
- **Keybind chords**: `>` separator (e.g. `ctrl+a>n=new_tab`).

Machine-local pattern:

```toml
config-file = ?local.conf                # silent if absent; for laptop-vs-desktop font-size tweaks
```

### Reload after edit

```sh
# In-app: cmd+shift+r (custom; default is cmd+shift+,)
# CLI: ghostty +reload-config           # works for non-global bindings only
```

## Troubleshooting

[Troubleshooting.md](Troubleshooting.md) covers the three Ghostty + tmux trap zones (Cmd+1-9 tab
routing, the Alt+Arrow regression, the option-as-alt + extkeys mismatch) and the common pitfalls.

## References

- <https://ghostty.org/docs/config/reference>
- <https://ghostty.org/docs/config>
- <https://sw.kovidgoyal.net/kitty/keyboard-protocol/>
- <https://invisible-island.net/xterm/ctlseqs/ctlseqs.html#h3-Operating-System-Commands>
- <https://github.com/ghostty-org/ghostty/discussions/8756>
- <https://github.com/ghostty-org/ghostty/discussions/2845>
- <https://github.com/ghostty-org/ghostty/discussions/9340>
