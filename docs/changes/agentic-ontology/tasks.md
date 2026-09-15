# Tasks

## 1. Implementation

- [x] 1.1 Add the AgenticOntology skill with the four routes and the three companions
- [x] 1.2 Add `rune:Proof`, `rune:proves`, and the proof kinds scheme to `ontology/rune.ttl`
- [x] 1.3 Add the proof shape and the orphan proof smoke instance, and update the hook counts
- [x] 1.4 Record DECK-0014

## 2. Verification

- [x] 2.1 `rudof data ontology/rune.ttl` parses and the smoke fixture reports four Violations and six Warnings
- [x] 2.2 `rune validate --skill-layers` on the new skill, Vale, rumdl, typos, and `rune spec validate`
- [x] 2.3 The commit and push stages through the ContinuousIntegration procedure

## 3. Follow-up

- [ ] 3.1 Extract ContinuousIntegration receipts as `rune:Proof` instances once `rune graph export` exists (declared-world task 2.4)
- [ ] 3.2 Compute semantic density in the extractor instead of by hand
- [ ] 3.3 Run the first drift audit over receipt, proof, attestation, and evidence, and merge the survivors
- [ ] 3.4 Move the proof shape to Violation after the first extracted proofs conform
