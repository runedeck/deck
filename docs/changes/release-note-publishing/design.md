# Release Note Publishing Design

## Approach

Use curated pull request notes as the structured source. Compile them into a GitHub Release draft for owner review.

The delta specification owns observable behavior. This design owns component boundaries and rejected alternatives.

Per-pull-request fragment files would duplicate the existing notes. GitHub generated notes would replace curated notes with titles and labels.

A maintained shared changelog would retain the merge-conflict source. These alternatives do not fit the current pull request contract.

## Structure

- The release-note compiler selects pull requests and renders their note lists.
- The release workflow gives the compiler a release boundary and manages one draft.
- The changelog ownership check is the only new repository gate.
- The Skeleton owns the ceremony source. Copier delivers the ceremony to Deck.
- The owner decisions in `tasks.md` set the remaining policy inputs.

## Risks

- A pull request body can change after merge. The owner must select one body snapshot policy.
- An incomplete API result can omit notes. The compiler validates the full interval before it changes a draft.
- A repeated run can duplicate entries. The compiler uses stable pull request links as entry keys.
- The first release can lose old history. The migration imports the current changelog and records its cutover commit.
- A Deck-only ceremony change can drift. Skeleton implementation and Copier delivery keep one ceremony source.
