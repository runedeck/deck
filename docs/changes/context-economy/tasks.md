## 1. Decisions

- [ ] 1.1 Write DECK-0011 Context Economy with the evidence and the layer map
- [ ] 1.2 Write DECK-0012 No Performance Personas with the study citation and the voice carve-out
- [ ] 1.3 Write DECK-0013 Positive Instruction with the prohibition carve-out
- [ ] 1.4 Write the forge-core compatibility table into DECK-0011 (CORE-0001..0012, ARCH-0001, 0004, 0011, 0014)
- [ ] 1.5 Write the turn-pipeline record: what loads at session start, per turn, and after compaction
- [ ] 1.6 Write DECK-0014 Adversarial Review over Councils: refutation replaces consensus

## 2. Gates

- [ ] 2.1 Add the rule-budget check to prek and quality (50 words, one instruction, with a baseline for the sixteen current rules)
- [ ] 2.2 Add the persona and negation Vale style, warning severity
- [ ] 2.3 Add the duplicated-sentence sweep with the declared-debt baseline
- [ ] 2.4 Record each gate's flip condition in the debt registry

## 3. Rewrite

- [ ] 3.1 Rewrite one rule (UseEfficientCLI) and bench it against the long form
- [ ] 3.2 On a favorable or neutral bench, rewrite the remaining fifteen rules
- [ ] 3.3 Move displaced content into the owning skill before deleting it
- [ ] 3.4 Retire the duplicated sentences the baseline does not declare
- [ ] 3.5 Author the AdversarialReviewer agent rune and retire the HarnessCouncil skill on the DECK-0007 path

## 4. Verification

- [ ] 4.1 `rune spec validate context-economy` passes
- [ ] 4.2 `make validate` and the quality workflow pass with the new gates at warning
- [ ] 4.3 The rule corpus lands under 900 words total, from 2232
- [ ] 4.4 Every gate fires on a seeded violation in a scratch file
