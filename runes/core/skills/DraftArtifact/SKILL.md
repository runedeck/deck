---
name: DraftArtifact
description: Start a new skill, agent, or rule as a draft that the harness loads now and the deck adopts later. USE WHEN draft a skill, try a skill before adding it, new rule idea, prototype an agent, rune draft, promote a draft, list drafts, stale draft in doctor. NOT FOR editing a rune that is already in the deck, adopting a third-party artifact, or the full authoring workflow (BuildSkill covers that).
metadata:
    version: 0.1.0
---

# DraftArtifact

A draft is a rune that lives in the consumer's provider directories before it lives in the deck. The harness loads it at once, `.manifest` never lists it, and `.drafts` at the consumer root records it. When the draft proves itself, `rune promote` moves it into the deck and opens its change. When it does not, `rune draft --drop` removes every copy.

## Prerequisites

- A consumer with at least one deployed provider directory (`rune install` has run, so `.claude/.manifest` or a sibling exists).
- The rune CLI with the `draft` and `promote` commands (`rune --help` lists them under Deck).
- For `rune promote`: the consumer's `.rune` names a local deck, or you pass `--deck <DIR>`.

## Constraints

- Never write a draft by hand into a provider directory. A file that `.drafts` does not know is an orphan, and `rune repair` quarantines orphans.
- Never edit `.manifest` or `.provenance/` to make room for a draft. The draft stays outside both until promotion.
- One name means one kind. `rune draft rule Foo` refuses when `Foo` is already a skill draft.
- A draft is local: `rune init` ignores `.drafts` and the provider directories in `.gitignore`. Do not commit them.
- A promoted rune enters the deck's normal lifecycle. The change stub that promote writes is a start, not an acceptance.

## Instructions

### Start a draft

1. Run `rune draft <kind> <name>` at the consumer root. `kind` is `skill`, `agent`, or `rule`. The name is one identifier, PascalCase for a skill or agent.
2. Open the file it printed for the provider you work in, for example `.claude/skills/<name>/SKILL.md`, and write the rune there. Keep the frontmatter `name` equal to the draft name.
3. Use the rune in the harness. A skill draft is invocable at once. A rule draft applies on the next session.
4. Copy the body to the other provider copies only when you need them. Promote takes the first registered copy.

### Check the drafts

Run `rune draft --list` for name, kind, age in days, and path. `rune doctor` shows the same block under `drafts` and never reports a registered draft as an orphan. A line marked `stale` means the file is gone. `rune doctor --verify` exits 1 until you run `rune draft --drop <name>` or restore the file.

### Promote or drop

When the draft earned its place, run:

```sh
rune promote <name> --domain <domain> --change <three-word-id>
```

The change id needs at least three lowercase hyphenated words. Promote copies the rune into `runes/<domain>/`, creates `docs/changes/<id>/` with a proposal that names the rune, then removes every provider copy and the `.drafts` entries. Continue in the deck with BuildSkill for the rune body, and with the change's `proposal.md`, `tasks.md`, and `adr.md` for the record.

When the draft did not earn its place, run `rune draft --drop <name>`.

## Verification

- `rune draft --list` shows the draft with the expected kind, or `no drafts` after promotion or drop.
- `rune doctor --target . --verify` exits 0 with no orphan for the draft path.
- After promotion, `runes/<domain>/<kind>/<name>` exists in the deck and `rune validate` passes there.

## Troubleshooting

- `no deployed provider directory`: run `rune install` first. Draft writes only where a `.manifest` exists.
- `is a managed rune in .manifest`: the deck already deploys that name. Edit the deck rune instead, or pick another name.
- `already exists; drop it or pick another name`: a hand-written file sits at the draft path. Move it aside, or use it as the draft body after `rune draft` creates the entry.
- `doctor.drafts_unreadable`: `.drafts` has an entry that is not a confined relative path or a plain name. Fix the file by hand, then run `rune doctor` again.
- Promote refuses with `already exists`: the change directory or the deck rune exists. Pick another change id, or remove the stale target in the deck.
