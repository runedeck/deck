# Cloud environment

## Why

The cloud agent environment installs the deck's pinned tools on every run and pushes from an identity the attribution contract must accept. The delta that describes both merged in #53 without a proposal or a task list, so `rune spec doctor` reports the change as broken on every run.

## What Changes

- The cloud installer downloads and verifies each pinned release asset on every run and never trusts a binary already on the path.
- A digest mismatch stops before extraction and leaves the existing installation untouched.
- The standalone `mdschema` validator installs through the same verified path.
- The quality workflow runs the installer regression suite with local assets and isolated paths.
- Outgoing commits and explicit-bookmark pushes from the cloud environment follow the canonical commit attribution contract.

## Capabilities

- `cloud-agent-environments`

## Impact

- `.cursor/install.sh`, `.cursor/environment.json`, and the installer tests.
- `.githooks/jj-push-bookmark.py` and `scripts/author-identity.py`.
