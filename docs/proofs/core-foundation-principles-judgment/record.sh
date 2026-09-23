#!/usr/bin/env bash
# Recorded proof of the five judgment scenarios of plain-text-first-principles:
# a reviewing model reads one requirement and one changed fixture through
# `rune run --clean`, with no user state, and answers with a review marker.
# The scene expects the marker and the fix the requirement calls for. The
# model id is part of the recording, since another model is another proof.
# shellcheck source-path=SCRIPTDIR
# shellcheck source=../../../scripts/fallback/prove.sh
. "$(dirname "$0")/../../../scripts/fallback/prove.sh"

printf '\033[2J\033[H'

ROOT=$(cd "$(dirname "$0")/../../.." && pwd) || exit 1
RUNE=${RUNE:-rune}
MODEL=${PROOF_MODEL:-claude-opus-5-5}
SPECS="$ROOT/docs/changes/plain-text-first-principles/specs"
PROOF_HOME=$(mktemp -d "${TMPDIR:-/tmp}/cfp-judgment.XXXXXX")
trap 'status=$?; command rm -rf "$PROOF_HOME"; proof_exit "$status"' EXIT
cd "$PROOF_HOME" || exit 1
export TYPE_DELAY=0.01 PAUSE_AFTER_COMMENT=0.8 PAUSE_AFTER_OUTPUT=1.0

preflight "$RUNE" jq python3

# brief CAPABILITY "Requirement Title" FIXTURE-DIR FILE [EXISTING-FILE]: writes brief.md for one scene.
brief() {
    python3 - "$SPECS/$1/spec.md" "$2" "$3" "$4" "${5:-}" > brief.md <<'EOF'
import pathlib, sys
spec = pathlib.Path(sys.argv[1]).read_text()
start = spec.index(f"### Requirement: {sys.argv[2]}")
end = spec.find("### Requirement:", start + 1)
req = spec[start:end if end > 0 else None]
root = pathlib.Path(sys.argv[3])
body = (root / sys.argv[4]).read_text()
print("You review one changed file against one requirement. Answer with exactly one line in the form `[ISSUE] <what to change>` when the file breaks the requirement, or `[PRAISE] ok` when it does not. No other text.\n")
print("## Requirement\n\n" + req)
if sys.argv[5]:
    print(f"## Existing file, unchanged: {sys.argv[5]}\n\n```\n{(root / sys.argv[5]).read_text()}```\n")
print(f"## Changed file: {sys.argv[4]}\n\n```\n{body}```")
EOF
}

# judge FIXTURE-DIR: runs the model with no user state and prints the marker line and the model id.
judge() {
    "$RUNE" run claude --model "$MODEL" --clean --json --timeout 5m --repo "$1" --prompt-file brief.md > reply.json 2> reply.err || true
    jq -r '.text' reply.json | rg '^\[(ISSUE|PRAISE)\]' | head -1
    printf 'model: %s\n' "$(jq -r '.resolved_model' reply.json)"
}

capability "plain-text-is-futureproof"

scenario "Database is rebuilt from plain text" judgment "$MODEL · rune run --clean"
comment "A change makes a database the place records are read from. The requirement says the store derives from the plain-text source."
mkdir -p store
printf '## What Changes\n\n- Records move into records.db, a SQLite file. Tools read a record from the database, and the Markdown files under docs/decisions/ are deleted after import.\n' > store/proposal.md
brief plain-text-is-futureproof "Plain Text Representation" store proposal.md
run "rune run claude --model $MODEL --clean --repo store --prompt-file brief.md" "judge store"
expect '^\[ISSUE\].*(plain.?text|derive|Markdown|source|regenerat)' "[ISSUE], and the fix keeps the plain-text source authoritative"
expect "model: $MODEL" "the reply came from $MODEL"

capability "directories-direct-the-tools"

scenario "Content goes into a catch-all directory" judgment "$MODEL · rune run --clean"
comment "A change adds misc/ with two notes. Nothing routes on that name."
mkdir -p catchall/misc
printf 'runes/\n  core/\n    rules/\n    skills/\nmisc/\n  ideas.md\n  scratch.md\n' > catchall/tree.txt
brief directories-direct-the-tools "Directories Direct" catchall tree.txt
run "rune run claude --model $MODEL --clean --repo catchall --prompt-file brief.md" "judge catchall"
expect '^\[ISSUE\].*(misc|rename|move|relocat|routes?|label|catch-all)' "[ISSUE], and the fix names the catch-all"
expect "model: $MODEL" "the reply came from $MODEL"

capability "ceremony-matches-the-task"

scenario "Small fix arrives with full ceremony" judgment "$MODEL · rune run --clean"
comment "A change directory holds a one-word typo fix and no requirement."
mkdir -p ceremony
printf '## Why\n\nThe README says "teh deck". It should say "the deck".\n\n## What Changes\n\n- Fix the typo in README.md, line 3.\n\n## Capabilities\n\n### New Capabilities\n\nNone.\n' > ceremony/proposal.md
brief ceremony-matches-the-task "Ceremony Matches The Task" ceremony proposal.md
run "rune run claude --model $MODEL --clean --repo ceremony --prompt-file brief.md" "judge ceremony"
expect '^\[ISSUE\].*(commit|ceremony|change director|fold|remove the director|no requirement|drop)' "[ISSUE], and the fix is a plain commit without the directory"
expect "model: $MODEL" "the reply came from $MODEL"

scenario "Comment restates the code" judgment "$MODEL · rune run --clean"
mkdir -p comment
printf 'def total(items):\n    # add up the items and return the total\n    return sum(items)\n' > comment/tally.py
brief single-source-of-truth "Code Is Truth" comment tally.py
run "rune run claude --model $MODEL --clean --repo comment --prompt-file brief.md" "judge comment"
expect '^\[ISSUE\].*(comment|remove|delete|repeat|restat)' "[ISSUE], and the fix removes the comment"
expect "model: $MODEL" "the reply came from $MODEL"

scenario "Fact appears in a second file" judgment "$MODEL · rune run --clean"
comment "A new file restates a sentence that signing.md already makes. The requirement says one home and a link."
mkdir -p twice
printf '# Signing\n\nThe owner signs every commit before push with the key in KEYS.\n' > twice/signing.md
printf '# Push\n\nThe owner signs every commit before push with the key in KEYS. Then the push runs the gates.\n' > twice/push.md
brief single-source-of-truth "One Home Per Fact" twice push.md signing.md
run "rune run claude --model $MODEL --clean --repo twice --prompt-file brief.md" "judge twice"
expect '^\[ISSUE\].*(link|signing\.md|one home|cop(y|ies)|duplicat|repeat|drift|already)' "[ISSUE], and the fix is a link to the one home"
expect "model: $MODEL" "the reply came from $MODEL"
