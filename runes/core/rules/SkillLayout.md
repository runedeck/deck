A canonical skill directory carries one root entrypoint and everything that entrypoint routes to. `SKILL.md` is the entrypoint. Its name is fixed.

Companion documents sit beside `SKILL.md` and use PascalCase. The canonical skill directory and frontmatter `name` also use PascalCase.

Provider variants use `<provider>/SKILL.md`. Model variants use `<provider>/<exact-model-id>/SKILL.md`, with an ID from the configured model registry. These nested entrypoints are variants of the canonical skill, not separate canonical skills. Each variant declares an explicit body mode.

A lowercase skill alias must set `disable-model-invocation: true` and forward all work to one canonical skill.

A lowercase command skill is permitted only when its identity equals the executable.

Both lowercase skill types still use identical directory, frontmatter name, and H1 values.

A companion named `CreateWorkflow.md` belongs to `BuildSkill`. A lowercase name uses a different naming system.

Supporting material belongs in directories that `SKILL.md` or a routed file references, with one directory for each role.

Provenance sidecars live in `.provenance/`, one per tracked file, named for the file they cover.

Renaming a file under sealed provenance rewrites the `subject.name` its sidecar records, which is evidence rather than metadata. Rename such a file only through Rune tooling that reseals the record.
