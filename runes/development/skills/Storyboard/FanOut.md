# Fan-out

Before parallel agents. Source: the packages, tracks, or angles the planner produced. One lane per child, its owned files or scope on the right, the join at the bottom.

```text
 <parent>  <n> children · conc <c> · isolation <workspace|none>
        ┌──────────────────────────────────────────────┐
        │ plan: <one line>                              │
        └──┬───────────┬──────────────┬─────────────────┘
           ▼           ▼              ▼
   ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
   │ <child-a>   │ │ <child-b>   │ │ <child-c>   │
   │ owns: a/    │ │ owns: b/    │ │ owns: c.md  │
   │ inherits: · │ │ inherits: a │ │ inherits: · │
   └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
          └───────────────┴───────────────┘
                          ▼
                   integrate on trunk · run suite
 confirm · edit a box · stop
```

Rules for the fill:

- Two lanes that name the same file are a defect in the plan. Redraw the plan, not the frame.
- A child that inherits from another child cannot run in the same column group. Show it as a second row.
- The join line names what happens after the children, or says "report only".
