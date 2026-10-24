---
adr: "docs/changes/automate-cloud-browsers-browserbase/adr.md"
status: proposed
decisions: ["Point at the upstream reference instead of vendoring it"]
---

# Automate cloud browsers

## Why

A session that writes browser automation on Browserbase gets the platform wrong without help. On 2026-10-24, Opus 5.5, Fable 5.1, and Haiku 5.5 each ran three cases with and without this change's *[skill][SKILL]*. Without it, every model wrote Stagehand V3 start code and listed the project identifier variable as required. No model read a refused page through Browserbase Fetch. Each opened a browser session for it instead. Stagehand V4 removed that start form ([migration guide][STAGEMIGRATE]), and the vendor's own skill file names the API key as the only secret ([Browserbase skill][BBSKILL]). With the skill, all nine runs passed every assertion, against 40 to 50 percent of assertions without it. The report gives no lint verdict, because the answers are code or single lines with no prose for its checker. The benchmark wrapper came from the deck change `benchmark-runs-without-manual-workarounds`. The runs are in `$ROOT_BENCHMARK/runedeck/BrowserbaseToolkit-deck/iteration-2/`. Earlier runs on 2026-10-20 and 2026-10-22 in forge-provision gave the same split on the first two cases.

The skill was written and measured in forge-provision. This *[change][CHANGE]* brings it into the *[deck][DECK]*, so every *[harness][HARNESS]* that installs the development domain gets it.

## What Changes

- The BrowserbaseToolkit [skill][SKILL] joins the development domain at `runes/development/skills/BrowserbaseToolkit/`: a *[canon][CANON]* and three *[companions][COMPANION]*, Stagehand V4, Starters, and Troubleshooting.
- The skill also loads when a session's own fetch tool is refused or returns a summary instead of the page. A scan of the owner's session records on 2026-10-24 found both failures in several sessions. The skill then reads the page through the platform's fetch first and a short browser session second.
- The skill points at the vendor's published skill file for the full command reference and carries no copy of it. The forge-provision version vendored that file with a sealed provenance sidecar. The record in `adr.md` holds that decision.
- The skill holds plain documents only, no executable, and names no harness tool.

## Capabilities

### New Capabilities

- automate-cloud-browsers-browserbase: a session on Browserbase picks the lightest capability, reads a refused page through the platform, writes current Stagehand code, needs one secret, names the real cause of a misleading error, and reads the command reference upstream.

## Impact

- `runes/development/skills/BrowserbaseToolkit/` (new): `SKILL.md`, `StagehandV4.md`, `Starters.md`, `Troubleshooting.md`.
- `CHANGELOG.md` gains one line.
- The record in `adr.md` moves to `docs/decisions/` at archive.

## Sources

- [Browserbase skill][BBSKILL], the vendor's own skill file, which names the API key as the only secret
- [Stagehand V3 to V4 migration][STAGEMIGRATE], the list of removed constructor, init, and agent calls

[SKILL]: ../../specs/glossary/skill.md
[CHANGE]: ../../specs/glossary/change.md
[DECK]: ../../specs/glossary/deck.md
[HARNESS]: ../../specs/glossary/harness.md
[CANON]: ../../specs/glossary/canon.md
[COMPANION]: ../../specs/glossary/companion.md
[BBSKILL]: https://browserbase.com/SKILL.md
[STAGEMIGRATE]: https://docs.stagehand.dev/v4/migrations/v3.md
