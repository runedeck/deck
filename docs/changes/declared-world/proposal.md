---
adr: "docs/decisions/DECK-0010 Declared World in RDF.md"
status: proposed
---

# Declared World

## Why

See the linked ADR for the decision rationale. This proposal records the change in scope.

Agents propose artifacts. The deck needs a deterministic layer that decides what is permitted. Established tools and vocabularies replace the custom checker draft.

## What Changes

- `ontology/rune.ttl` declares the deck's artifact kinds in Turtle. It reuses PROV-O, Dublin Core, and schema.org, and mints three terms: `rune:DecisionRecord`, `rune:Rule`, `rune:Verdict`.
- `ontology/shapes.ttl` carries three SHACL shapes: unique record identifiers, resolvable references, and a verdict pointer on every rule.
- The prek configuration gains six guarded hooks: rumdl, typos, Vale, lychee, actionlint, and zizmor. Each hook skips when its binary is absent.
- An `STE` Vale style encodes the first Simplified Technical English rules as declarative data.
- The graph extractor becomes a `rune` subcommand in the cli repository. That work is a separate change. Until it lands, the shapes are reviewed artifacts without a runtime gate.

## Capabilities

- declared-world (new)

## Impact

- `ontology/` (new): `rune.ttl`, `shapes.ttl`.
- `.pre-commit-config.yaml`: six new hooks.
- `.vale.ini`, `.vale/styles/STE/` (new), `.rumdl.toml` (new).
- `docs/decisions/`: DECK-0010.
- The cli repository receives a follow-up change for `rune ontology export`.
- The skeleton receives the configuration files through a follow-up change after one week of deck use.
