# Decision record shape design

## Approach

The directory schema checks headings and field presence. A content check reads what the schema cannot: the sign on each consequence, the harness on each consulted model, and whether each `upstream` or `related` entry resolves. A second check compares each idea snapshot with its vault source. The [proposal](proposal.md) states why.

## Commands

A requirement names a role. This table names the program, flags, and hook behind each requirement, so nothing is lost when a command moves out of a requirement.

| Requirement | Command | Notes |
|---|---|---|
| Consequences carry a sign | `python3 scripts/check-decision-shape` | hook `check-decision-shape`. The schema check in `docs/decisions/.mdschema` rejects `## Consequences` at the second heading level |
| Consulted entries name the harness | `python3 scripts/check-decision-shape` | the harness list comes from `model_domains` in `authors.yaml` |
| Provenance entries resolve | `python3 scripts/check-decision-shape` | records under `docs/decisions/`, capabilities and requirements under `docs/specs/` or `docs/changes/<change>/specs/` |
| Canvas source is linked and its snapshot is checked | `python3 scripts/sync-idea <link>` writes the snapshot, `python3 scripts/sync-idea --check` reports a stale one | hook `sync-idea`. The link is an `obsidian://` URI, for example `obsidian://open?vault=Atlas&file=Library%2FCanvas%2FMarkdown%20First`. Snapshots sit under `docs/ideas/`. The check answers only while Obsidian runs |
| Adopted record keeps its source dates | none yet | the content check does not read `created` or `updated` |
