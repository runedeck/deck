---
adr: "docs/changes/scanner-routines-from-deck/adr.md"
status: proposed
decisions: ["Scanner routines run a deterministic detector from the deck"]
type: proposal
---

# Scanner routines from deck

## Why

The three scanner routines kept their whole prompts in the provider account while the digest and the audit had moved to deck files a stub reads at run time. A council review on 2026-10-02 (Codex `gpt-6-astra` and Proton `lumo-max`) found that the Dotfiles Scanner let a model compute the status, so identical evidence changed severity between runs, that a shallow clone made every run INCOMPLETE, that the report named no repair location, and that the Online Mentions queries measured namesakes and blocked websites. The GitHub Exposure routine had no subject: the provider proxy refuses every GitHub path outside an attached source.

## What Changes

- `routines/scripts/exposure_scan.py` is a deterministic, standard-library detector that reads a repository through Git objects only, applies versioned rules for secrets, private hosts, and personal data, and prints findings with stable ids, locations, a finding status, and a separate scan health. A finding id is the rule code plus ten hex digits of the SHA-256 of the value, so no value leaves the detector, and an acknowledgement is an id plus the commit it was acknowledged at. Tests build their fixtures in a temporary repository.
- `routines/DotfilesScanner.md` runs the detector by streaming it from the deck object store, takes its status and counts as printed, may add review items with a location, and reports a three-line push plus a session table with id, new or known, rule, path, line, commit, and action.
- `routines/OnlineMentions.md` runs weekly with a fixed identity-qualified query plan from the stub values, discards namesakes, treats owner-reviewed exclusions as neither findings nor failures, and keeps finding status apart from scan health.
- The stub fetches the ref in a POLICY_REF value with the default `main`, so the owner can test a branch before merge. The stub contract, the routine-prompts-from-deck spec, and the README say so.
- `routines/README.md` documents the scanner inputs. Instance values, such as a sensitive domain or a known finding id, never enter the deck.
- The GitHub Exposure routine is retired.
- Unenforceable ritual leaves the prompts: environment marker checks, tool bans that the tools ignore, and claims the run cannot observe. The lines that block real attack paths stay.

## Capabilities

### New Capabilities

- scanner-routines-from-deck

## Impact

- `routines/DotfilesScanner.md`, `routines/OnlineMentions.md`, `routines/scripts/exposure_scan.py`, and `tests/test_exposure_scan.py` are new.
- `routines/README.md` gains the scanner inputs, the POLICY_REF contract, and the streamed-code rule. `docs/changes/routine-prompts-from-deck/specs/routine-prompts-from-deck/spec.md` gains the POLICY_REF sentence.
- `.pre-commit-config.yaml` gains the `exposure-scan-tests` hook, `.github/workflows/quality.yaml` gains the matching step, and `CHANGELOG.md` gains one line.
- `runes/security/skills/ConfigureScanners/` is untouched. Its Claude repository template overlaps with the Dotfiles Scanner, and the overlap is a task of this change.
- The consumer replaces the Dotfiles Scanner and Online Mentions prompts with stubs that carry the instance values, and marks the GitHub Exposure routine retired.
