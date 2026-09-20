# Migration

Read this before applying an authorized organization change.
Authorization can come from the current instruction or earlier explicit approval in the conversation.
A proposal alone does not authorize a live migration.

## Preserve a scoped before-state

Record the exact affected note paths and relevant incoming references.
Inspect folder-note conventions and relevant enabled plugin behavior before renaming a note that matches its parent folder.
Record the parent folder and sibling paths as part of the operation's expected boundary.
Some folder-note plugins rename the containing folder when its same-named note changes.
Do not assume the CLI's file operation prevents plugin side effects.
Save original bytes, hashes, intended destinations, and planned edits outside the knowledge notes.
Record asset paths and hashes when notes move or embeds change.
Include dated log sections and provenance in the preservation inventory.
Prepare a reviewable diff and follow the vault's existing preview requirements.

Immediately before each mutation, compare the live note with its saved before-state.
If it changed, read the new content and revise the planned edit around the user's changes.
Do not overwrite it with the prepared snapshot.
Keep independent, unaffected work moving while resolving a specific conflict.

## Apply the smallest coherent change

Use supported link-aware operations when they fit the vault's rules.
When folder-note coupling exists, choose a supported detachment or move sequence after checking the current plugin behavior.
Do not change plugin or global settings as an automatic workaround.
These examples require confirmation against installed CLI help:

```text
obsidian-cli vault=Example move path="Crafts/Old Guide.md" to="Crafts/Painting/Guide.md"
obsidian-cli vault=Example rename path="Crafts/Miniature Painting.md" name="Painting Overview"
```

These commands mutate vault paths and can update references in other notes.
Inspect those references before the operation and read them afterward.
Immediately compare the parent folder and recorded sibling paths with the expected operation boundary.
A successful CLI exit does not prove that only the requested file moved.
If the parent or unrelated siblings moved unexpectedly, stop dependent operations and reconcile the exact path changes first.
Preserve concurrent edits and use scoped reversal when the unplanned changes can be reversed safely.
Do not assume every link form, alias, asset embed, or desired retarget is repaired automatically.
Use exact scoped text edits for content under the applicable file-edit rules.

When splitting a hub, keep one authoritative copy of each reusable recipe.
Move operational logs into the owning project while retaining their original dates and content.
Keep reference records, source URLs, creator roles, assets, and uncertainty with their reusable evidence.
Preserve incoming navigation through corrected links or safe aliases appropriate to the resulting roles.
Do not keep an old alias if it recreates the identity ambiguity being fixed.

Validate each coherent group before broadening the migration.
Write the completed work log in the owning project using the actual date and local syntax.
Add a daily summary only when the vault's standard requires it.
Keep detailed generated diagnostics in the workshop or repository.

## Reverse only this change

Record the applied after-state and the path/link transformations.
Before reversal, compare current files with the recorded after-state.
If they match, reverse the scoped transformations through supported operations.
If they differ, preserve intervening user edits and reverse only the identified migration hunks.
Use the before-state as evidence, not as a blanket restore command.
If a hunk cannot be separated safely, leave that hunk unchanged and identify the conflict for the user.

Never delete the whole destination tree or restore an entire vault to reverse a few notes.
Verify content, assets, link destinations, and view membership after any reversal.
Report both the successful reversal and any unresolved conflict accurately.
