#!/usr/bin/env bash
# Driver for a recorded acceptance proof of the prove-each-scenario
# specification: the AcceptanceTesting skill's own driver grammar, proven
# on itself. docs/proofs/cast.py records this script.
# shellcheck source=../driver.sh
. "$(dirname "$0")/../driver.sh"

printf '\033[2J\033[H'

ROOT=$(cd "$(dirname "$0")/../../.." && pwd) || exit 1
RUNE=${RUNE:-rune}
export RUNE
PROOF_HOME=$(mktemp -d "${TMPDIR:-/tmp}/prove-each-scenario.XXXXXX")
trap 'command rm -rf "$PROOF_HOME"' EXIT
cd "$PROOF_HOME" || exit 1
# The candidate is the skill's record.sh, used as the skill says: copy it,
# keep the grammar, replace the example scenes at its tail with the
# change's own. A two-scenario specification stands in for a change.
sed '/^scenario "Files are listed"/,$d' "$ROOT/runes/core/skills/AcceptanceTesting/scripts/record.sh" > grammar.sh
{
    cat grammar.sh
    printf '%s\n' 'scenario "Greeting prints"' 'run "echo hello"' 'expect "hello"'
    printf '%s\n' 'scenario "Exit status is carried"' 'run "true && echo done"' 'expect "done"'
} > passing.sh
{
    cat grammar.sh
    printf '%s\n' 'scenario "Greeting prints"' 'run "echo hello"' 'expect "goodbye"'
} > failing.sh
export TYPE_DELAY=0 PAUSE_AFTER_COMMENT=0 PAUSE_AFTER_OUTPUT=0

scenario "Implementation is finished"
comment "One scene per scenario, one expectation per THEN: the driver prints each scene as it runs it."
run "bash passing.sh 2>&1 | grep -c 'Scenario: '"
expect "^2$"

scenario "Expectation misses"
comment "A THEN that does not match fails the recording: the driver exits nonzero and names the miss."
run "bash failing.sh > out.txt 2>&1; echo \"exit \$?\""
expect "^exit 1$"
run "grep -i 'expect' out.txt | head -1"
expect "goodbye"

scenario "Proof is filed"
comment "A filed proof carries the recording, the transcript, and a record with the exit status and the transcript digest. The skeleton's trusted-key-anchor proof is one."
FILED=${FILED_PROOF:-/Users/N4M3Z/Developer/runedeck/skeleton/docs/proofs/trusted-key-anchor}
run "ls docs/proofs/trusted-key-anchor" "ls $FILED"
expect "proof.gif"
expect "proof.txt"
expect "README.md"
run "grep -E 'exit 0|digest' docs/proofs/trusted-key-anchor/README.md" "grep -E 'exit 0|digest' $FILED/README.md"
expect "exit 0"
expect "Transcript digest .*[0-9a-f]{64}"

scenario "Change has no behavior"
comment "The skill tells the pull request to say so when no behavior proof applies."
run "grep -o 'no behavior proof applies' $ROOT/runes/core/skills/AcceptanceTesting/SKILL.md"
expect "no behavior proof applies"

scenario "Scenario has no proof at merge"
comment "Unproven: the warning merge check is task 3.5 of the change and does not exist yet. This scene records the gap."
run "ls $ROOT/.github/workflows | grep -c 'proof' || echo 'no proof check workflow'"
expect "no proof check workflow"
