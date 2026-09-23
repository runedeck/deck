# Decision records design

## Commands

A requirement names a role. This table names the path, script, or schema behind each row, so nothing is lost when a path moves out of a requirement.

| Requirement | Command | Notes |
|---|---|---|
| Record Per Decision | `docs/decisions/` | the decisions directory that stores every dated record |
| Record lives in its change until archive | `docs/decisions/` | the archiver moves `adr.md` here and assigns the id |
| Change and record link both ways | `docs/decisions/` | the link check reads records from this directory |
| Record ids are never reused | `scripts/check-decision-numbers` | the validator that fails on a shared id and reports both files |
| Directory schema runs on every record | `docs/decisions/.mdschema` | the directory schema that the commit stage and CI run against every record |
