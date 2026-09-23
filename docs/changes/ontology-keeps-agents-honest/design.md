# Design: Declared World

This document explains the vocabulary, the decisions, and the wiring. It is also the primer for contributors who have not used RDF before.

## The five terms

- **Triple.** One fact: subject, predicate, object. `DECK-0010 — replaces — DECK-0002`. Frontmatter is triples in YAML clothing.
- **Ontology** (`ontology/rune.ttl`). The dictionary of kinds: which classes exist and how they relate. It describes. It never rejects data.
- **Shapes** (`ontology/shapes.ttl`). The checkable rules, written in SHACL. A shape violation is a deterministic failure. This is the check that rejects data.
- **IRI and namespace.** Every term and every entity gets one globally unique name that looks like a URL. Prefixes such as `rune:` and `prov:` abbreviate them.
- **Open versus closed world.** OWL and RDFS assume unknown facts may exist, so they infer and never fail. SHACL assumes the graph is complete, so it validates. Agents propose triples. Shapes decide.

## Namespaces

| Prefix | Base | Holds | Lives in |
|---|---|---|---|
| `rune:` | `https://runedeck.dev/ns#` | product vocabulary and shapes | deck, later skeleton |
| `n4m3z:` | `https://martinzeman.net/ns#` | the owner's personal vocabulary | the private consumer repository |

Entities get IRIs under `/id/`, separate from terms under `/ns#`. Example: `https://runedeck.dev/id/DECK-0010`. The personal graph imports the product graph. The product graph never imports the personal graph. This mirrors the provider-independence contract: the product ships with no knowledge of its owner.

## Identity

The record identifier is the identity. The extractor mints the entity IRI from the identifier. The file path plays no part in the IRI. Two files that claim one identifier merge into one node in the graph. The shape on `dcterms:title` then reports two titles on one node. The duplicate detection falls out of the identity decision, and no counting code exists.

## Severity ratchet

New shapes start at `sh:Warning`. A recorded follow-up moves a shape to `sh:Violation` when the existing corpus conforms. Two shapes still wait:

- The rule-verdict shape waits until existing rules carry verdicts.
- The references-resolve shape waits until the extractor lands and every related entry resolves.

## The ladder of checks

Validation runs as early as possible and blocks as late as necessary:

0. **Command policy.** dcg evaluates every agent shell command before execution, across harnesses. The repository ships `.dcg/packs/toolpolicy.yaml`, which redirects `grep` to `rg` and `find` to `fd` with the replacement named in the denial. The destructive-command packs come from dcg core.
1. **Harness hook.** A PostToolUse hook lints a Markdown file the moment an agent writes it. The agent repairs immediately.
2. **`jj fix`.** The auto-fixers (rumdl, typos) rewrite changed files in revisions.
3. **Gated `jj push`.** prek runs every blocking hook before the push leaves the machine.
4. **CI.** The same prek configuration re-runs as the last defense. CI defines nothing that does not also run locally.

jj has no hook system by design. The gated push alias is the jj-native blocking point.

## Tool stack

| Tool | Language | Checks |
|---|---|---|
| rumdl | Rust | Markdown structure |
| typos | Rust | spelling |
| Vale | Go | Simplified Technical English style plus the Deslop package for machine-writing tells |
| lychee | Rust | links and fragments, offline |
| actionlint | Go | workflow schema |
| zizmor | Rust | workflow security |
| rudof | Rust | SHACL validation, once the extractor lands |

Every tool is a single binary. No Java. No Python runs in a blocking hook. All hooks skip when the binary is absent, so a fresh clone stays installable.

## Spec layout

`docs/` already matches the openspec directory contract: `docs/changes/` holds change directories and `docs/specs/` holds capability specifications. The openspec CLI hard-codes the `openspec/` directory name, so the dotfiles wrapper keeps one symlink per repository under `~/.openspec/<org>/<repo>` that points at `docs/`. The repository carries no extra entry, and `openspec validate --strict` becomes a usable blocking check.

## Portability

Every blocking check runs locally. GitHub Actions re-run prek as the last defense. Only actionlint, zizmor, and the review bot's workflow jobs are GitHub-specific. A GitLab migration rewrites the CI shims and keeps every local check unchanged.

## The first-generation survey

The first-generation repositories carry the earlier concept model. Their survey on 2026-08-26 shaped the class model:

- The taxonomy says "kind", never "ontology", because the first generation spent that word on filesystem roots.
- `rune:Rune` is the umbrella class the first generation lacked. Its absence forced a closed kind enum through the whole codebase.
- Canon, Sidecar, Companion, Template, Variant, and StructureSchema become classes, because the first generation proved each is load-bearing.
- Provider and Target are separate classes. The first generation conflated them.
- Derivation reuses PROV-O. Integrity is two digests. Drift states are queries over the digests, never stored facts, exactly as the first generation derives them.

## Open questions

- The `related:` frontmatter entries are strings today. A migration to relative links would let lychee check them and would simplify the extractor.
- The sidecar-never-duplicates-canon invariant becomes a shape once the extractor emits canon and sidecar fields.

## Commands

A requirement names a role. This table names the command, path, or namespace behind each row, so nothing is lost when one moves out of a requirement.

| Requirement | Command | Notes |
|---|---|---|
| Description and Validation Separate | `ontology/rune.ttl` | The ontology file. It describes kinds and relations only. |
| Description and Validation Separate | `ontology/shapes.ttl` | The SHACL shapes file. Every pass-or-fail check comes from it. |
| Identifier Is Identity | `https://runedeck.dev/id/` | The project identifier namespace. The extractor mints every entity IRI under it. |
