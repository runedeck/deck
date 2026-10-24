# Starters

A project can begin from a Browserbase starter project or from a tested automation in the browse.sh
catalog. Both lists change, so read the current list before you pick one. The commands below match
the `--help` output of `browse` 0.11.3.

## Starter projects

```sh
browse templates list
browse templates find "<task>"
browse templates clone <slug> <dir> --language typescript
```

`clone` copies a ready-to-run project into the directory. Without `--language`, it takes TypeScript
when the starter has it, then Python. On 2026-10-20 the list had `sec-filing-research`,
`form-filling`, and `dynamic-form-filling`.

## Catalog skills

```sh
browse skills find "<task>" --json
browse skills add <domain>/<task>
```

Each catalog skill automates one task on one site, and its id names both, such as
`yelp.com/extract-reviews`.
