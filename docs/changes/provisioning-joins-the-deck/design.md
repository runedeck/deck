# Provisioning Joins The Deck Design

## Approach

Each skill gets the treatment its benchmark result earned. A skill that changed a correct answer for at least one model moves whole. A skill that changed no answer shrinks to the facts that belong to the owner, and it must then show a changed answer on cases that ask for those facts. A skill that gave weaker advice than the models stays behind.

The scripts move as a clone with history. The clone keeps every commit, so the reason behind each script stays readable, and the deck parts are removed from it in one commit.

## Structure

### Where each source part goes

| Source part | Destination | Treatment |
| --- | --- | --- |
| BrowserbaseToolkit | `runes/provisioning/skills/` | whole, upstream reference keeps its pending adoption review |
| HomebrewToolkit, GhosttyToolkit, TmuxToolkit | `runes/provisioning/skills/` | whole |
| DmgInstall | `runes/provisioning/skills/` | whole, with the `-quiet` contradiction between its two companions fixed |
| GpgToolkit, Chezmoi, SshToolkit, PasswordToolkit, SandboxToolkit, HarnessSecurity | `runes/provisioning/skills/` | rewrite to owner facts: scripts, decisions, local traps |
| DotfilesStrategy | none | stays behind, the chezmoi choice is already in Chezmoi |
| dotfiles boundary rule | `runes/provisioning/rules/` | rewrite with frontmatter, after its comparison |
| scripts, manifests, orchestrator, tests, records, journal | `~/Developer/runedeck/provision` | clone with history |

### Benchmark result that decides each skill

| Skill | Opus 5.5 | Fable 5.1 | Haiku 5.5 |
| --- | --- | --- | --- |
| BrowserbaseToolkit | helps | helps | helps |
| HomebrewToolkit | helps | helps | helps |
| GhosttyToolkit | helps | none | helps |
| DmgInstall | none | helps | helps |
| TmuxToolkit | none | none | helps |
| GpgToolkit | helps a little | none | none |
| the other six | none | none | none |

### Roles and the commands that fill them

| Role | Command | Reads |
| --- | --- | --- |
| validator | `scripts/check-provisioning-module` from the commit and push hooks | every file under `runes/provisioning/` |
| archiver | `rune spec archive` after `scripts/check-provisioning-evidence` | the change's `comparisons/` directory |
| deployer | `rune install` | the deck's default selection and the module's defaults |
| generator | `scripts/record-comparison <workspace>` | a BenchArtifact `benchmark.json` per model |

A comparison record is one file per rune under `docs/changes/<change>/comparisons/<Rune>.json`. The generator writes it from the BenchArtifact results. It lists the models, the cases, and the result of each case with the rune and without it. The evidence check reads it.

The module's defaults give the codebase location as `PROVISION_ROOT`. A skill writes a script path as `$PROVISION_ROOT/scripts/install/<name>.sh`, which resolves through the loader that `environment-variables-supported-syntax` specifies.

## Risks

- The deployer has no flag that keeps a module out of every selection. The `all` cast excludes `provisioning/**` instead. A consumer `.rune` with `include: ['**']` still receives the module, because that pattern asks for every rune. The owner accepted that on 2026-10-26, so the cli needs no change.
- A rewrite can drop a fact that a weaker model needs. The comparison runs on Haiku 5.5 as one of its models.
- The clone carries personal data from the old codebase: names, addresses, and host names in records and manifests. The codebase stays local until task 5.1 passes.
- A script path in a rune breaks when the codebase renames a script. Task 4.3 adds a check in the codebase that resolves every path the module names.
