Play a proof's cast on a page a person reads, and keep the GIF for surfaces that render images only.

## Plan

A GIF loops and cannot pause with position. The cast beside every proof GIF carries the scene titles the driver prints, and html-tools `runtime/cast-player.js` plays it with pause, a scrubber, and the current scene. The AcceptanceTesting skill should say so where it tells the author how to embed a proof.

## Changes

- Extend the Embed section of `runes/core/skills/AcceptanceTesting/Recording.md`: play the cast through the html-tools player on a page, vendor html-tools with `python3 -m htmltools export`, keep the GIF for a pull request body.
- Add `docs/changes/cast-player-in-proofs/` with proposal, delta spec, tasks, and `adr.md`.

## Testing

- [x] `rune validate --skill-layers --source runes/core/skills/AcceptanceTesting` checks 4 layer files.
- [x] `prek run --all-files` and `prek run --stage pre-push --all-files` with `REQUIRE_GATES=1` in an isolated clone of `5d4386fd`, both exit 0.
- [x] The workshop proof page of 2026-09-20 plays its three casts through the player.

## Release Notes

- N/A
