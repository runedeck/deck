# Behavior settings

## Quick terminal (drop-down)

```toml
keybind = global:cmd+§=toggle_quick_terminal
quick-terminal-position = top
quick-terminal-size = 100%,40%           # full width, 40% height
quick-terminal-screen = mouse
quick-terminal-animation-duration = 0.12
quick-terminal-autohide = true
```

`cmd+§` is the ISO key above Tab on Czech/UK/EU layouts: unclaimed by macOS, leaves bare § typing
intact elsewhere. US/QWERTY users without § pick another unused global chord (e.g.
`cmd+ctrl+space`).

**One-time setup**: System Settings → Privacy & Security → Accessibility → toggle on for Ghostty,
then fully quit and relaunch. `reload-config` does NOT pick up new global bindings. cmux lacks a
quick-terminal equivalent. Ghostty stays installed for this drop-down alone.

## Shell integration + SSH

```toml
shell-integration = detect
shell-integration-features = cursor,sudo,title,ssh-env,ssh-terminfo
scrollback-limit = 100000000             # ~100MB; Claude Code emits a lot
```

`ssh-terminfo` installs `xterm-ghostty` on remote hosts on first SSH connection. `ssh-env`
auto-downgrades TERM to `xterm-256color` when the remote lacks the ghostty terminfo. No `tic` dance,
no manual `TERM=xterm-256color ssh ...`.

## OSC 8 hyperlink hover

```toml
link-previews = osc8                     # hover preview only for explicit OSC 8 links
```

Default `true` regex-scans every visible line on cursor move, which is noticeable in long buffers.
`osc8` limits hover previews to explicit OSC 8 hyperlinks (emitted by `gh`, modern shells, `eza`,
build tools). Plain text URLs stay Cmd-clickable. Only the popover hover preview goes away for them.

## Mouse + clipboard

```toml
mouse-hide-while-typing = true
mouse-shift-capture = false              # Shift+click escapes to tmux/vim selection
copy-on-select = clipboard
clipboard-paste-protection = true        # warn on multi-line / control-char paste
clipboard-paste-bracketed-safe = true    # auto-trust bracketed-paste-aware apps
```

`mouse-shift-capture = false` is load-bearing for tmux: it lets Shift+click bypass tmux's mouse-on
capture and use Ghostty's native selection. Without it, Cmd+click and Cmd+Shift+click both end up
captured by tmux.

`copy-on-select = clipboard` writes selections to the system clipboard immediately. No explicit
Cmd+C needed. Trailing whitespace is trimmed by Ghostty's default
`clipboard-trim-trailing-spaces = true`. No leading-whitespace trim is available.

## Notifications

```toml
notify-on-command-finish = unfocused
notify-on-command-finish-after = 10s
```

macOS notification fires when a foreground command exits in an *unfocused* Ghostty window after the
threshold. Useful for long-running tests, builds, code reviews where you have task-switched away.
Set to `always` if you want the notification even on focused windows, `never` to disable entirely.

## Custom keybinds (over the 1.3+ defaults)

Ghostty 1.3+ defaults cover splits (`cmd+d` / `cmd+shift+d`), split navigation (`cmd+alt+arrows`),
split zoom (`cmd+shift+enter`), split resize (`cmd+ctrl+arrows`), equalize (`cmd+ctrl+=`), tab
navigation (`cmd+shift+[/]`), tab jump (`cmd+1..9`), prompt jump (`cmd+shift+up/down` via
shell-integration), clear (`cmd+k`), command palette (`cmd+shift+p`).
`ghostty +list-keybinds --default` enumerates the full set.

```toml
keybind = cmd+shift+r=reload_config      # over Ghostty's default cmd+shift+,
keybind = shift+enter=text:\n            # multi-line input when kitty negotiation misses
```

`shift+enter=text:\n` is the workaround for Claude Code multi-line input under older Claude Code,
nested tmux, or SSH without extkeys. Modern stack with kitty-protocol forwarding makes this
redundant. Keep it as belt-and-braces.
