# Change map

The first frame inside a change. Source: `rune spec context <id>` and `tasks.md`. Brackets mark the current stage. Task lines show the first open task per section and the tick count.

```text
 ┌ change: <id> ──────────────────────────────────────────────────────┐
 │ prompt · pushback · specify · isolate · [swarm] · gates · skim ·     │
 │ lanes · babysit · approve · extract · recycle                        │
 │                                                                      │
 │ capabilities  <cap-a>  <cap-b>                                       │
 │ adr           <PREFIX>-<NNNN> <Title>            status <proposed>   │
 │                                                                      │
 │ 1 authoring     3/9   next 1.4 <task text, truncated at 50>           │
 │ 2 review        1/2   next 2.2 <task text>                            │
 │ 3 verification  0/4   next 3.1 <task text>                            │
 │ 4 deferred      0/5                                                   │
 │                                                                      │
 │ this turn: <one line naming what will be written or run>             │
 └──────────────────────────────────────────────────────────────────────┘
 confirm · edit a box · stop
```

Rules for the fill:

- The stage comes from ForgeCycle's Stages.md location rules, never from the last thing discussed.
- A section with every task ticked shows its count and no next task.
- "this turn" is the only line that carries a plan. Everything above it is data.
