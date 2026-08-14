# Technical admission workflow

Use this workflow only after the human selects a creative direction.

## Declare the technical profile

The technical steward must declare one versioned technical profile before validation.

The profile lists transforms, checks, thresholds, tool identities, contexts, and evidence. It also names the technical steward.

List each deterministic operation, its limits, measurement domain, and processing rule. The operations depend on the asset medium.

Image operations can include keying, uniform scaling, translation, cropping, cleanup, and deterministic encoding.

Audio operations can include trimming, channel mapping, level measurement, sample-rate conversion, fades, and deterministic encoding.

Font operations can include subsetting, table normalization, hint preservation, specimen generation, and deterministic packaging.

Any operation that changes identity, expression, structure, rhythm, tone, timbre, composition, readability, style, or feel creates a new candidate. Return that candidate to human direction.

## Normalize and validate

1. Preserve the raw candidate and hash it.
2. Apply the transform policy once and record each parameter.
3. Produce exact intended-use bytes through the production path.
4. Run medium-specific checks from the technical profile.
5. Preserve every failure and its evidence.
6. Classify the candidate as `admissible`, `inadmissible`, or `indeterminate`.
7. Treat `indeterminate` as technically blocked.

A blocked result remains visible and can still inform creative direction. It cannot enter exact-byte approval.

A technical steward can revise the technical profile. The revised profile requires a new verdict and does not waive the old verdict.

## Present context evidence

Present the exact bytes in each context that can expose creative defects.

Images can need scale, background, crop, animation, mirroring, atlas, UI, scene, and layout previews.

Audio can need level-matched playback, loops, transitions, stems, mix context, loudness data, and target-device playback.

Fonts can need specimen pages, target scripts, sizes, weights, shaping, fallback, rasterization, and application context.

Models and motion can need turntables, camera views, deformations, loops, collisions, lighting, and target-engine playback.

Keep machine checks and transforms in a separate evidence section. Ask the human to judge the asset in context.

Technical admissibility does not answer whether the asset feels correct.

## Bind exact approval

Record approval only after the human identifies the candidate or derivative they reviewed. Bind at least:

```text
human approver
approval decision and time
raw candidate hash
normalized asset hash
effective configuration hash
technical verdict hash
context preview hashes
integration target
canonical approval-manifest hash
```

The canonical manifest also binds the transform policy, renderer or build identity, and all reviewed artifacts.

Do not ask the human to compare hashes manually. The system uses hashes to prove that later bytes match the reviewed bytes.

## Prepare integration and activation

1. Verify approval freshness before integration.
2. Prepare one integration plan with its target, change boundary, and rollback boundary.
3. Request separate human authorization for that integration plan.
4. Prepare the smallest source and metadata change from approved bytes.
5. Prove unrelated source and output regions remain unchanged.
6. Create an integration receipt with actual hashes and isolation evidence.
7. Keep the integrated asset inactive.
8. Request separate activation authorization for one integration receipt and one target context.
9. Activate only the authorized receipt through the owning runtime gate.

If any bound byte, profile, tool, transform, verdict, preview, or manifest changes, mark all dependent records stale.

Resume at the earliest review state that owns the changed dependency.
