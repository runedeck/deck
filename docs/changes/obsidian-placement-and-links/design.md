## Context

See [proposal.md](proposal.md) for the motivation and [the capability spec](specs/obsidian-placement-and-links/spec.md) for required behavior.

Deck currently has an Art module with collection and Obsidian guidance.
It has no `runes/obsidian/` module in the inspected checkout.
The new module will own reusable vault organization behavior.
Art will retain painting and artwork classification responsibilities.

The Atlas audit used the dedicated Obsidian CLI on 2026-09-11.
It read notes, properties, resolved outgoing links, and backlinks.
An independent audit read the relevant Base definitions through the same CLI.

Observed examples:

| Record or view | Observation | Consequence |
| --- | --- | --- |
| `Index/Miniature Painting.md` | Reviewed topic with aliases and Keyword Base embeds | Reuse the established topic identity when organizing painting knowledge |
| `Domains/Crafts/Miniature Painting/Miniature Painting.md` | Separate topic with the same name and a manual hub | Do not assume matching names identify the same graph node |
| Euthia project and art hub | Their topic links resolve to the local Domain hub | Their relationships differ from those of paint inventory records |
| Speedpaint Collection | Its topic link resolves to the Index topic | A visible identical wikilink can select a different destination |
| Keyword and Project Bases | Select `file.links.contains(this.file)` | These views require a direct incoming link |
| Resources views | Exclude projects, events, and journals | A resource view can contain guides and artwork without retagging them |
| Map Base | Matches `keywords` or `related` against the map's related topics | Existing graph properties support discovery across folders |
| Painting Base | Selects item tags | Shelf membership has its own contract |

The audit also found a working `Entire` resource linked to the `AI Stack` project through `keywords`.
Its companion `Entire Guide` appears through `related`.
This example shows that an existing keywords field can contain a project relationship.
These examples establish useful property conventions, not a universal schema for every vault.

## Goals / Non-Goals

**Goals:**

- Make physical placement and relationship discovery parts of the same organization workflow.
- Preserve topics as shared concepts across projects, resources, collections, and inventory.
- Make the proposed destination and link changes reviewable before application.
- Verify the graph through resolved note identities and actual view selection rules.
- Keep the workflow usable by Art and other domain skills.

**Non-Goals:**

- Rebuild Atlas, replace its schema, or impose a universal folder tree.
- Generate every possible topic link or maximize graph density.
- Add a graph database, watcher, background service, or new hierarchy property.
- Deploy a skill or reorganize Atlas during this planning change.
- Treat the availability of artwork as evidence that a painting recipe was tested.

## Decisions

### 1. Use a shared Obsidian module with a bounded organization workflow

Implement an Obsidian skill entry and supporting organization guidance under `runes/obsidian/`.
Follow the Deck module and skill conventions current at implementation time.
Add module metadata, defaults, documentation, and review cases as required by those conventions.

Art will refer to the shared workflow for placement, link identity, and Obsidian validation.
It will retain reference classification and palette review.
Preserve existing Art edits when making this integration.

Alternative considered: extend only Art's Obsidian page.
That would leave the same organization requirement unavailable to other domains.

### 2. Begin with a scoped application audit

Discover the dedicated CLI and its supported commands through installed help.
Use `search`, `read`, `properties`, `links`, and `backlinks` for relevant notes.
Read Base files as vault records to understand their filters.
Inspect folder conventions and current examples alongside these relationships.
Keep generated reports and fixtures in the workshop or repository, outside the user's knowledge notes.

Do not read unrelated or restricted areas while expanding the graph.
Use filesystem inspection for preparation or comparison where useful, but label it separately from application evidence.

Alternative considered: infer organization from filenames and directory listings.
The two Miniature Painting destinations demonstrate why that evidence is insufficient.

### 3. Decide purpose, placement, and relationships in one record

For each affected note, record:

| Field | Meaning |
| --- | --- |
| Identity | Existing exact path, title, aliases, and intended role |
| Home | Current and proposed physical location, with a short routing reason |
| Topic links | Concepts that describe the note, using current property conventions |
| Work links | The project that uses or owns the active work |
| Reference links | Companion resources, source records, artwork, and actual recipe ingredients |
| Membership | Existing collection or shelf relationship |
| Expected views | The specific topic, project, or collection views that should include it |

Use `keywords` for topics where the vault already uses that convention.
Use `related` for relevant companion records and existing work relationships.
Preserve established `collection` links.
Do not assign semantics to an unused `upstream` field merely because a template contains it.

A folder change is optional when the current home is already useful.
Link decisions emerge from understanding the note's purpose while placing it.
Do not schedule a later pass that connects every nearby note indiscriminately.

### 4. Keep project, resource, and topic roles distinct

The painting project owns current work, decisions, progress, and dated operational logs.
The Euthia resource owns reusable synthesis and navigation to recipes and reference records.
Both link directly to the existing Miniature Painting topic.
Relevant guides link directly to that topic and their project when those relationships are meaningful.
Art records retain their source evidence and collection membership.
Paint notes retain their inventory identity and are linked from recipes that use them.

This yields several useful routes to the same guide without duplicate recipe text.
Folders still provide predictable human browsing.

Alternative considered: use one growing project note for recipes, gallery indexes, and work logs.
That approach caused duplicated summaries and stale status in the audited Euthia notes.

### 5. Resolve ambiguous identities before changing references

Use exact paths during discovery and compare actual Obsidian resolutions.
Prefer unambiguous short wikilinks in the resulting vault where its conventions require them.
If the desired targets remain ambiguous, propose a distinct title, safe alias, or explicit target appropriate to the vault.
An alias that recreates the same ambiguity is not a repair.

For the Euthia review case, preserve the reviewed Index topic as the proposed shared topic.
Give the local manual hub a distinct role or integrate its useful content through a reviewed migration.
This is a proposed identity decision, not authorization to merge live notes.

Alternative considered: accept all resolved links as valid.
A link can resolve successfully to the wrong same-named note.

### 6. Validate each layer with the evidence it needs

File validation checks saved content, source assets, metadata, and preserved history.
Relationship validation checks exact outgoing destinations and relevant incoming backlinks.
View validation checks the actual Base filters and intended membership.

Context-dependent Bases use `this.file`.
Do not treat a standalone query with a different context as proof of an embedded view's membership.
Use a supported application context check, a disposable fixture, or report that view validation remains incomplete.
If a visual review is requested, use authorized Computer Use and report that separately.

No GUI executable fallback is allowed when the dedicated CLI fails.
After a save, compare current application content with the latest file before attributing a mismatch to cache delay.
Permit a bounded follow-up read after the application has processed the change.
Persistent failures remain explicit.

### 7. Clean frontmatter through its field contract

Inspect current schemas, working notes, and affected Base filters before removing metadata.
Normalize formatting and field order only within the authorized records.
Remove unused empty placeholders when they have no semantic or consumer dependency.
Preserve meaningful false, null, and unknown values, source uncertainty, thumbnails, and required fields.
Treat absent values and empty values as potentially different states.
Formatting does not establish substantive review or painting completion.
Validate property readback and affected view behavior after cleanup.

## Risks / Trade-offs

- Duplicate names can redirect valid-looking links. Mitigation: compare exact destinations and test changed contexts.
- Bulk link additions can obscure useful relationships. Mitigation: require a semantic reason for each relationship class.
- Stale templates can reintroduce retired fields. Mitigation: compare them with current rules and working notes.
- Dynamic views can be tested in the wrong context. Mitigation: record the context and the filter used for validation.
- A rename can affect notes outside the planned folder. Mitigation: inspect backlinks before defining the affected change set.
- Concurrent edits can invalidate a prepared migration. Mitigation: compare live notes with snapshots before applying or reversing changes.
- Folder-note plugins can expand a file rename into a parent-folder rename. Mitigation: inspect coupling and compare parent and sibling paths immediately afterward.
- A shared workflow can overfit Atlas. Mitigation: keep property names and folder examples conditional on the target vault's conventions.

## Migration Plan

1. Implement and validate the reusable module in Deck without deployment.
2. Connect Art to the shared organization workflow while preserving its specialized responsibilities.
3. Evaluate disposable examples for folder placement, duplicate topics, direct links, note roles, and application failures.
4. Present the module change and validation evidence for review before any installation.
5. In a separately authorized Atlas task, prepare the exact note, folder, and relationship diff for the Euthia migration.
6. Apply that scoped migration through supported operations and verify files, links, backlinks, and affected views.
7. Preserve before-state evidence and reverse only the migration's changes if validation fails.

The OpenSpec artifacts remain planning records until implementation and deployment are separately completed.
