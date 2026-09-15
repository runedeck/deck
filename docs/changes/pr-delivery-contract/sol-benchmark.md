# Artifact Benchmark: VersionControl

## VersionControl versus no artifact

skill VersionControl · source runes/core/skills/VersionControl · sha256 8cd1d619fe73

Deltas are treatment minus baseline within one model. Lower lint density is better. Preferences run from -1 (baseline) to +1 (treatment).

| Model | Verdict | Pairs | Assertions | Lint /100w | Tokens | Clarity | Fluency | Directness |
|---|---|---:|---|---|---|---:|---:|---:|
| gpt-5.6-sol | No material improvement | 3 | 1.00 → 1.00 | 0.00 → 0.00 | — → — | — | — | — |

Verdict rule: facts must hold, findings must fall, and blind preference must stay acceptable.
Dimension settings: clarity: trade-off below 0.4, win above 0.5, weight 1 · fluency: trade-off below 0.4, win above 0.5, weight 0.5 · directness: trade-off below 0.4, win above 0.5, weight 1.

## Limitations

- Compare results only within one model.
- Lint uses heuristics and does not measure semantic quality.
- Assertions measure only their stated checks.
- Missing tokens mean the provider did not report usage.
- Invalid and excluded runs reduce the sample.
- The report does not average models.
