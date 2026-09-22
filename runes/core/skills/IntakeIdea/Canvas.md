# Canvas

An idea can arrive as a link to a drawing in the owner's Obsidian vault. The drawing is the origin of the change and of its decision record, and it stays in the vault. This page says how to read it, what its parts mean, and what the change keeps.

## Read the drawing

1. Take the link as given: `obsidian://open?vault=Atlas&file=Library%2FCanvas%2FMarkdown%20First`. The `vault` and `file` values name the source. A `vault.martinzeman.net` URL names the same file once the vault is published.
2. Read the file through the Obsidian CLI, never by path on disk: `obsidian vault=Atlas read path="Library/Canvas/Markdown First.md"`. The CLI answers only when Obsidian runs, which is the owner's signal that the vault is live.
3. The `## Text Elements` section lists every text in the drawing, in the order it was written. Read it first. It is the whole content when the drawing is cards and labels.
4. Connections and frames are in the drawing JSON, which the plugin stores compressed. Run `obsidian vault=Atlas command id=obsidian-excalidraw-plugin:decompress-current-excalidraw-file` with the file open, or read the `.svg` the plugin writes beside the file for the text and positions. An arrow's `startBinding` and `endBinding` name the elements it joins.

## What the parts mean

The owner draws with the origin on the left and the result on the right. Read every arrow that way.

- The largest text, or the title: the sharpened intent, first line of Why.
- A frame, or a group of cards under one heading: one considered option.
- A loose card: one decision driver, or one requirement when it states a MUST.
- An arrow A → B: B came from A. `B` lists `A` in `upstream`, or the proposal's Why states it.
- A card with a record id or a capability name: a link to that node, never a new node.
- A question mark, a red card, or crossed text: an open question, a task, never a requirement.

A drawing with no arrows is a list. Ask the owner which card is the intent before you write anything.

## What the change keeps

1. The record's `upstream` lists the `obsidian://` link first. The record's origin is the drawing.
2. `scripts/sync-idea "<link>"` writes the snapshot `docs/ideas/<name>.md` and its sidecar `docs/ideas/.provenance/<name>.md.yaml`, which records the link and the sha256 of the bytes the CLI returned. The repository is then complete without the vault, and `scripts/sync-idea --check` says when the vault moved on.
3. Do not edit the snapshot. Edit the drawing in Obsidian and run the sync again.
4. Do not write on the drawing's markdown side. The owner keeps that side empty, and the frontmatter is the plugin's.

## Verification

- `scripts/sync-idea --check` passes for the new snapshot.
- `scripts/check-decision-shape` accepts the record's `upstream` link.
- Every arrow on the drawing is one origin edge in the proposal or the record, read origin to result.
