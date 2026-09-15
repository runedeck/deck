---
name: AcceptanceTesting
description: "Prove that a built change behaves as its specification says: one recorded scene per scenario, run end to end with expectations on the output, rendered to GIF and MP4, and linked from the pull request as the behavior proof. USE WHEN an implementation is finished, a change has user-visible behavior, a pull request needs proof that the feature works, a spec scenario must be demonstrated, or a README needs a demo. NOT FOR unit tests, the repository's check stages (ContinuousIntegration), or screen capture of a GUI window."
license: EUPL-1.2
compatibility: "Requires bash, asciinema 3.2 or later, agg 1.9 or later, ffmpeg, and one installed monospace font. Verified on macOS."
metadata:
    version: 0.1.0
---

# AcceptanceTesting

A change is done when its behavior is demonstrated, not when its checks pass. The specification already states the behavior as scenarios: WHEN a condition holds, THEN an observable result follows. This skill turns each scenario into a recorded scene, runs the scenes end to end against the built candidate, fails when an expectation fails, and files the recording as the proof. [Recording.md](Recording.md) carries the asciinema mechanics and [Scenes.md](Scenes.md) the scene grammar.

## Prerequisites

- The change's delta specification with its scenarios, under `docs/changes/<change>/specs/`.
- The built candidate: the binary, the deployed runes, or the rendered output the scenarios exercise.
- `brew install asciinema agg ffmpeg` and one monospace font. Verified with asciinema 3.2.1 and agg 1.9.0.

## Constraints

- One scene per scenario, in the order the specification lists them. A scenario with no scene is an unproven requirement, and the pull request says so.
- Every THEN is an `expect` on the output. A scene without an expectation is a demo, not a proof.
- Run against the frozen head, the same commit the ContinuousIntegration receipt names, so both proofs cover one candidate. Any edit after the recording restarts both. Record in a clean directory outside every repository, so no instruction file reaches a harness under test.
- Never edit the transcript or the cast. A failed expectation fails the recording, and the fix goes into the candidate, then the recording runs again.
- Keep the recording short: few commands, short outputs, one scene per scenario. Length hides defects.
- Do not commit a cast, a GIF, or a transcript before the secret check in Verification passes.

## Instructions

### Write the scenes

1. Copy [record.sh](scripts/record.sh) into a clean directory outside every repository, with only the configuration the candidate needs.
2. For each scenario, add a scene: `scenario "<title>"`, one `run` per WHEN step, and one `expect` per THEN clause. [Scenes.md](Scenes.md) shows the grammar and how to phrase an expectation.
3. List every command that can open a dialog in the `preflight` call.

### Record the proof

```sh
asciinema rec --command "bash record.sh" --headless --window-size 100x30 --idle-time-limit 2 --overwrite --return proof.cast
echo "record-exit=$?"
```

`--return` makes the recording carry the script's exit status, and the script exits nonzero on the first failed expectation. A nonzero exit is a finding against the candidate.

### Render and check

1. Render: `agg --theme github-dark --font-size 18 --last-frame-duration 4 proof.cast proof.gif`, then the MP4 as [Recording.md](Recording.md) gives.
2. Write the transcript: `asciinema convert -f txt proof.cast proof.txt`.
3. Confirm every THEN in the transcript by reading it, and grep it for secrets, addresses, and private content.

### File the proof

1. Commit the GIF under `docs/proofs/<change>/` and embed it in the pull request's Testing section with the commit id it proves.
2. State which scenarios have scenes. A scenario without one is listed as unproven.
3. Record the proof in the receipt shape the ContinuousIntegration skill gives, with the same candidate commit, and add the scenario list, `record-exit`, and the transcript digest. This is the `rune:Proof` of kind `behavior`.

## Verification

- `record-exit=0`, and the transcript contains the output each `expect` matched.
- The scene count equals the scenario count of the delta specification, or the pull request names the gap.
- The transcript holds no secret, address, or private content.
- `ffmpeg -ss 5 -i proof.mp4 -frames:v 1 frame.png` shows the font, theme, and window as intended.

## Troubleshooting

- The recording stops on a dialog: a command opened one during a scene. Add it to `preflight`.
- The recording carries stray tool calls: the directory or a parent holds an instruction file. Move the directory.
- An `expect` fails on output that looks right: the pattern is anchored to a line. Match the fragment, not the layout.
- The GIF has the wrong font: agg did not find the family. Check the name with `fc-list`.

## References

- asciinema recorder documentation [ASCIINEMA]
- agg, the asciinema GIF generator [AGG]
- FFmpeg documentation [FFMPEG]

[ASCIINEMA]: https://docs.asciinema.org/ "asciinema documentation"
[AGG]: https://github.com/asciinema/agg "agg, asciinema gif generator"
[FFMPEG]: https://ffmpeg.org/documentation.html "FFmpeg documentation"
