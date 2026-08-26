# Asset state model

Read this model when you start, resume, or audit creative asset work.

## States

`briefed`: the asset brief can support an exploration round.

`exploring`: worker attempts exist and await complete presentation.

`awaiting-critique`: every emission, partial output, and failed attempt has a presentation record. The human must respond.

`directed`: human critique defines the next creative direction.

`selected`: the human selected one reviewed candidate lineage for technical admission.

`technical-gating`: normalization and validation run under one technical profile.

`technical-blocked`: the verdict is `inadmissible` or `indeterminate`.

`technical-admissible`: the verdict is `admissible`.

`awaiting-context-review`: exact intended-use previews await human judgment.

`byte-approved`: exact bytes and evidence have human approval.

`integration-authorized`: a human authorized one integration plan.

`integrated-inactive`: approved bytes exist in the source system but remain inactive.

`activation-authorized`: a human authorized one integration receipt for activation.

`active`: the integrated bytes are selected by the runtime or delivered product.

`abandoned`: the human ended the work without approval.

`superseded`: a successor work item replaced this item.

`stale`: a dependency, configuration, transform, or reviewed byte changed.

## Transitions

`briefed → exploring`: the human director opens a bounded round from one asset brief.

`exploring → awaiting-critique`: every emission, partial output, and failed attempt has a presentation record.

`awaiting-critique → directed`: the human director records critique for another round.

`directed → exploring`: the operator starts the directed round without adding creative choices.

`awaiting-critique|directed → selected`: the human director selects one reviewed candidate lineage.

`selected → technical-gating`: the operator uses one versioned technical profile.

`technical-gating → technical-blocked|technical-admissible`: declared checks create one technical verdict.

Treat `indeterminate` as technically blocked. A human cannot waive an existing technical verdict.

`technical-blocked → directed`: the human director requests a perceptible change.

`technical-blocked → selected`: the technical steward revises the profile. The operator must create a new verdict.

`technical-admissible → awaiting-context-review`: the operator builds bound context previews.

`awaiting-context-review → directed`: the human director rejects the asset in context.

`awaiting-context-review → byte-approved`: the human director approves the canonical manifest.

`byte-approved → integration-authorized`: the integration authorizer approves one integration plan.

`integration-authorized → integrated-inactive`: the operator executes the plan and creates an integration receipt.

`integrated-inactive → activation-authorized`: the runtime owner approves one receipt and target context.

`activation-authorized → active`: the operator activates the authorized receipt and creates an activation receipt.

The human director can move any inactive state to `abandoned` or `superseded`.

A perceptible change returns any later state to a new candidate emission in `exploring`.

A bound change moves dependent states to `stale`. Resume at the earliest state that owns the changed dependency.

## Invariants

Visibility invariant: every emission, partial output, and failed attempt gets a presentation record before critique closes the round.

Failure visibility invariant: show partial outputs and safe failure cards. Never claim visibility when no accessible output exists.

Authority invariant: no machine record substitutes for human critique or approval.

Separation invariant: creative direction, technical admission, approval, integration, and activation remain distinct.

Identity invariant: every derivative points to one raw candidate and one recorded transform sequence.

Exactness invariant: approval identifies exact bytes, not a filename, label, or visual resemblance.

Freshness invariant: changed bytes, checks, configuration, or context evidence invalidate dependent approval.

Reversibility invariant: exploration and evidence do not mutate source assets or runtime state.

Provenance invariant: keep rejected candidates, failed attempts, stale approvals, and failed transitions in the audit record.

Activation invariant: activation authorization binds one integration receipt and one runtime or publication context.

## Invalid shortcuts

- Generate repeatedly until machine metrics choose a winner.
- Hide failures or place them outside the creative comparison.
- Claim visibility without accessible bytes or a safe failure card.
- Ask for creative direction only after technical validation.
- Normalize every candidate before the human selects a direction.
- Treat creative-worker self-checks as technical admission.
- Treat a validator pass as approval.
- Treat a direction decision as approval of candidate bytes.
- Repair identity, structure, timing, expression, or composition during deterministic normalization.
- Integrate a selected candidate before exact context review.
- Reuse approval after bytes, transforms, evidence, or technical policy changes.
- Integrate after byte approval without separate integration authorization.
- Activate after integration without separate activation authorization.
