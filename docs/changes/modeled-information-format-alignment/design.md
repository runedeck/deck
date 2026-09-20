# MIF Alignment Design

## Approach

Align vocabularies, adopt instances, keep machinery. The deck reuses MIF terms where they fit, trials MIF-native instances where the deck has a declared gap, and keeps its own validation machinery. The alternative (wholesale adoption of the MIF stack) couples the deck to a pre-1.0 upstream and swaps a working closed-world check for an open-world model.

## Evidence

- The organization publishes MIT-licensed repositories with recent activity: the MIF specification at v1.0.0, the Rust workspace at v0.9.0, the ontology corpus with a fail-closed sha-vendoring index, and the mnemonic memory plugin at MIF Level 3.
- MIF declares markdown canonical and JSON-LD a derived, regenerable projection. Provenance aligns with W3C PROV.
- Structured MADR lives under the same organization and is already the runeADR upstream.
- The deck's Established Vocabularies First requirement mandates reuse before minting.

## Structure

- Vocabulary: `ontology/rune.ttl` records a mapping per term: reused from the MIF corpus, or minted with the reason no MIF term fits.
- Memory: the MIF memory profile (mnemonic) is the named trial instance for advisory memory in the pushback stage. A recorded verdict decides adoption.
- Documentation skills: the mif-docs ADR skill gets an evaluation against the planned deck ADR skill before any authoring.
- Distribution: the attested marketplace's sha-pinned, fail-closed patterns enter as study input for rune distribution.
- Validation: SHACL shapes over the extracted graph stay the deterministic check. JSON-LD stays a projection and never decides a pass or a fail.

## Risks

- The upstream is young and single-organization. Guard: every component enters through the adoption review with provenance and a maturity note, and machinery takes no pre-1.0 dependency.
- Open-world JSON-LD semantics could leak into the pass-or-fail decision. Guard: the shapes requirement pins SHACL as the only pass-or-fail authority.
- Two ontology corpora can drift. Guard: the mapping lives in the ontology with a source citation per reused term, and the graph validation reports a broken reference.
- MIF carries provenance in frontmatter, and the deck seals provenance in digest-bound sidecars. Guard: the two stay separate jobs, description in frontmatter and evidence in sidecars, and no adoption merges them.
- MIF commits markdown beside its JSON-LD projection, which doubles each fact. Guard: a projection is acceptable only with an enforced drift check that proves it regenerates from the source.
- The OKF envelope requires a `type` field on every file, and deck rules stay frontmatter-free by design. Guard: the deck aligns vocabulary, never claims envelope conformance for rules.
