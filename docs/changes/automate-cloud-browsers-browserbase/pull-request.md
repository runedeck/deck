Add the BrowserbaseToolkit skill to the development domain: read a blocked page through a Browserbase cloud browser as clean markdown.

## Plan

A session's own fetch tool gets blocked: HTTP 403, a redirect it does not follow, or a summary instead of the page. Without help, Opus 5.5, Fable 5.1, and Haiku 5.5 also wrote Stagehand V3 code, asked for a project ID, and opened a browser where Fetch would do. The skill keeps daily use short: a canon that routes to the Workflow companion, a Claude variant that runs one script, and the technical detail in companions that daily reading never loads.

## Changes

- Add `runes/development/skills/BrowserbaseToolkit/` with `SKILL.md`, `Workflow.md`, `Features.md`, `StagehandV4.md`, `Starters.md`, `Troubleshooting.md`, and `INSTALL.md` in the Mintlify install.md shape.
- Add `claude/SKILL.md` with `mode: replace`: it injects the installed tool paths and runs `scripts/read-page`, which tries the Fetch API, then one browser session that it always stops, and prints defuddled markdown. The variant pre-approves only the tool check: the session passes the address in single quotes, and the script refuses a non-http address or one that contains the API key.
- Add the `mdschema-skill-install` hook to `.pre-commit-config.yaml`, which checks every skill `INSTALL.md` against `schemas/INSTALL.mdschema`.
- Add `docs/changes/automate-cloud-browsers-browserbase/` with proposal, delta spec, design, tasks, `adr.md`, and this body, and one `CHANGELOG.md` line.

## Testing

- [x] With the skill, Opus 5.5, Fable 5.1, and Haiku 5.5 passed every assertion in three bench cases, against 40 to 50 percent without it (`$ROOT_BENCHMARK/runedeck/BrowserbaseToolkit-deck/iteration-2/`).
- [x] Opus 5.5, Fable 5.1, and Haiku 5.5 read the skill files cold and gave the same steps. This change fixes what they found unclear.
- [x] `scripts/read-page` read a cvedetails.com page that refused a fetch tool, through a browser session, and reported an opengameart.org page as blocked with its "Access denied" title.
- [x] `jj push --dry-run` replays both prek stages with `REQUIRE_GATES=1` on the head and exits 0.

## Release Notes

- Add the BrowserbaseToolkit skill: read a blocked page through a Browserbase cloud browser as clean markdown.
