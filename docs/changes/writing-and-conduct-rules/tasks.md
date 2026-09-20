# Tasks

## 1. Authoring

- [x] 1.1 Add each rule with the text that is deployed in the owner's harness
- [x] 1.2 Add the rules to the `prose`, `authoring`, and `delivery` casts

## 2. Verification

- [x] 2.1 `rune validate` passes with the rules present
- [ ] 2.2 One bench run for each rule against a baseline with no rule (BenchArtifact). A rule with no measured effect leaves the default casts
- [ ] 2.3 Record each verdict as the rule's `rune:verdict` pointer, which clears the RuleShape warning

## 3. Record

- [ ] 3.1 Archive moves `adr.md` to `docs/decisions/` with the next free DECK number
