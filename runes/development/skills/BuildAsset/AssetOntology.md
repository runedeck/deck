# Asset ontology

Use this ontology to assign authority, name records, and prevent state shortcuts.

## Roles

Human director: owns creative intent, critique, direction selection, context judgment, and exact-byte approval.

Creative worker: produces candidate media from the current brief and permitted references. It has no operational or approval authority.

Technical steward: owns the versioned technical profile. Each profile revision requires a new verdict.

Pipeline operator: runs declared transforms, validation, evidence assembly, and authorized integration.

Validator: reports technical admissibility against one technical profile. It has no creative authority.

Integration authorizer: authorizes one integration plan. Approval of asset bytes does not grant this authority.

Runtime owner: authorizes one integration receipt for activation in one target context.

One person can hold several human roles. The authority boundaries still remain separate.

## Entities

Asset brief: invariants, open choices, use context, reference roles, prohibited content, medium, and review cadence.

Reference: an input with one declared role, such as identity, style, structure, timing, palette, timbre, registration, or context.

Worker attempt: one creative-worker invocation, including its status and all outputs.

Candidate emission: immutable raw output bytes with worker provenance, lineage, medium, and round identity.

Presentation record: proof that the human reviewed a candidate, partial output, or safe failure card.

Direction board: every candidate emission from one round, presented through a medium-appropriate comparison without technical ranking.

Critique: human observations that name what to preserve, reject, combine, or change.

Direction decision: the human-selected basis and constraints for the next round.

Technical profile: versioned transforms, checks, thresholds, tools, contexts, and technical owner.

Transform policy: deterministic operations allowed between raw candidate and technical evidence.

Normalized asset: candidate bytes after one recorded transform sequence.

Technical verdict: `admissible`, `inadmissible`, or `indeterminate`, with checks and evidence. It is not a creative verdict.

Context preview: exact normalized bytes presented in their intended scene, playback, layout, animation, sample text, mix, or runtime context.

Approval record: human decision bound to exact reviewed bytes, configuration, verdict, and context evidence.

Integration plan: target, expected changes, production derivations, and rollback boundary for approved bytes.

Integration authorization: separate human permission to execute one integration plan.

Integration receipt: actual integrated hashes and isolation evidence. Integration remains inactive.

Activation authorization: separate human permission to make one integration receipt active.

Activation receipt: evidence of the resulting active runtime state.

Audit event: append-only record for each attempted and completed transition.

All records are immutable revisions. Their links form an evidence graph.

Read [StateModel.md](StateModel.md) for lifecycle states, transition guards, invalidation rules, and prohibited shortcuts.
