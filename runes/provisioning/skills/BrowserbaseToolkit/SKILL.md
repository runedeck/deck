---
name: BrowserbaseToolkit
description: "Drive real Chrome browsers in the cloud with Browserbase and the browse CLI: automate, scrape, fill forms, and run browser agents (Stagehand V4, the Agents API), plus Fetch, Search, Sessions, Contexts, and Functions. USE WHEN automating or scraping a website, driving a headless/cloud browser, using Browserbase or the browse CLI or Stagehand, migrating Stagehand V3 code to V4, fetching a page's content, web search for URLs, filling a web form programmatically, or deciding which browser-automation capability to use."
metadata:
    version: 0.2.0
---

# BrowserbaseToolkit

Browserbase runs real Chrome browsers in the cloud. Your code or your agent drives them, so no
browser runs on your machine. The `browse` CLI talks to the platform. Stagehand drives a page with
plain-language instructions where selectors break.

The upstream command reference is <https://browserbase.com/SKILL.md>.
[`Troubleshooting.md`](Troubleshooting.md) maps misleading errors to their real causes.

## Prerequisites

- Node.js for the `browse` CLI. Stagehand V4 needs Node.js 22.18, Python 3.11, or Go 1.26 or
  later [STAGEINSTALL].
- One secret: `BROWSERBASE_API_KEY`. The key alone identifies the project.
- Install the CLI and check access:

```sh
npm install -g browse@latest
export BROWSERBASE_API_KEY=bb_live_<your-key>
browse cloud projects list
```

## Constraints

- Do not set `BROWSERBASE_PROJECT_ID` and do not pass a `projectId`. Older docs that require it
  are out of date.
- Do not put the API key in a chat, a log, or a tracked file. Keep it in the local environment or
  a secret store.
- On the Free plan, leave provider keys such as `MODEL_API_KEY` empty. A placeholder value sends a
  bad key to the provider, and the error looks like a broken Browserbase key.
- Proxies and Verified sessions are paid features [PRICING]. A plain session on a bot-protected
  site gets blocked.
- Do not write Stagehand V3 code. V4 removed `new Stagehand({ env })`, `init()`, `agent()`, and
  `cacheDir` [STAGEMIGRATE].

## Instructions

### Choose a capability

Use the lightest capability that answers the task.

- **Fetch:** you need page content without JavaScript or interaction. No browser starts.
- **Search:** you need URLs or ranked web results for a query.
- **Stagehand:** you script the steps and want `act`, `extract`, and `observe` over selectors.
- **Agents API:** you state a goal in plain words and a hosted agent picks the steps.
- **Sessions over CDP:** the project already uses Playwright, Puppeteer, or Selenium.
- **Contexts:** a run must reuse a login or cookies.
- **Functions:** the automation runs in Browserbase's cloud on a schedule or a webhook. TypeScript
  only.
- **Model Gateway:** the code calls a model through the Browserbase key instead of a provider key.

### Write Stagehand V4 code

Read [`StagehandV4.md`](StagehandV4.md) before you write or change Stagehand code. A script gets a
browser from `browserbase.launch()` and passes it to `Stagehand.create()` [STAGEMIGRATE]. Then
read the V4 pages that the docs index lists for the task [STAGEDOCS].

### Start from a template or a catalog skill

- `browse templates list` shows the starters. Slugs change, so check the list before you clone. On
  2026-10-20 the list had `sec-filing-research`, `form-filling`, and `dynamic-form-filling`.
- `browse templates clone <slug> <dir> --language typescript` copies a starter into a folder.
- `browse skills find "<task>" --json` searches the browse.sh catalog of tested per-site
  automations. `browse skills add <domain>/<task>` installs one.

## Verification

```sh
browse cloud sessions list
```

A browser run appears as `RUNNING` or `COMPLETED`. Open its replay at
`https://www.browserbase.com/sessions/<full-id>` and keep the full ID. Fetch and Search start no
session, so a result payload is their proof.

## Troubleshooting

[`Troubleshooting.md`](Troubleshooting.md) lists symptoms whose error message names the wrong
cause: a placeholder provider key, the used-up free token allowance, bot protection, and V3 code
on the V4 SDK.

## References

- Upstream command reference: <https://browserbase.com/SKILL.md>. A local copy waits for its
  adoption review, and the deployer leaves it out until then.
- Browserbase docs: <https://docs.browserbase.com>
- Stagehand V4 docs index: <https://docs.stagehand.dev/llms.txt>

[STAGEINSTALL]: https://docs.stagehand.dev/v4/first-steps/installation.md
[STAGEMIGRATE]: https://docs.stagehand.dev/v4/migrations/v3.md
[STAGEDOCS]: https://docs.stagehand.dev/llms.txt
[PRICING]: https://www.browserbase.com/pricing
