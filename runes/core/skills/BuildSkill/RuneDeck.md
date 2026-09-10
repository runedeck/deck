# Rune deck integration

Read this file when the skill you are authoring lives in a Rune deck. Shared companions describe portable procedures and conditional provider features. This file defines the source layout, assembly rules, and validation commands for Rune.

## Where skills live

A deck groups artifacts by domain, and skills sit under `runes/<domain>/skills/<skill-name>/`. The domain is a routing decision: `core` for the authoring standard, `development` for review and delivery, and so on. Ask the maintainer which domain owns a new skill rather than guessing.

```sh
mkdir -p runes/<domain>/skills/<skill-name>
```

Casts name a selection of runes for a consumer to install together. A new skill needs no cast entry unless the maintainer wants it in a named bundle.

## What validation expects

The validators enforce the heading convention. The deck applies the length limits during review. The `.mdschema` beside each `skills/` directory checks the section shell. Its diagnostics call this check `stable shell identity`. Rune warns when a `SKILL.md` body exceeds 100 lines, excluding frontmatter. Deck review treats 150 lines as the limit. Markdown companions must stay under 150 lines.

## Validation

```sh
rune validate --source .
rune validate --skill-layers --source <skill-path>
```

Rune's built-in schema checker is a partial fallback. It reports required-section presence and heading depth, but it does not replace standalone `mdschema` for section vocabulary, ordering, uniqueness, or subsection placement:

```sh
mdschema check <skill-path>/SKILL.md --schema runes/<domain>/skills/.mdschema
```

The ordinary project and schema checks run under `make validate`, which the commit hook invokes. The source-layer check is separate and required for skill changes. It checks canonical, harness, model, user, and effective content against the configured provider and model registry. Quoted examples and conditional instructions receive the same literal checks as other text.

Do not infer deployment readiness from these checks. Inspect the rendered bundles and obtain native evidence before claiming native readiness. See [ValidateWorkflow.md](ValidateWorkflow.md).

## Source layers

Keep generic instructions in `SKILL.md` and shared companions. Use `<provider>/SKILL.md` for a harness variant and `<provider>/<model>/SKILL.md` for an exact configured model variant. Every variant declares `mode: append`, `mode: prepend`, or `mode: replace`.

A harness variant can contain only metadata with an empty body when its mode is `append` or `prepend`. Model variants can contain only `mode` in frontmatter. Keep effective `name`, `description`, and body nonempty.

Assembly selects one variant: the matching model variant first, otherwise the matching harness variant. It merges that winner with the canonical entrypoint. A model variant does not inherit its harness variant's body or metadata.

Provider and model folders do not supply companion overrides. Keep shared companions at the skill root or in ordinary support directories. A local `user/SKILL.md` is a complete replacement with `mode: replace`, the canonical name, a description, and a full body. Local `user/` companion files replace whole files at matching relative paths.

## Deployment

```sh
rune install
```

Assembly maps canonical content into each provider's native format without changing the canonical contract: frontmatter is stripped to the fields a provider keeps, tool names are remapped, and provider-specific fields come from `claude/` and other qualifier variants rather than from the canonical file.

This deck authors skill names in PascalCase. The opt-in `agentskills` provider in Rune enables `kebab-case-skills` because it requires lowercase names.

The rule converts directory segments, Markdown companion names, and the frontmatter `name`. It also updates relative Markdown links. These changes keep companion links valid.

`SKILL.md`, bundled scripts, and assets keep their exact names. Harnesses, Python module paths, and in-document references use those exact names.

Never edit a deployed file under a provider directory. Edit the source and reinstall. Put a local exception in the rune's `user/` override using the replacement rules above.

## Per-user configuration

A skill that needs per-user runtime data reads one file at `~/.config/rune/<artifact>.{ext}`. [UserConfigSchema.md](UserConfigSchema.md) describes the file. [SkillInstallation.md](SkillInstallation.md) has the setup step.

## Adopting rather than authoring

Third-party artifacts do not go through this skill. They enter through `rune adopt`, which records a maintainer verdict on every block and seals a review record. Use the `AdoptArtifact` skill for that. Use this skill only for artifacts that you author.
