# Design: The Rune Stack

This document names the layers of the rune stack, the contracts between them, and the places where today's tooling diverges from the abstraction. It is a thinking artifact. It changes no behavior.

## The three planes

The stack separates into three planes:

- The **flow plane** moves an artifact through seven stages: Capture, Author, Prove, Measure, Review, Ship, Operate.
- The **governance plane** defines the contracts the flow plane obeys: specifications, decision records, and the ceremony that enforces them.
- The **state plane** names the four stores an artifact may inhabit and the rules for each.

The key structural claim: governance artifacts are themselves flow-plane artifacts. The ceremony ships from the skeleton to consumer repositories exactly as a rune ships from the deck to a provider tree. The live drift report (deck issue #45) shows what happens when the governance plane skips its own Ship stage: the label grammar split and the Copier pin lag are shipping failures, not authoring failures.

## The flow plane

Each stage has one input contract, one output contract, and one evidence token. An artifact advances only by acquiring the stage's token. The token travels with the artifact.

| Stage | Instance today | Input contract | Evidence token |
|---|---|---|---|
| Capture | LearnFrom, CaptureOnTouch, workshop ledgers | none — anything enters | a dated note with owner and source context |
| Author | BuildSkill, BuildRule, BuildAgent, BuildTask | a captured note or an upstream import | a schema-valid artifact (mdschema + kind schema) |
| Prove | authorship ceremony, rune adopt + sidecars | a schema-valid artifact | first-party: a listed author identity. Third-party: a sealed block-review record and an in-toto sidecar |
| Measure | BenchArtifact, bench driver, DECK-0001..0003 | a proven artifact and a bench manifest | a three-metric verdict per model |
| Review | seer lanes, ceremony checks, owner merge | a pushed branch | an exact-head clean verdict and a merge commit |
| Ship | rune install from the consumer manifest | a merged artifact selected by a manifest | a deploy-manifest entry with a digest |
| Operate | provider routines, doctor, drift, audits | an installed artifact | routine coverage: audit comments and drift reports |

Three rules bind the table:

1. A stage MUST NOT consume an artifact that lacks the previous stage's token. Today several hops are manual and unenforced. The gap register below lists them.
2. Evidence is append-only. Retirement removes an artifact, never its evidence.
3. Operate feeds Capture. A drift report, a bench regression, or an audit finding is a captured note, and the loop closes.

### The leverage ladder selects the stage

When a problem repeats, the workshop ladder (eliminate through architecture, then lint, then skill or rule, then human review) is a stage selector. Architecture fixes land in Author. Lints land in Review as ceremony checks. Rules land in Author and pay rent through Measure. Human review is the Review stage's floor, not its ceiling. The ladder gives one answer to "which layer owns this fix."

## The governance plane

The governance plane has two artifact kinds and one enforcement loop:

- **Specifications** (`docs/changes/`, `docs/specs/`, OpenSpec-compatible) define capability behavior with MUST requirements. The `spec/presence` check with its `ignore:spec` waiver enforces that machinery changes carry them.
- **Decision records** (`docs/decisions/`, `DECK-NNNN` and `RUNE-NNNN`) record why a contract has its shape.
- **Ceremony** (workflows, hooks, labels, `authors.yaml`) enforces both. Its source of truth is the skeleton, and consumers receive it through Copier updates.

The governance plane MUST obey its own flow: a ceremony change is authored in the skeleton (both the repository root and `templates/base/`), reviewed there, and shipped to consumers through `copier update` — never hand-copied. Drift between skeleton and consumers is an Operate-stage signal that MUST be watched by an audit routine, which issue #45 already instantiates.

## The state plane

| Store | Path pattern | May hold | MUST NOT hold |
|---|---|---|---|
| Workshop | `~/Agents/<owner>/<project>` | anything: ledgers, briefs, captures, reference copies | anything a consumer installs from |
| Deck | `runedeck/deck` and sibling repos | reviewed, proven, schema-valid artifacts and their sidecars | rendered personal values, and review transcripts (DECK-0002 Temporary Adoption State) |
| Consumer | `~/Agents/runedeck` (`.rune`, `private/`) | the manifest, rendered private prompts, deploy manifests | canonical artifact content |
| Provider account | Claude, Codex, ChatGPT, Gemini surfaces | routine configuration installed from templates | unique state — an account MUST be reproducible from the deck and the consumer |

Promotion between stores follows the flow plane. Workshop content enters the deck only through Author and Prove. Deck content reaches a consumer only through Review and Ship. Provider accounts receive only rendered instances of shipped templates.

## The provider edge

Providers plug in at exactly two edges, and nowhere else:

1. **Ship-side**: assembly transforms driven by provider configuration — `targets` routing, keep-fields, casing rules, plugin layout, qualifier overlays. The canonical artifact carries Agent Skills fields plus three assembly directives (`targets`, `disable-model-invocation`, `user-invocable`). Everything else a provider needs arrives from provider data during assembly.
2. **Operate-side**: routines and environments per provider capability, assigned by data sensitivity (DECK-0004). Providers get adapted variants, not copies, and each variant records its trust model in its header.

The provider-independence contract: deleting a provider MUST require zero edits to canonical artifacts. Adding a provider MUST require only a provider configuration, optional overlays, and routine variants.

## Retirement

Retirement is the reverse path, defined per store:

- **Provider account**: remove the rendered routines and configuration. Manual today.
- **Consumer**: remove the manifest entry. Then `rune clean` and prune remove the deployed files the deploy manifest tracks.
- **Deck**: remove the artifact and its sidecar in a reviewed change. The change records the reason. Evidence records (bench verdicts, review history, decision records) stay.
- **Workshop**: the ledger captures the retirement decision, closing the loop.

The live case is the first first-party module teardown, which also sets a principle: provenance sidecars exist to import trust across an ownership boundary. First-party artifacts carry their trust in the authorship ceremony, so removing their sidecars is a correction, not a loss.

## Gap register

Reality diverges from this abstraction in the following places. This change records them and fixes none of them.

1. **Ceremony shipping lag.** The deck's Copier pin trails the skeleton by 24 `templates/base` commits. The label grammar split the fleet: `spec:none` in the consumers against `ignore:spec` in the skeleton, until the deck adopted `ignore:spec` by hand while this change was in review. That hand-carry proves the seam rather than closing it: the governance plane's Ship stage is manual, and each consumer converges only when someone notices.
2. **No canonical evidence slot for bench verdicts.** Verdicts live in workspace benchmark directories. The Measure token does not travel with the artifact. Seam: sidecars or artifact metadata have no verdict pointer.
3. **Review evidence is platform-bound.** Exact-head verdicts and sealed rounds live in GitHub. Nothing exports them beside the artifact.
4. **Unenforced hops.** Nothing blocks a rule from shipping without a bench verdict, or an adopted artifact from merging without a sealed record. The tokens exist, and the gates do not.
5. **No retirement command.** Deck removal, consumer manifest cleanup, and provider teardown are three manual acts with no shared transaction.
6. **Provider routine install is manual by nature.** Provider UIs accept pasted prompts. The CLI can render and verify, but it cannot install. This is an accepted edge, not a fixable seam.
7. **Decision-record numbering collides.** Two DECK-0002 records exist on the deck's default branch. The numbering has no reservation mechanism across parallel changes.
8. **Workshop capture is convention-only.** CaptureOnTouch is a rule, and nothing measures whether capture happens. The Operate-to-Capture feedback loop has no coverage signal.
