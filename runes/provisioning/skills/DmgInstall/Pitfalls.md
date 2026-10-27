# Common pitfalls

- **`hdiutil attach` succeeds but mount point parsing returns empty:** either `-quiet` is on (it
  closes stdout and stderr, so `hdiutil` prints no mount point), or the parse looks for `/Volumes/`
  or a literal `/tmp/` prefix while `-mountrandom /tmp` mounts at `/private/tmp/dmg.XXXXXX`. Drop
  `-quiet` from `hdiutil attach` and read the third tab-separated field of its `/dev` line, or
  pass `-plist` and read the `mount-point` key under `system-entities`.
- **`cp -R` copies into existing `.app` instead of replacing:** bundle merging. Remove the old
  `.app` first when `--force` is passed.
- **`codesign --verify` fails on a notarized app:** notarization stripped the embedded signature.
  Verify with `spctl --assess --type execute` instead.
- **CLI symlink works in script but not in next session:** `~/.local/bin` not in PATH. Add to shell
  init: `export PATH="$HOME/.local/bin:$PATH"`.
- **DMG download succeeds but file is HTML (login wall):** upstream changed asset URL. Print HTTP
  status from `curl -w "%{http_code}"` to diagnose.
- **Re-running the script downloads the DMG every time:** idempotency check (`-d "${APP}"`) missing
  or wrong path. Verify with `ls /Applications/<Name>.app`.
- **Trap cleanup deleted DMG before failure-path detach succeeded:** put
  `trap 'rm -f "${DMG_TMP}"' EXIT` at the top. Make sure the failure-path `hdiutil detach` runs
  before the trap fires.
