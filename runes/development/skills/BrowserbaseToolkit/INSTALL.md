# browse

> The Browserbase `browse` CLI drives cloud Chrome browsers and calls the Fetch and Search APIs.
> The BrowserbaseToolkit skill uses it for every Browserbase task.

I want you to install the Browserbase `browse` CLI for me. Execute all the steps below autonomously.

## OBJECTIVE

Install the `browse` CLI with bun and confirm that it reaches Browserbase with the user's API key.

## DONE WHEN

`browse --version` runs the copy you installed, and `browse cloud projects list` lists at least one
project.

## TODO

- [ ] Install `browse` with bun
- [ ] Remove an npm copy that hides the bun copy on `PATH`
- [ ] Confirm that `BROWSERBASE_API_KEY` is set
- [ ] Verify access to Browserbase

## Steps

### 1. Install the CLI

You must install with bun. When bun is missing, install bun first. On macOS, use Homebrew:

```sh
command -v bun >/dev/null 2>&1 || brew install oven-sh/bun/bun
bun add -g browse@latest
```

### 2. Remove an npm copy

An npm copy in the Homebrew prefix can come before bun's `~/.bun/bin` on `PATH` and hide the bun
copy. List every copy:

```sh
which -a browse
```

When the list shows a path outside `~/.bun/bin`, remove the npm copy:

```sh
npm uninstall -g browse
```

### 3. Confirm the key

You need one secret, `BROWSERBASE_API_KEY`. The key alone resolves the default project, so do not
ask for a project ID. Check the key without printing it:

```sh
[ -n "$BROWSERBASE_API_KEY" ] && echo "set" || echo "not set"
```

When the key is not set, stop and ask the user to put it in the environment. Do not ask for the
key in the chat.

### 4. Verify access

```sh
browse --version
browse cloud projects list
```

EXECUTE NOW: Complete the above TODO list to achieve: `browse --version` runs the copy you
installed, and `browse cloud projects list` lists at least one project.
