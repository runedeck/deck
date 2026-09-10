# Portable SafetyFirst discovery

## Why

SafetyFirst uses Claude injection to obtain guard state.
Other providers receive literal commands, which do not establish the installed guard state.

## What Changes

- Give the canonical entrypoint an explicit, bounded discovery procedure.
- Move the existing guard policy into one shared companion without changing its text.
- Keep Claude injection in a short provider entrypoint with explicit `mode: replace`.
- Distinguish executable presence, version evidence, and active guard enforcement.
- Put actual process status outside escaped guard output in one bounded JSON record.
- Test real assembly and probe failures with local fixtures.

## Capabilities

### New Capabilities

- `portable-safety-discovery`: Obtain bounded guard evidence through the selected provider.

### Modified Capabilities

None.

## Impact

This change affects only SafetyFirst content, its shared probe helper, its source digest, and focused tests.
It uses existing provider folders, body replacement, and shared companion handling.
It adds no provider, deployment route, CLI feature, or numbered architecture decision.

VCS authorization and denial-recovery policy remain separate readiness work.
The extracted shared policy preserves those existing instructions exactly.
This change does not claim to resolve their known contradictions.
