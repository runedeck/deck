---
max_turns: 4
allowed_tools: [Read, Glob, Grep, Skill]
---

STE rewrite this paragraph from our deploy runbook:

> Prior to deploying, you'll want to spin up a staging instance and leverage the smoke suite to validate the build; the suite runs 42 checks and typically takes about 90 seconds, though on a cold cache it can take considerably longer because the runner has to pull every container image again before any of the checks are able to start. If the last deploy failed, the migration may have left the schema in a partial state, so take a look at the migrations table before you kick off a new deploy.
