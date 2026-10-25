# Troubleshooting

## Three Ghostty + tmux trap zones

Diagnostic: apply only if the symptom is observed.

### Cmd+1-9 routes to Ghostty tabs

Default behavior: `cmd+1..9` jumps to Ghostty tab N. If tmux windows are the primary axis and you
would prefer `cmd+N` to send `prefix+N` (one keystroke vs two), rebind to send the tmux escape
sequence directly. Tmux prefix `Ctrl+B` is `\x02`:

```toml
keybind = cmd+one=text:\x021
keybind = cmd+two=text:\x022
# ... cmd+three through cmd+nine
```

Source: <https://github.com/ghostty-org/ghostty/discussions/8756>

### Alt+Arrow word-jump regression under tmux+extkeys

Test: in nvim inside tmux, does Option+Left move by word? If broken (beeps, garbage characters),
Ghostty's Alt+Arrow handlers are eating the event before it reaches tmux. Unbind on the Ghostty side
so the keys forward cleanly:

```toml
keybind = alt+left=unbind
keybind = alt+right=unbind
```

Source: <https://github.com/ghostty-org/ghostty/discussions/2845>

### `macos-option-as-alt` + `extkeys` mismatch (Ghostty 1.2.3+)

tmux emits xterm format `ESC[27;2;13~` while kitty-protocol-aware apps expect `ESC[13;2u`. Symptom:
modifier+key combos behave inconsistently inside tmux vs outside. Fix on the tmux side, not the
Ghostty side:

```tmux
# either:
set -s extended-keys always              # force xterm format everywhere
# OR drop extkeys from terminal-features in tmux.conf and accept the
# capability loss for inner TUIs that wanted extended-keys.
```

Source: <https://github.com/ghostty-org/ghostty/discussions/9340>

## Common pitfalls

- **Trailing comments on config lines break parsing:** Ghostty parses `key = value # comment` as
  `value = "...# comment"`. Put comments on their own line.
- **Quick terminal binding does nothing after install:** Privacy & Security → Accessibility was not
  toggled on for Ghostty, or the app was not fully restarted.
- **URL Cmd+click hover is laggy in long buffers:** `link-previews = true` regex-scans every visible
  line. Set `link-previews = osc8`.
- **Cmd+click on URL inside tmux does nothing:** tmux `mouse on` captures the click. Use
  Cmd+Shift+click to hand it back to Ghostty.
- **Multi-line input broken in Claude Code (older versions):** add
  `keybind = shift+enter=text:\n` to inject a literal newline.
- **Nord theme colors look slightly off:** `window-colorspace = display-p3` shifts sRGB-defined
  themes. Switch to `srgb` if it bothers.
- **tic + ssh complaints about `xterm-ghostty` on remotes:** `shell-integration-features` missing
  `ssh-terminfo` and `ssh-env`. Add both.
