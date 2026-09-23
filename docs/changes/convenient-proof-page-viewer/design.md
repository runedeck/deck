# Proof page handover design

## Approach

The AcceptanceTesting skill gets one generator that builds the handover page from the casts. The page is then one step at the end of every proof, and the scene list cannot drift from the recording. The [proposal](proposal.md) states why.

## Commands

A requirement names a role. This table names the program and flags behind each requirement, so nothing is lost when a command moves out of a requirement.

| Requirement | Command | Notes |
|---|---|---|
| A proof is handed over as a page | `python3 runes/core/skills/AcceptanceTesting/scripts/proof-page.py --title <title> --player <cast-player.js> --cast <name>=<proof.cast> --out <page.html>` | step 4 of `File the proof` in the skill runs it. The player is html-tools `runtime/cast-player.js` |
| The page builds from the casts alone | the same generator with `--caption <name>=<sentence>` and repeatable `--meta <name>=<fact>` | the scene list comes from the `# Scenario:` lines in each cast. No flag accepts a hand-written list |
