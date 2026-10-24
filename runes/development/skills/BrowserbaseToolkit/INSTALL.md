# browse

> The Browserbase `browse` CLI drives cloud Chrome browsers and calls the Fetch and Search APIs.
> Defuddle turns the pages it reads into clean markdown. The BrowserbaseToolkit skill uses both.

I want you to install the Browserbase `browse` CLI and Defuddle for me. Execute all the steps below
autonomously.

## OBJECTIVE

Install `browse` and Defuddle with bun, and confirm that `browse` reaches Browserbase with the
user's API key.

## DONE WHEN

`which -a browse` lists one path under `~/.bun/bin`, `defuddle --version` and `jq --version` run,
and `browse cloud projects list` lists at least one project.

## TODO

- [ ] Install bun and jq when they are missing
- [ ] Install `browse` and Defuddle with bun
- [ ] Remove an npm copy of `browse` that hides the bun copy on `PATH`
- [ ] Confirm that `BROWSERBASE_API_KEY` is set
- [ ] Verify access to Browserbase

## Steps

### 1. Install bun and jq

On macOS, use Homebrew. On another system, install bun from <https://bun.sh> and jq from the system
package manager.

```sh
command -v bun >/dev/null 2>&1 || brew install oven-sh/bun/bun
command -v jq >/dev/null 2>&1 || brew install jq
```

### 2. Install the tools with bun

The `defuddle-cli` package gives the `defuddle` command.

```sh
bun add -g browse@latest defuddle-cli@latest
```

### 3. Remove an npm copy

An npm copy in the Homebrew prefix can come before `~/.bun/bin` on `PATH` and hide the bun copy.
When `which -a browse` lists a path outside `~/.bun/bin`, remove the npm copy:

```sh
npm uninstall -g browse
```

### 4. Confirm the key

You need one secret, `BROWSERBASE_API_KEY`. Keep it in the environment or a secret store, never in
a chat, a log, or a tracked file. The key alone resolves the default project, so do not ask for a
project ID. Set `BROWSERBASE_PROJECT_ID` only to pin a non-default project on a key with several
projects. Check the key without printing it:

```sh
[ -n "$BROWSERBASE_API_KEY" ] && echo "set" || echo "not set"
```

When the key is not set, stop and ask the user to put it in the environment.

### 5. Verify access

```sh
which -a browse
defuddle --version
jq --version
browse cloud projects list
```

EXECUTE NOW: Complete the above TODO list to achieve: `which -a browse` lists one path under
`~/.bun/bin`, `defuddle --version` and `jq --version` run, and `browse cloud projects list` lists at
least one project.
