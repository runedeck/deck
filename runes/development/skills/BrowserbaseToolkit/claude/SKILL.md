---
mode: replace
allowed-tools: 'Bash(which -a browse defuddle jq 2>/dev/null | head -c 600), Bash(bash "${CLAUDE_SKILL_DIR}/scripts/read-page" *)'
---

# BrowserbaseToolkit

## Prerequisites

!`which -a browse defuddle jq 2>/dev/null | head -c 600`

Each of `browse`, `defuddle`, and `jq` needs a path above. When one is missing, or `browse` shows a
path outside `~/.bun/bin`, do [`INSTALL.md`](INSTALL.md) first. A literal command line above means
the check did not run: run `which -a browse defuddle jq` yourself.

## Instructions

Read the constraints in [`Workflow.md`](Workflow.md) before the first browser session.

For a blocked page (HTTP 403, a redirect the fetch tool does not follow, or a summary instead of
the page), run:

`bash "${CLAUDE_SKILL_DIR}/scripts/read-page" <url>`

The script checks the key, tries the Fetch API, then one browser session that it always stops, and
prints the page as clean markdown. Exit 2 means a missing tool or key: do `INSTALL.md`. Exit 3
means the site blocked Browserbase too: tell the user. Any other exit: report its stderr. When the
markdown shows a login form or private content, stop and ask the user.

To click, fill, or take a screenshot, do Drive a page in `Workflow.md`.

## Verification

The script exits 0, and the markdown contains the page's main text, and no navigation bar or
footer.
