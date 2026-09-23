#!/usr/bin/env bash
# Recorded proof of the plain-text-first-principles change: one scene per
# scenario of its ten delta specifications, in coverage-table order. A
# check scene runs the real linter on a fixture the repository commits. A
# run scene assembles a scratch deck. An unproven scene records the gap
# and says so. Judgment scenes run a reviewing model through
# `rune run --clean` and live in ../core-foundation-principles-judgment/record.sh.
# Here each is a pointer scene that the proof README lists as unproven.
# shellcheck source-path=SCRIPTDIR
# shellcheck source=../../../scripts/fallback/prove.sh
. "$(dirname "$0")/../../../scripts/fallback/prove.sh"

printf '\033[2J\033[H'

ROOT=$(cd "$(dirname "$0")/../../.." && pwd) || exit 1
RUNE=${RUNE:-rune}
export RUNE
FIX="$ROOT/tests/fixtures"
VALE_FIX="$FIX/vale/.vale.ini"
PROOF_HOME=$(mktemp -d "${TMPDIR:-/tmp}/plain-text-first-principles.XXXXXX")
# shellcheck disable=SC2154
trap 'status=$?; command rm -rf "$PROOF_HOME"; proof_exit "$status"' EXIT
cd "$PROOF_HOME" || exit 1
export TYPE_DELAY=0.01 PAUSE_AFTER_COMMENT=0.8 PAUSE_AFTER_OUTPUT=1.0

preflight "$RUNE" vale rumdl lychee mdschema python3

capability "plain-text-is-futureproof"

scenario "Database is rebuilt from plain text" unproven "judgment scene, recorded beside this proof"
comment "Judgment scene: a model reviews the fixture in the judgment proof beside this one. This scene points at it."
run "rg -c 'Database is rebuilt from plain text' docs/proofs/core-foundation-principles-judgment/record.sh" "rg -c 'Database is rebuilt from plain text' '$ROOT/docs/proofs/core-foundation-principles-judgment/record.sh'"
expect "^[1-9]"

scenario "Binary asset enters the repository" check "scripts/check-binary-assets"
comment "A PNG with no description beside it fails; the same PNG with logo.png.md passes."
run "python3 scripts/check-binary-assets tests/fixtures/binary-assets/invalid" "python3 '$ROOT/scripts/check-binary-assets' '$FIX/binary-assets/invalid'"
expect 'binary: logo.png has no description beside it'
run "python3 scripts/check-binary-assets tests/fixtures/binary-assets/valid" "python3 '$ROOT/scripts/check-binary-assets' '$FIX/binary-assets/valid'"
expect 'binary assets: 0 findings'

scenario "Render drifts from its state file" unproven "scripts/check-provenance sees the seal, no regeneration check"
comment "Unproven. The seal on the idea snapshot reports a changed derived form, one byte is enough. No check regenerates the form from its source and compares, and the coverage table says so."
mkdir -p drift/docs/ideas/.provenance
cp "$ROOT/docs/ideas/Plain Text Wins.svg" drift/docs/ideas/
cp "$ROOT/docs/ideas/.provenance/Plain Text Wins.svg.yaml" drift/docs/ideas/.provenance/
printf '\n' >> "drift/docs/ideas/Plain Text Wins.svg"
run "cd drift && python3 scripts/check-provenance 'docs/ideas/.provenance/Plain Text Wins.svg.yaml'" "cd drift && python3 '$ROOT/scripts/check-provenance' 'docs/ideas/.provenance/Plain Text Wins.svg.yaml'; cd .."
expect 'stale subject digest'
run "rg 'Lossless Renders' docs/changes/plain-text-first-principles/design.md" "rg 'Lossless Renders' '$ROOT/docs/changes/plain-text-first-principles/design.md'"
expect 'missed requirement'

capability "markdown-with-yaml-frontmatter"

scenario "Instruction arrives in another format" unproven "rune validate accepts it"
comment "Unproven. A domain holds Thing.txt and a Thing.md without frontmatter. rune validate ignores the first and accepts the second, so nothing rejects a non-Markdown instruction today. The coverage table says so."
mkdir -p fmt/runes/core/rules
printf 'schema: 1\nname: fmt\nversion: 0.0.1\ndescription: A scratch deck.\nproviders:\n    - claude\n' > fmt/deck.yaml
printf 'name: core\nversion: 0.0.1\ndescription: A scratch domain.\n' > fmt/runes/core/module.yaml
printf '# core\n' > fmt/runes/core/README.md
printf 'MIT\n' > fmt/runes/core/LICENSE
printf '{}\n' > fmt/runes/core/defaults.yaml
printf 'Do the thing.\n' > fmt/runes/core/rules/Thing.txt
printf 'Do the thing.\n' > fmt/runes/core/rules/Thing.md
run "rune validate --source fmt" "$RUNE validate --source fmt --no-color; true"
expect 'Thing.md'
run "rg 'Markdown System Language' docs/changes/plain-text-first-principles/design.md" "rg 'Markdown System Language' '$ROOT/docs/changes/plain-text-first-principles/design.md'"
expect 'missed requirement'

scenario "Provenance evidence arrives" check "scripts/check-provenance"
comment "The adopted idea snapshot has its seal in a sidecar beside it, the seal verifies, and no record or idea in the repository carries a digest in its frontmatter."
run "ls docs/ideas docs/ideas/.provenance" "ls '$ROOT/docs/ideas' '$ROOT/docs/ideas/.provenance'"
expect 'Plain Text Wins.svg.yaml'
run "python3 scripts/check-provenance 'docs/ideas/.provenance/Plain Text Wins.svg.yaml'; echo \"exit \$?\"" "cd '$ROOT' && python3 scripts/check-provenance 'docs/ideas/.provenance/Plain Text Wins.svg.yaml'; echo \"exit \$?\"; cd '$PROOF_HOME'"
expect '^exit 0$'
run "rg -l '^(sha256|digest|fingerprint):' docs/decisions docs/ideas || echo 'no digest in any frontmatter'" "rg -l '^(sha256|digest|fingerprint):' '$ROOT/docs/decisions' '$ROOT/docs/ideas' || echo 'no digest in any frontmatter'"
expect 'no digest in any frontmatter'

scenario "Derived index disagrees with frontmatter" check "rune graph export"
comment "The graph is a derived index. A scratch deck exports it, then the record's frontmatter title changes: the stored export disagrees, and a regeneration follows the frontmatter."
mkdir -p idx/docs/decisions
printf 'schema: 1\nname: idx\nversion: 0.0.1\ndescription: A scratch deck.\nproviders:\n    - claude\n' > idx/deck.yaml
printf -- '---\nid: IDX-0001\ntitle: Title A\nstatus: accepted\ndate: 2026-09-24\ntype: decision\n---\n\n# IDX-0001 Title A\n\n## Context and Problem Statement\n\nA.\n\n## Decision Outcome\n\nA.\n' > 'idx/docs/decisions/IDX-0001 Title A.md'
run "rune graph export --source idx > idx/graph.ttl && rg 'dcterms:title' idx/graph.ttl" "$RUNE graph export --source idx > idx/graph.ttl && rg 'dcterms:title' idx/graph.ttl"
expect 'Title A'
perl -pi -e 's/^title: Title A$/title: Title B/' 'idx/docs/decisions/IDX-0001 Title A.md'
run "rg '^title:' 'idx/docs/decisions/IDX-0001 Title A.md'; rg 'dcterms:title' idx/graph.ttl" "rg '^title:' 'idx/docs/decisions/IDX-0001 Title A.md'; rg 'dcterms:title' idx/graph.ttl"
expect 'title: Title B'
expect 'Title A'
run "rune graph export --source idx | rg 'dcterms:title'" "$RUNE graph export --source idx | rg 'dcterms:title'"
expect 'Title B'

scenario "Numbered citation appears" check "vale · Core.Citations"
comment "A bare number as a citation carries no meaning at the point of use. The Core style says so."
printf '# Note\n\nThe format is standard [1].\n' > cite.md
run "vale --no-global --config .vale.ini --output=line cite.md" "vale --no-global --config '$ROOT/.vale.ini' --output=line cite.md; true"
expect 'Core.Citations'

scenario "Term link points at no entry" unproven "rune spec validate names the glossary"
comment "Unproven. A delta marks *nonsense* in the legacy italics form. The installed rune names the term and asks for a glossary entry; no fixer adds a draft entry yet, and the coverage table says so."
mkdir -p term/docs/changes/x/specs/some-thing-here term/docs/specs term/ontology
cp "$ROOT/ontology/rune.ttl" term/ontology/
cp "$ROOT/deck.yaml" term/deck.yaml
printf '## Why\n\nWhy.\n\n## What Changes\n\n- x\n' > term/docs/changes/x/proposal.md
printf -- '- [ ] 1.1 x\n' > term/docs/changes/x/tasks.md
printf '## ADDED Requirements\n\n### Requirement: Thing\n\nEvery *nonsense* [NONSENSE] MUST exist.\n\n#### Scenario: Thing happens\n\n- **WHEN** a thing happens\n- **THEN** it is seen\n\n[NONSENSE]: https://runedeck.ai/ns#Nonsense\n' > term/docs/changes/x/specs/some-thing-here/spec.md
run "rune spec validate --source term" "$RUNE spec validate --source term --no-color; true"
expect "defined term 'nonsense'"
run "rg 'Defined Terms Cite the Ontology' docs/changes/plain-text-first-principles/design.md" "rg 'Defined Terms Cite the Ontology' '$ROOT/docs/changes/plain-text-first-principles/design.md'"
expect 'missed requirement'

scenario "Change links to a draft term at archive" unproven "scripts/fallback/check-terms reports the term, no archiver refuses it"
comment "Unproven. The tag [NONSENSE] resolves to a term the ontology does not declare, and the term check names the file and the tag. No archiver refuses a draft term yet."
run "python3 scripts/fallback/check-terms term" "python3 '$ROOT/scripts/fallback/check-terms' term; true"
expect 'spec.md: \[NONSENSE\] names https://runedeck.ai/ns#Nonsense, which is not in ontology/rune.ttl'

capability "markdown-relative-links-matching"

scenario "Wikilink enters a repository file" check "vale · Core.DeckLinks"
run "vale --no-global --config tests/fixtures/vale/.vale.ini --output=line tests/fixtures/vale/invalid/deck-links.md" "vale --no-global --config '$VALE_FIX' --output=line '$FIX/vale/invalid/deck-links.md'; true"
expect 'Core.DeckLinks.*\[\[CORE-0001'

scenario "At-sign reference enters a state file" check "vale · Core.DeckLinks"
run "vale --no-global --config tests/fixtures/vale/.vale.ini --output=line tests/fixtures/vale/invalid/deck-links.md" "vale --no-global --config '$VALE_FIX' --output=line '$FIX/vale/invalid/deck-links.md'; true"
expect 'Core.DeckLinks.*@docs/decisions/CORE-0002.md'
run "vale --no-global --config tests/fixtures/vale/.vale.ini --output=line tests/fixtures/vale/valid/deck-links.md; echo \"exit \$?\"" "vale --no-global --config '$VALE_FIX' --output=line '$FIX/vale/valid/deck-links.md'; echo \"exit \$?\""
expect '^exit 0$'

scenario "Link target moves" check "lychee --offline"
comment "A link whose target was renamed fails the offline link check."
mkdir -p links
printf '# A\n\nSee [B](b-old.md#top).\n' > links/a.md
printf '# B\n\n## Top\n' > links/b.md
run "lychee --offline --include-fragments --no-progress links" "lychee --offline --include-fragments --no-progress links; true"
expect 'ERROR|Errors'

capability "open-knowledge-format-bundle"

scenario "Type is derived from the directory" unproven "the recording predates the type decision"
comment "Unproven. The recording shows a missing type as a finding. The type is now derived from the directory's structure schema, and no scene shows the graph export filling it in."
run "python3 scripts/check-okf tests/fixtures/okf/invalid" "python3 '$ROOT/scripts/check-okf' '$FIX/okf/invalid'; true"
expect 'okf:'

scenario "Identifier key appears" check "scripts/check-okf"
run "python3 scripts/check-okf tests/fixtures/okf/invalid" "python3 '$ROOT/scripts/check-okf' '$FIX/okf/invalid'; true"
expect "id: docs/record.md carries id 'something-else'"

scenario "Reserved name holds frontmatter" check "scripts/check-okf"
run "python3 scripts/check-okf tests/fixtures/okf/invalid" "python3 '$ROOT/scripts/check-okf' '$FIX/okf/invalid'; true"
expect "reserved: log.md carries a frontmatter block with keys \['title'\]"

scenario "Version declaration is absent" check "scripts/check-okf"
run "python3 scripts/check-okf tests/fixtures/okf/invalid" "python3 '$ROOT/scripts/check-okf' '$FIX/okf/invalid'; true"
expect 'version: the bundle root index.md does not declare okf_version'
run "python3 scripts/check-okf tests/fixtures/okf/valid" "python3 '$ROOT/scripts/check-okf' '$FIX/okf/valid'"
expect 'okf: 0 findings'

capability "directories-direct-the-tools"

scenario "Content goes into a catch-all directory" unproven "judgment scene, recorded beside this proof"
comment "Judgment scene: a model reviews the fixture in the judgment proof beside this one."
run "rg -c 'catch-all directory' docs/proofs/core-foundation-principles-judgment/record.sh" "rg -c 'catch-all directory' '$ROOT/docs/proofs/core-foundation-principles-judgment/record.sh'"
expect "^[1-9]"

scenario "Item ages in the queue" unproven "no scene runs the stale-item check yet"
comment "Unproven: the coverage row names the stale-item check, and no scene runs it on an aged fixture yet."
run "rg 'Catch-All Directories Drain' docs/changes/plain-text-first-principles/design.md" "rg 'Catch-All Directories Drain' '$ROOT/docs/changes/plain-text-first-principles/design.md'"
expect 'check-stale-queue'

capability "user-values-and-variables"

scenario "Instruction embeds a configurable value" check "vale · Core.UserValue"
run "vale --no-global --config tests/fixtures/vale/.vale.ini --output=line tests/fixtures/vale/invalid/user-value.md" "vale --no-global --config '$VALE_FIX' --output=line '$FIX/vale/invalid/user-value.md'; true"
expect "Core.UserValue.*/Users/martin"

scenario "Harness placeholder enters the canon" check "vale · Core.HarnessPlaceholder"
run "vale --no-global --config tests/fixtures/vale/.vale.ini --output=line tests/fixtures/vale/invalid/harness-placeholder.md" "vale --no-global --config '$VALE_FIX' --output=line '$FIX/vale/invalid/harness-placeholder.md'; true"
expect 'Core.HarnessPlaceholder.*\$\{CLAUDE_PROJECT_DIR\}'
comment "The same line inside a harness companion directory is where it belongs: the repository's Vale configuration exempts it there."
mkdir -p mirror/runes/core/skills/S/claude mirror/runes/core/skills/S
cp -Rf "$ROOT/.vale" mirror/.vale
sed "s|^StylesPath = .*|StylesPath = $PROOF_HOME/mirror/.vale/styles|" "$ROOT/.vale.ini" > mirror/.vale.ini
cp -f "$FIX/vale/invalid/harness-placeholder.md" mirror/runes/core/skills/S/SKILL.md
cp -f "$FIX/vale/invalid/harness-placeholder.md" mirror/runes/core/skills/S/claude/SKILL.md
run "cd mirror && vale --no-global --output=line runes/core/skills/S/SKILL.md | rg -c HarnessPlaceholder" "cd mirror && vale --no-global --output=line runes/core/skills/S/SKILL.md | rg -c HarnessPlaceholder; cd .."
expect '^[1-9]'
run "cd mirror && vale --no-global --output=line runes/core/skills/S/claude/SKILL.md | rg -c HarnessPlaceholder || echo 'exempt in the companion'" "cd mirror && vale --no-global --output=line runes/core/skills/S/claude/SKILL.md | rg -c HarnessPlaceholder || echo 'exempt in the companion'; cd .."
expect 'exempt in the companion'

capability "instructions-stay-vendor-neutral"

scenario "Second canon appears for one instruction" unproven "rune validate reports no duplicate"
comment "Unproven. A rule and a skill share the name thing in one domain. rune validate passes both and reports no duplicate, and the coverage table says so."
mkdir -p dup/runes/core/skills/thing dup/runes/core/rules
printf 'schema: 1\nname: dup\nversion: 0.0.1\ndescription: A scratch deck.\nproviders:\n    - claude\n' > dup/deck.yaml
printf 'name: core\nversion: 0.0.1\ndescription: A scratch domain.\n' > dup/runes/core/module.yaml
printf '# core\n' > dup/runes/core/README.md
printf 'MIT\n' > dup/runes/core/LICENSE
printf '{}\n' > dup/runes/core/defaults.yaml
printf -- '---\nname: thing\ndescription: Does the thing. USE WHEN a thing is due.\n---\n\n# thing\n\n## Instructions\n\nDo the thing, then check the result and report it in one line.\n' > dup/runes/core/skills/thing/SKILL.md
printf -- '---\nname: thing\ndescription: Do the thing.\n---\n\n# thing\n\nDo the thing.\n' > dup/runes/core/rules/thing.md
run "rune validate --source dup" "$RUNE validate --source dup --no-color; true"
expect 'rules/thing.md'
expect 'skills/thing/SKILL.md'
run "rg 'Reusable Across Harnesses and Models' docs/changes/plain-text-first-principles/design.md" "rg 'Reusable Across Harnesses and Models' '$ROOT/docs/changes/plain-text-first-principles/design.md'"
expect 'missed requirement'

# A scratch deck with one skill, its Claude companion, and one rule, and a
# consumer that installs both. Identity, H1, and directory agree.
mkdir -p roster/deck/runes/core/skills/thing/claude roster/deck/runes/core/rules roster/app
printf 'schema: 1\nname: scratch\nversion: 0.0.1\ndescription: A scratch deck.\nproviders:\n    - claude\n    - codex\n' > roster/deck/deck.yaml
printf 'name: core\nversion: 0.0.1\ndescription: A scratch domain.\n' > roster/deck/runes/core/module.yaml
printf '# core\n' > roster/deck/runes/core/README.md
printf 'MIT\n' > roster/deck/runes/core/LICENSE
printf 'thing_root: /work\n' > roster/deck/runes/core/defaults.yaml
# shellcheck disable=SC2016
printf -- '---\nname: thing\ndescription: Does the thing.\n---\n\n# thing\n\n## Instructions\n\nDo the thing with $THING_ROOT.\n' > roster/deck/runes/core/skills/thing/SKILL.md
# shellcheck disable=SC2016
printf -- '---\nname: thing\ndescription: Does the thing.\n---\n\n# thing\n\n## Instructions\n\nDo the thing with $THING_ROOT. Claude only: read the file with the Read tool first.\n' > roster/deck/runes/core/skills/thing/claude/SKILL.md
printf -- '---\nname: Neat\ndescription: Keep it neat.\n---\n\n# Neat\n\nKeep it neat.\n' > roster/deck/runes/core/rules/Neat.md
printf 'version: 1\nsources:\n  deck:\n    local: %s/roster/deck\nrunes:\n  deck:\n    include:\n    - core/skills/thing\n    - core/rules/Neat\n' "$PROOF_HOME" > roster/app/.rune

scenario "Assembly writes an instance" run "rune install on a scratch deck"
comment "The consumer installs the skill and the rule. The manifest holds each instance's fingerprint, and the sidecar names its source."
run "rune install --source roster/app" "$RUNE install --source roster/app --no-color"
expect 'deployed'
run "rg -A2 '^  thing:' roster/app/.claude/.manifest" "rg -A2 '^  thing:' roster/app/.claude/.manifest"
expect 'fingerprint: [0-9a-f]{64}'
run "rg 'uri: skills/thing/SKILL.md' roster/app/.claude/skills/thing/.provenance/SKILL.md.yaml" "rg 'uri: skills/thing/SKILL.md' roster/app/.claude/skills/thing/.provenance/SKILL.md.yaml"
expect 'uri: skills/thing/SKILL.md'

scenario "Harness needs different wording" run "rune install on a scratch deck"
comment "The Claude companion's sentence reaches the Claude instance and no other."
run "rg -c 'Claude only' roster/app/.claude/skills/thing/SKILL.md" "rg -c 'Claude only' roster/app/.claude/skills/thing/SKILL.md"
expect '^1$'
run "rg -c 'Claude only' roster/app/build/codex/skills/thing/SKILL.md || echo 'not in the codex instance'" "rg -c 'Claude only' roster/app/build/codex/skills/thing/SKILL.md || echo 'not in the codex instance'"
expect 'not in the codex instance'

scenario "Deployed copy is edited in place" run "rune doctor --verify, rune install --force"
comment "A line appended to the deployed copy is drift: the doctor reports it, and a forced install restores the instance from the source."
printf '\nEdited in place.\n' >> roster/app/.claude/skills/thing/SKILL.md
run "rune doctor --target roster/app/.claude --verify" "$RUNE doctor --target roster/app/.claude --verify --no-color; true"
expect 'modified 1'
run "rune install --source roster/app --force" "$RUNE install --source roster/app --force --no-color"
expect 'deployed'
run "rg -c 'Edited in place' roster/app/.claude/skills/thing/SKILL.md || echo 'restored from the source'" "rg -c 'Edited in place' roster/app/.claude/skills/thing/SKILL.md || echo 'restored from the source'"
expect 'restored from the source'

scenario "Instruction depends on one harness's hook event" unproven "no hook rendering yet, cli #69"
comment "Unproven: a hook rune is not rendered into a harness's hook configuration yet (cli #69), so the scene has nothing to assemble."
run "rg -c 'hook' roster/deck/runes/core/module.yaml || echo 'no hook rendering yet'"
expect 'no hook rendering yet'

scenario "Layout rule has no analysis tool" unproven "Agent Skills validator, open gap"
comment "The Agent Skills validator is the one layout check that does not exist, and the coverage table lists it as an open gap."
run "rg 'Layout Is Enforced' docs/changes/plain-text-first-principles/design.md" "rg 'Layout Is Enforced' '$ROOT/docs/changes/plain-text-first-principles/design.md'"
expect 'missed requirement'

scenario "New harness joins" run "rune install with gemini added"
comment "Gemini joins the roster. The sources do not change, and the new target fills from the same instructions."
digest() { rg --files "$1" | sort | python3 -c "import hashlib, sys; h = hashlib.sha256()
for line in sys.stdin: h.update(open(line.strip(), 'rb').read())
print(h.hexdigest()[:16])"; }
BEFORE=$(digest roster/deck/runes)
printf 'schema: 1\nname: scratch\nversion: 0.0.1\ndescription: A scratch deck.\nproviders:\n    - claude\n    - codex\n    - gemini\n' > roster/deck/deck.yaml
run "rune install --source roster/app" "$RUNE install --source roster/app --no-color"
expect 'deployed'
run "rg --files roster/app/.gemini | rg SKILL.md" "rg --files roster/app/.gemini | rg SKILL.md"
expect 'roster/app/.gemini/.*thing/SKILL.md'
run "digest roster/deck/runes" "digest roster/deck/runes"
expect "^$BEFORE\$"

scenario "Every sidecar is removed" run "rune install, rune validate"
comment "Codex has no Read tool, the mechanism the Claude wording names. The canon alone still assembles for codex and the scratch deck validates, and that wording sits only in the Claude file."
run "rune install --source roster/app" "$RUNE install --source roster/app --no-color"
expect 'codex'
run "rune validate --source roster/deck" "$RUNE validate --source roster/deck --no-color"
expect '0 errors'
run "rg -l 'Read tool' roster/deck/runes roster/app/build" "rg -l 'Read tool' roster/deck/runes roster/app/build | sort"
expect 'roster/deck/runes/core/skills/thing/claude/SKILL.md'
expect 'roster/app/build/claude/skills/thing/SKILL.md'
run "rg -c 'Read tool' roster/app/build/codex/skills/thing/SKILL.md || echo 'codex assembles from the source alone'" "rg -c 'Read tool' roster/app/build/codex/skills/thing/SKILL.md || echo 'codex assembles from the source alone'"
expect 'codex assembles from the source alone'

capability "ceremony-matches-the-task"

scenario "Small fix arrives with full ceremony" unproven "judgment scene, recorded beside this proof"
comment "Judgment scene: a model reviews the fixture in the judgment proof beside this one."
run "rg -c 'Small fix arrives with full ceremony' docs/proofs/core-foundation-principles-judgment/record.sh" "rg -c 'Small fix arrives with full ceremony' '$ROOT/docs/proofs/core-foundation-principles-judgment/record.sh'"
expect "^[1-9]"

scenario "Filler enters an instruction" check "vale · STE and Deslop"
comment "A sentence that states no fact, constraint, or action: the prose linter reports it."
printf '# Rule\n\nIt is important to note that this rule may potentially help to improve things in a robust and seamless way.\n' > filler.md
run "vale --no-global --config .vale.ini --output=line filler.md" "vale --no-global --config '$ROOT/.vale.ini' --output=line --minAlertLevel suggestion filler.md; true"
expect 'Deslop|STE\.'

scenario "Nominalization enters a heading" check "vale · Core.Nominalization"
run "vale --no-global --config tests/fixtures/vale/.vale.ini --output=line tests/fixtures/vale/invalid/nominalization.md" "vale --no-global --config '$VALE_FIX' --output=line '$FIX/vale/invalid/nominalization.md'; true"
expect 'Core.Nominalization.*Specification acceptance'

capability "single-source-of-truth"

scenario "Comment restates the code" unproven "judgment scene, recorded beside this proof"
comment "Judgment scene: a model reviews the fixture in the judgment proof beside this one."
run "rg -c 'Comment restates the code' docs/proofs/core-foundation-principles-judgment/record.sh" "rg -c 'Comment restates the code' '$ROOT/docs/proofs/core-foundation-principles-judgment/record.sh'"
expect "^[1-9]"

scenario "Fact appears in a second file" unproven "judgment scene, recorded beside this proof"
comment "Judgment scene: a model reviews the fixture in the judgment proof beside this one."
run "rg -c 'Fact appears in a second file' docs/proofs/core-foundation-principles-judgment/record.sh" "rg -c 'Fact appears in a second file' '$ROOT/docs/proofs/core-foundation-principles-judgment/record.sh'"
expect "^[1-9]"

capability "lint-enforced-foundation-requirements"

scenario "Foundation requirement has no row" check "scripts/check-coverage"
run "python3 scripts/check-coverage tests/fixtures/coverage/invalid" "python3 '$ROOT/scripts/check-coverage' '$FIX/coverage/invalid'; true"
expect 'no coverage row for one-two-three / Thing Is Checked'

scenario "Missed requirement gains a check" check "the coverage table and the linter file"
comment "Verbs Name Actions was a missed requirement this morning. Its row now names the linter, and the linter exists."
run "rg 'Verbs Name Actions' docs/changes/plain-text-first-principles/design.md" "rg 'Verbs Name Actions' '$ROOT/docs/changes/plain-text-first-principles/design.md'"
expect 'Core.Nominalization'
run "ls .vale/styles/Core/Nominalization.yml" "ls '$ROOT/.vale/styles/Core/Nominalization.yml'"
expect 'Nominalization.yml'

scenario "Analysis tool arrives without fixtures" check "scripts/check-fixtures"
comment "The fixture check names the checker. In the repository, the six checkers still without fixtures sit in the baseline, and the coverage table lists them as an open gap."
run "python3 scripts/check-fixtures tests/fixtures/fixtures/invalid" "python3 '$ROOT/scripts/check-fixtures' '$FIX/fixtures/invalid'; true"
expect 'scripts/check-thing: no tests/fixtures/thing'
run "rg 'Analysis Tool Has Fixtures' docs/changes/plain-text-first-principles/design.md" "rg 'Analysis Tool Has Fixtures' '$ROOT/docs/changes/plain-text-first-principles/design.md'"
expect 'missed requirement'

scenario "Analysis rule is weakened" check "tests/test_check_scripts.py"
comment "Delete the version rule from a copy of check-okf: the invalid fixture stops reporting it, and the fixture test fails."
cp "$ROOT/scripts/check-okf" weak-check-okf
perl -0pi -e 's/    index = root \/ "index.md".*?return errors/    return errors/s' weak-check-okf
run "python3 weak-check-okf tests/fixtures/okf/invalid | rg -c '^version:' || echo 'version rule gone'" "python3 weak-check-okf '$FIX/okf/invalid' | rg -c '^version:' || echo 'version rule gone'"
expect 'version rule gone'
run "RUNE_CHECK_OKF=weak-check-okf python3 -m unittest tests.test_check_scripts.FixtureVerdicts.test_okf_names_every_rule" "cd '$ROOT' && RUNE_CHECK_OKF='$PROOF_HOME/weak-check-okf' python3 -m unittest tests.test_check_scripts.FixtureVerdicts.test_okf_names_every_rule 2>&1 | tail -4; cd '$PROOF_HOME'"
expect 'FAILED'

scenario "Record is accepted without proof" unproven "no check reads the proves edge"
comment "Unproven: the record shape check reads no proof edge yet. The graph carries the edge since the exporter change; the check is task 1.5 of the proof plan."
run "rg 'Record Cites Its Proofs' docs/changes/plain-text-first-principles/design.md" "rg 'Record Cites Its Proofs' '$ROOT/docs/changes/plain-text-first-principles/design.md'"
expect 'missed requirement'
