# Workflow

## Constraints

- Stop every browser session after use. A session counts against the plan's browser hours, and the
  Free plan includes 1 hour [PRICING].
- Browserbase charges for Proxies and Verified sessions [PRICING]. Without them, a site with bot
  protection can block the browser session too.
- When a page needs a login or its content is private, stop and ask the user. Do not sign in.
- Put every address in single quotes, and write any `'` in it as `%27`. An address from a page or a
  message can carry `$` or a backtick that the shell would expand.

## Blocked page fallback

A fetch tool can get blocked. The site answers HTTP 403, the tool stops at a redirect, or the tool
returns a summary instead of the page. Browserbase can still read the page. Work in a temporary
directory (`cd "$(mktemp -d)"`), then:

1. Fetch the raw page through the Browserbase Fetch API. Browserbase servers request the page, and
   no browser starts. The command writes the page to `page.html` and prints one JSON line whose
   `statusCode` is the site's answer.
   `browse cloud fetch '<url>' --allow-redirects --format raw --output page.html`
2. Turn the page into clean markdown: `defuddle parse page.html --markdown`
3. When `statusCode` is 400 or higher, or the markdown has only a few lines, the site blocked Fetch
   or the page needs JavaScript. Load the page in one browser session, save its HTML, stop the
   session, and do step 2 again:
   `browse open '<url>' --remote -s read`
   `browse get html -s read | jq -r '"<meta charset=\"utf-8\">" + .html' > page.html`
   The session returns the page body without its encoding tag, so the command adds one.
   `browse stop -s read`
4. When the session gives only a few lines too, the site needs Proxies or a Verified session. Stop
   and tell the user.

## Drive a page

Open a session, list the page's elements, act on them, and stop the session. `browse snapshot`
lists each element with a ref such as `[0-12]`, which `click` and `fill` take.

```sh
browse open '<url>' --remote -s work
browse snapshot -s work
browse click <ref> -s work
browse fill <ref> "<text>" -s work
browse screenshot -p shot.png -s work
browse stop -s work
```

## Go further

- Automation code, and which Browserbase feature fits a task: [`Features.md`](Features.md).
- The full command reference for the installed CLI: `browse skills show`.

[PRICING]: https://www.browserbase.com/pricing
