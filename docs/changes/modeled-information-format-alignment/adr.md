---
title: "Align with the Modeled Information Format under scoped adoption"
description: "The deck maps its ontology terms to the Modeled Information Format corpus and trials its parts one at a time, and takes no dependency on a pre-1.0 implementation."
type: adr
category: architecture
tags:
    - runedeck
    - ontology
    - vocabulary
status: proposed
created: 2026-09-20
updated: 2026-09-20
author: "@N4M3Z"
project: deck
related:
    - "DECK-0010 Declared World in RDF"
    - "DECK-0014 Vocabulary Governance"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5-1"]
informed: []
upstream:
    - "https://github.com/modeled-information-format"
change: modeled-information-format-alignment
---

# Align with the Modeled Information Format under scoped adoption

## Context and Problem Statement

The Modeled Information Format organization made the same base choices as the deck: Markdown as the canonical form, W3C PROV for provenance, distribution pinned by digest, and Rust tooling. The deck's vocabulary rule says to reuse a fitting vocabulary before it mints a term. The upstream is young, so a wholesale dependency is a risk.

## Considered Options

1. Ignore the upstream and keep the deck's own terms.
2. Depend on the upstream implementation now.
3. Map terms to the upstream corpus and trial its parts one at a time, each with a recorded verdict.

## Decision Outcome

Option 3. The deck MUST map an ontology term to the upstream corpus before it mints a new one. Each adopted part MUST carry a recorded verdict and a maturity note. The SHACL shapes MUST stay the check that decides, and the deck MUST NOT depend on an upstream implementation below version 1.0.

## Consequences

- The deck gains a shared vocabulary without a runtime dependency.
- Each trial costs an evaluation and a written verdict before anything is adopted.
- The upstream can change its terms. A mapping then needs a repair, and the verdict for that term is void until it is repeated.
