## 1. Specifications

- [ ] 1.1 Name the model identifiers the assembler knows, and where a model sidecar lives beside the canon
- [ ] 1.2 Name the harness events that carry a model change, for each harness

## 2. Implementation

- [ ] 2.1 Build a variant for each known model from the canon and the model's sidecar
- [ ] 2.2 Resolve variants in the order user, harness and model, harness, base rune
- [ ] 2.3 Write the hook that reads the active model at session start and on a model change
- [ ] 2.4 Make the hook swap in the model's variant, or inject its difference as context
- [ ] 2.5 Keep the deployment check true across a swap

## 3. Verification

- [ ] 3.1 A fixture with a user variant, a harness and model variant, and a harness variant proves the order
- [ ] 3.2 A recorded proof shows a model change in a session and the swapped variant
- [ ] 3.3 `openspec validate --all --strict` and `rune spec validate one-instance-per-model` pass
- [ ] 3.4 Every missed requirement in the coverage table has a task above
