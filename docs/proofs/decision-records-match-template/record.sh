#!/usr/bin/env bash
# Driver for a recorded acceptance proof of the decision-records-match-template
# specification: the tightened decisions schema and check-decision-shape,
# run on fixture records in a scratch tree and on the real deck.
# shellcheck source=../../../scripts/fallback/prove.sh
. "$(dirname "$0")/../../../scripts/fallback/prove.sh"

printf '\033[2J\033[H'

ROOT=$(cd "$(dirname "$0")/../../.." && pwd) || exit 1
RUNE=${RUNE:-rune}
export RUNE
FORGE=${FORGE_CORE:-/Users/N4M3Z/Developer/N4M3Z/forge-core}
PROOF_HOME=$(mktemp -d "${TMPDIR:-/tmp}/decision-records-match-template.XXXXXX")
trap 'command rm -rf "$PROOF_HOME"' EXIT
cd "$PROOF_HOME" || exit 1
mkdir -p deck/docs/decisions deck/docs/specs/example-capability
printf '%s\n' 'authors:' '    - Owner <owner@example.org>' 'model_domains:' \
    '    - claude.noreply.nexus.local' '    - codex.noreply.nexus.local' > deck/authors.yaml
printf '%s\n' '### Requirement: Thing Is Checked' '' 'Body.' > deck/docs/specs/example-capability/spec.md
CHECK="$ROOT/scripts/check-decision-shape"
SCHEMA="$ROOT/docs/decisions/.mdschema"
# Short pauses keep the cast scrubbable: a zero pause plays the whole
# proof in one second, and a person cannot read it.
export TYPE_DELAY=0.01 PAUSE_AFTER_COMMENT=0.8 PAUSE_AFTER_OUTPUT=1.0

# fixture CONSULTED UPSTREAM HEADING ITEM: one record in the scratch tree.
fixture() {
    {
        printf -- '---\ntitle: "Example"\ndescription: "An example record"\ntype: adr\ncategory: process\n'
        printf 'tags: [example]\nstatus: proposed\ncreated: 2026-09-22\nupdated: 2026-09-22\n'
        printf 'author: "@owner"\nproject: deck\nrelated: []\nresponsible: ["@owner"]\naccountable: ["@owner"]\n'
        printf 'consulted: [%s]\ninformed: []\nupstream: [%s]\n---\n\n# Example\n\n' "$1" "$2"
        printf '## Context and Problem Statement\n\nA record needs a context statement of at least twenty words so that the schema word count passes for this fixture.\n\n'
        printf '## Considered Options\n\n1. One\n\n## Decision Outcome\n\nOption 1.\n\n%s\n\n- [+] Gain\n- %s\n' "$3" "$4"
    } > "deck/docs/decisions/DECK-0001 Example.md"
}

scenario "Consequences become their own section"
comment "The schema requires ### Consequences under ## Decision Outcome. A record with ## Consequences fails."
fixture '"@owner"' '' '## Consequences' '[-] Cost'
run "mdschema check 'deck/docs/decisions/DECK-0001 Example.md' --schema docs/decisions/.mdschema" \
    "mdschema check 'deck/docs/decisions/DECK-0001 Example.md' --schema '$SCHEMA'"
expect 'Required element "### Consequences" not found within "Decision Outcome"'

scenario "Consequence bullet has no sign"
comment "Each consequence starts with [+] or [-]. The check names the record and the item."
fixture '"@owner"' '' '### Consequences' 'Cost without a sign'
run "python3 scripts/check-decision-shape deck" "python3 '$CHECK' deck"
expect 'consequence has no sign: `- Cost without a sign`'

scenario "Consulted entry names a model without a harness"
fixture '"claude-fable-5-1"' '' '### Consequences' '[-] Cost'
run "python3 scripts/check-decision-shape deck" "python3 '$CHECK' deck"
expect 'consulted `claude-fable-5-1` is neither `@handle` nor `<model-id>@<harness>`'

scenario "Consulted entry names an unknown harness"
fixture '"gpt-6-astra@openai"' '' '### Consequences' '[-] Cost'
run "python3 scripts/check-decision-shape deck" "python3 '$CHECK' deck"
expect 'unknown harness. Known: claude, codex'

scenario "Upstream names a file that does not exist"
fixture '"@owner"' 'MarkdownFirst.md' '### Consequences' '[-] Cost'
run "python3 scripts/check-decision-shape deck" "python3 '$CHECK' deck"
expect 'upstream `MarkdownFirst.md` matches no record, capability, requirement, file, or URL'

scenario "Upstream names a capability requirement"
comment "A requirement reference resolves in the scratch tree, and the real deck passes with CORE-0001 pointing at seven requirements."
fixture '"@owner"' '"example-capability#thing-is-checked"' '### Consequences' '[-] Cost'
run "python3 scripts/check-decision-shape deck; echo \"exit \$?\"" "python3 '$CHECK' deck; echo \"exit \$?\""
expect '^exit 0$'
run "python3 scripts/check-decision-shape; echo \"exit \$?\"" "python3 '$CHECK' '$ROOT'; echo \"exit \$?\""
expect '^exit 0$'
run "grep -E '^    - \"[a-z-]+#' docs/decisions/CORE-0001*.md" \
    "grep -E '^    - \"[a-z-]+#' '$ROOT/docs/decisions/CORE-0001 Markdown as System Language.md'"
expect 'markdown-with-yaml-frontmatter#markdown-system-language'
expect 'lint-enforced-foundation-requirements#checker-coverage'

scenario "Record is adopted from forge-core"
comment "The deck record and its forge-core source carry the same created and updated dates."
mkdir -p forge-core/docs/decisions
cp -n "$ROOT/docs/decisions/CORE-0001 Markdown as System Language.md" deck/docs/decisions/
cp -n "$FORGE/docs/decisions/CORE-0001 Markdown as System Language.md" forge-core/docs/decisions/
run "grep -hE '^(created|updated):' */docs/decisions/CORE-0001*.md | sort | uniq -c"
expect '2 created: 2026-02-19'
expect '2 updated: 2026-03-30'
run "grep -o 'forge-core/blob/main/[^\"]*' deck/docs/decisions/CORE-0001*.md"
expect 'CORE-0001%20Markdown%20as%20System%20Language.md'
