A skill directory carries one entrypoint and everything that entrypoint routes to. `SKILL.md` is the entrypoint. Its name is fixed; nothing else in the directory shares it.

Companion documents sit beside `SKILL.md` and take the skill's own casing: lowercase kebab-case, matching the directory and the frontmatter `name`. A companion named `create-workflow.md` belongs to `build-skill`; one named `CreateWorkflow.md` reads as a different naming system living in the same directory.

Supporting material uses these directories and no others:

- `scripts/`: executable helpers the skill invokes.
- `agents/`: agent definitions the skill dispatches.
- `assets/`: files the skill reads or copies verbatim.
- `references/`: material the skill cites but does not execute.

Anything that does not fit one of those four belongs in a companion document, not a new directory. Two directories holding the same kind of thing is the defect this list exists to prevent.

Provenance sidecars live in `.provenance/`, one per tracked file, named for the file they cover.

Renaming a file under sealed provenance rewrites the `subject.name` its sidecar records, which is evidence rather than metadata. Rename such a file only through Rune tooling that reseals the record. `build-skill` predates this rule and keeps PascalCase companions for that reason; it conforms once a supported rename exists.
