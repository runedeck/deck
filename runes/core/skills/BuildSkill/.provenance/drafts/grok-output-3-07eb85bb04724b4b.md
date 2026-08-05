Reading the full offloaded prompt for complete unit content (grader, comparator, schemas were truncated).UNIT: agents/analyzer.md
VERDICT: adapt
WHY: Pure skill-creator eval machinery with no forge coupling; safe and deck-portable as build-skill’s post-hoc analyzer. One clear typo is the only fix needed before accept.
REPLACEMENT:
- In Role (comparison mode), change `"unblids"` → `"unblinds"` (sentence: `The Post-hoc Analyzer "unblinds" the results...`).

UNIT: agents/comparator.md
VERDICT: keep
WHY: Blind A/B comparison contract is harness- and product-agnostic; no forge naming, no provider routing, no INSTALL/user-config conventions. Matches deck eval-loop needs as-is.

UNIT: agents/grader.md
VERDICT: keep
WHY: Grading + eval-critique prompts are portable; tool names in examples (`Read`/`Bash`/etc.) are illustrative metrics keys, not forge-specific. No forge paths or multi-provider defaults; no network/injection hazards beyond ordinary “check outputs or external sources” claim verification.

UNIT: references/schemas.md
VERDICT: adapt
WHY: Schemas are the eval-viewer/script contract and must ship; only branding is wrong for the deck (`skill-creator` vs `build-skill`). Field names and kebab-case examples already match deck naming.
REPLACEMENT:
- Intro line: `This document defines the JSON schemas used by skill-creator.` → `This document defines the JSON schemas used by build-skill’s eval loop (skill-creator lineage).`
- No other edits (benchmark/comparison/analysis/grading field contracts stay verbatim so scripts and eval-viewer keep working).
