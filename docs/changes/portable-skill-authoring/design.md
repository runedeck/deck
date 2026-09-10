# Portable authoring design

## Context

The source-layer audit found 30 authored literal findings across five skills before this change.
Repeated provider and model checks produced additional reports for the same authored text.
The count does not imply 390 independent defects.

## Goals / Non-Goals

Keep shared instructions usable without a particular harness's symbolic tool names.
Preserve each workflow's substantive outcomes and evidence requirements.
Keep source, rendered, and native evidence checks distinct.
Do not change shared schemas, deployment ownership, accepted spec status, or the active Claude issue run.

## Decisions

Use plain capability names for shared steps, such as the available structured question tool.
If that capability is absent, prescribe a concrete portable fallback.
Use the tool's observed capacity rather than a Claude-specific question limit.

Keep provider tool scopes in a provider entrypoint with explicit `mode: append` and an empty body.
The existing resolver merges those metadata keys and preserves the base procedure.
Use complete replacement when a provider changes the procedure itself.
Do not introduce companion overlays or cumulative provider/model bodies.
Shared rules use the same `<provider>/<exact-model-id>/SKILL.md` path contract.
A variant entrypoint does not create a second canonical skill.
Shared file-reading instructions name the available capability.

Shared authoring guides explain provider boundaries in plain language and link to authoritative provider documentation.
They do not ship native invocation examples as generic instructions.
Require `rune validate --skill-layers --source <skill-folder>` for new or changed skills.
Require the applicable schema checks separately.
Route creation and validation through the shared implementation-loop companion.
That companion assigns independent review, a frozen work order, executable checks, and an evidence-based repair procedure.
The CLI runbook owns runner details so they do not diverge between skills.
Keep native discovery and model behavior unverified until their separate evidence exists.

## Risks / Trade-offs

The literal policy has a finite vocabulary. It does not prove arbitrary prose correct.
Provider reference links require a later documentation lookup when an author needs native syntax.
Metadata-only variants preserve existing native scopes but do not establish their runtime enforcement.

## Migration Plan

1. Correct the five shared skills in the isolated content clone.
2. Refresh only the affected source subject digests.
3. Run the source-layer gate against all current Deck skills.
4. Run focused content tests and existing schema, provenance, and prose checks.
5. Publish the content PR against the pinned architecture revision.
