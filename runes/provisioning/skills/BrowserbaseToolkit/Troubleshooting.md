# Troubleshooting

Symptom-first fixes for Browserbase failures whose error message points at the wrong cause. The
upstream reference (<https://browserbase.com/SKILL.md>) covers CLI mechanics such as a missing key or an unknown
flag. This file covers the traps where the message misleads.

- **"API key not valid" or "Incorrect API key provided" from a model call, while the browser
  session started fine.** Cause: a placeholder provider key in `.env`
  (`MODEL_API_KEY=your_api_key_here`) overrides Model Gateway, so Stagehand sends the placeholder to
  the provider. Fix: empty every provider key so model calls go through the Browserbase key (snippet
  below).
- **Model calls start to fail in a script that worked before, and sessions still start.** Cause:
  the Free plan's Model Gateway allowance of 5 USD in tokens [PRICING] is used up, and no warning comes
  first. Fix: use your own model key, remove the model calls (below), or upgrade. Say "the free
  token allowance is used up", not "the plan is broken".
- **`new Stagehand(...)`, `init()`, or `agent()` fails after an SDK upgrade.** Cause: Stagehand V4
  made the constructor private and removed `init()` and `agent()` [STAGEMIGRATE]. Fix: launch a
  browser with `browserbase.launch()`, pass it to `Stagehand.create()`, and replace `agent()` with a
  script or your own tool loop. See [`StagehandV4.md`](StagehandV4.md).
- **The session starts, but the target site blocks, loops a CAPTCHA, or never loads.** Cause: a
  bot-protected or login-walled target (LinkedIn, Instagram, Facebook, TikTok, Yelp, ticketing, most
  large retailers). Proxies and Verified are paid. The response usually names the wall: HTTP 403
  with `X-Datadome: protected`, or Cloudflare challenge markup. Fix: get the same answer from an
  unprotected source through Fetch or Search. Suggest an upgrade only when the protected site is
  required.
- **`browse cloud fetch` returns a 301 or 302 and stops.** Cause: Fetch stops at a redirect by
  default. Fix: pass `--allow-redirects`.
- **Setup stops and asks for `BROWSERBASE_PROJECT_ID`.** Cause: old docs and old training data. The
  API key alone identifies the project. Fix: do not set it and do not pass `projectId`. Leave the
  variable empty if a template includes it.

## Template `.env` hygiene

This sequence sets the real key and empties every placeholder in one pass. It is safe for BSD
`sed`, and it makes the starter templates run on the Browserbase key alone:

```sh
sed -i.bak "s|^BROWSERBASE_API_KEY=.*|BROWSERBASE_API_KEY=$BROWSERBASE_API_KEY|" .env
for V in MODEL_API_KEY OPENAI_API_KEY GOOGLE_API_KEY ANTHROPIC_API_KEY \
    AZURE_API_KEY AZURE_ENDPOINT BROWSERBASE_PROJECT_ID; do
    sed -i.bak "s|^$V=.*|$V=|" .env
done
rm -f .env.bak
```

## Past the token cap: two real exits

- **Use your own model key.** Pass `model: { modelName: "<provider>/<model>", apiKey }` to
  `Stagehand.create()`. Model names always carry a provider prefix [STAGEMIGRATE]. The browser
  stays on Browserbase, and the provider bills the model calls.
- **Remove the model calls.** Replace `act` and `extract` steps with `page.locator()` and
  `page.goto()` on the same Stagehand page. This uses no model tokens and works on Free, but it
  breaks more easily when the page changes.

## Escalation order for a blocked site

Try the cheapest option first: `browse cloud fetch <url>` (no browser, no tokens). Next, use
`browse cloud search "<query>"` to find another source. Next, use a plain session on an unprotected
copy of the data. Use Proxies or Verified on a paid plan only after that.

[PRICING]: https://www.browserbase.com/pricing
[STAGEMIGRATE]: https://docs.stagehand.dev/v4/migrations/v3.md
