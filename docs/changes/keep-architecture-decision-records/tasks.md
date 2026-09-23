## 1. Implementation

- [x] 1.1 State the record format, accountability, and provenance requirements
- [x] 1.2 Publish the format as runeADR at `runedeck/adr`
- [x] 1.3 Bare RACI names are canonical, and `x-rune-` is the compliant long form
- [x] 1.4 Point the decisions schema at the public home

## 2. Verification

- [ ] 2.1 `openspec validate --all --strict` passes (`rune spec validate` covers the native tree until the trees unify)
- [x] 2.2 The decisions schema runs on every record through a prek hook. It ran nowhere before, and two records lacked `upstream`
- [x] 2.3 `scripts/check-decision-numbers` fails on a shared record id
- [x] 2.4 `scripts/check-decision-links` fails when a proposal or a record lacks its side of the link
- [ ] 2.5 `rune spec archive` moves `adr.md` to `docs/decisions/` and assigns the id (cli)
- [ ] 2.6 `rune spec archive` matches requirement headings without regard to case, so a recased canonical heading does not duplicate (cli)
- [x] 2.7 `scripts/check-decision-fields` accepts the bare form or the `x-rune-` long form, rejects both at once, and rejects any other `x-` prefix
- [ ] 2.8 The public home's JSON Schema requires the bare names, so a long-form record fails it. Change the home so that either form satisfies a field (runedeck/adr)
