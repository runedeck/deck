# Features

Use the lightest Browserbase feature that does the task.

- **Fetch:** page content without JavaScript or clicks. No browser starts.
- **Search:** URLs or ranked web results for a query.
- **Browser session:** a page that needs JavaScript, clicks, or forms.
- **Stagehand:** Browserbase's code library for a script that steers a page with plain-language
  steps (`act`, `extract`, `observe`) instead of selectors. Read [`StagehandV4.md`](StagehandV4.md)
  before you write or change Stagehand code.
- **Agents API:** the user states a goal in plain words, and a hosted agent picks the steps.
- **Sessions over CDP (Chrome DevTools Protocol):** the project already uses Playwright, Puppeteer,
  or Selenium.
- **Contexts:** a run must reuse a login or cookies.
- **Functions:** automation that runs in Browserbase's cloud on a schedule or a webhook. TypeScript
  only.
- **Model Gateway:** code calls a model through the Browserbase key instead of a provider key.
- **Starters:** a ready-to-run starter project, or a tested automation for one site. Read
  [`Starters.md`](Starters.md).
