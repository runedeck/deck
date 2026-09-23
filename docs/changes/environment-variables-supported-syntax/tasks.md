## 1. Specifications

- [ ] 1.1 Decide the overlap with Configuration Defaults in one-domain-one-plugin: merge it here or keep both
- [ ] 1.2 Decide whether the loader needs an ontology term beside the roles

## 2. Implementation

- [ ] 2.1 Build the loader: merge the four sources in order and export the result as environment variables
- [ ] 2.2 Teach the assembler the Claude Code form: the argument hint and the dynamic context line from the basis parameters
- [ ] 2.3 Teach the assembler the Codex and OpenCode form: a first step that runs the loader
- [ ] 2.4 Write the basis parameters into the provenance record
- [ ] 2.5 Convert one skill as the worked example: a presentation skill and its assets directory variable

## 3. Verification

- [ ] 3.1 A fixture that sets all four sources proves the order
- [ ] 3.2 A recorded proof shows the Claude Code instance and a Codex instance loading the same value
- [ ] 3.3 `openspec validate --all --strict` and `rune spec validate environment-variables-supported-syntax` pass
- [ ] 3.4 Every missed requirement in the coverage table has a task above
