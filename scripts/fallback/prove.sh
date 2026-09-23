#!/usr/bin/env bash
# The recorded-proof grammar, scenario, run, expect, expect_not, and
# preflight. A proof's record.sh sources this file and holds only its
# scenes. A missed expectation exits nonzero, and the recorder carries
# that status out. The variables at the top tune pace; a proof exports
# them before sourcing when it needs another pace.
set -u

TYPE_DELAY=${TYPE_DELAY:-0.02}
PAUSE_AFTER_COMMENT=${PAUSE_AFTER_COMMENT:-1.2}
PAUSE_AFTER_OUTPUT=${PAUSE_AFTER_OUTPUT:-1.5}

PROMPT_COLOR=$'\033[1;32m'
COMMENT_COLOR=$'\033[2;3m'
CAPABILITY_COLOR=$'\033[1;36m'
BOX_COLOR=$'\033[2m'
TITLE_COLOR=$'\033[1m'
KIND_COLOR=$'\033[35m'
DETAIL_COLOR=$'\033[2m'
PASS_COLOR=$'\033[32m'
FAIL_COLOR=$'\033[1;31m'
RESET=$'\033[0m'

LAST_OUTPUT=""
CURRENT_SCENARIO=""
SCENE_HAS_RUN=0
SCENE_NUMBER=0
EXPECTATIONS=0
# The scene count comes from the proof script itself, one `scenario "` line
# per scene, so the header can say 3/41. PROOF_TOTAL overrides it. The
# script path is resolved now, before a proof changes directory.
PROOF_SCRIPT=$(cd "$(dirname "$0")" && pwd)/$(basename "$0")
PROOF_TOTAL=${PROOF_TOTAL:-$(grep -c '^ *scenario "' "$PROOF_SCRIPT" 2>/dev/null || printf '0')}
OUTPUT_FILE=$(mktemp)
# proof_exit STATUS
# On a failed run the captured output of the last scene is the diagnosis.
# On success the tally closes the recording. A proof that sets its own
# EXIT trap, for a scratch directory, calls this from that trap with $?.
proof_exit() {
    if [ "$1" -ne 0 ]; then
        sed "s/^/last output: /" "$OUTPUT_FILE" >&2
    else
        printf '\n%s%s scenes, %s expectations, 0 failed%s\n' "$PROMPT_COLOR" "$SCENE_NUMBER" "$EXPECTATIONS" "$RESET"
    fi
    rm -f "$OUTPUT_FILE"
}
trap 'proof_exit $?' EXIT

prompt() {
    printf '%s❯%s ' "$PROMPT_COLOR" "$RESET"
}

type_out() {
    local text=$1
    local index
    for ((index = 0; index < ${#text}; index++)); do
        printf '%s' "${text:index:1}"
        sleep "$TYPE_DELAY"
    done
}

comment() {
    printf '%s%s%s\n' "$COMMENT_COLOR" "$1" "$RESET"
    sleep "$PAUSE_AFTER_COMMENT"
}

# capability NAME
# Opens the scenes of one capability with a rule that carries the name
# and the number of scenes that follow it in the proof script, up to the
# next capability line.
capability() {
    local count width text rule
    count=$(awk -v name="$1" '/^ *capability "/ { on = ($0 ~ "\"" name "\"") } on && /^ *scenario "/ { n++ } END { print n + 0 }' "$PROOF_SCRIPT")
    width=${COLUMNS:-$(tput cols 2>/dev/null || printf '100')}
    text=" $1 · $count scene$([ "$count" -eq 1 ] || printf 's') "
    rule=$(printf '%*s' "$((width - 2 - ${#text}))" '')
    printf '\n%s──%s%s%s\n' "$CAPABILITY_COLOR" "$text" "${rule// /─}" "$RESET"
    sleep "$PAUSE_AFTER_COMMENT"
}

# scenario TITLE [KIND] [DETAIL]
# Starts a scene named for the specification scenario it proves, in a box
# with its number, then one line with the scene kind (check, run,
# judgment, unproven) and what the scene runs. The captured output is
# cleared, so an expect before the scene's first run fails instead of
# matching the previous scene.
scenario() {
    local kind=${2:-check}
    local detail=${3:-}
    local title
    CURRENT_SCENARIO=$1
    LAST_OUTPUT=""
    SCENE_HAS_RUN=0
    SCENE_NUMBER=$((SCENE_NUMBER + 1))
    title="$SCENE_NUMBER/$PROOF_TOTAL · $1"
    # A bash replacement, not tr: tr works on bytes in a C locale and
    # splits the box-drawing character.
    local rule
    rule=$(printf '%*s' "$((${#title} + 2))" '')
    rule=${rule// /─}
    printf '\n%s┌%s┐%s\n' "$BOX_COLOR" "$rule" "$RESET"
    printf '%s│%s %s%s%s %s│%s\n' "$BOX_COLOR" "$RESET" "$TITLE_COLOR" "$title" "$RESET" "$BOX_COLOR" "$RESET"
    printf '%s└%s┘%s\n' "$BOX_COLOR" "$rule" "$RESET"
    printf '%s%s%s' "$KIND_COLOR" "$kind" "$RESET"
    [ -n "$detail" ] && printf '  %s%s%s' "$DETAIL_COLOR" "$detail" "$RESET"
    printf '\n'
    sleep "$PAUSE_AFTER_COMMENT"
}

# run SHOWN [ACTUAL]
# SHOWN is the command the viewer sees. ACTUAL is the command that runs.
# ACTUAL defaults to SHOWN. Use ACTUAL to filter tool noise off camera.
# The command runs in this shell, not a subshell, so cd and export carry
# into the next run. The output is printed and kept for the next expect.
run() {
    # The viewer sees the command as the owner types it: `rune`, not the
    # path of the binary under test.
    local shown=${1//$RUNE/rune}
    local actual=${2:-$1}
    prompt
    type_out "$shown"
    printf '\n'
    eval "$actual" >"$OUTPUT_FILE" 2>&1
    LAST_OUTPUT=$(<"$OUTPUT_FILE")
    SCENE_HAS_RUN=1
    printf '%s\n' "$LAST_OUTPUT"
    sleep "$PAUSE_AFTER_OUTPUT"
}

# matches PATTERN
# Returns 0 on a match and 1 on no match. An expectation before the
# scene's first run, or a malformed pattern (matcher status 2), is an
# unevaluated expectation, and that must never pass, so both exit 1.
matches() {
    local status
    if [ "$SCENE_HAS_RUN" -eq 0 ]; then
        printf '%sexpectation before any run in scenario "%s": /%s/%s\n' "$FAIL_COLOR" "$CURRENT_SCENARIO" "$1" "$RESET"
        exit 1
    fi
    printf '%s\n' "$LAST_OUTPUT" | grep -Eq -- "$1"
    status=$?
    if [ "$status" -gt 1 ]; then
        printf '%smalformed pattern in scenario "%s": /%s/%s\n' "$FAIL_COLOR" "$CURRENT_SCENARIO" "$1" "$RESET"
        exit 1
    fi
    return "$status"
}

# expect PATTERN [LABEL]
# Matches an extended regular expression against the last run's output.
# A match prints a tick with LABEL, or the pattern when there is none.
# A miss prints the pattern and the output, then exits 1.
expect() {
    if matches "$1"; then
        EXPECTATIONS=$((EXPECTATIONS + 1))
        printf '%s✓%s %s%s%s\n' "$PASS_COLOR" "$RESET" "$DETAIL_COLOR" "${2:-matches /$1/}" "$RESET"
        return 0
    fi
    printf '%sexpectation failed in scenario "%s": /%s/%s\n' "$FAIL_COLOR" "$CURRENT_SCENARIO" "$1" "$RESET"
    printf '%s\n' "$LAST_OUTPUT"
    exit 1
}

# expect_not PATTERN [LABEL]
# The inverse: exits 1 when the pattern appears.
expect_not() {
    if matches "$1"; then
        printf '%sunexpected output in scenario "%s": /%s/%s\n' "$FAIL_COLOR" "$CURRENT_SCENARIO" "$1" "$RESET"
        printf '%s\n' "$LAST_OUTPUT"
        exit 1
    fi
    EXPECTATIONS=$((EXPECTATIONS + 1))
    printf '%s✓%s %s%s%s\n' "$PASS_COLOR" "$RESET" "$DETAIL_COLOR" "${2:-no /$1/}" "$RESET"
}

# preflight COMMAND...
# Runs a command once with its output hidden, so a keychain or permission
# dialog is answered before the first scene.
preflight() {
    "$@" >/dev/null 2>&1 || true
}
