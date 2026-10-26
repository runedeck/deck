---
name: BrowserbaseToolkit
description: "Read or drive a web page in a Browserbase cloud browser with the browse CLI. USE WHEN a fetch tool is blocked (HTTP 403, a redirect it does not follow, or a summary instead of the page), a page needs JavaScript or clicks, or the user asks for Browserbase. NOT FOR driving a browser on this machine."
metadata:
    version: 0.1.0
---

# BrowserbaseToolkit

Browserbase runs Chrome browsers in the cloud, so the browser does not run on this machine. The
`browse` CLI is the interface to the platform, and Defuddle turns a saved page into clean markdown.

## Prerequisites

- `browse`, `defuddle`, `jq`, and `BROWSERBASE_API_KEY` in the environment. When one is missing, or
  `browse cloud projects list` fails, do the steps in [`INSTALL.md`](INSTALL.md).

## Instructions

Read [`Workflow.md`](Workflow.md) and do its steps: the constraints first, then the blocked page
fallback or Drive a page.

## Verification

- The markdown contains the page's main text, and no navigation bar or footer.
- After a browser session, the `browserbaseSessionUrl` that `browse open` printed shows the replay,
  and `browse cloud sessions list` shows the session as `COMPLETED`. Fetch starts no session.

## Troubleshooting

[`Troubleshooting.md`](Troubleshooting.md) maps each error whose message names the wrong cause to
the real cause.

## References

- The vendor's skill file, the full command reference: <https://browserbase.com/SKILL.md>.
  `browse skills show` prints the copy that matches the installed CLI.
- Defuddle: <https://github.com/kepano/defuddle>
