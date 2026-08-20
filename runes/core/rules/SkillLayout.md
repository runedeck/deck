A skill directory carries one entrypoint and everything that entrypoint routes to. `SKILL.md` is the entrypoint. Its name is fixed; nothing else in the directory shares it.

Companion documents sit beside `SKILL.md` and use PascalCase. The canonical skill directory and frontmatter `name` also use PascalCase.

A nested provider variant is not a canonical skill directory.

A lowercase skill alias must set `disable-model-invocation: true` and forward all work to one canonical skill.

A lowercase command skill is permitted only when its identity equals the executable.

Both lowercase skill types still use identical directory, frontmatter name, and H1 values.

A companion named `CreateWorkflow.md` belongs to `BuildSkill`. A lowercase name uses a different naming system.

Supporting material uses these directories and no others:

- `scripts/`: executable helpers the skill invokes.
- `agents/`: agent definitions the skill dispatches.
- `assets/`: files the skill reads or copies verbatim.
- `references/`: material the skill cites but does not execute.

Anything that does not fit one of those four belongs in a companion document, not a new directory. Two directories holding the same kind of thing is the defect this list exists to prevent.

Provenance sidecars live in `.provenance/`, one per tracked file, named for the file they cover.

Renaming a file under sealed provenance rewrites the `subject.name` its sidecar records, which is evidence rather than metadata. Rename such a file only through Rune tooling that reseals the record.
