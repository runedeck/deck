# Recording

The asciinema mechanics behind a proof. Record the terminal, not the screen: a cast records only the session, while screen capture records the front window and every macOS permission dialog.

## Directory

Record in an empty directory outside every repository and workshop. Claude Code and opencode load `AGENTS.md` and `CLAUDE.md` from the working directory and its parents, and unrelated instructions reach the model under test and produce stray tool calls. Copy only the configuration the candidate needs.

## Record

```sh
asciinema rec --command "bash record.sh" --headless --window-size 100x30 --idle-time-limit 2 --overwrite --return proof.cast
```

- `--headless` is required when no TTY is attached, in an agent session or in CI.
- `--idle-time-limit 2` caps each pause so a slow command does not stretch the video.
- `--return` makes `asciinema rec` exit with the script's status, so a failed expectation fails the recording.

## Render

```sh
agg --theme github-dark --font-family "Hack Nerd Font Mono" --font-size 18 --last-frame-duration 4 proof.cast proof.gif
ffmpeg -i proof.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" proof.mp4
```

Without a named font, agg uses its bundled font. A short cast at 100 by 30 cells renders to a GIF well under a megabyte. agg renders one frame per output batch, so few commands and short outputs keep the file small.

## Check without watching

- `asciinema convert -f txt proof.cast proof.txt` writes the plain transcript. Read it against the specification's THEN clauses and grep it for secrets.
- `ffmpeg -ss 5 -i proof.mp4 -frames:v 1 frame.png` writes one still. Look at it for font, theme, and window size.
- `shasum -a 256 proof.txt` is the transcript digest the proof record carries. `shasum` ships on macOS and Linux alike.

## Embed

Commit the GIF under `docs/proofs/<change>/proof.gif` and embed it:

```markdown
![Proof: <scenario titles>](docs/proofs/<change>/proof.gif)
```

The pull request's Testing section carries the same image with the commit id it proves.

A GIF loops and cannot pause with position. On a page that a person reads, play the cast instead, through the
html-tools cast player: it pauses, resumes, scrubs, and names the scene the playhead is in, from the
`# Scenario:` lines the driver prints. Vendor html-tools into the page's repository with
`python3 -m htmltools export <repo>/vendor/html-tools`, load `vendor/html-tools/runtime/cast-player.js`, put the
cast text in a `<script type="text/plain">` block, and call `CastPlayer.attach(host, castText)`. Keep the GIF
for surfaces that render images only, such as a pull request body.
