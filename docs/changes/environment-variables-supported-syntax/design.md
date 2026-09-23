# Environment variable support design

## Approach

One loader, four sources, one order. The alternative was substitution at build time: the *[assembler][ASSEMBLER]* writes the value into the *[instance][INSTANCE]*. It lost, because the user and the machine own the value and the build does not. One [instance][INSTANCE] then serves every user.

## Worked example

A presentation *[skill][SKILL]* builds slides from images. Its *[state file][STATEFILE]* says: read the images from `${SLIDES_ASSETS:-assets}`. That line is readable in every *[harness][HARNESS]* and falls back to the assets directory when nothing is set. A defaults file that comes with the [skill][SKILL]'s domain sets the assets path. A user who keeps images elsewhere puts one line in their own configuration file, which git ignores.

For Claude Code, the *[basis parameters][BASISPARAMETERS]* add an argument hint for a path and one dynamic context line that runs the loader. The merged values are then in context when the [skill][SKILL] loads. An argument, if given, wins. For Codex and OpenCode, which have no injection, the [instance][INSTANCE] opens with a step that runs the loader in the shell. Each [instance][INSTANCE] carries its *[provenance record][PROVENANCERECORD]*, which names the [basis parameters][BASISPARAMETERS] that produced it.

## Coverage table

| Capability | Requirement | Check or missed requirement |
|---|---|---|
| environment-variables-supported-syntax | Value Sources Have One Order | missed requirement: no check runs the loader against a fixture that sets all four sources |
| environment-variables-supported-syntax | The Loader Exports Environment Variables | missed requirement: no loader exists yet |
| environment-variables-supported-syntax | The Shell Resolves the Variable | missed requirement: no check finds a named variable that no step reads, carried over from the foundations' coverage table |
| environment-variables-supported-syntax | Each Harness Runs the Loader | missed requirement: the assembler writes no loader step and no context line yet |
| environment-variables-supported-syntax | Provenance Shows the Parameters | missed requirement: `scripts/check-provenance` checks that the sidecar exists, and no check reads a parameters field yet |

## Commands

No command implements this change yet. When the cli change that builds the loader exists, this table names the command, flags, hook, and diagnostic ids for each requirement.

## Decisions

- Variables Are $NAME in the foundations allows both shell forms and the shell's default form. This change defines where the value comes from (voice review, 2026-10-18).
- The Shell Resolves the Variable moved here from the foundations, because keeping it there would describe resolution in two places.
- A [harness][HARNESS]'s own placeholders, such as Claude Code's `$ARGUMENTS`, belong to Canon Stays Vendor-Neutral in the foundations. This change leaves them alone.
- Configuration Defaults in one-domain-one-plugin names the same defaults file, the same git-ignored user file, and the same export. It is undecided and probably merges here. Until it is decided, both stand.
- The records behind this change: [CORE-0005](../../decisions/CORE-0005%20Variables%20in%20Markdown%20Instructions%20and%20Templates.md) for the `$NAME` form and [CORE-0020](../../decisions/CORE-0020%20YAML%20Configuration%20Files.md) for the defaults file, the user file, and the export.

## Risks

- The loader runs when a Claude Code [skill][SKILL] loads, so a slow or failing loader delays every invocation. Guard: the loader reads local files only, and a missing file is not an error.
- The defaults rule has two homes while Configuration Defaults stays undecided. Guard: the decisions note names the overlap, and the merge closes it.
- A fallback in the [state file][STATEFILE] hides a missing configuration. Guard: the fallback is a working default and no placeholder.

[ASSEMBLER]: ../../specs/glossary/assembler.md
[INSTANCE]: ../../specs/glossary/instance.md
[SKILL]: ../../specs/glossary/skill.md
[STATEFILE]: ../../specs/glossary/state-file.md
[HARNESS]: ../../specs/glossary/harness.md
[BASISPARAMETERS]: ../../specs/glossary/basis-parameters.md
[PROVENANCERECORD]: ../../specs/glossary/provenance-record.md
