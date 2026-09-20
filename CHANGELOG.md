# Changelog

All notable changes to Rune Deck are documented here, following [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Writing and conduct rules in core, with the text the owner already runs: CiteSources, LessIsMore, NoEmDash, NoItemCounts, NoAgenticAttribution, AsciiDiagrams, ScenarioTitles, OnePurpose, and AvoidDuplication. The `prose`, `authoring`, and `delivery` casts select them.
- The spec-change-lifecycle change and CORE-0019: the change layout, testable requirements, one canonical tree, three-word names, archive as acceptance, and the owner's review of each rule before archive.
- The core-foundation-principles change: records CORE-0001 to CORE-0009 and CORE-0018 state the first principles, and four capabilities make them checkable: plain-text-wins, markdown-first-authoring, harness-independent-authoring, and lint-enforced-foundations.
- The architecture-decision-records change: records CORE-0010 to CORE-0012 state the record format, and two checks fail on a shared record id and on a one-sided link between a change and its record. Each added record field has a bare name and an `x-rune-` long form, and the decisions schema now runs on every record.
- Four casts: `core`, `authoring`, `delivery`, and `prose`. A consumer selects a cast in `.rune` instead of listing paths.
- The AcceptanceTesting skill in core: one recorded scene per specification scenario with an expectation on every THEN, a failed expectation fails the recording, and the GIF and transcript are filed as the behavior proof (DECK-0015).
- The ContinuousIntegration skill in core: run the repository's commit and push check stages locally and repeatedly, with every tool required, and record each stage's own exit status before a push or a signature (DECK-0013).
- The AgenticOntology skill in core: admit a term into the declared world before prose uses it, name an artifact from its lifecycle stage, audit the corpus for synonyms, and retire a term by deprecation. The ontology gains `rune:Proof` as prove-stage evidence with its shape (DECK-0014).
- Five micro-rules in core, extracted from the tuicr workshop brief: CaptureOnTouch, FixAtTheHighestLeverage, ReportFailures, FlagRuleConflicts, and OwnersVoice.
- The VerifyClaims and Deslop rules in core: evidence before assertion, and slop stripped at write time.
- The agentic-first-pipelines change: the idea-to-merge flywheel design, DECK-0008 and DECK-0009, the intake-with-pushback, extract-valuable-lessons, and declared-ontology-constraints capabilities, and the IntakeIdea skill.
- The VersionControl BabysitPR companion runs review pipelines, repairs bot findings, and repeats until the current head is merge-ready.
- The check-provenance hook: a rune or sidecar edit fails when its provenance subject digest is stale, and `--fix` repairs it.
- BenchArtifact ships bench.py again: one config-driven driver for the quick, snapshot, plan, run, grade, judge, and report steps.
- The AnchorWorkingDirectory rule in core: each shell command chain starts from an absolute path.
- The declared world: `ontology/rune.ttl` names the deck's kinds with established vocabularies, and `ontology/shapes.ttl` states the first three axioms as SHACL shapes (DECK-0010).
- Six guarded prek hooks: rumdl, typos, Vale with the STE and Deslop styles, lychee offline, actionlint, and zizmor. Each hook skips when its binary is absent. Two more prove the ontology parses and validate changed spec folders with the openspec CLI.
- Repo-local dcg packs: the tool policy redirects grep to rg and find to fd and blocks casual secret reads, and the repository guardrails block bare git push and shell writes into `.provenance/`.
- The backlog at `docs/todos/todo.txt` uses the todo.txt format. The dated markdown backlog retires.
- Benchmark tables carry an output-token column: corpus mean per arm and the delta, so efficiency artifacts can show their token effect.
- Initial scaffold.
- BenchArtifact skill: benchmark any skill, rule, or agent against a baseline across models, with per-model aggregation and a self-contained comparison report (DECK-0001).
- The ReviewMarkers rule in core, adopted through the block-review ceremony.
- The UseSimplifiedTechnicalEnglish rule in core: all prose follows ASD-STE100, with a bad and good example pair.
- The SimplifiedTechnicalEnglish skill in core, adopted from two upstreams and merged: the STE rule set, the 39 recurring errors, worked examples, measured samples, and the ste-lint checker.
- The VersionControl skill in core: commit and staging discipline, push policy, history rewrites, branch cleanup, worktrees, jj colocated flow, hardware-key signing, and platform governance companions.
- The `ste` skill provides a short Claude command for `SimplifiedTechnicalEnglish`. It stays hidden from model invocation.
- The RTK skill and the UseEfficientCLI rule in core: prefix shell commands with the rtk proxy for 60 to 90 percent output-token savings, and search selectively with fd, rg, ast-grep, and gh --json field selection.
- BuildTask prepares provider tasks. ConfigureScanners adds four prompt-only public exposure scanners for Claude and ChatGPT.

### Changed

- The VersionControl skill: the owner can direct a small fix straight to the default branch. The full prek check set must pass locally with `REQUIRE_GATES=1` first, and the push is a fast-forward through the guarded push.
- The `all` cast selects every rune. It selected only `meta/**` before.
- Every specification and delta uses MUST, and model-commit-attribution splits off worktree-commit-identity so each capability stays under 150 lines.
- The VersionControl skill: the primary checkout stays on the default branch, and each work branch gets a worktree.
- The VersionControl skill: a landing checklist and a supersession check for dirty worktrees.
- The VersionControl skill: a jj colocated repository uses jj workspaces and the repository jj push alias.
- The VersionControl skill: no generation footer, tool badge, or session link in commit messages and pull request bodies.
- The spec waiver label is `ignore:spec`, matching the `ignore:` family every runedeck repository uses. `spec:none` retires.
- AdoptArtifact keeps block verdicts in temporary CLI sessions and commits only source-level provenance sidecars (DECK-0002).
- The authorship check reads separate author and trailer lists from `authors.yaml`. A trailer attribution can no longer validate an author field.
- BuildSkill defers its evaluation step to BenchArtifact. The loop, agent templates, review viewer, and evaluation schemas moved there.
- The core skill schema now accepts `targets`, `disable-model-invocation`, and `user-invocable`.

### Fixed

- The RTK guidance preserves standard-input payloads through passthrough or file arguments.
- The meta module again includes its required empty defaults file.
- Stable shell now validates the `rune` skill with the shared meta skill schema.
- The skill hook validates each entrypoint against its nearest `.mdschema`.

### Removed

- Legacy per-block review ledgers from BuildSkill and ReviewMarkers.
