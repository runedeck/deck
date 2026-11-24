# Canon runs

These recordings run a skill's eval suite with `scripts/eval-rune --canon`, which removes the skill's Claude Code variant before assembly. Each one sits beside the run of the assembled skill in the parent directory, so the two show whether the variant earns its place.

- `SafetyFirst.cast` and `SafetyFirst.gif`: the canon alone scores 0.44, against 0 with the variant. The variant is removed in this change.
- `FullSend.cast` and `FullSend.gif`: the canon alone scores 0.5, against 0.75 with the variant. The variant stays.
