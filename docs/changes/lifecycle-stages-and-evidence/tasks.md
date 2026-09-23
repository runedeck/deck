## 1. Thinking artifacts

- [x] 1.1 Write the design document: planes, stages, tokens, stores, edges, retirement, gap register
- [x] 1.2 Record DECK-0005 Artifact Lifecycle and Evidence Tokens
- [x] 1.3 Record DECK-0006 State Stores and Provider Edges
- [x] 1.4 Record DECK-0007 Retirement Path

## 2. Follow-up work this change does not do

- [ ] 2.1 Give bench verdicts a canonical evidence slot beside the artifact
- [ ] 2.2 Gate the unenforced hops: rules without verdicts, adoptions without sealed records
- [ ] 2.3 Give the rune CLI a ceremony-drift command that owns the Copier seam
- [ ] 2.4 Give the rune CLI a retirement command spanning deck, consumer, and provider stores
- [ ] 2.5 Reserve decision-record numbers across parallel changes

## 3. Verification

- [x] 3.1 mdschema passes on every new document
- [x] 3.2 rune validate and rune spec validate pass
