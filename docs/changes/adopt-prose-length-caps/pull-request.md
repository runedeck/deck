Split six requirement walls and rewrite the changelog to one line per change, under the caps `rune spec validate` and `rune docs check` now enforce.

## Plan

The cli change `prose-length-caps` refuses a requirement statement over 100 words, a scenario step over 30, a changelog line over 200 characters, and a change or capability name under three words. The deck had six requirements and twelve changelog lines over the caps. Rewrite them now so the deck passes the day the pinned rune moves.

## Changes

- Split `Trusted policy` in `docs/specs/model-commit-attribution/spec.md` into `Trusted policy` and `Policy domains and parsing`, scenarios kept under the MUST they prove.
- Split `Reviewer recovery has a bounded budget` and `Owner-directed push to the default branch` in `docs/changes/pull-request-delivery-contract/specs/pull-request-delivery-contract/spec.md` into five requirements, one new scenario (`Remote moved before the push`).
- Split `Historical Transition` and `Changelog Ownership Gate` in `docs/changes/release-note-publishing/specs/release-note-publishing/spec.md` into four requirements.
- Split `Remote writes belong to the owner` in `docs/changes/restrict-remote-writes/specs/restrict-remote-writes/spec.md` into two requirements, one new scenario (`Harness has no rules path`).
- Rewrite `CHANGELOG.md`: 51 entries become 71 one-line changes, groups in the Keep a Changelog order, no change dropped.
- Add `docs/changes/adopt-prose-length-caps/` with proposal, delta spec, tasks, and `adr.md`.

## Testing

- [x] `rune spec validate` and `rune docs check` from the cli `prose-length-caps` build (`c520f6f7`) print no error for this tree.
- [x] `prek run --all-files` and `prek run --stage pre-push --all-files` with `REQUIRE_GATES=1` in an isolated clone of `00b11a34`, both exit 0.
- [x] MUST counts per split file are unchanged before and after.

## Release Notes

- N/A
