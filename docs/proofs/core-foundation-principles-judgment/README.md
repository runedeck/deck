---
type: proof
change: plain-text-first-principles
recorded: 2026-09-25
transcript: ea3ea868794716f32d73b76fe6a5f321b2b197248ad15b3c25ed0e8a1e3c1c44
scenes:
  - scenario: plain-text-is-futureproof#plain-text-representation/database-is-rebuilt-from-plain-text
    kind: instruction
    model: claude-opus-5-5
  - scenario: directories-direct-the-tools#directories-direct/content-goes-into-a-catch-all-directory
    kind: instruction
    model: claude-opus-5-5
  - scenario: ceremony-matches-the-task#ceremony-matches-the-task/small-fix-arrives-with-full-ceremony
    kind: instruction
    model: claude-opus-5-5
  - scenario: single-source-of-truth#code-is-truth/comment-restates-the-code
    kind: instruction
    model: claude-opus-5-5
  - scenario: single-source-of-truth#one-home-per-fact/fact-appears-in-a-second-file
    kind: instruction
    model: claude-opus-5-5
---

# Behavior proof: plain-text-first-principles, judgment scenarios

`record.sh` holds the five scenarios whose THEN is a review judgment. Each scene gives one requirement and one changed fixture to a model through `rune run claude --model claude-opus-5-5 --clean`, so the model sees the requirement, the fixture, and nothing from any user's harness state, and asks for one review marker line. The scene expects an `[ISSUE]` marker that names the fix the requirement calls for, and the model id the run resolved. A model's answer is not deterministic, so the expectation is the marker and the fix's key words, and a rerun with another model is another proof.

The recording was made on the host, where the harness login lives, with asciinema on a real pty. `proof.cast` is the cast, `proof.txt` the transcript, and `proof.gif` the render by agg.

Transcript digest (`shasum -a 256 proof.txt`): `ea3ea868794716f32d73b76fe6a5f321b2b197248ad15b3c25ed0e8a1e3c1c44`

Re-record, from the repository root, outside the command sandbox:

```sh
asciinema rec --command 'bash docs/proofs/core-foundation-principles-judgment/record.sh' --headless --window-size 100x30 --idle-time-limit 2 --overwrite --return docs/proofs/core-foundation-principles-judgment/proof.v3.cast
```

then `asciinema convert -f asciicast-v2`, `asciinema convert -f txt`, and `agg --theme github-dark --font-size 14 --line-height 1.3 --fps-cap 10 --idle-time-limit 2`. Set `PROOF_MODEL` to record with another model.
