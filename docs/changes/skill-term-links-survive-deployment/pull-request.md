Point the ReviewChange term links at the published glossary pages by repository URL, so the skill bundle passes the source-layer check and every term link still resolves after deployment.

## Plan

The `contract` job fails on `main` with three `CSI008_LAYER_SOURCE` findings: the term definitions in `runes/core/skills/ReviewChange/SKILL.md` point at `../../../../docs/specs/glossary/<term>.md`, and the path leaves the bundle. The check is right, and a term link is never removed to satisfy a check. The smallest fix that keeps every link working after deployment is the one the deck already uses for a skill's external sources: an absolute URL. The assembler design that would strip term links per instance is not in the cli yet.

## Changes

- Rewrite the three definitions in `runes/core/skills/ReviewChange/SKILL.md` to `https://github.com/runedeck/deck/blob/main/docs/specs/glossary/<term>.md`. Tags, link text, and emphasized first uses are unchanged.
- Add one sentence to `runes/core/rules/ConsultTheOntology.md`: a skill file points at a glossary page by its repository URL, because a relative path leaves the bundle.
- Add `docs/changes/skill-term-links-survive-deployment/` with proposal, delta spec for `skill-term-links-survive-deployment`, tasks, and this file.
- Add a changelog line.

## Testing

- [x] `rune validate --skill-layers --source .` prints `Checked 170 skill layer files.` and no finding.
- [x] `rune validate` prints 0 errors. The 9 warnings are the same delta-length and skill-breadth warnings as before the change.
- [x] `rune spec validate` prints no error.
- [x] `rune spec fix --terms` and `rune spec fix --links` on a copy of the tree print `nothing to fix`. The ontology and the glossary page count are unchanged.
- [x] `scripts/fallback/check-terms` on the same copy prints `0 findings, 0 errors`.

## Release Notes

- N/A
