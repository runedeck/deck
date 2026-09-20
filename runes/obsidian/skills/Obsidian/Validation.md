# Validation

Read this after an applied change or when reviewing a proposed validation plan.
Use four separate evidence layers.

## Files and content

Compare saved content and metadata with the approved transformation and latest live input.
Parse frontmatter and run the vault's scoped checker when available.
Verify local assets and preserve their hashes when their bytes should remain unchanged.
Confirm recipe text, source URLs, creator roles, uncertainty, and dated work logs survive.
Read the changed records and properties through the dedicated CLI.
Report filesystem consistency and application readback separately within this layer.

If a read differs, compare it with the latest file before attributing the difference to cache delay.
Allow one bounded follow-up after application processing.
A persistent difference is unresolved evidence, not a reason to restart the GUI or loop indefinitely.

## Relationships

Use Obsidian to obtain outgoing resolved destinations and relevant incoming backlinks.
Compare them with the exact intended identities, including duplicate-name and alias cases.
Verify each new project, topic, resource, collection, and ingredient relationship has a semantic reason.
Check preserved incoming references from outside the moved folder.
Do not count a resolved link to the wrong note as a pass.
Do not broaden the task into unrelated vault-wide link repair.

## Views

Read the actual Base filters and record each view's context and membership contract.
Check representative expected inclusions and exclusions after property or relationship changes.
Inspect category-specific thumbnails when a gallery uses them.
For `this.file` filters, verify the intended embedding context or report this layer incomplete.
A disposable fixture or filter prediction is not live application membership evidence.

## Requested visual inspection

Use Computer Use only under the environment's GUI authorization rules and the user's requested task.
Acquire fresh application state after navigation and each material change.
Open the intended note and verify its visible identity, rendered layout, and useful navigation.
Inspect the actual gallery membership and thumbnails when those are part of the request.
Do not infer visual correctness from a filesystem read or a stale screenshot.

Reduce simultaneous gallery embeds only when relevant evidence supports that layout change.
Do not claim that it proves a crash cause or change global settings as a side effect.
After a launcher failure, preserve the exact failure evidence and stop repeated probes.
Investigate crash logs only when diagnosis is within the user's task.

## Report the result

Use separate states such as passed, failed, incomplete, or not requested for each layer.
Include the affected paths, commands or observation method, exact contexts, and relevant counts.
For example:

```text
Files: Passed. Saved content and CLI readback match for the changed guide.
Relationships: Failed. The topic link resolves to the local hub, not the Index topic.
Views: Incomplete. The standalone query does not establish the intended embed context.
Visual: Not requested.
```

This example is not a fully validated organization change.
Retain completed work and identify the narrow remaining action.
When the CLI is unavailable, filesystem checks can still pass but application and graph evidence remain incomplete.
Distinguish local skill source edits, validated fixtures, installation, and a live vault migration in the final report.
