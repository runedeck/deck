# State box

When behavior has states, or a decision has options. Source: an enum, a state field, or the Considered Options of a decision record. States as boxes, transitions as labeled arrows, the current or chosen state in brackets.

```text
 <subject>
 ┌───────────┐  summon   ┌───────────┐  verdict   ┌───────────┐
 │  open     │──────────▶│ reviewing │───────────▶│ [ready]   │
 └───────────┘           └─────┬─────┘            └─────┬─────┘
       ▲                       │ changes requested      │ owner merges
       └───────────────────────┘                        ▼
                                                  ┌───────────┐
                                                  │  merged   │
                                                  └───────────┘
```

For options instead of states, one column per option with the drivers as rows and `✓ ✗ ~` per cell:

```text
 decision: <title>
                     option 1      option 2      [option 3]
 driver a            ✓             ✗             ✓
 driver b            ~             ✓             ✓
 driver c            ✗             ✗             ✓
```

Rules for the fill:

- Every arrow has a label. An unlabeled transition is a missing requirement.
- The chosen option or current state is the only bracketed cell.
