# Tasks

## 1. Implementation

- [x] 1.1 Point the three term definitions in `runes/core/skills/ReviewChange/SKILL.md` at the glossary pages by repository URL
- [x] 1.2 Add the bundle sentence to `runes/core/rules/ConsultTheOntology.md`
- [x] 1.3 Add the delta for `skill-term-links-survive-deployment` and the changelog line
- [x] 1.4 Move the `AskUserQuestion` text of ReviewChange into a `claude/SKILL.md` variant, so the generic layer names no harness tool

## 2. Verification

- [x] 2.1 `rune validate --skill-layers --source .` prints no `CSI008_LAYER_SOURCE` finding
- [x] 2.2 `rune validate` and `rune spec validate` print no error
- [x] 2.3 `rune spec fix --terms` and `rune spec fix --links` on a copy of the tree leave the URL definitions and the ontology unchanged
- [ ] 2.4 The `contract` check on this change's pull request is green

## 3. Follow-up

- [ ] 3.1 Teach the cli term model to read the repository URL form, so the first-use emphasis rule covers a skill file again
- [ ] 3.2 Once the assembler strips term links into a per-instance definition block (plain-text-first-principles 4.4), decide whether skill definitions return to relative paths
