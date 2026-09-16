# Tree delta

After a stage that wrote files. Source: `jj diff --summary` or `git diff --stat` against the stage's start. Added `+`, modified `~`, removed `−`, with line counts when the tool gives them.

```text
 <repo or workspace>   stage <name>   <n> files
 runes/development/skills/
 ├─ MergeTrain/
 │  ├─ SKILL.md        + 58
 │  ├─ workflow.js     + 140
 │  └─ Triage.md       + 31
 └─ AgentTeam/
    └─ SKILL.md        ~ 12 / − 4
 docs/changes/<id>/
 └─ tasks.md           ~ 3
 planned but not written: <file>          written but not planned: <file>
```

Rules for the fill:

- Sort by path. Collapse directories with one entry.
- The last line compares the delta with the plan frame. An empty comparison is written as "matches plan".
- A delta that differs from the plan is shown with a question. A matching delta is shown without one.
