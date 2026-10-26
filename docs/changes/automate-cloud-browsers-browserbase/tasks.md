# Tasks

## 1. Authoring

- [x] 1.1 BrowserbaseToolkit canon: the feature ladder, the V4 rule, the one-secret rule, and the upstream link in place of the vendored reference
- [x] 1.2 StagehandV4 companion: the start shape, the method moves, caching, and the removed forms
- [x] 1.3 Troubleshooting companion: the misleading errors, the template secret hygiene, the two exits past the token cap, the escalation order
- [x] 1.4 Record the decision in `adr.md`
- [x] 1.5 The CHANGELOG line
- [x] 1.6 The blocked page fallback in the canon, its trigger and four steps, and the Starters companion that keeps the canon under 100 lines
- [x] 1.7 `INSTALL.md` in the Mintlify shape, bun only, and the Claude variant that reads the installed CLI state at load
- [x] 1.8 Daily-use rework: a short canon routing to the Workflow companion, the Features companion, Defuddle for clean markdown, the Claude variant replacing the body with the read-page script, and the `INSTALL.md` schema hook
- [x] 1.9 Keep a page address literal: single quotes in every command, no pre-approval for `read-page`, and a script guard that refuses a non-http address or one that contains the API key

## 2. Verification

- [x] 2.1 `rune validate --skill-layers` on the skill and `rune validate` on the deck
- [x] 2.2 `rune spec validate`, `scripts/check-spec-names`, the skill mdschema check, and `vale --no-global` on the added files
- [x] 2.3 Bench the deck skill against a baseline with no skill (BenchArtifact): three cases on Opus 5.5, Fable 5.1, and Haiku 5.5, iteration 2 of 2026-10-24
- [ ] 2.4 One recorded proof per scenario under `docs/proofs/automate-cloud-browsers-browserbase/`

## 3. Record

- [ ] 3.1 Archive moves `adr.md` to `docs/decisions/` with the next free DECK number
