## Purpose

Organize Obsidian notes so people can find them through folders and discover meaningful relationships through the graph.
Keep note identity, roles, and application views consistent as content finds its place.

## ADDED Requirements

### Requirement: Inspect the current vault before organization

The workflow MUST inspect the target vault through its supported Obsidian CLI before proposing an organization change.
It MUST examine relevant note content, properties, resolved links, backlinks, aliases, and Base filters.
It MUST use current vault rules and working examples to interpret those observations.
It MUST distinguish observed behavior from proposed conventions when templates or notes disagree.

#### Scenario: A folder listing hides a topic relationship

- **WHEN** a project and a resource occupy different folders but link to the same topic
- **THEN** the audit records their shared topic and their separate physical homes
- **AND** it does not infer unrelated content from their folder separation

#### Scenario: A template conflicts with current rules

- **WHEN** a template includes retired tags that current vault rules reject
- **THEN** the workflow records that conflict and uses the current accepted metadata
- **AND** it does not copy the retired fields into newly organized notes

### Requirement: Choose a human-readable home and note role together

For each organized note, the workflow MUST identify its purpose, note role, and proposed physical home.
The home MUST follow the vault's established routing and support human browsing.
Folder placement MUST NOT redefine a topic as a project, resource, or container merely because names match.
Existing suitable homes MUST remain valid when only relationships need correction.

#### Scenario: Painting work and reusable knowledge

- **WHEN** a painting collection contains active work and reusable reference material
- **THEN** the plan identifies a project for actions and progress and a resource for reusable knowledge
- **AND** both receive suitable physical homes and links to the existing Miniature Painting topic
- **AND** the topic retains its conceptual role

### Requirement: Add meaningful relationships when notes find their place

The workflow MUST assess relationships as part of each note's placement, creation, or revision.
It MUST propose links supported by the note's subject, work context, membership, cited sources, or actual dependencies.
It MUST reuse existing topic, project, resource, collection, and item identities where they fit.
It MUST NOT create links solely from shared folder placement or a goal of increasing graph density.
It MUST use existing property meanings instead of introducing a mandatory hierarchy field.

#### Scenario: A miniature guide uses an existing paint

- **WHEN** an Euthia guide specifies a paint that already has an inventory note
- **THEN** the guide links to that paint and its relevant project, topic, and reference material
- **AND** unrelated paints and artwork receive no new link merely because they share a shelf

#### Scenario: A new relationship becomes clear during filing

- **WHEN** the content establishes that a note belongs to an existing topic while its home is selected
- **THEN** the same organization plan includes the topic relationship and the physical destination
- **AND** graph integration is not deferred to a separate indiscriminate linking pass

### Requirement: Verify note identity and resolved destinations

The workflow MUST detect ambiguous names and aliases among the affected notes and their intended targets.
It MUST verify the actual resolved destination of each affected relationship through Obsidian.
It MUST NOT treat a resolved link as correct solely because its visible title matches the intended topic.
Duplicate names MUST trigger an explicit identity decision before an affected rename, merge, or retarget operation.
The workflow MUST preserve unrelated identities when resolving that decision.

#### Scenario: Two Miniature Painting notes divide the graph

- **WHEN** an Euthia project resolves Miniature Painting to a local hub and inventory notes resolve it to an Index topic
- **THEN** the audit reports the two exact destinations and the divided backlinks
- **AND** the proposal identifies the intended shared topic and a distinct role for the local hub
- **AND** no automatic merge occurs solely because both notes have the same filename

### Requirement: Respect the relationship rules of existing views

The workflow MUST inspect the selection rules of every affected Base view.
It MUST distinguish direct links, transitive relationships, property membership, and tag membership.
For a context-dependent view, it MUST verify the expected embedding context or report view validation as incomplete.
It MUST add a direct relationship when that relationship is meaningful and required for intended view membership.
It MUST NOT retag records or add unrelated links merely to force them into a view.

#### Scenario: A topic view requires a direct link

- **WHEN** a guide links to a project that links to Miniature Painting and the topic view selects direct incoming links
- **THEN** the audit does not claim that the guide appears in that topic view
- **AND** a direct topic link is proposed if the guide belongs in the topic

#### Scenario: A resource view accepts several note types

- **WHEN** a project resource view selects linked notes while excluding projects, events, and journals
- **THEN** guides and artwork retain their accurate note types
- **AND** the workflow does not require an additional resource tag solely to satisfy the view name

#### Scenario: A Base query uses a different context

- **WHEN** a Base filter depends on `this.file` and a standalone query uses a different context from the intended embed
- **THEN** the workflow does not use that result to establish embedded-view membership
- **AND** it verifies the intended context or reports that validation as incomplete

### Requirement: Preserve knowledge and links during authorized changes

An organization proposal MUST identify affected notes, destinations, role changes, relationship changes, and expected view membership.
When applied with authorization, it MUST preserve content, provenance, source assets, and dated work logs.
It MUST preserve existing references through supported link updates or unambiguous aliases where appropriate.
It MUST follow the target vault's review and logging standards and retain enough scoped evidence to reverse its own changes.
Reversal MUST preserve intervening user edits.

#### Scenario: A mixed hub becomes a project and a resource

- **WHEN** an authorized reorganization separates a mixed hub into project work and reusable knowledge
- **THEN** operational logs retain their dates in the owning project
- **AND** references and recipes retain their source evidence
- **AND** existing links resolve to the appropriate resulting note or section

#### Scenario: A folder-note plugin expands a successful rename

- **WHEN** a same-named folder note is renamed and an enabled plugin can rename its parent folder
- **THEN** preflight records the expected parent and sibling paths and checks the plugin's current behavior
- **AND** validation compares those paths immediately after the operation, regardless of the CLI exit status
- **AND** any unplanned parent or sibling move stops dependent operations until the paths are reconciled without automatic global settings changes

### Requirement: Clean metadata without losing meaning or view dependencies

The workflow MUST normalize affected frontmatter using the target vault's current conventions.
It MUST inspect field consumers before removing empty, obsolete, or apparently unused metadata.
It MUST preserve value types, meaningful false or unknown states, source uncertainty, and fields used by schemas or Base views.
It MUST NOT infer substantive review or painting completion from formatting or reference availability.

#### Scenario: Noisy artwork frontmatter drives a gallery

- **WHEN** artwork metadata contains an unused empty placeholder, a false painted flag, a category thumbnail, and unresolved attribution
- **THEN** cleanup removes the placeholder only after confirming it has no semantic or consumer dependency
- **AND** it preserves the category flag, thumbnail, attribution uncertainty, and their value types
- **AND** validation checks the affected gallery behavior separately from YAML formatting

### Requirement: Validate files and graph outcomes separately

The workflow MUST report separate results for saved content, resolved relationships, and affected application views.
It MUST verify intended link destinations, relevant backlinks, local assets, and expected Base membership after applied changes.
A successful file read MUST NOT establish graph correctness or visual correctness.
Validation MUST remain scoped to the authorized change and report unrelated defects separately.

#### Scenario: Content succeeds while a topic link is wrong

- **WHEN** Obsidian reads an edited guide correctly but its topic link resolves to the wrong same-named note
- **THEN** content validation passes and relationship validation fails
- **AND** the workflow does not report the organization change as fully validated

### Requirement: Report unavailable application evidence without unsafe fallback

When Obsidian CLI evidence is unavailable, the workflow MUST identify the failed validation layer and preserve completed discovery work.
It MUST NOT present filesystem observations as application verification.
It MUST NOT invoke the Obsidian GUI executable as a replacement CLI launcher.
It MUST follow existing authorization rules for any requested GUI inspection.

#### Scenario: The dedicated CLI cannot read the vault

- **WHEN** the supported CLI fails during a scoped graph audit
- **THEN** the workflow reports that application discovery or validation remains unavailable
- **AND** it does not infer missing notes or correct links from the failed call
