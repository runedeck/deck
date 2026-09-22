## ADDED Requirements

### Requirement: Consequences carry a sign

A record MUST place its consequences under `### Consequences` inside `## Decision Outcome`, as the runeADR template does. Each consequence MUST be one list item that starts with `[+]` for a gain or `[-]` for an accepted cost. A record with `## Consequences` as its own section MUST fail the schema check.

#### Scenario: Consequences become their own section

- **WHEN** a record writes `## Consequences` at the second heading level
- **THEN** the schema check reports the record and names the missing `### Consequences` under `## Decision Outcome`

#### Scenario: Consequence bullet has no sign

- **WHEN** a consequence item starts with neither `[+]` nor `[-]`
- **THEN** `scripts/check-decision-shape` fails and names the record and the item

### Requirement: Consulted entries name the harness

A `consulted` entry MUST be a human handle that starts with `@`, or a model identity in the form `<model-id>@<harness>`. The harness MUST be the first label of a domain in `model_domains` of `authors.yaml`. A bare model id MUST fail the check.

#### Scenario: Consulted entry names a model without a harness

- **WHEN** a record writes `consulted: ["claude-fable-5-1"]`
- **THEN** `scripts/check-decision-shape` fails and names the entry and the accepted form

#### Scenario: Consulted entry names an unknown harness

- **WHEN** a record writes `consulted: ["gpt-6-astra@openai"]` and `openai` is not a harness in `authors.yaml`
- **THEN** `scripts/check-decision-shape` fails and lists the known harnesses

### Requirement: Provenance entries resolve

Each `upstream` and `related` entry MUST resolve to one of: a record in `docs/decisions/` by its file stem, a capability `<capability>` or a requirement `<capability>#<requirement-slug>` in `docs/specs/` or in an active change, or a URL. A capability reference MUST resolve before and after the change archives, because the reference names no path.

#### Scenario: Upstream names a file that does not exist

- **WHEN** a record writes `upstream: [MarkdownFirst.md]` and no record, capability, or URL matches it
- **THEN** `scripts/check-decision-shape` fails and names the entry

#### Scenario: Upstream names a capability requirement

- **WHEN** a record writes `upstream: ["markdown-first-authoring#markdown-system-language"]` and the requirement heading exists in a delta or canonical spec
- **THEN** `scripts/check-decision-shape` passes the entry

### Requirement: Canvas source is linked and its snapshot is checked

A record that started from a drawing in the owner's vault MUST list the drawing's `obsidian://` link in `upstream`. The repository MUST keep a snapshot of the drawing under `docs/ideas/` with a provenance sidecar that records the link and the sha256 of the bytes the Obsidian CLI returned. `scripts/sync-idea --check` MUST report a snapshot whose vault source has a different digest.

#### Scenario: Record links a drawing

- **WHEN** a record's `upstream` lists `obsidian://open?vault=Atlas&file=Library%2FCanvas%2FMarkdown%20First`
- **THEN** `scripts/check-decision-shape` accepts the entry as a URI

#### Scenario: Drawing changes after the snapshot

- **WHEN** the drawing in the vault is edited after `scripts/sync-idea` wrote its snapshot
- **THEN** `scripts/sync-idea --check` names the snapshot, both digests, and the sync command that refreshes it

### Requirement: Adopted record keeps its source dates

A record adopted from another repository MUST keep the `created` and `updated` dates of its source and MUST name the source in `upstream`. A later edit in the deck moves `updated` and states the edit under `## More Information`.

#### Scenario: Record is adopted from forge-core

- **WHEN** the deck adopts a forge-core record
- **THEN** the deck record and the source carry the same `created` and `updated` values, and `upstream` names the source record
