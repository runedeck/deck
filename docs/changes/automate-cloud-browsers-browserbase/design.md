# Browserbase skill design

## Approach

Daily use is reading a page that a fetch tool could not read. The canon stays short and routes to the Workflow companion, which holds the constraints, the blocked page fallback, and the steps to drive a page. Automation code, the feature ladder, and the misleading errors sit in their own companions, so a session that only reads pages loads none of them.

The Claude variant replaces the canonical body. It lists the installed tools when the skill loads and hands the whole fallback to one script. The script exits with a code that names the outcome, so the session reads one line instead of following four steps.

## Layers

- `SKILL.md`: the canon for every harness. Prerequisites, then one instruction: read `Workflow.md`.
- `Workflow.md`: the shared procedure. Constraints, the blocked page fallback by hand, and the steps to drive a page.
- `claude/SKILL.md`: `mode: replace`. It injects the tool check, runs `scripts/read-page`, and links the shared companions through `claude/Workflow.md` and `claude/INSTALL.md`, which resolve to the files at the skill root.
- `Features.md`, `StagehandV4.md`, `Starters.md`, `Troubleshooting.md`: reference material that the procedure routes to.
- `INSTALL.md`: setup in the Mintlify install.md shape, checked by the `mdschema-skill-install` hook.

## Risks

- The script recognizes a blocked page by size: under 200 bytes of markdown counts as blocked or empty. A short page that is not blocked opens one browser session it did not need.
- The Fetch API does not get past most sites that refuse the session's own fetch tool. On 2026-10-25, two pages that had answered HTTP 403 to a session's fetch also answered 403 to the Fetch API. The browser session read one of them, a cvedetails.com product page, and the other, an opengameart.org page, stayed blocked. Fetch stays first because it costs no browser time, and the session does the real work on a blocked page.
- `browse get html` prints JSON with an `html` field in `browse` 0.11.3, and the field holds the page body without its encoding tag. The script adds a UTF-8 tag, because defuddle otherwise misreads characters such as "»". A change to that JSON shape breaks the browser step, and the script then exits 3.

## Commands

A requirement names a role. This table names the command behind each role, so nothing is lost when a command changes.

| Requirement | Command | Notes |
|---|---|---|
| Blocked page fallback | `browse cloud fetch <url> --allow-redirects --format raw --output page.html` | the platform's fetch, whose JSON result gives `statusCode` |
| Blocked page fallback | `browse open <url> --remote -s <name>`, `browse get html -s <name>`, `browse stop -s <name>` | one browser session, stopped after the read |
| Read page arrives as clean markdown | `defuddle parse page.html --markdown` | the converter that drops navigation and footer |
| Blocked page fallback | `bash scripts/read-page '<url>'` | the Claude variant runs the three rows above in order, with no pre-approval. Exit 0 means a page, 2 a setup gap or a refused address, 3 blocked |
| Command reference stays upstream | `browse skills show` | prints the vendor's skill file that matches the installed CLI |
| One secret identifies the project | `browse cloud projects list` | proves the key works without a project ID |
