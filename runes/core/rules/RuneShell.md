Every canonical `SKILL.md` uses one H1 whose text equals the frontmatter `name` and skill directory. The identifier uses PascalCase.

Use this H2 vocabulary in order, omitting optional sections that have no content:

- `Prerequisites` (optional): state required tools, access, inputs, or prior state.
- `Constraints` (optional): state boundaries and prohibited actions.
- `Instructions` (required): route or perform the skill's work.
- `Verification` (optional): prove the expected result.
- `Troubleshooting` (optional): recover from known failures.
- `References` (optional): cite sources and supporting material.

Put task-specific H3 headings only under `Constraints`, `Instructions`, `Verification`, and `Troubleshooting`. Keep `Prerequisites` and `References` flat. Do not use H4 or deeper headings.

If `Instructions` has more than four H3 headings, move details into companion files or split the skill. Validation warns but does not fail.

Stable shell is a Runedeck authoring convention. Agent Skills does not prescribe body headings.

Stable shell names the convention above. RuneShell names this rule, which carries the convention to each harness. Validation messages name the convention, so a diagnostic reads `stable shell identity`, never `RuneShell`. Neither name refers to `rune shell`, a planned interactive command.

Standalone `mdschema` enforces the H2 vocabulary, order, permitted H3 locations, and depth limit. Rune's built-in checker verifies only required sections, heading sequence, and depth.

Without the standalone checker, Rune does not check optional sections. Rune always enforces identity and always warns about breadth.
