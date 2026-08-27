---
adr: "docs/decisions/DECK-0011 Context Economy.md"
status: proposed
---

# Context Economy

## Why

Claude 5 generation models need less instruction, not more. Anthropic removed over 80 percent of the Claude Code system prompt with no measured loss. A controlled study (arXiv 2311.10054) shows personas in system prompts do not improve task performance. Negative phrasing can prime the behavior it names. The deck ignores all three findings today: the sixteen core rules carry 2232 words (about 2.9k resident tokens in every deployed session), twenty negative constructions, and 101 duplicated sentences across runes.

## What Changes

- Three decision records: DECK-0011 Context Economy, DECK-0012 No Performance Personas, DECK-0013 Positive Instruction.
- One compatibility table: every forge-core CORE and context-relevant ARCH decision, judged affirmed, amended, or diverged.
- The sixteen core rules rewrite to the shape: one imperative instruction, within 50 words, positively framed.
- Four warning-first gates: rule budget, persona lint, negation density, duplicated-sentence check.
- Adversarial review replaces consensus councils: DECK-0014, an AdversarialReviewer agent, and the HarnessCouncil retirement.
- Existing violations enter a declared-debt baseline that shrinks. New violations fail.

## Capabilities

- context-economy (new)

## Impact

- `runes/core/rules/` (all sixteen rules), `runes/*/skills/` (duplication cleanup), `docs/decisions/`, `.pre-commit-config.yaml`, `.github/workflows/quality.yaml`, Vale styles.
