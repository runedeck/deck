# Plan graph

Before a workflow run or a multi-step edit. Source: the script's `meta.phases` and each phase's `agent()` calls, or the ordered list of edits. One box per phase, model class under the name, the constraint that binds the phase under the box.

```text
 <workflow>  <args summary>                     agents ≤ <cap>   conc <n>
 ┌──────────┐   ┌────────────────┐   ┌───────────────┐   ┌──────────┐
 │ Survey   │──▶│ Repair ×n≤8    │──▶│ Verify ×n     │──▶│ Report   │
 │ plan     │   │ code           │   │ review        │   │ cheap    │
 └──────────┘   └────────────────┘   └───────────────┘   └──────────┘
   read only      edit only            findings only       URLs, paths
                  no commit, push
 run · edit a box · stop
```

After the run the same shape carries results. Counts replace `×n`, and a failed or stopped node gets its reason on a dangling line:

```text
 ┌──────────┐   ┌────────────────┐   ┌───────────────┐   ┌──────────┐
 │ Survey ✓ │──▶│ Repair 3/5 ✓   │──▶│ Verify 2 ✓    │──▶│ Report ✓ │
 │ 12 PRs   │   │ #57 #58 #61    │   │ #58 blocking  │   │          │
 └──────────┘   └───────┬────────┘   └───────────────┘   └──────────┘
                        └─ #60 head moved · #62 owner decision
```

Rules for the fill:

- Model class, not model id: plan, code, review, cheap. The id differs per harness.
- The line under a box is the phase's binding constraint, one per box.
- A phase with no fan-out has no `×`.
