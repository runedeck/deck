# Tasks: Declared World

## 1. This change

- [x] 1.1 Declare the ontology in `ontology/rune.ttl` with established vocabularies.
- [x] 1.2 Declare the three shapes in `ontology/shapes.ttl`.
- [x] 1.3 Add the six guarded prek hooks.
- [x] 1.4 Add `.vale.ini` and the STE style seed.
- [x] 1.5 Add `.rumdl.toml`.
- [x] 1.6 Record DECK-0010.

## 2. Follow-up

- [x] 2.1 Install the tools: `brew install rumdl lychee typos-cli zizmor actionlint vale`, plus the rudof release binary. Verify each guarded hook fires.
- [x] 2.2 Run the first rumdl and typos pass over the corpus and commit the baseline fixes. Adopted digest-bound trees stay byte-stable and sit on the rumdl excludes list.
- [x] 2.3 Survey forge-cli, forge-core, and forge-dev. Expand `rune.ttl` with the kinds the survey confirms.
- [ ] 2.3a Add the sidecar-never-duplicates-canon shape and the mergeMode value shape once the extractor emits part-level fields.
- [ ] 2.4 Add `rune graph export` to the cli repository: walk frontmatter, mint `/id/` IRIs, emit Turtle. The `ontology` name was taken: the cli already uses it for the unified config model (CLI-0013).
- [ ] 2.5 Add the rudof hook at the pre-push stage: `rune graph export | rudof shacl-validate -s ontology/shapes.ttl -`. rudof 0.3.12 exits zero on violations, so the hook greps `sh:Violation` in the `-r turtle` report for its exit status. The fixture at `ontology/smoke/instances.ttl` proves the shapes: four Violations and two Warnings.
- [ ] 2.6 Grow the STE style toward the full rule set in the SimplifiedTechnicalEnglish skill.
- [ ] 2.6a Run `vale sync` once per checkout to fetch the Deslop package. Remove STE rows that Deslop already covers.
- [ ] 2.7 Decide the `related:` migration from strings to relative links, so lychee checks them.
- [x] 2.8 Move the duplicate-identifier shape to Violation after the DECK-0002 collision is resolved.
- [ ] 2.9 Move the rule-verdict shape to Violation after existing rules carry verdicts.
- [ ] 2.9a Move the references-resolve shape to Violation after the extractor lands and the corpus resolves every related entry.
- [ ] 2.10 Add the harness PostToolUse hook that lints Markdown at write time.
- [ ] 2.11 After one week of deck use, land the configuration files in the skeleton root and `templates/base/`, and update consumers through `copier update`.
- [ ] 2.12 Verify the `.rumdl.toml` schema against the rumdl release in use.
- [ ] 2.13 Decide digest-aware linting for adopted artifacts: today the rumdl excludes list them by path, and an adoption refresh must update the list.
- [x] 2.15 Ship the repo-local dcg tool-policy pack at `.dcg/packs/toolpolicy.yaml`. The user config loads the glob, so the pack binds every harness dcg hooks into.
- [x] 2.19 Ship the `rune.repo` guardrail pack at `.dcg/packs/repo.yaml`: bare `git push` redirects to the gated `jj push`, and shell writes into `.provenance/` are blocked. The skeleton ships this file to every consumer after the soak.
- [ ] 2.16 Apply the dotfiles copy of the pack with `chezmoi apply`, so the policy holds outside this repository.
- [x] 2.17 Write the lint-on-write PostToolUse hook that runs rumdl, typos, and Vale on the file an agent writes. It lives in the dotfiles Claude settings template.
- [x] 2.20 Wire `jj fix`: rumdl fmt, typos, and shfmt are user-level fix tools in the dotfiles jj configuration, because repo-level `.jj` config is untracked and the tools bound their own blast radius to files a revision changes.
- [ ] 2.21 Codex carries no post-edit hook event today, so the lint-on-write loop stays Claude-only. The hooks-as-rune-artifacts backlog item owns the cross-harness path.
- [x] 2.18 Connect the openspec CLI: `docs/` already matches its layout (`docs/changes/`, `docs/specs/`). The dotfiles `openspec` wrapper shadows the repository through `~/.openspec/<org>/<repo>/openspec -> docs`, so `openspec list` and `openspec validate --strict` work with no extra entry in the repository.
- [ ] 2.14 Triage the workflow lint baseline: pin action references, tighten permissions, and add a zizmor configuration that records the deliberate `pull_request_target` design as an audit exception. Until then, actionlint and zizmor block only changes that touch workflow files.
