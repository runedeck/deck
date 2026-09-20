# Identity and views

Read this before renaming same-named notes or validating dynamic membership.

## Resolve identities deliberately

Compare exact paths, titles, aliases, role tags, content, and backlink sets.
A displayed `[[Miniature Painting]]` can resolve to different notes from different source paths.
The title alone cannot establish the intended topic.
Record the actual destination returned by Obsidian for each affected source.

For a duplicate topic and manual hub, choose the shared topic from current rules and established use.
Give the useful hub a distinct role and name, or integrate its content through a scoped migration.
Do not merge records automatically because their filenames match.
For example, two artwork records titled Spring by different artists remain separate identities.

Prefer short wikilinks when they resolve unambiguously and the vault uses them.
Otherwise use an explicit target, distinct title, or safe alias under the vault's conventions.
An alias that recreates the ambiguity is not a repair.
Link-aware rename operations can preserve the old wrong relationship under a new title.
Inspect their results and retarget the intended topic links explicitly.

## Classify each view contract

Direct link: A source record links to the selected target.
Transitive relationship: A source links to an intermediate record that links to the target.
Property membership: A field names the collection or other group.
Tag membership: A filter selects the record's type or category tag.

A filter such as `file.links.contains(this.file)` selects direct incoming links.
A guide that links only to a project is not thereby selected by the topic's direct-link view.
Add a direct topic link when it describes the guide and the intended topic view requires it.
Do not add an irrelevant relationship solely to obtain a desired row.

A view named Resources can accept guides, artwork, or other types while excluding projects, events, and journals.
Read the filter before adding `type/resource` or changing a correct record type.
Inventory and art galleries can use different tag or property contracts.
Keep those contracts intact during a project/resource split.

## Verify context as well as results

Record the Base path, selected view, expected embedding note, filter, and target records.
This supported command can inspect a Base when the installed help confirms it:

```text
obsidian-cli vault=Example base:query path="Templates/Keyword.base" view=Resources format=paths
```

The command offers no embedding-context argument in the observed help.
If the filter uses `this.file`, determine what file the actual query binds to it.
A result bound to the Base file does not prove membership when embedded in a topic note.
Use a supported application context inspection or the authorized rendered embed.
A disposable fixture can test the procedure, but does not verify the live vault's embedded result.
If the intended context cannot be checked, mark that view incomplete.

Compare expected and actual membership, including representative exclusions.
Report missing intended records and unexpected records separately.
A successful file read or nonempty query result does not establish view correctness.
