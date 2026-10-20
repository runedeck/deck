---
max_turns: 3
allowed_tools: [Read]
---

Write the message I send to the owner about what we decided in today's meeting. Use plain words.

Meeting notes, in the order things happened:

- We looked at three ways to store eval records: SQLite, Postgres, and one JSON file per run.
- SQLite needs a migration tool. Postgres needs a running server.
- JSON files show clean diffs in code review.
- Decision: one JSON file per run, under `evals/<rune>/records/`.
- Open question: how long we keep old records.

Reply with the message only.
