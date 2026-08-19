Every canonical `SKILL.md` uses one H1 whose text equals the frontmatter `name` and skill directory. The identifier is lowercase kebab-case.

Use this H2 vocabulary in order, omitting optional sections that have no content:

- `Prerequisites` (optional): state required tools, access, inputs, or prior state.
- `Constraints` (optional): state boundaries and prohibited actions.
- `Instructions` (required): route or perform the skill's work.
- `Verification` (optional): prove the expected result.
- `Troubleshooting` (optional): recover from known failures.
- `References` (optional): cite sources and supporting material.

Task-specific H3 headings are allowed under `Constraints`, `Instructions`, `Verification`, and `Troubleshooting`. Keep `Prerequisites` and `References` flat. Do not use H4 or deeper headings. More than four H3 headings under `Instructions` warrants moving detail into companion files or splitting the skill; validation warns without failing.

Stable shell is a Runedeck authoring convention. Agent Skills does not prescribe body headings.

Stable shell names the convention above. RuneShell names this rule, which carries the convention to each harness. Validation messages name the convention, so a diagnostic reads `stable shell identity`, never `RuneShell`. Neither name refers to `rune shell`, a planned interactive command.

Standalone `mdschema` enforces the H2 vocabulary, the order, the permitted H3 placements, and the depth limit. Rune's built-in checker verifies only that required sections exist, that heading levels do not skip, and that depth stays within the limit; every optional section above goes unchecked when the standalone checker is absent. Rune always enforces the identity rule and always emits the breadth warning.
