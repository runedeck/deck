---
type: proof
change: plain-text-first-principles
recorded: 2026-09-25
transcript: bc725f5149592054951e2da87563e6f8be85f4480dd671f23959f2ea100d39b0
scenes:
  - scenario: plain-text-is-futureproof#plain-text-representation/database-is-rebuilt-from-plain-text
    kind: unproven
  - scenario: plain-text-is-futureproof#binary-assets-carry-a-description/binary-asset-enters-the-repository
    kind: check
  - scenario: plain-text-is-futureproof#lossless-renders/render-drifts-from-its-state-file
    kind: unproven
  - scenario: markdown-with-yaml-frontmatter#markdown-system-language/instruction-arrives-in-another-format
    kind: unproven
  - scenario: markdown-with-yaml-frontmatter#metadata-inside-files/provenance-evidence-arrives
    kind: check
  - scenario: markdown-with-yaml-frontmatter#metadata-inside-files/derived-index-disagrees-with-frontmatter
    kind: check
  - scenario: markdown-with-yaml-frontmatter#reference-citations/numbered-citation-appears
    kind: check
  - scenario: markdown-with-yaml-frontmatter#the-ontology-defines-every-term/term-link-points-at-no-entry
    kind: unproven
  - scenario: markdown-with-yaml-frontmatter#the-ontology-defines-every-term/change-links-to-a-draft-term-at-archive
    kind: unproven
  - scenario: markdown-relative-links-matching#markdown-links-between-files/wikilink-enters-a-repository-file
    kind: check
  - scenario: markdown-relative-links-matching#markdown-links-between-files/at-sign-reference-enters-a-state-file
    kind: check
  - scenario: markdown-relative-links-matching#link-targets-resolve/link-target-moves
    kind: check
  - scenario: open-knowledge-format-bundle#type-on-every-file/type-is-derived-from-the-directory
    kind: unproven
  - scenario: open-knowledge-format-bundle#path-is-the-identifier/identifier-key-appears
    kind: check
  - scenario: open-knowledge-format-bundle#reserved-names/reserved-name-holds-frontmatter
    kind: check
  - scenario: open-knowledge-format-bundle#bundle-declares-its-version/version-declaration-is-absent
    kind: check
  - scenario: directories-direct-the-tools#directories-direct/content-goes-into-a-catch-all-directory
    kind: unproven
  - scenario: directories-direct-the-tools#catch-all-directories-drain/item-ages-in-the-queue
    kind: unproven
  - scenario: user-values-and-variables#variables-are-name/instruction-embeds-a-configurable-value
    kind: check
  - scenario: user-values-and-variables#canon-stays-vendor-neutral/harness-placeholder-enters-the-canon
    kind: check
  - scenario: instructions-stay-vendor-neutral#reusable-across-harnesses-and-models/second-canon-appears-for-one-instruction
    kind: unproven
  - scenario: instructions-stay-vendor-neutral#reusable-across-harnesses-and-models/deployed-copy-is-edited-in-place
    kind: run
  - scenario: instructions-stay-vendor-neutral#layout-is-enforced/layout-rule-has-no-analysis-tool
    kind: unproven
  - scenario: user-values-and-variables#canon-stays-vendor-neutral/harness-needs-different-wording
    kind: run
  - scenario: user-values-and-variables#canon-stays-vendor-neutral/instruction-depends-on-one-harness-s-hook-event
    kind: unproven
  - scenario: instructions-stay-vendor-neutral#one-instance-per-harness/assembly-writes-an-instance
    kind: run
  - scenario: instructions-stay-vendor-neutral#one-instance-per-harness/new-harness-joins
    kind: run
  - scenario: instructions-stay-vendor-neutral#reusable-across-harnesses-and-models/every-sidecar-is-removed
    kind: run
  - scenario: ceremony-matches-the-task#ceremony-matches-the-task/small-fix-arrives-with-full-ceremony
    kind: unproven
  - scenario: ceremony-matches-the-task#semantic-density/filler-enters-an-instruction
    kind: check
  - scenario: ceremony-matches-the-task#verbs-name-actions/nominalization-enters-a-heading
    kind: check
  - scenario: single-source-of-truth#code-is-truth/comment-restates-the-code
    kind: unproven
  - scenario: single-source-of-truth#one-home-per-fact/fact-appears-in-a-second-file
    kind: unproven
  - scenario: lint-enforced-foundation-requirements#analysis-tool-coverage/foundation-requirement-has-no-row
    kind: check
  - scenario: lint-enforced-foundation-requirements#analysis-tool-coverage/missed-requirement-gains-a-check
    kind: check
  - scenario: lint-enforced-foundation-requirements#analysis-tool-has-fixtures/analysis-tool-arrives-without-fixtures
    kind: check
  - scenario: lint-enforced-foundation-requirements#analysis-tool-has-fixtures/analysis-rule-is-weakened
    kind: check
  - scenario: lint-enforced-foundation-requirements#record-cites-its-proofs/record-is-accepted-without-proof
    kind: unproven
---

# Behavior proof: plain-text-first-principles

`record.sh` holds one scene per scenario of the ten delta specifications of the change as they stood on 2026-09-25. The scenes follow the order of the coverage table in the change's `design.md`. A check scene runs the linter the coverage row names on a fixture the repository commits under `tests/fixtures/`. The fixture, the CORE-0007 proof of the linter, and this recording are therefore one artifact. A run scene builds a scratch deck with one skill, its Claude companion, one rule, and a consumer, and assembles it. An unproven scene records a gap and says so in its comment. The five judgment scenarios are recorded in `../core-foundation-principles-judgment/`, and this proof lists them as unproven.

The review of 2026-10-17 renamed requirements and scenarios and dropped Flat Frontmatter. It moved The Shell Resolves the Variable to the change `environment-variables-supported-syntax`. It merged Harness Specifics Stay Beside the Source and Portable Instructions into other requirements. The scene keys above follow the renamed scenarios. The recording predates the review, so two scenes that were checks are listed as unproven until the next recording. The draft-term archive scene was a check on the reference tag in the italics form, and no archiver refuses a draft term yet. The type scene showed a missing `type` as a finding, and the type now comes from the directory's structure schema. The queue scene stays unproven until the stale-item check gets a scene. Scenarios the review added have no scene yet.

The recording ran inside the `runedeck/proof:1` container from `docs/proofs/Containerfile`: Debian slim with the pinned linters and a linux `rune`. There asciinema had a real pty, and every scene ran the same versions the repository's hooks run. `proof.cast` is the cast, `proof.txt` the transcript `asciinema convert -f txt` wrote from it, and `proof.gif` the render by agg.

Transcript digest (`shasum -a 256 proof.txt`): `bc725f5149592054951e2da87563e6f8be85f4480dd671f23959f2ea100d39b0`

Scenes: 18 checks, 5 runs, 15 unproven here.

Re-record, from the repository root, outside the command sandbox, with the image built from `docs/proofs/Containerfile`:

```sh
container run --rm -v "$PWD:/work" -w /work -e HOME=/tmp runedeck/proof:1 \
  asciinema rec --command 'bash docs/proofs/plain-text-first-principles/record.sh' --headless --window-size 100x30 --idle-time-limit 2 --overwrite --return docs/proofs/plain-text-first-principles/proof.v3.cast
```

then `asciinema convert -f asciicast-v2`, `asciinema convert -f txt`, and `agg`. Without the container, the pty-free fallback recorder: `python3 scripts/fallback/asciinema.py docs/proofs/plain-text-first-principles/record.sh docs/proofs/plain-text-first-principles/proof.cast`.
