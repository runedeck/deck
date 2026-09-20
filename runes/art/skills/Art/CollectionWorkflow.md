# Collection workflow

Use this procedure when the user authorizes saving or correcting an art collection.
Use the destination's current conventions instead of imposing a personal vault layout.

## Inspect before editing

Read the collection schema, subject notes, asset layout, gallery views, and logging instructions.
Search content and properties as well as filenames before concluding that a reference is missing.
Build a scoped list of subjects, existing evidence categories, duplicates, missing credits, and coverage gaps.
Retain useful previous references while adding stronger evidence.
Treat the user's current request and earlier authorization as the scope for changes.

## Keep evidence categories consistent

Separate standalone artwork, partial artwork, card photographs, painted references, and sculpt renders.
A single subject can have several categories. Do not force each subject into only one category.
Keep each asset's category and provenance distinct within a subject note.
Use a thumbnail from the category represented by its gallery view.

When the collection uses the demonstrated Euthia schema, preserve this invariant:

```text
art.illustration == (art.full_illustration OR art.partial_illustration)
```

That schema uses full illustration for standalone artwork without a sculpt overlay.
It does not establish an uncropped original master.
Do not copy these property names into a collection with a different schema.
Availability text, Boolean properties, filters, and thumbnails must describe the same evidence.

Keep separate gaps for image availability, original source, creator identity, higher resolution, and painted examples.
A new small standalone image can close an availability gap while leaving provenance and resolution unresolved.
Do not preserve a stale missing status after the user supplies new evidence.

## Save useful records

Preserve the source page and asset link alongside any authorized local copy.
Record dimensions, variant, image type, creator roles, and inspection limits where they affect later use.
Keep third-party artwork rights separate from the collection's own license.
Link painting plans to their references and inventory instead of copying inconsistent paint lists into several notes.
For Obsidian, load the shared `Obsidian` skill through [ObsidianWorkflow.md](ObsidianWorkflow.md) when organization or link identity needs work.
Choose the physical home and meaningful topic, project, resource, and ingredient links together.
Do not link records solely because they share a folder or gallery.

Make related note, asset, coverage, and gallery changes together.
Keep changes scoped and recoverable. Preserve unrelated user edits.
Do not rebuild the whole collection when correcting a few categories.

## Validate and log

Check changed files, properties, local image links, category thumbnails, and affected gallery results.
Confirm that referenced assets open and duplicate links point to the intended original.
For Obsidian, use the shared validation layers and Art's category checks in [ObsidianWorkflow.md](ObsidianWorkflow.md).
Check exact resolved identities and relevant backlinks as well as file content.
A standalone Base query does not prove membership when its `this.file` context differs from the intended embed.
A generic full-vault warning is not automatically a failure of the edited notes.

Read the current worklog and daily-note standard before adding entries.
For the demonstrated Atlas convention, use these elements:

```text
Work-log section: ## Work log
Date heading: ### [[2026-09-09]]
Completed effort: - [#] #log/effort Corrected the Hydra reference category and verified its gallery link.
```

Use the actual work date and completed action. The example date and subject are not defaults.
Put detailed changes and validation evidence in the owning project note.
Add a linked one-line summary to the daily journal when that convention requires it.
Do not invent an effort-duration subtype, elapsed time, or completed validation.

Report saved notes, asset counts, category corrections, validation scope, and unresolved gaps only when useful to the request.
