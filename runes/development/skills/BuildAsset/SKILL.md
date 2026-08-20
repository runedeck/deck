---
name: BuildAsset
description: "Build human-directed creative assets through complete exploration rounds, critique, direction selection, technical admission, exact-byte approval, and gated integration. USE WHEN generating or revising images, sprites, animation, audio, music, voice, fonts, icons, motion, models, or other creative assets that need human direction. NOT FOR one-shot disposable generation, no-change format conversion, provenance-only audits, or autonomous acceptance without a human reviewer."
metadata:
    version: 0.2.0
---

# BuildAsset

Creative asset work is a dialogue before it is a pipeline. The human owns taste and direction. Machines create options and enforce technical constraints.

## Prerequisites

- Identify the human who can direct the work and approve final bytes.
- Identify the asset medium, use context, references, constraints, and integration boundary.
- Read [AssetOntology.md](AssetOntology.md) before assigning roles or naming records.
- Read [StateModel.md](StateModel.md) before starting, resuming, or auditing the lifecycle.

## Constraints

- Show every generated output to the human. A machine failure can classify an output but cannot hide it from creative review.
- Keep the direction board separate from technical evidence. Failure-first diagnostics must not become the creative ranking.
- Stop after each creative round. Request human critique before refinement, combination, or another generation round.
- Never infer taste from validator scores, prior selections, silence, or approval of different bytes.
- A machine can reject technical inadmissibility. It cannot approve identity, expression, composition, rhythm, timbre, readability, style, or feel.
- A useful candidate can fail technical checks. A technical pass can still be creatively wrong.
- Use only the deterministic operations in the declared transform policy. A perceptible edit returns to human direction.
- Bind final approval to exact reviewed bytes and evidence. Any bound change invalidates that approval.
- Require one presentation record for each output, partial result, or safe failure card.
- Keep generation, approval, integration, and activation as separate transitions. A creative worker cannot edit operational source, manifests, hashes, runtime lists, or version-control state.

## Instructions

### Frame the asset commission

Extract the demonstrated intent from the conversation before asking questions. Record invariants, open choices, references by role, use context, technical constraints, and prohibited content. Ask only for unresolved decisions that can change the first exploration round.

State the human review cadence before generation: exploration, critique, directed iteration, selection, technical admission, context review, exact-byte approval, integration, then optional activation.

### Run human-directed creative rounds

Read and follow [CreativeWorkflow.md](CreativeWorkflow.md). Generate a bounded set of distinct candidates. Account for every worker attempt on a neutral direction board before technical diagnostics. Ask the human what to preserve, reject, combine, or change. Record the direction decision, then stop until the human responds.

Repeat directed rounds only from recorded critique. Do not let the generator choose the winning direction or silently repair a rejected creative choice.

### Admit and deliver the selected asset

After the human selects a direction, read and follow [TechnicalWorkflow.md](TechnicalWorkflow.md). Normalize and validate without replacing creative judgment. Return perceptible changes to the direction loop. Present exact use-context evidence for human review. Record approval only for exact reviewed bytes. Prepare integration as a separate reviewable change.

## Verification

- The record names the human director, asset brief, references, candidates, critique, decisions, and selected candidate.
- The direction board includes every accessible output and one safe failure card for each inaccessible output.
- Each creative round ends with a human checkpoint before the next round begins.
- Technical evidence identifies every transform, check, failure, and output hash without claiming creative approval.
- Final approval binds exact bytes and becomes stale after any bound change.
- Integration and activation occur only through their own explicit transitions.

## Troubleshooting

- No human is available: prepare references, constraints, prompts, and an exploration plan. Do not start a creative round or approve an asset.
- The human finds value in a failed output: retain it and use its selected traits in the next directed round.
- Every candidate fails technically: show all candidates, explain failures separately, and ask which direction deserves another creative round.
- A validator rejects container dimensions or placement: verify that the rule belongs to the technical profile and intended use.
- A deterministic repair changes the perceived result: classify it as a new candidate and return it to human review.
- Approval exists but a bound dependency changed: mark approval stale and request new context review and exact-byte approval.
