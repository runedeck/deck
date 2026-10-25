# Installer steps in detail

## Canonical-latest GitHub releases URL

Use the redirector path so the script does not pin to a version:

```text
https://github.com/<owner>/<repo>/releases/latest/download/<asset-filename>
```

GitHub redirects to the actual asset of the latest release. Pinning to a version
(`/releases/download/v1.2.3/<asset>`) defeats the purpose of opt-out-of-cask: you would be
hardcoding an upgrade decision into the script.

If upstream uses a non-GitHub release artifact (their own CDN, Cloudflare R2, etc.), use whatever
"latest stable" URL they provide. Document the URL contract in a comment so a future session knows
whether the URL guarantees freshness or just last-time-the-script-was-written.

## Idempotency

```sh
if [[ -d "${CMUX_APP}" && ${FORCE} -eq 0 ]]; then
    echo "skip:cmux (${CMUX_APP} already installed; pass --force to reinstall)"
    exit 0
fi
```

Skip on presence of the `.app`. `--force` removes the existing `.app` before reinstalling (avoids
the `cp -R` merging old + new bundle contents). Always print the skip reason so re-running the
orchestrator is informative, not silent.

## Attach the DMG safely

```sh
MOUNT_POINT=$(hdiutil attach "${DMG_TMP}" -nobrowse -mountrandom /tmp 2>/dev/null | \
    grep '^/dev/' | cut -f 3 | grep -m 1 .)
if [[ -z "${MOUNT_POINT}" ]]; then
    echo "fail:<app> (DMG mount failed)"
    exit 1
fi
if [[ ! -d "${MOUNT_POINT}/<App>.app" ]]; then
    hdiutil detach "${MOUNT_POINT}" -quiet
    echo "fail:<app> (no <App>.app inside the DMG)"
    exit 1
fi
```

Why each flag:

- `-nobrowse`: do not show the DMG in Finder sidebar.
- No `-quiet` on `attach`: `-quiet` closes stdout and stderr and prints no mount point, so the
  parse would return empty. `-quiet` is fine on `detach`, whose output the script does not read.
- `-mountrandom /tmp`: random mount point under `/tmp` instead of `/Volumes/<DMGName>`. Avoids
  collision when re-running before previous detach completed. The directory comes from
  `mkdtemp(3)` and prints in its resolved form, `/private/tmp/dmg.XXXXXX`.

`hdiutil attach` prints one line per device entry: the `/dev` node, a tab, a content hint, a tab,
and a mount point when that entry holds a mounted filesystem (`man hdiutil`, section `attach`).
Space padding sits inside the fields, so split on tabs: `grep '^/dev/'` keeps the device lines,
`cut -f 3` prints the third tab-separated field of each, and `grep -m 1 .` keeps the first one
that is not empty. The result has no trailing whitespace. A pattern on
`/Volumes/` or on a literal `/tmp/` prefix never matches a `-mountrandom /tmp` mount, so a check
built on either pattern reports a failed mount and leaves the image attached.

An empty `MOUNT_POINT` means nothing mounted, so there is nothing to detach. When the mount holds
no `<App>.app`, the script detaches it before it exits.

## Copy and detach

```sh
cp -R "${MOUNT_POINT}/<App>.app" /Applications/ || {
    hdiutil detach "${MOUNT_POINT}" -quiet
    echo "fail:<app> (copy to /Applications failed)"
    exit 1
}

hdiutil detach "${MOUNT_POINT}" -quiet
```

`cp -R` over `ditto`: both work for `.app` bundles. `cp -R` is faster and POSIX-portable. `ditto`
preserves extended attributes more aggressively (useful for code-signed apps where xattrs carry
signature metadata) but is macOS-only. Use `cp -R` unless you observe signature breakage afterward.

Always detach in the failure path too: leaving a DMG mounted leaks a device entry.

## Verify the code signature

```sh
codesign --verify --quiet "${CMUX_APP}" 2>&1 || {
    echo "warn:cmux (code signature verification failed — proceed with caution)"
}
```

`codesign --verify` exits non-zero if the bundle is not signed or the signature is invalid. **Warn,
do not fail**: some apps ship unsigned (ad-hoc signed, notarized but signature stripped during DMG
conversion). The script's job is to report the situation, not to enforce a security policy.

For stricter checks, layer `spctl --assess --type execute` (Gatekeeper assessment) on top. Most
install scripts do not need this. The warn-on-codesign-fail is sufficient for the use case.

## Link the CLI

When the app ships a CLI binary inside the bundle (cmux, Visual Studio Code, etc.):

```sh
mkdir -p "$(dirname "${CLI_SYMLINK}")"
ln -sf "${CMUX_APP}/Contents/Resources/bin/cmux" "${CLI_SYMLINK}"
```

`ln -sf` overwrites any existing symlink. Symlink target: `~/.local/bin/<tool>`. That directory
must be on `PATH`. No shell adds it on macOS by default, so check with `command -v <tool>`.

Verify post-symlink:

```sh
if command -v <tool> >/dev/null 2>&1; then
    echo "ok:<tool> ($(command <tool> --version 2>&1 | head -1))"
else
    echo "warn:<tool> installed but CLI not on PATH (expected ~/.local/bin in PATH)"
fi
```

## Post-install hints

Some apps need a one-time setup that the script cannot do (Accessibility opt-in, hooks wiring, App
Store auth):

```sh
echo "      next: launch <app> from /Applications, then run \`<app> hooks setup\`"
echo "            to wire Claude Code lifecycle hooks into ~/.claude/settings.json"
```

Print these *after* successful install so the user knows the manual steps that follow.
