# Common pitfalls

- **Cmd+click on a URL inside tmux does nothing:** tmux's `mouse on` captures the click. Use
  `Cmd+Shift+click` to bypass tmux mouse capture and hand the click to Ghostty.
- **Alt+Arrow does nothing inside tmux+Ghostty:** `extended-keys on` +
  `terminal-features 'xterm*:extkeys'` missing, or `macos-option-as-alt` and extkeys disagree.
- **Resurrect restore leaves processes as bare shells:** process not in `@resurrect-processes`. Add
  it, save, retry restore.
- **Plugins do not load after `chezmoi apply` cloned them:** TPM only loads at server start.
  `tmux kill-server && tmux`, or source the TPM `run` line manually.
- **Status-line modules render as raw `#{...}` strings:** `@plugin 'catppuccin/tmux'` is below the
  `@catppuccin_status_modules_right` line. Move the @plugin line above it.
- **`default-terminal` warning at start:** `tmux-256color` terminfo missing.
  `infocmp tmux-256color` to verify. On stale macOS, fetch from ncurses git.
- **Vim-style hjkl pane navigation jumps inside an inner editor:** use `vim-tmux-navigator` plugin
  or guard `bind-key h select-pane -L` with `if-shell` that checks the active program.
- **`prefix+I` does nothing:** TPM not bootstrapped at the end of tmux.conf. The
  `run '~/.config/tmux/plugins/tpm/tpm'` line must be the last line.
