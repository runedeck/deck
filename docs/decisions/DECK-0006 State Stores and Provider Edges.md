---
title: State Stores and Provider Edges
description: Four stores with strict content contracts hold every artifact state, and provider specifics enter only at the Ship and Operate edges
type: adr
category: architecture
tags:
    - architecture
    - state
    - providers
status: accepted
created: 2026-08-19
updated: 2026-10-19
author: "@N4M3Z"
project: deck
related:
    - "DECK-0005 Artifact Lifecycle and Evidence Tokens"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: []
informed: []
upstream: []
change: lifecycle-stages-and-evidence
---

# State Stores and Provider Edges

## Context and Problem Statement

*[Artifact][ARTIFACT]* state is in four places. The first is the workshop directories under `~/Agents/<owner>/<project>`. The second is the *[repositories][REPOSITORY]* that contain the *[decks][DECK]*. The third is the consumer checkout with its manifest and rendered private prompts. The fourth is the provider accounts.
Nothing states what each place may contain, so content leaks across the boundaries. An author edits canonical text in a provider tree. A personal value almost reaches a [repository][REPOSITORY]. A provider account accumulates configuration that nobody can rebuild. Providers also differ in what they accept, and every difference tempts a fork of the canonical [artifact][ARTIFACT].

## Decision Drivers

- A fresh machine must be able to rebuild every store below the workshop from the [repositories][REPOSITORY] alone.
- Personal values and rendered prompts must never enter a [repository][REPOSITORY].
- A canonical [artifact][ARTIFACT] must stay provider-independent. Otherwise every provider change multiplies across the [deck][DECK].
- The environment matrix (DECK-0004) already bounds provider sessions by data sensitivity. The store contract must compose with it.

## Considered Options

1. **One store**: everything is in the [repository][REPOSITORY], and providers read it directly.
2. **Free placement**: any state anywhere, conventions only.
3. **Four stores with content contracts and two provider edges**: each store has a MUST list and a MUST NOT list. A provider plugs in at the Ship stage and the Operate stage only.

## Decision Outcome

Option 3. The workshop holds anything, and nothing installs from it. The [repository][REPOSITORY] contains only reviewed, proven, schema-valid [artifacts][ARTIFACT] and their *[sidecars][SIDECAR]*. It never contains a review transcript or a personal value.
The consumer contains the manifest, the deploy manifests, and the rendered private prompts. It never contains canonical content. The provider account contains only configuration rendered from the deployed *[templates][TEMPLATE]*, and it MUST stay reproducible from the [repository][REPOSITORY] plus the consumer.
A provider enters at two edges. On the Ship side it enters through *[assembly][ASSEMBLY]* configuration (`targets`, keep-fields, casing rules, overlays). On the Operate side it enters through adapted *[routine][ROUTINE]* *[variants][VARIANT]* under the DECK-0004 matrix. Canonical frontmatter has the Agent Skills fields plus the three [assembly][ASSEMBLY] directives. It has no other field.

### Consequences

- [+] Removing a provider changes no canonical [artifact][ARTIFACT]. Adding one needs a provider configuration, optional overlays, and [routine][ROUTINE] [variants][VARIANT].
- [+] Reproducibility becomes testable: the owner rebuilds a provider account from the [templates][TEMPLATE] and compares.
- [+] The store contracts give the audit [routines][ROUTINE] concrete assertions. Canonical content outside the [repository][REPOSITORY] is a violation, and so is a personal value inside it. Neither is a judgment call.
- [+] The workshop stays the one place with no content contract, so capture stays cheap.

## More Information

- Rewritten on 2026-10-19 in the plain spoken register. The decision is unchanged.

[REPOSITORY]: ../specs/glossary/repository.md
[DECK]: ../specs/glossary/deck.md
[ARTIFACT]: ../specs/glossary/artifact.md
[SIDECAR]: ../specs/glossary/sidecar.md
[TEMPLATE]: ../specs/glossary/template.md
[ROUTINE]: ../specs/glossary/routine.md
[VARIANT]: ../specs/glossary/variant.md
[ASSEMBLY]: ../specs/glossary/assembly.md
