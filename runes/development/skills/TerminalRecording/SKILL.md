---
name: TerminalRecording
description: "Record a scripted terminal demo as an asciinema cast and render it to GIF and MP4 for a README or a talk. USE WHEN recording a terminal demo, making a GIF of a CLI, adding a README demo, using asciinema or agg, or making a screen recording of a command. NOT FOR screen capture of a GUI window, video editing, or recording a live session by hand."
license: EUPL-1.2
compatibility: Requires bash, asciinema 3.2 or later, agg 1.9 or later, ffmpeg, and one installed monospace font. Verified on macOS.
metadata:
    version: 0.1.0
---

# TerminalRecording

Record the terminal, not the screen. A cast records only the session. Screen capture records the front window and every macOS permission dialog.

Drive the session with a script. A scripted demo is repeatable, and the commands are the only part that changes between demos.

## Prerequisites

- `brew install asciinema agg ffmpeg` on macOS. This procedure was verified with asciinema 3.2.1 and agg 1.9.0.
- One installed monospace font, for example Hack Nerd Font Mono. Without a named font, agg uses its bundled font.
- A dedicated recording directory that holds only the configuration the demo needs.

## Constraints

- Do not record a live session by hand. Use the driver script.
- Do not record inside a repository or a workshop directory. Claude Code and opencode load `AGENTS.md` and `CLAUDE.md` from the working directory and its parents. Unrelated instructions reach the model and produce stray tool calls.
- Phrase demo questions so that the answers stay generic. Ask for folder names, not message subjects. Ask for counts, not lists.
- Keep commands few and outputs short. agg renders one frame for each output batch. A 40 second demo with a few commands renders to about 200 frames.
- Do not commit a cast, a GIF, or a transcript before the secret check in Verification passes.

## Instructions

### Prepare the recording directory

1. Create an empty directory outside every repository. Copy only the configuration files that the demo needs.
2. Copy [record.sh](scripts/record.sh) into the directory. Edit only the scene section at the end of the file.
3. Run each command that can open a dialog once before the first scene. A rebuilt macOS binary that reads the keychain opens an approval dialog on first use. The `preflight` function in the script does this off camera.

### Write the scenes

The script has four functions. `prompt` prints a colored prompt character. `type_out` prints a command one character at a time with `sleep 0.02`. `comment` prints a dimmed `# ...` line and pauses. `run` types a command, runs it with `eval`, and pauses after the output.

Compose scenes from `comment` and `run` lines only:

```sh
comment "List the files in the demo directory"
run "ls -1"
comment "Show the working tree status"
run "git status --short"
```

When a tool prints startup warnings, give `run` a second argument. The first argument is the command that the viewer sees. The second argument is the command that runs. Codex CLI prints warnings about malformed agent files and hooks. This filter removed them:

```sh
run "codex exec 'How many files are in this directory?'" \
    "codex exec 'How many files are in this directory?' 2>&1 | grep -v -E 'Ignoring malformed agent role definition|^[[:space:]]*\|[[:space:]]*\^?[[:space:]]*$|^[[:space:]]*[0-9]+ \| |^missing escaped value|warning: loading hooks from both|warning: Skill descriptions were shortened'"
```

### Record the cast

```sh
cd /path/to/recording-directory
asciinema rec --command "bash record.sh" --headless --window-size 100x30 --idle-time-limit 2 --overwrite --return demo.cast
```

`--headless` is required when no TTY is attached, for example in an agent session or in CI. `--idle-time-limit 2` caps each pause so a slow command does not produce a long wait in the video. `--return` makes `asciinema rec` exit with the exit code of the script.

### Render the GIF and the MP4

```sh
agg --theme github-dark --font-family "Hack Nerd Font Mono" --font-size 18 --last-frame-duration 4 demo.cast demo.gif
ffmpeg -i demo.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" demo.mp4
```

A 40 second cast at 100 by 30 cells renders to a GIF of about 600 KB. Commit the GIF under `docs/` and embed it in the README:

```markdown
![Demo of the CLI](docs/demo.gif)
```

## Verification

Check the result without watching it.

- `asciinema convert -f txt demo.cast demo.txt` writes a plain transcript. Grep it for secrets, email addresses, and private message content.
- `ffmpeg -ss 18 -i demo.mp4 -frames:v 1 frame.png` writes one still image. Look at it to check the font, the theme, and the window size.
- `asciinema rec` exited with code 0. With `--return`, a failed scene fails the recording.

## Troubleshooting

- The recording contains stray tool calls or unrelated answers: the recording directory or one of its parents holds an instruction file. Move the recording directory.
- The recording stops on a dialog: a command opened a dialog during a scene. Add the command to the `preflight` call.
- The GIF has the wrong font: agg did not find the font family. Check the exact family name with `fc-list` and pass it to `--font-family`.
- The GIF is too large: shorten the outputs, remove commands, or lower `--idle-time-limit`.

## References

- asciinema recorder documentation [ASCIINEMA]
- agg, the asciinema GIF generator [AGG]
- FFmpeg documentation [FFMPEG]

[ASCIINEMA]: https://docs.asciinema.org/ "asciinema documentation"
[AGG]: https://github.com/asciinema/agg "agg, asciinema gif generator"
[FFMPEG]: https://ffmpeg.org/documentation.html "FFmpeg documentation"
