Add an opt-in `provisioning` module that holds only the machine setup facts models lack, with a comparison record for every rune.

## Plan

A benchmark of the forge-provision skills on Opus 5.5, Fable 5.1, and Haiku 5.5 showed that most of them repeat what the models already know. This change ports only what changes an answer into a `provisioning` module that the `all` cast leaves out. The scripts that change a machine moved to the private provisioning codebase, and each skill names them as `$PROVISION_ROOT/scripts/...`. Every rune carries a comparison record, and the archiver refuses a rune without one.

## Changes

- Add `runes/provisioning/` with its module identity, `PROVISION_ROOT` defaults, schemas, README, and license, and exclude `provisioning/**` in `casts/all.yaml`.
- Add `scripts/check-provisioning-module`, which rejects an executable file in the module, with its hook and test.
- Add `scripts/record-comparison`, which writes a record from graded benchmark runs, and `scripts/check-provisioning-evidence`, which refuses a rune without a changed answer on two models, with hooks, tests, and quality steps.
- Move HomebrewToolkit, GhosttyToolkit, DmgInstall, and TmuxToolkit whole: the DmgInstall mount step reads the real mount point, and HomebrewToolkit's Claude-only syntax sits in a `claude/` variant.
- Rewrite GpgToolkit, SshToolkit, PasswordToolkit, Chezmoi, SandboxToolkit, and HarnessSecurity to the owner's scripts, decisions, and traps, and add the DotfilesScope rule.
- Add one comparison record per rune under `docs/changes/provisioning-joins-the-deck/comparisons/`.
- Add `docs/changes/provisioning-joins-the-deck/` with the proposal, design, delta spec, `adr.md`, tasks, and storyboard frames, and the proof under `docs/proofs/provisioning-joins-the-deck/`.

## Testing

- [x] `rune validate` reports 0 errors, `rune spec validate` is clean, and `rune validate --skill-layers` reports only the ReviewChange CSI008 errors that `main` already has.
- [x] The four new test files pass, and `check-provisioning-module` and `check-provisioning-evidence` exit 0 on the tree.
- [x] `rune proof run provisioning-joins-the-deck` proves 6 of 6 scenes, and `--check` holds.
- [x] The comparison records come from 120 runs on Opus 5.5, Fable 5.1, and Haiku 5.5, each case with the rune and without it.

## Release Notes

- Add an opt-in `provisioning` module: `rune add provisioning` installs machine setup skills that point at scripts in a separate provisioning codebase.
