# Discovery

Read this before proposing vault organization.
Inspect only the requested collection and relevant relationship targets.

## Establish scope and access

1. Recover authorization and corrections from the conversation.
2. Read vault rules, current schema guidance, and representative working notes.
3. Locate the supported dedicated CLI through the environment's tool inventory or installation documentation.
4. Confirm its presence and read its help before choosing commands.
5. Record the exact executable, version when available, vault, command arguments, exit status, and output.

The demonstrated macOS installation includes a dedicated `obsidian-cli` launcher inside the application bundle.
Its presence does not authorize a probe of the separate GUI executable.
Other installations can expose a different supported launcher.
Require command support from installed help rather than a guessed minimum version.

## Select supported commands

These forms were checked against installed Obsidian CLI help.
`obsidian-cli` below means the discovered dedicated executable, not an assumed PATH entry.
Replace the illustrative vault and paths with observed values.
Use an argument array when paths or values contain spaces.

```text
obsidian-cli help
obsidian-cli version
obsidian-cli vault=Example search query="Miniature Painting" path=Index limit=20 format=json
obsidian-cli vault=Example read path="Index/Miniature Painting.md"
obsidian-cli vault=Example properties path="Index/Miniature Painting.md" format=json
obsidian-cli vault=Example aliases path="Index/Miniature Painting.md"
obsidian-cli vault=Example links path="Index/Miniature Painting.md"
obsidian-cli vault=Example backlinks path="Index/Miniature Painting.md" format=json
obsidian-cli vault=Example read path="Templates/Keyword.base"
```

`path` addresses an exact vault-relative record. `file` resolves a name like a wikilink.
Prefer exact paths while identity is uncertain.
Most commands use the active file if neither argument is supplied. Avoid that implicit context during an audit.
The listed discovery calls return text or the selected structured format and do not change notes.
They communicate with the application. Application startup and availability depend on the installed launcher.
Record nonzero exits, timeouts, signal termination, and error text separately from a successful empty result.
Do not assume an empty result means a note is absent when the call failed.

## Build the bounded evidence set

For each affected note, read its content, properties, aliases, outgoing destinations, and incoming references.
Expand to an external target only when identity, membership, or a proposed relationship requires it.
Respect restricted areas even when a note links to them.

Read each affected Base definition and identify its filter, view, and embedding note.
Compare role tags, collection fields, and relationship properties with working records.
Record conflicts with stale templates explicitly.
For example, a retired language tag in a template does not override current vault rules.

Filesystem inspection can compare bytes, inventory assets, or prepare snapshots.
Label that evidence separately from CLI-backed resolution.
Do not infer graph edges from filename matches or directory proximity.
Proceed to [Placement.md](Placement.md) after the evidence explains both homes and relationships.
