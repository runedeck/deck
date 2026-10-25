# Brew and commit signing

`brew tap-new`, and any edit brew commits inside a tap repo, auto-commit and run the commit-signing path. With the signing key on a YubiKey, expect a PIN or touch prompt to appear mid-`brew`; approve it. A cancelled prompt fails that git step (the tap scaffold lands but uncommitted) rather than the whole command, re-run the commit to finish.
