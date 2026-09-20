# Delivery recovery replay

An independent agent received the complete VersionControl source and eight mock observation sets on 2026-09-10.
The agent received no expected answers, council conclusions, or benchmark checker.
It selected actions without changing a repository or calling GitHub.
The parent compared those actions with the specification.

Source: VersionControl at `a414359be1809d8cd87a8ecc468b0e32a6c6e239`.
The complete skill digest is `8cd1d619fe73e6d61555529a43265e0e86e9c9247260e0de3c76f0779d408e7c`.

| Observation | Returned decision | Result |
| --- | --- | --- |
| Green checks, but organization policy returns `403` | Block readiness and record unknown policy with the read failure | Pass |
| Final head changes from `b1` to `b2` | Discard the stale judgment and reconcile ownership | Pass |
| Conflict-free PR with an explicit owner base-update request | Apply a scoped base merge, validate, normally push, and obtain fresh evidence | Pass |
| Three failed summons within an owner budget of four | Record the unknown cause and permit the fourth attempt | Pass |
| Push transport fails, but remote confirms repair `e2` | Record `e2` as published and assess review requirements separately | Pass |
| Push transport and subsequent remote read both fail | Record blocked, unverified publication and preserve the last verified head | Pass |
| Policy requires zero approvals and every other condition passes | Report merge-ready without merging | Pass |
| A verified wrapper correction follows exhausted retries | Permit another attempt after recording the correction and checking pending runs | Pass |

All eight replay cases pass.
This replay checks decisions, not preferred phrases or response length.
It is a single-agent treatment replay, not the paired GPT and Opus benchmark.
It does not establish production success, comparative improvement, or token efficiency.
