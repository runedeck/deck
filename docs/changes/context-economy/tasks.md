## 1. Decisions

- [x] 1.1 Write CORE-0013 Context Economy with the evidence and the layer map
- [x] 1.2 Write CORE-0014 No Performance Personas with the study citation and the voice carve-out
- [x] 1.3 Write CORE-0015 Positive Instruction with the prohibition carve-out
- [x] 1.4 Write the forge-core compatibility table into CORE-0013 (CORE-0001..0012, ARCH-0001, 0004, 0011, 0014)
- [x] 1.5 Write CORE-0017 The Inference Turn: what loads at session start, per turn, and after compaction
- [x] 1.6 Write CORE-0016 Adversarial Review over Councils: refutation replaces consensus

## 2. Gates

- [ ] 2.1 Add the rule-budget check to prek and quality (50 words, one instruction, with a baseline for the sixteen current rules)
- [ ] 2.2 Add the persona and negation Vale style, warning severity
- [ ] 2.3 Add the duplicated-sentence sweep with the declared-debt baseline
- [ ] 2.4 Record each gate's flip condition in the debt registry
- [ ] 2.5 Record the first-class compaction-event dependency and implement PostCompact for each provider that exposes it

## 3. Rewrite

- [ ] 3.1 Rewrite one rule (UseEfficientCLI) and bench it against the long form
- [ ] 3.2 On a favorable or neutral bench, rewrite the remaining fifteen rules
- [ ] 3.3 Move displaced content into the owning skill before deleting it
- [ ] 3.4 Retire the duplicated sentences the baseline does not declare
- [ ] 3.5 Author the AdversarialReviewer agent rune

## 4. Verification

- [ ] 4.1 `rune spec validate context-economy` passes
- [ ] 4.2 `make validate` and the quality workflow pass with the new gates at warning
- [ ] 4.3 The rule corpus lands under 900 words total, from 2232
- [ ] 4.4 Every gate fires on a seeded violation, including zero-instruction, two-instruction, over-budget, cross-rune duplication, and reviewer-fault cases
- [ ] 4.5 A session fixture proves PostCompact runs after compaction and before the next inference turn
