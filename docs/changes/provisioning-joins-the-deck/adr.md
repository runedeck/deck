---
title: "Provisioning runes join the deck and scripts stay outside it"
description: "The deck gains a provisioning module for the facts models lack, and the scripts that change a machine move to a separate codebase that the deck never deploys."
type: adr
category: architecture
tags:
    - adr
    - architecture
    - provisioning
status: proposed
created: 2026-10-25
updated: 2026-10-25
author: "@N4M3Z"
project: deck
related: []
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-opus-5-5@claude"]
informed: []
upstream:
    - "https://github.com/N4M3Z/forge-provision"
    - "provisioning-joins-the-deck#provisioning-runes-share-one-module"
    - "provisioning-joins-the-deck#the-validator-rejects-executable-files-in-the-module"
    - "provisioning-joins-the-deck#the-default-deployment-omits-the-module"
    - "provisioning-joins-the-deck#a-provisioning-rune-shows-that-it-helps"
change: provisioning-joins-the-deck
---

# Provisioning runes join the deck and scripts stay outside it

## Context and Problem Statement

The owner's machine setup is one codebase: twelve skills, one rule, shell scripts that install and configure the machine, package manifests, and decision records ([forge-provision][SOURCE]). The deck has no module for any of it. A benchmark ran each skill on two cases with the skill and without it, on Opus 5.5, Fable 5.1, and Haiku 5.5. Six skills changed no model's answer. One skill gave weaker advice than the models gave without it. Five skills helped at least one model, and each time the skill carried a fact that no model learns in training: an interface newer than the training data, a convention of the owner, or a fix the owner tested. The deck must not deploy scripts that change a machine, and its default deployment must not install provisioning. The question is what enters the deck, in which form, and where the scripts go.

## Considered Options

1. Move the whole codebase into one deck module, scripts included. Every consumer of the deck would then receive code that changes a machine.
2. Keep the codebase and deploy its skills from it as a second source. The skills stay unreviewed, and most of them repeat what the models already know.
3. Port only the instructions that change a model's answer into a deck module that the default deployment omits. Move the scripts, manifests, and records into a separate provisioning codebase.

## Decision Outcome

Option 3.

- HomebrewToolkit, GhosttyToolkit, DmgInstall, and TmuxToolkit move as whole skills. Each one helped at least one model. BrowserbaseToolkit also helped, and it moved to the development module through the change automate-cloud-browsers-browserbase.
- GpgToolkit, Chezmoi, SshToolkit, PasswordToolkit, SandboxToolkit, and HarnessSecurity shrink to the facts that belong to the owner: the scripts to run, the decisions that apply, and the traps found on this machine.
- DotfilesStrategy does not move. Its comparison of tools is general knowledge, and the owner's choice of chezmoi is already part of the Chezmoi skill.
- The dotfiles boundary rule moves as a rule after its own comparison.
- Scripts, manifests, the orchestrator, tests, and decision records move to `~/Developer/runedeck/provision`. That codebase stays unpublished until a review removes personal data from it.
- The old codebase is archived after the move.

### Consequences

- [+] A consumer of the whole deck receives no provisioning rune and no script.
- [+] Every provisioning rune carries a comparison that shows it changes an answer, so the module contains no restated documentation.
- [+] The deck stays public while the scripts, which name the owner's machines and accounts, stay private.
- [-] Two places hold one subject: the deck holds the instructions, and the provisioning codebase holds the scripts. A rename in the codebase can break a path in a rune.
- [-] Every port costs a comparison run on at least two models before the change can archive.
- [-] The six rewritten skills lose general guidance that a weaker model might need. The comparison covered three models only.

## More Information

The benchmark results are in the owner's working layer at `~/Data/Benchmarks/forge-provision/`, iterations 1 and 2, one workspace per skill. The cases test answers to questions, not the behavior of an agent inside the codebase. A later comparison with tasks in a scratch copy of the codebase can show whether the rewritten skills steer an agent to the owner's scripts.

[SOURCE]: https://github.com/N4M3Z/forge-provision
