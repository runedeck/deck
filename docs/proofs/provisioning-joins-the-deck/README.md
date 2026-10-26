---
type: proof
change: provisioning-joins-the-deck
head: d4164ca9a5308ef0e142aaca34134527839e7b72
head_change: npqsvqlstvzqzwtqvmzrmyrzvnvnuzsy
head_tree: 5a48ae5bc6c3506b32bb42f8519f1df2c6251048
recorded: 2026-10-26
transcript: dd02028ab29bbe55864b572a5b03432cf837635f6a37882569b021119115769a
scenes:
- scenario: provisioning-joins-the-deck#provisioning-runes-share-one-module/machine-setup-skill-joins-the-deck
  kind: check
- scenario: provisioning-joins-the-deck#the-validator-rejects-executable-files-in-the-module/install-script-enters-the-module
  kind: check
- scenario: provisioning-joins-the-deck#the-default-deployment-omits-the-module/consumer-takes-the-default-selection
  kind: check
- scenario: provisioning-joins-the-deck#a-provisioning-rune-shows-that-it-helps/rune-arrives-without-a-comparison
  kind: check
- scenario: provisioning-joins-the-deck#provisioning-runes-point-at-scripts-inside-the-provisioning-codebase/deployed-skill-points-at-an-install-script
  kind: unproven
- scenario: provisioning-joins-the-deck#provisioning-runes-contain-no-personal-data/skill-contains-the-owner-s-host-name
  kind: check
---

# Proof: provisioning-joins-the-deck

One `console` scene per scenario of the `provisioning-joins-the-deck` delta specification, in closure order. The candidates are the provisioning module under `runes/provisioning/` and the `all` cast with the deployer. The checks `scripts/check-provisioning-module` and `scripts/check-provisioning-evidence` with their hook entries are candidates too, as is the path check `scripts/verify/deck-script-paths.sh` in the provisioning codebase. Each scene runs the real tools.

A scene that starts with `$ cd .` reads the working copy and does not write to it. Each other scene builds a scratch copy in a fresh temporary directory, which the runner removes when the scene ends. The consumer scene keeps `HOME` and `XDG_CONFIG_HOME` inside that directory, so the run never reads or writes `~/.config/rune/`. The runner resolves `rune` to the binary that runs the proof, and `RUNE_PROOF_ROOT` names the working copy. `deployed-module-runes.py` beside this file lists, for each harness tree of a consumer, the names of the provisioning runes present in it.

The scene `Deployed skill points at an install script` needs the provisioning codebase at the location the module's defaults give, `~/Developer/runedeck/provision`, so it runs on the owner's machine.

`proof.txt` is the transcript and `proof.cast` the recording. The frontmatter binds the transcript digest and the head commit. Re-record from the repository root after a change to a scene or a candidate. Commit the scenes first and run from an empty working copy, so the head is the commit the proof binds. Then commit the recording above it:

```sh
rune proof run provisioning-joins-the-deck
rune proof run provisioning-joins-the-deck --check
```

## provisioning-joins-the-deck#provisioning-runes-share-one-module/machine-setup-skill-joins-the-deck

`module.yaml` declares the module `provisioning`. The skills about machine setup and the dotfiles rule are under `runes/provisioning/`. A search of the whole `runes/` tree finds each name once, so no other module contains a copy.

```console
$ cd .
$ cat runes/provisioning/module.yaml
name: provisioning
version: 0.1.0
description: Machine setup skills and rules that hold the facts models lack, with every script outside the deck.
events: []
$ ls runes/provisioning/skills
Chezmoi
DmgInstall
GhosttyToolkit
GpgToolkit
HarnessSecurity
HomebrewToolkit
PasswordToolkit
SandboxToolkit
SshToolkit
TmuxToolkit
$ ls runes/provisioning/rules
DotfilesScope.md
$ sh -c 'for name in $(ls runes/provisioning/skills); do fd -t d "^$name$" runes; done'
runes/provisioning/skills/Chezmoi/
runes/provisioning/skills/DmgInstall/
runes/provisioning/skills/GhosttyToolkit/
runes/provisioning/skills/GpgToolkit/
runes/provisioning/skills/HarnessSecurity/
runes/provisioning/skills/HomebrewToolkit/
runes/provisioning/skills/PasswordToolkit/
runes/provisioning/skills/SandboxToolkit/
runes/provisioning/skills/SshToolkit/
runes/provisioning/skills/TmuxToolkit/
$ fd '^DotfilesScope\.md$' runes
runes/provisioning/rules/DotfilesScope.md
```

## provisioning-joins-the-deck#the-validator-rejects-executable-files-in-the-module/install-script-enters-the-module

A scratch copy of the module passes the check. A shell script with an execute permission and an interpreter line enters the copy. The check reports the file and exits 1. The hook entry runs the same check on each commit and push that touches the module. The change fails its checks.

```console
$ sh -c 'mkdir -p scratch/runes scratch/scripts && cp -R "$RUNE_PROOF_ROOT/runes/provisioning" scratch/runes/ && cp "$RUNE_PROOF_ROOT/scripts/check-provisioning-module" scratch/scripts/'
$ python3 scratch/scripts/check-provisioning-module scratch
$ sh -c 'printf "#!/bin/sh\nbrew install --cask ghostty\n" > scratch/runes/provisioning/skills/GhosttyToolkit/install.sh'
$ chmod +x scratch/runes/provisioning/skills/GhosttyToolkit/install.sh
$ head -n 1 scratch/runes/provisioning/skills/GhosttyToolkit/install.sh
#!/bin/sh
$ python3 scratch/scripts/check-provisioning-module scratch
? 1
runes/provisioning/skills/GhosttyToolkit/install.sh: execute permission and interpreter line
$ sh -c 'rg -e "check-provisioning-module" "$RUNE_PROOF_ROOT/.pre-commit-config.yaml"'
[..]- id: check-provisioning-module
[..]entry: python3 scripts/check-provisioning-module
```

## provisioning-joins-the-deck#the-default-deployment-omits-the-module/consumer-takes-the-default-selection

A scratch consumer takes the deck's `all` cast. The deployer writes every harness tree, and no tree holds a provisioning rune. The consumer then selects the module with `rune add provisioning` and installs again. Each harness tree receives the provisioning skills and the dotfiles rule. The Codex harness reads skills from `.agents/skills/`, so `.codex/` receives the rule and `.agents/` the skills.

```console
$ sh -c 'mkdir -p home/.config consumer && printf "version: 1\nsources:\n  deck:\n    local: %s\nrunes:\n  deck:\n    casts: [all]\n" "$RUNE_PROOF_ROOT" > consumer/.rune'
$ cat consumer/.rune
version: 1
sources:
  deck:
    local: [..]
runes:
  deck:
    casts: [all]
$ sh -c 'cd consumer && HOME="$PWD/../home" XDG_CONFIG_HOME="$PWD/../home/.config" rune install --no-color'
...
 ✓ claude
...
 ✓ codex
...
 ✓ gemini
...
 ✓ opencode
...
 ● [..] deployed
$ sh -c 'python3 "$RUNE_PROOF_ROOT/docs/proofs/provisioning-joins-the-deck/deployed-module-runes.py" consumer'
.agents: none
.claude: none
.codex: none
.gemini: none
.opencode: none
$ sh -c 'cd consumer && HOME="$PWD/../home" XDG_CONFIG_HOME="$PWD/../home/.config" rune add provisioning --no-color'
...
staged rune selection 'provisioning' in consumer → [..]
next: rune install (or: rune tui --edit to review)
$ cat consumer/.rune
version: 1
sources:
  deck:
    local: [..]
runes:
  deck:
    casts:
    - all
    include:
    - provisioning
$ sh -c 'cd consumer && HOME="$PWD/../home" XDG_CONFIG_HOME="$PWD/../home/.config" rune install --no-color'
...
 ✓ claude
...
 ✓ codex
...
 ✓ gemini
...
 ✓ opencode
...
 ● [..] deployed  ○ [..] skipped
$ sh -c 'python3 "$RUNE_PROOF_ROOT/docs/proofs/provisioning-joins-the-deck/deployed-module-runes.py" consumer'
.agents: Chezmoi DmgInstall GhosttyToolkit GpgToolkit HarnessSecurity HomebrewToolkit PasswordToolkit SandboxToolkit SshToolkit TmuxToolkit
.claude: Chezmoi DmgInstall DotfilesScope GhosttyToolkit GpgToolkit HarnessSecurity HomebrewToolkit PasswordToolkit SandboxToolkit SshToolkit TmuxToolkit
.codex: DotfilesScope
.gemini: Chezmoi DmgInstall DotfilesScope GhosttyToolkit GpgToolkit HarnessSecurity HomebrewToolkit PasswordToolkit SandboxToolkit SshToolkit TmuxToolkit
.opencode: Chezmoi DmgInstall DotfilesScope GhosttyToolkit GpgToolkit HarnessSecurity HomebrewToolkit PasswordToolkit SandboxToolkit SshToolkit TmuxToolkit
```

## provisioning-joins-the-deck#a-provisioning-rune-shows-that-it-helps/rune-arrives-without-a-comparison

A scratch copy contains the module and the change's comparison records, one per rune. The check passes. The record of one skill leaves the copy. The check reports that rune and exits 1. The hook entry runs the same check on each commit that touches the module or a change directory. The archiver refuses the change.

```console
$ sh -c 'mkdir -p scratch/runes scratch/scripts scratch/docs/changes/provisioning-joins-the-deck && cp -R "$RUNE_PROOF_ROOT/runes/provisioning" scratch/runes/ && cp -R "$RUNE_PROOF_ROOT/docs/changes/provisioning-joins-the-deck/comparisons" scratch/docs/changes/provisioning-joins-the-deck/ && cp "$RUNE_PROOF_ROOT/scripts/check-provisioning-evidence" scratch/scripts/'
$ ls scratch/docs/changes/provisioning-joins-the-deck/comparisons
Chezmoi.json
DmgInstall.json
DotfilesScope.json
GhosttyToolkit.json
GpgToolkit.json
HarnessSecurity.json
HomebrewToolkit.json
PasswordToolkit.json
SandboxToolkit.json
SshToolkit.json
TmuxToolkit.json
$ python3 scratch/scripts/check-provisioning-evidence scratch
$ rm scratch/docs/changes/provisioning-joins-the-deck/comparisons/TmuxToolkit.json
$ python3 scratch/scripts/check-provisioning-evidence scratch
? 1
runes/provisioning/skills/TmuxToolkit: no comparison record
$ sh -c 'rg -e "check-provisioning-evidence" "$RUNE_PROOF_ROOT/.pre-commit-config.yaml"'
[..]- id: check-provisioning-evidence
[..]entry: python3 scripts/check-provisioning-evidence
```

## provisioning-joins-the-deck#provisioning-runes-point-at-scripts-inside-the-provisioning-codebase/deployed-skill-points-at-an-install-script

The module's defaults give `PROVISION_ROOT`, the location of the provisioning codebase. A skill writes each script path as `$PROVISION_ROOT/scripts/<verb>/<target>.sh`, and the deployer copies that text unchanged into each harness tree. The codebase's own check runs from its default location with `DECK_ROOT` at the working copy. It resolves each path the module gives and reports none missing.

```console
$ cd .
$ tail -n 1 runes/provisioning/defaults.yaml
PROVISION_ROOT: ~/Developer/runedeck/provision
$ rg -o -e '\$PROVISION_ROOT/scripts/[A-Za-z0-9_./-]+\.sh' runes/provisioning/skills/HarnessSecurity/SKILL.md
$PROVISION_ROOT/scripts/configure/codex.sh
$PROVISION_ROOT/scripts/configure/dcg.sh
$PROVISION_ROOT/scripts/install/dcg.sh
$PROVISION_ROOT/scripts/configure/claude-plugins.sh
$PROVISION_ROOT/scripts/verify/harness-proxy.sh
$PROVISION_ROOT/scripts/verify/ai-proxy-egress.sh
$PROVISION_ROOT/scripts/verify/codex-skills.sh
$ DECK_ROOT=. sh -c '"$HOME/Developer/runedeck/provision/scripts/verify/deck-script-paths.sh"'
...
verify:deck-script-paths
      module: ./runes/provisioning
...
summary:deck-script-paths ([..] checked, 0 missing)
```

## provisioning-joins-the-deck#provisioning-runes-contain-no-personal-data/skill-contains-the-owner-s-host-name

Review, not a hook, rejects a provisioning rune that contains personal data. The concrete check a reviewer runs is a pattern scan of the module. The patterns are an email address, a home directory on macOS with an account name, a host name with a local suffix, and an `ssh user@host` target. On a scratch copy of the module the scan returns nothing. A line with a host name enters one skill of the copy. The scan reports the line, and the reviewer rejects the change.

```console
$ sh -c 'mkdir -p scratch/runes && cp -R "$RUNE_PROOF_ROOT/runes/provisioning" scratch/runes/'
$ rg -n -e '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' -e '/Users/[A-Za-z0-9_.-]+' -e '\b[A-Za-z0-9-]+\.(local|lan|home|internal)\b' -e 'ssh +[A-Za-z0-9_-]+@' scratch/runes/provisioning
? 1
$ sh -c 'printf "Connect with ssh owner@laptop.local before the key lands.\n" >> scratch/runes/provisioning/skills/SshToolkit/SKILL.md'
$ rg -n -e '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' -e '/Users/[A-Za-z0-9_.-]+' -e '\b[A-Za-z0-9-]+\.(local|lan|home|internal)\b' -e 'ssh +[A-Za-z0-9_-]+@' scratch/runes/provisioning
scratch/runes/provisioning/skills/SshToolkit/SKILL.md:[..]:Connect with ssh owner@laptop.local before the key lands.
```
