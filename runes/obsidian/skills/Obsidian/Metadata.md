# Metadata

Read this when cleaning frontmatter or changing a note's role.
Make metadata easier to read without removing meaning or view dependencies.

## Establish the field contract

Read current vault rules, schema checks, representative notes, and affected Base filters.
Inspect both property names and value types through Obsidian CLI.
Do not copy retired tags or unused template fields simply because a template contains them.

For each field, classify its purpose:

- Identity: title and useful unambiguous aliases.
- Lifecycle: created, updated, review, and actual project or item status.
- Role: current type and note tags.
- Relationships: topic, project, resource, collection, and source links.
- Evidence: attribution, inspected asset categories, uncertainty, and source provenance.
- Presentation: image or display fields used by the current gallery.
- Unused: empty placeholders or obsolete fields with no remaining semantic or consumer dependency.

## Normalize only the authorized records

Use the vault's accepted field order, indentation, quoting, and list style consistently.
Preserve YAML scalar types and quote wikilinks where required for valid YAML.
Remove empty or unneeded fields only after checking relevant schema, templates, Bases, and known consumers.
An empty string, `null`, `false`, and an absent field can have different meanings.
Keep required empty fields and fields whose emptiness records a meaningful state.

Do not remove a false category flag because it seems visually noisy.
Do not remove an unresolved creator or source field when it preserves known uncertainty.
Do not add a completion status because a guide exists or a reference was found.
Preserve created dates and use the actual work date for updates under the vault's rules.
Keep reviewed status accurate. A formatting change does not imply substantive review.

## Verify the cleanup

Show removed and changed fields in the diff with their reasons.
Parse the resulting YAML and compare meaningful property values before and after.
Read the saved properties through Obsidian.
Check affected view membership and thumbnails after any dependent field changes.
Report cosmetic normalization separately from corrected semantic metadata.
