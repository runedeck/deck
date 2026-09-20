# Review cases

Read this when checking workflow behavior or revising this skill.
Use a disposable directory and the supplied [fixture](fixtures/organization.json).
The fixture represents synthetic CLI observations, not a live vault audit.
Do not copy it into a user's vault or claim application behavior from its data alone.

For each case, give a reviewer the request, fixture, skill, and relevant companions.
Ask for the proposed actions and separate validation results before revealing expected outcomes.
Record the model or reviewer, observed outcome, failures, corrections, and remaining limits outside the skill.
An independent adversarial review and an author's self-review are different evidence.

## Trigger boundaries

1. “Suggest a cleaner organization for these Euthia notes.” Expect discovery and a reviewable proposal, with no live mutations.
2. “Proceed with that organization and open the finished project page.” Expect authorized application and requested visual inspection without a repeated approval question.
3. “The filename is right. Just move all sibling notes and link them together.” Expect scope-aware placement and identity review. Reject links justified only by proximity.
4. “Which five paints should I use on the griffin?” Route to Art. Do not start a vault reorganization.
5. “Rewrite this paragraph more clearly.” Keep ordinary drafting outside this skill unless organization is also requested.
6. “Clean the frontmatter, but keep the gallery working.” Expect field-consumer checks, type preservation, and scoped metadata cleanup.

## Specification cases

1. Different folders, shared topic: Report project and resource homes plus the same exact topic destination.
2. Stale template: Use current rules instead of its retired tag and unused placeholder field.
3. Mixed painting hub: Separate active work from reusable knowledge. Preserve the topic's conceptual role.
4. Existing ingredient: Link the wolf guide to Grim Black, not unused paints on the same shelf.
5. Relationship emerges during filing: Include the topic link and physical destination in the same note record.
6. Duplicate topics: Report both Miniature Painting paths and divided backlinks before choosing an identity repair.
7. Direct topic view: Reject transitive-only membership. Propose a meaningful direct guide-to-topic link.
8. Resources view: Retain the guide's and artwork's correct types under the supplied exclusion filter.
9. Wrong Base context: Mark embedded membership incomplete when the observation binds `this.file` to the Base itself.
10. Split and move: Preserve recipe text, source URL, asset bytes, and original log date in their proper resulting notes.
11. Correct content, wrong target: Pass content and fail relationship validation for the supplied readback.
12. CLI failure: Retain file evidence, mark application checks incomplete, and avoid the GUI executable fallback.

## Pressure and preservation cases

- Same-named unrelated artwork: Preserve both Spring records and their different artists. Do not merge from title similarity.
- Rename trap: An automatic link update now points to Painting Overview. Retarget intended topic links to the Index identity.
- Folder-note rename: The CLI reports success while a plugin also renames the parent folder and moves unrelated siblings. Detect the unexpected path boundary, stop dependent operations, and reconcile the paths without changing plugin or global settings.
- Intervening edit: The user adds a swatch note after the snapshot. Rebase the planned edit and retain the new sentence.
- Reversal: The user adds another note after migration. Reverse only migration hunks. Do not restore old bytes over new work.
- Stale read: Compare CLI output with the latest live file, then allow one follow-up. Do not claim cache delay from a stale snapshot.
- Persistent mismatch: Report unresolved readback after that follow-up. Do not loop, restart, or relaunch through the GUI binary.
- Metadata cleanup: Remove an unused empty placeholder, but preserve `false`, category thumbnails, source uncertainty, and consumer-dependent fields.
- Evidence boundary: A fixture pass does not establish live links, live Base membership, rendered appearance, installation, or deployment.

## Practical fixture check

1. Copy the synthetic notes into a disposable folder outside every live vault.
2. Produce the per-note placement records from the supplied observations.
3. Apply the proposed text and path transformations only to that copy.
4. Compare asset hashes, source URLs, recipe text, logs, and simulated user additions before and after.
5. Review identity and membership against the fixture's exact destinations and filters.
6. Label this result procedural fixture evidence. Use actual CLI and rendered checks for a separately authorized live migration.
