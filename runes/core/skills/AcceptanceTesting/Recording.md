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

A GIF loops and cannot pause with position. Where a person reads, the proof is a page that plays the cast
through the html-tools cast player: it pauses, resumes, scrubs, and names the scene the playhead is in, from the
`# Scenario:` lines the driver prints. Keep the GIF for surfaces that render images only, such as a pull request body.

## Page

`scripts/proof-page.py` writes the page. It inlines the player and each cast, so the file opens offline:

```sh
python3 <skill>/scripts/proof-page.py --title "<Two To Four Words>" --eyebrow "<repo>, <date>" \
    --player vendor/html-tools/runtime/cast-player.js \
    --cast <change>=docs/proofs/<change>/proof.cast \
    --caption <change>="<what the proof shows, one sentence>" \
    --meta <change>="<repo> <head>" --meta <change>="transcript sha256 <first 8>…" \
    --out <page>
```

The page lives in the owner's workshop under `docs/specs/<date>-proof-set.html`, one page per landing round, so
proofs from several repositories sit together and survive the change directories. The player comes from
`python3 -m htmltools export <repo>/vendor/html-tools`, or from a checkout of html-tools when the workshop has no
vendor directory. The handover message carries the page's absolute path.
