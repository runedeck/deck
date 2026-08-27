---
adr: "docs/decisions/CORE-0013 Context Economy.md"
status: proposed
---

# Context Economy

## Why

Claude 5 generation models need less instruction, not more. Anthropic removed over 80 percent of the Claude Code system prompt with no measured loss. A controlled study (arXiv 2311.10054) shows personas in system prompts do not improve task performance. Negative phrasing can prime the behavior it names. The deck ignores all three findings today: the sixteen core rules carry 2232 words (about 2.9k resident tokens in every deployed session), twenty negative constructions, and 101 duplicated sentences across runes.

## What Changes

- Five decision records: CORE-0013 Context Economy, CORE-0014 No Performance Personas, CORE-0015 Positive Instruction, CORE-0016 Adversarial Review over Councils, CORE-0017 The Inference Turn.
- One compatibility table in CORE-0013: every forge-core CORE and context-relevant ARCH decision, judged affirmed, amended, or diverged.
- The sixteen core rules rewrite to the shape: one imperative instruction, within 50 words, positively framed.
- Four warning-first gates: rule budget, persona lint, negation density, duplicated-sentence check.
- Adversarial review replaces consensus gating. CORE-0016 defines the contract, and an AdversarialReviewer agent will implement refutation.
- Existing violations enter a shrinking declared-debt baseline. New violations warn first and fail after the recorded flip condition.

## Capabilities

- context-economy (new)

## Impact

- `runes/core/rules/` (all sixteen rules), `runes/*/skills/` (duplication cleanup), `docs/decisions/`, `.pre-commit-config.yaml`, `.github/workflows/quality.yaml`, Vale styles.
