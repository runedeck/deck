#!/usr/bin/env bash
# Driver for a scripted terminal demo. asciinema records this script.
# Edit only the scenes at the end of the file.
set -u

TYPE_DELAY=0.02
PAUSE_AFTER_COMMENT=1.2
PAUSE_AFTER_OUTPUT=1.5

PROMPT_COLOR=$'\033[1;32m'
COMMENT_COLOR=$'\033[2m'
RESET=$'\033[0m'

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
    printf '%s# %s%s\n' "$COMMENT_COLOR" "$1" "$RESET"
    sleep "$PAUSE_AFTER_COMMENT"
}

# run SHOWN [ACTUAL]
# SHOWN is the command the viewer sees. ACTUAL is the command that runs.
# ACTUAL defaults to SHOWN. Use ACTUAL to filter tool noise off camera.
run() {
    local shown=$1
    local actual=${2:-$1}
    prompt
    type_out "$shown"
    printf '\n'
    eval "$actual"
    sleep "$PAUSE_AFTER_OUTPUT"
}

# preflight COMMAND...
# Runs a command once with its output hidden, so a keychain or permission
# dialog is answered before the first scene.
preflight() {
    "$@" >/dev/null 2>&1 || true
}

printf '\033[2J\033[H'

# Preflight: list here every command that can open a dialog.
preflight git --version

# Scenes: the only section that changes between demos.
comment "List the files in the demo directory"
run "ls -1"

comment "Show the working tree status"
run "git status --short"

comment "Done"
sleep 1
