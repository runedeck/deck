# Stagehand V4

Stagehand V4 changed how a script starts, where the methods live, and how caching works. V3 code
fails on the V4 SDK. The migration guide [STAGEMIGRATE] is the source for every rule here.

## Start a script

Get a browser from a factory, then give it to Stagehand. Python and Go use the same shape.

```ts
import { browserbase, Stagehand } from "@browserbasehq/stagehand";

const browser = await browserbase.launch({ apiKey: process.env.BROWSERBASE_API_KEY });
const stagehand = await Stagehand.create({ browser });
```

Use `localBrowser.launch()` for a browser on your machine. Use `browserbase.connect({ apiKey,
sessionId })` to attach to a session that already runs.

## Write the steps

- Call `act`, `extract`, and `observe` on the Stagehand instance. Pass `{ page }` to target
  another tab.
- `extract` takes the instruction and the schema as two separate arguments.
- Every method returns the result in `.data`, plus metadata.
- Use `page.locator()` and `page.goto()` where a selector is stable. Spend a model call only where
  the page needs judgement.
- Pass dynamic or secret values through the `variables` option of `act` and `observe`, so the
  instruction text stays stable.
- Call `browser.close()` when the run ends. Stagehand closes only the browsers that it launched
  itself.

## Models and caching

- Omit `model` and Model Gateway picks a model on a Browserbase browser. Pass `model: { modelName,
  apiKey }` to use your own provider. Model names always carry a provider prefix.
- Caching runs on Browserbase's servers and is on by default. Pass `{ cache: false }` to skip it
  for one call. There is no local cache directory.

## What V4 removed

- **`new Stagehand({ env })`, then `init()`:** now `browserbase.launch()` or
  `localBrowser.launch()`, then `Stagehand.create({ browser })`.
- **`stagehand.page`:** now `await browser.context.activePage()`.
- **`page.act(...)`:** now `stagehand.act(...)`.
- **`stagehand.agent()`:** now a script, or a tool-calling loop that you own.
- **`modelName`, `modelClientOptions`:** now `model: { modelName, apiKey }`.
- **`serverCache`:** now `cache`.
- **`enableCaching`, `cacheDir`:** nothing. Caching is server-side.

Read the V4 pages that the docs index lists before you write code [STAGEDOCS].

[STAGEMIGRATE]: https://docs.stagehand.dev/v4/migrations/v3.md
[STAGEDOCS]: https://docs.stagehand.dev/llms.txt
