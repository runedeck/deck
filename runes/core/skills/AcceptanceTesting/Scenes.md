# Scenes

A scene is one specification scenario made executable. The driver script gives five words, and a scene uses only these.

## Grammar

- `scenario "<title>"`: prints the scenario title as a dimmed comment and starts a scene. Use the specification's own scenario title.
- `comment "<text>"`: prints a dimmed line and pauses. Use it for the WHEN condition in prose when the command alone does not say it.
- `run "<shown>" ["<actual>"]`: types the shown command, runs the actual one, captures the output, and prints it. The actual command defaults to the shown one. Use the second form to filter tool noise off camera.
- `expect "<pattern>"`: matches an extended regular expression against the output of the last `run`. On a miss it prints the pattern and the output, then exits 1, which fails the recording.
- `expect_not "<pattern>"`: the inverse, for a THEN that says something must not appear.

## From scenario to scene

The specification says:

```markdown
#### Scenario: Candidate is frozen

- **WHEN** a session freezes a head for publication
- **THEN** it runs the push-stage checks on that head in a disposable checkout
- **AND** it reports each stage's own exit status with the commit id
```

The scene says:

```sh
scenario "Candidate is frozen"
run "jj log -r @- --no-graph -T 'commit_id.short()'"
run "REQUIRE_GATES=1 bash .githooks/jj-push -b change/example --dry-run 2>&1 | tail -3"
expect "authorship \(push range\).*Passed"
expect "dry run: nothing pushed"
```

One `run` per WHEN step. One `expect` per THEN clause, and one per AND. The pattern matches a fragment of a line, not the whole layout, so a column shift does not fail the proof.

## Phrasing an expectation

- Match the fact, not the formatting: `expect "3 files"` rather than the full table row.
- Anchor only when the position is the requirement: `expect "^exit=0$"`.
- Escape regular-expression metacharacters in literal output: `expect "receipt\.json"`.
- Keep secrets out of the pattern and the output. A scene that needs a token uses a placeholder value the candidate accepts.

## A scene that must fail

A scenario that states a refusal is proven by the refusal:

```sh
scenario "Push hook stops a publication"
run "bash .githooks/jj-push -b change/broken --dry-run 2>&1 | tail -2"
expect "typos.*Failed"
```

The driver does not treat a nonzero command status as a failure. Only a missed expectation fails the recording, so a refusal scene passes when the refusal appears.
