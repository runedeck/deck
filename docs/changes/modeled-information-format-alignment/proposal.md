---
adr: docs/changes/modeled-information-format-alignment/adr.md
status: proposed
decisions: ["Align with the Modeled Information Format under scoped adoption"]
---

# Modeled Information Format alignment

## Why

The Modeled Information Format organization builds on the same choices the deck made: markdown as the canonical form, W3C PROV for provenance, sha-pinned fail-closed distribution, and Rust tooling. Established Vocabularies First requires the deck to reuse a fitting vocabulary before minting a term, and the MIF ontology corpus is such a vocabulary. The upstream is young, so adoption stays scoped, and each step needs a recorded verdict.

## What Changes

- The deck ontology maps its terms to the MIF ontology corpus and mints a term only where none fits.
- The MIF memory profile becomes the trial instance for advisory memory, against a recorded verdict.
- The mif-docs ADR skill gets an evaluation before the deck authors its own.
- The attested marketplace patterns enter as study input for rune distribution.
- Machinery keeps its ground: SHACL shapes stay the check that decides, and the deck takes no dependency on a pre-1.0 implementation.

## Capabilities

- modeled-information-format-alignment (new)

## Impact

- `ontology/`, the advisory-memory wiring in the agent pipeline, the planned ADR skill, `docs/changes/modeled-information-format-alignment/`.
