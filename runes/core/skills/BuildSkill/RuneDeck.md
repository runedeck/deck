# Rune deck integration

Everything in the other companions is portable: it holds for a skill shipped anywhere. This file is the part that only holds inside a Rune deck. Read it when the skill you are authoring lives in one.

## Where skills live

A deck groups artifacts by domain, and skills sit under `runes/<domain>/skills/<skill-name>/`. The domain is a routing decision: `core` for the authoring standard, `development` for review and delivery, and so on. Ask the maintainer which domain owns a new skill rather than guessing.

```sh
mkdir -p runes/<domain>/skills/<skill-name>
```

Casts name a selection of runes for a consumer to install together. A new skill needs no cast entry unless the maintainer wants it in a named bundle.

## The body convention has a name here

The heading convention the other companions describe is distributed to each harness by the `RuneShell` rule, and enforced by the `.mdschema` beside each `skills/` directory. Validation messages name the convention rather than the rule, so a diagnostic reads `stable shell identity`, never `RuneShell`. Neither name refers to `rune shell`, a planned interactive command.

The body length limits come from the `ArtifactLength` rule: a `SKILL.md` body warns after 100 lines and fails after 150, excluding frontmatter, and Markdown companions stay under 150.

## Validation

```sh
rune validate --source .
```

Rune's built-in schema checker is a partial fallback. It reports required-section presence and heading depth, but it does not replace standalone `mdschema` for section vocabulary, ordering, uniqueness, or subsection placement:

```sh
mdschema check <skill-path>/SKILL.md --schema runes/<domain>/skills/.mdschema
```

Both run under `make validate`, which the commit hook invokes.

## Deployment

```sh
rune install
```

Assembly maps canonical content into each provider's native format without changing the canonical contract: frontmatter is stripped to the fields a provider keeps, tool names are remapped, and provider-specific fields come from `claude/` and other qualifier variants rather than from the canonical file.

A deck that authors skills in PascalCase enables the `kebab-case` assembly rule for its providers. Directory segments and Markdown companions convert, the frontmatter `name` converts with them, and relative Markdown links are retargeted so companions stay reachable. `SKILL.md`, bundled scripts, and assets keep their exact names, because harnesses, Python module paths, and in-document references all resolve those by spelling.

Never edit a deployed file under a provider directory. Edit the source and reinstall; a local exception belongs in the rune's `user/` override.

## Per-user configuration

A skill that needs per-user runtime data reads one file per artifact at `~/.config/rune/<artifact>.{ext}`. See [UserConfigSchema.md](UserConfigSchema.md) for the shape, and [SkillInstallation.md](SkillInstallation.md) for the setup step that creates it.

## Adopting rather than authoring

An artifact that comes from somewhere else does not go through this skill. It enters the deck through `rune adopt`, which segments it and records a maintainer verdict on every block before sealing a review record. Use the `adopt-artifact` skill for that workflow, and this one only for what you write yourself.
