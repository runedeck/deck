# Changelog

All notable changes to Rune Deck are documented here, following [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Add the PreferTrash rule in core: delete with `trash`, the FreeDesktop-layout script every repository and the dotfiles ship, never with `rm`; recovery is a move back from `~/.local/share/Trash`.
- Add the DetachedJob skill in development: start a long command in its own session so no tool timeout, terminal close, or session exit stops it, then wait for its exit code and read its log.
- Add recorded proofs for prove-each-scenario, cast-player-in-proofs, and proof-page-handover under `docs/proofs/`, and DECK-0019 from the archived cast-player decision.
- AcceptanceTesting hands over a proof as a page: `scripts/proof-page.py` builds it from the casts with the html-tools player, and the GIF alone is an unfinished handover (proof-page-handover).
- Map the ontology terms to the upstream corpus, trial each part alone with a recorded verdict, and take no dependency on a pre-1.0 implementation (modeled-information-format-alignment).
- Adopt five open-source tools for the review funnel and keep custom code for the ceremony only (DECK-0011).
- Add the Links workflow, which fetches every external URL one time each week and leaves the commit path offline.
- Add the Core Vale style rule for a named citation (CORE-0009).
- Add the Core Vale style rule for the word directory (CORE-0004).
- Add the Core Vale style rule that requires MUST in a specification, an error that runs on specification files only (CORE-0019).
- Add the writing and conduct rules in core: CiteSources, LessIsMore, NoEmDash, NoItemCounts, NoAgenticAttribution, AsciiDiagrams, ScenarioTitles, OnePurpose, and AvoidDuplication.
- Select the writing and conduct rules from the `prose`, `authoring`, and `delivery` casts.
- Add the change layout, testable requirements, one canonical tree, three-word names, archive as acceptance, and owner review of each rule before archive (spec-change-lifecycle, CORE-0019).
- Add records CORE-0001 to CORE-0009 and CORE-0018 for the first principles (core-foundation-principles).
- Add four capabilities that make the first principles checkable: plain-text-wins, markdown-first-authoring, harness-independent-authoring, and lint-enforced-foundations.
- Add records CORE-0010 to CORE-0012 for the decision record format (architecture-decision-records).
- Add two checks that fail on a shared record id and on a one-sided link between a change and its record (architecture-decision-records).
- Add a bare name and an `x-rune-` long form to each record field, and run the decisions schema on every record.
- Add four casts, `core`, `authoring`, `delivery`, and `prose`, so a consumer selects a cast in `.rune` instead of listing paths.
- Add the AcceptanceTesting skill in core: one recorded scene for each scenario, an expectation on every THEN, and the GIF and transcript filed as behavior proof (DECK-0015).
- Fail a recording when an expectation fails (DECK-0015).
- Add the ContinuousIntegration skill in core: run the commit and push check stages locally with every tool required, and record each stage exit status before a push or a signature (DECK-0013).
- Add the AgenticOntology skill in core: admit a term before prose uses it, name an artifact from its lifecycle stage, audit for synonyms, and retire a term by deprecation (DECK-0014).
- Add `rune:Proof` to the ontology as prove-stage evidence, with its shape (DECK-0014).
- Add five micro-rules in core: CaptureOnTouch, FixAtTheHighestLeverage, ReportFailures, FlagRuleConflicts, and OwnersVoice.
- Add the VerifyClaims and Deslop rules in core: evidence before assertion, and slop stripped at write time.
- Add the idea-to-merge flywheel design with records DECK-0008 and DECK-0009 (agentic-first-pipelines).
- Add the intake-with-pushback, extract-valuable-lessons, and declared-ontology-constraints capabilities and the IntakeIdea skill (agentic-first-pipelines).
- Add the VersionControl BabysitPR companion, which runs review pipelines, repairs bot findings, and repeats until the head is merge-ready.
- Add the check-provenance hook: a rune or sidecar edit fails when its provenance subject digest is stale, and `--fix` repairs it.
- Restore bench.py in BenchArtifact as one config-driven driver for the quick, snapshot, plan, run, grade, judge, and report steps.
- Add the AnchorWorkingDirectory rule in core: each shell command chain starts from an absolute path.
- Add `ontology/rune.ttl`, which names the deck kinds with established vocabularies (DECK-0010).
- Add `ontology/shapes.ttl`, which states the first three axioms as SHACL shapes (DECK-0010).
- Add six guarded prek hooks: rumdl, typos, Vale with the STE and Deslop styles, lychee offline, actionlint, and zizmor. Each hook skips when its binary is absent.
- Add a prek hook that proves the ontology parses.
- Add a prek hook that validates changed spec directories with the openspec CLI.
- Add a repo-local dcg tool policy that redirects grep to rg and find to fd and blocks casual secret reads.
- Add repo-local dcg guardrails that block bare git push and shell writes into `.provenance/`.
- Add the backlog at `docs/todos/todo.txt` in the todo.txt format.
- Add an output-token column to benchmark tables with the corpus mean for each arm and the delta.
- Add the initial scaffold.
- Add the BenchArtifact skill to benchmark any skill, rule, or agent against a baseline across models, with per-model aggregation and a self-contained report (DECK-0001).
- Add the ReviewMarkers rule in core through the block-review ceremony.
- Add the UseSimplifiedTechnicalEnglish rule in core: all prose follows ASD-STE100, with a bad and good example pair.
- Add the SimplifiedTechnicalEnglish skill in core from two merged upstreams: the STE rule set, the 39 recurring errors, worked examples, measured samples, and the ste-lint checker.
- Add the VersionControl skill in core: commit and staging discipline, push policy, history rewrites, branch cleanup, worktrees, jj colocated flow, and hardware-key signing.
- Add the VersionControl platform governance companions, `GitHub.md` for `gh` and `GitLab.md` for `glab`.
- Add the `ste` skill, a short Claude command for `SimplifiedTechnicalEnglish` that stays hidden from model invocation.
- Add the RTK skill in core: prefix shell commands with the rtk proxy for 60 to 90 percent output-token savings.
- Add the UseEfficientCLI rule in core: search selectively with fd, rg, ast-grep, and gh --json field selection.
- Add the BuildTask skill, which prepares provider tasks.
- Add the ConfigureScanners skill with four prompt-only public exposure scanners for Claude and ChatGPT.

### Changed

- Fix the guarded push: the root checkout is refused by workspace identity (the old template test passed a dirty root), and a head that does not descend from the remote bookmark is refused.
- RemoteWrites: a remote pull request or branch write is offered, not refused: the session lists the commands and asks "Do you want me to do this on your behalf?" A yes covers them once.
- Sync the ceremony files to skeleton `6374d8fc` through `copier update`: seven dcg packs with fixtures, `.dcg.toml`, the lane table, the direct-push signature check, admin-role rulesets.
- Write the Purpose of the `cast-player-in-proofs` and `proof-page-handover` specifications in place of the archive stub.
- Change the correctness caller to skeleton `5e4657bf`: the controller runs on every same-repository push, draft or ready, so the green draft starts the review round.
- Change the ceremony files to skeleton `60ad8249` through `copier update`: owner-seal and verify-seal messages and nonce, jq guards, versioned display names, `thread-resolver.yaml` retired.
- Allow the owner to direct a small fix straight to the default branch in VersionControl.
- Require the full prek check set locally with `REQUIRE_GATES=1` and a fast-forward guarded push for a direct fix.
- Change the `all` cast to select every rune. It selected only `meta/**` before.
- Change every specification and delta to use MUST.
- Split worktree-commit-identity out of model-commit-attribution so each capability stays under 150 lines.
- Change VersionControl so the primary checkout stays on the default branch and each work branch gets a worktree.
- Document a landing checklist and a supersession check for dirty worktrees in VersionControl.
- Change VersionControl so a jj colocated repository uses jj workspaces and the repository jj push alias.
- Refuse a generation footer, tool badge, or session link in commit messages and pull request bodies (VersionControl).
- Rename the spec waiver label from `spec:none` to `ignore:spec`, matching the `ignore:` family every runedeck repository uses.
- Change AdoptArtifact to keep block verdicts in temporary CLI sessions and commit only source-level provenance sidecars (DECK-0002).
- Change the authorship check to read separate author and trailer lists from `authors.yaml`, so a trailer attribution no longer validates an author field.
- Move the BuildSkill evaluation step to BenchArtifact, with the loop, agent templates, review viewer, and evaluation schemas.
- Change the core skill schema to accept `targets`, `disable-model-invocation`, and `user-invocable`.

### Removed

- Remove the legacy per-block review ledgers from BuildSkill and ReviewMarkers.
- Remove the dated markdown backlog.

### Fixed

- Fix the identity tests to expect the versioned display names the synced `author-identity.py` derives (`Claude Fable 5.2`, not `Claude`).
- Fix the decision record shape to accept every uppercase family. It allowed DECK and RUNE only, so all nineteen CORE records failed on the real graph.
- Add a hook that validates the real graph on every ontology, record, or rule commit.
- Fix the RTK guidance to preserve standard-input payloads through passthrough or file arguments.
- Fix the meta module to include its required empty defaults file.
- Fix stable shell to validate the `rune` skill with the shared meta skill schema.
- Fix the skill hook to validate each entrypoint against its nearest `.mdschema`.
