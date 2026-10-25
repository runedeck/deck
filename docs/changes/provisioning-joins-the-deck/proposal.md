---
adr: "docs/changes/provisioning-joins-the-deck/adr.md"
status: proposed
decisions: ["Provisioning runes join the deck and scripts stay outside it"]
---

# Provisioning Joins The Deck

## Why

The deck gains a provisioning module that contains only the setup facts models lack, and the scripts that change a machine move to a separate codebase that the deck never deploys.

The owner's machine setup is one codebase with skills, a rule, scripts, manifests, and decision records. A benchmark on three models showed that most of its skills repeat what the models already know. The facts that did change an answer were the owner's own: newer interfaces, house conventions, and tested fixes. The deck keeps those facts and leaves the restated documentation behind.

## What Changes

- A new `provisioning` module in `runes/` with skills and rules only. The default deployment of the deck leaves it out.
- A check that reports every executable file in the module.
- A check that refuses a provisioning rune without a recorded comparison on at least two models.
- Five skills move whole: BrowserbaseToolkit, HomebrewToolkit, GhosttyToolkit, DmgInstall, and TmuxToolkit.
- Six skills move as rewrites that contain only the owner's facts: GpgToolkit, Chezmoi, SshToolkit, PasswordToolkit, SandboxToolkit, and HarnessSecurity.
- DotfilesStrategy stays behind. The dotfiles boundary rule moves after its own comparison.
- The scripts, manifests, orchestrator, tests, and decision records move with their history to `~/Developer/runedeck/provision`, which stays unpublished until a personal-data review.
- The old codebase is archived.

## Capabilities

- provisioning-joins-the-deck (new)

## Impact

- New module `runes/provisioning/` with its defaults, schemas, and runes.
- New checks under `scripts/` and their hooks.
- The deck's default selection, or the module's defaults, so the default deployment omits the module.
- New local codebase `~/Developer/runedeck/provision`, and its entry in the workshop's list of active clones.
- The old codebase on GitHub, which the owner archives.
