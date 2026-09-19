# Pull request delivery design

## Context

See [proposal.md](proposal.md) for motivation and scope.
The new [delivery specification](specs/pull-request-delivery/spec.md) extends an existing stage rather than adding a pipeline stage.
The [authorization PR](https://github.com/runedeck/deck/pull/56) already defines permission and post-push verification.

## Goals / Non-Goals

Goals:

- Replace contradictory instructions and add only the evidence-acquisition and recovery steps that the current skill lacks.
- Keep one session-local record that survives a handover without becoming a public status comment.
- Use platform data and existing policy checks instead of inventing approval or model rules.

Non-goals:

- A new orchestrator, dashboard, reservation-label convention, or review provider.
- Changes to owner-controlled routines, reviewer configuration, capture wrappers, or CHANGELOG publishing.
- Deployment or implementation before owner review of these planning artifacts.

## Decisions

### Keep the existing skill and its companions

Update `BabysitPR.md` for selection, evidence acquisition, and bounded recovery.
Correct the contradictory rebase sentences in `SKILL.md` and `Jujutsu.md`.
Replace the entrypoint's exact-model-list instruction with a reference to the trusted attribution contract.
Keep authorization in the companion introduced by #56.

A new always-on rule would add resident context and duplicate the existing skill.
A new orchestration service would expand the change beyond the demonstrated defects.

### Compare required evidence with observed evidence

Derive required checks and approvals from effective policy before evaluating a check listing.
Record missing, failing, pending, skipped, and unknown results separately.
Use existing CLI data sources during the initial skill implementation.
A future readiness helper can automate this comparison through a separate change with fixture tests.

The alternative, another generic merge-ready checklist, repeats conditions that already exist and leaves the same acquisition gap.

### Keep ownership and delivery state local

Extend the pass's existing local record with the fields required by the specification.
Use explicit user reservations and observed concurrent work as inputs.
Create no new GitHub labels, comments, or ownership service.
On resumption, refresh live state and preserve outstanding reservations and publication boundaries.

### Bound recovery without diagnosing from timing alone

Replace the unlimited rerun advice with the specification's recovery budget.
Treat an expected reset according to the repository's live workflow.
Keep transient API retries distinct from a paid review summon.
For the known GitHub TLS error, preserve the owner's same-call retry after 60 seconds when that instruction applies.

Elapsed time and reported cost can help describe a failure.
They do not establish its cause.
Missing terminal diagnostics belong in a separate reviewer-tooling repair.

### Preserve existing sources of truth

The [commit-attribution specification](../../specs/commit-attribution/spec.md) already supports future models.
The [release-note-publishing change](../release-note-publishing/proposal.md) already addresses shared CHANGELOG writes.
BenchArtifact owns paired measurement and report generation.
This change references those contracts rather than copying their implementation into VersionControl.

## Risks / Trade-offs

- Extra prose can increase context cost. Replace obsolete text first and keep conditional procedures in companions.
- A readiness read can race a push. Re-read the head before reporting or acting.
- A local ownership record can become stale. Refresh it from owner instructions and live heads at each resumption.
- A retry default can stop too soon. The owner can declare a different budget, and corrected causes permit a new attempt.
- Council reviewers can miss contradictions in excerpts. Verify candidates against complete source files before accepting them.

## Migration Plan

First review the planning artifacts and the DECK-0008 amendment.
Then apply the scoped skill edits after the authorization companion is available.
Use replay fixtures for the specification's scenarios before a fresh GPT and explicit Claude Opus benchmark.
Reuse historical benchmark inputs only after reviewing their expectations against the current owner policy.
Deploy through the normal Rune path after evidence and review requirements pass.
Rollback restores the prior skill through that same path.

This change introduces no automated enforcement check.
Any later enforcement follows the [Gate Ratchet](../context-economy/specs/context-economy/spec.md#requirement-gate-ratchet), including debt and a flip condition.

## Research status

Lumo, Claude Opus, and Grok completed independent research reviews.
The native Grok route rejected a wrapper option.
The completed Grok call used the existing `sol-run@claude` profile with explicit `--model grok-4.6`.
Claude's documented model-flag precedence and its SDK diagnostic identify that requested model.
The research runs reported session-capture failures.
Their durable returned findings support investigation, not a benchmark or an archived-session claim.

Source review rejected duplicate publication instructions, a new reservation-label convention, and another CHANGELOG redesign.
It retained the rebase contradiction despite Lumo and Opus initially dismissing a rebase change.
The exact-model-list instruction also contradicts the current attribution contract.
The council did not determine acceptance by agreement.

Grok confirmed the missing-evidence and unbounded-retry gaps.
Source review rejected its proposal to block PRs merely because they share a file.
Shared files do not establish a merge conflict.
Source review also rejected diagnosis from short duration or zero cost.
Grok's dismissal of attribution and resumption changes conflicts with the obsolete catalog sentence and missing ownership-recovery procedure.
Persisting underlying provider errors remains a separate tooling repair.
