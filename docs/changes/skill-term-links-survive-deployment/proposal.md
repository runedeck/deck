---
status: proposed
decisions: []
---

# Skill term links survive deployment

## Why

The `contract` job runs `rune validate --skill-layers --source .` and fails on `main` with three `CSI008_LAYER_SOURCE` findings in `runes/core/skills/ReviewChange/SKILL.md`: each term definition points at `../../../../docs/specs/glossary/<term>.md`, and the path leaves the bundle. The check is right. A skill directory is deployed on its own, so a relative path out of it points at nothing after deployment. The ConsultTheOntology rule says a term link is never removed to satisfy a check, and the design that would make the problem disappear, the assembler stripping term links into a per-instance definition block (plain-text-first-principles, task 4.4), is not in the cli yet.

## What Changes

- The three term definitions in `runes/core/skills/ReviewChange/SKILL.md` point at the published glossary pages by repository URL, `https://github.com/runedeck/deck/blob/main/docs/specs/glossary/<term>.md`, the way BuildSkill already points at the cli runbook and other skills point at their external sources. The tags, the emphasized first uses, and the link text stay as they are.
- The generic ReviewChange layer says "the harness's question tool", and a new `claude/SKILL.md` variant names `AskUserQuestion`. Once the paths pass, the source-layer check also runs its harness leakage rule. That rule rejects a Claude tool name in the generic and non-Claude layers.
- `runes/core/rules/ConsultTheOntology.md` gains one sentence: a skill file points at a glossary page by its repository URL, because a relative path leaves the bundle.
- The new `skill-term-links-survive-deployment` capability requires that a term link in a skill bundle resolves after deployment.

The alternatives were larger. Shipping the three pages inside the bundle duplicates generated files that the glossary drift check never sees, and a copy is not a term link to either checker. Changing the check lives in the cli repository, needs a pin bump in two workflows, and would teach the check to pass a reference that does break after deployment.

## Capabilities

### New Capabilities

- `skill-term-links-survive-deployment`: a term link in a skill bundle points at the published glossary page, so it resolves after deployment and the source-layer check passes.

## Impact

- `runes/core/skills/ReviewChange/SKILL.md`, `runes/core/skills/ReviewChange/claude/SKILL.md`, `runes/core/rules/ConsultTheOntology.md`, `CHANGELOG.md`.
- `rune spec fix --terms` and `--links` leave a URL definition alone, and `rune spec validate`, `rune validate`, and `scripts/fallback/check-terms` report nothing for it. The same three readers treat a URL definition as not a term link, so the first-use emphasis rule is not checked for those three terms in that one file until the term model reads the repository URL form. That is a cli follow-up, recorded in the tasks.
