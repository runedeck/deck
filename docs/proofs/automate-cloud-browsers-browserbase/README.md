---
type: proof
change: automate-cloud-browsers-browserbase
recorded: 2026-10-27
transcript: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
scenes:
- scenario: automate-cloud-browsers-browserbase#lightest-feature-answers-the-task/user-needs-page-content-without-interaction
  kind: unproven
- scenario: automate-cloud-browsers-browserbase#blocked-page-fallback/own-fetch-tool-returns-a-summary
  kind: unproven
- scenario: automate-cloud-browsers-browserbase#blocked-page-fallback/platform-fetch-cannot-read-the-page
  kind: unproven
- scenario: automate-cloud-browsers-browserbase#read-page-arrives-as-clean-markdown/fetched-page-carries-navigation-and-a-footer
  kind: unproven
- scenario: automate-cloud-browsers-browserbase#page-address-stays-literal/hostile-address-names-the-key-variable
  kind: unproven
- scenario: automate-cloud-browsers-browserbase#blocked-page-stops-for-the-user/blocked-page-asks-for-a-login
  kind: unproven
- scenario: automate-cloud-browsers-browserbase#stagehand-code-matches-the-current-major-version/user-asks-for-a-stagehand-script
  kind: unproven
- scenario: automate-cloud-browsers-browserbase#one-secret-identifies-the-project/template-asks-for-a-project-identifier
  kind: unproven
- scenario: automate-cloud-browsers-browserbase#misleading-errors-name-their-real-cause/model-call-fails-after-the-browser-session-started
  kind: unproven
- scenario: automate-cloud-browsers-browserbase#command-reference-stays-upstream/reviewer-lists-the-skill-directory
  kind: unproven
---

# Proof: automate-cloud-browsers-browserbase

One scene per scenario, in closure order. The candidate is `runes/development/skills/BrowserbaseToolkit/scripts/read-page`, which reads one web page as clean markdown through Browserbase: the Fetch API first, then one cloud browser session that it always stops. Three scenes run the script against live sites. The other seven fences are empty and stay unproven until they get a scene.

The scenes need, in the shell that records them:

- `BROWSERBASE_API_KEY` in the environment. The script exits 2 without it, before it reads any address.
- Network access to `browserbase.com`: the Fetch API and the browser session both run there.
- `browse`, `defuddle`, and `jq` on `PATH`, installed as the skill's `INSTALL.md` says.

Each scene starts with `$ cd .`, so it runs in the repository root, where the script path resolves, instead of the runner's scratch directory. The runner captures stdout and stderr on one stream, so the markdown and the status line the script writes to stderr appear together in the transcript.

Two scenes depend on what the site does on the day of the recording:

- `platform-fetch-cannot-read-the-page` reads `cvedetails.com`, which refuses a plain fetch. The expected status line, `read-page: read through [..]`, accepts both ends of the fallback: `read through a cloud browser session, now stopped` when the Fetch API is refused, and `read through the Fetch API, HTTP 200` on a day the site lets the Fetch API through. In the second case the recording proves `own-fetch-tool-returns-a-summary` rather than this scenario.
- `blocked-page-asks-for-a-login` reads `opengameart.org`, which blocks the Fetch API and the browser session alike. The fence elides the page title with `"[..]"`, because the title the site serves to a blocked session varies. The scene fails if the browser session does not open at all. Then the script's last line names the open error instead of the title.

Record, from the repository root, outside the command sandbox:

```sh
rune proof run automate-cloud-browsers-browserbase
```

The run writes `proof.txt` and `proof.cast` beside this file and rewrites the frontmatter above with the head, the date, the transcript digest, and `kind: check` for each scene that passed. It exits 1 while any scene is unproven. With the seven empty fences that is the expected status, and the three filled scenes still report `ok (check)`.

## automate-cloud-browsers-browserbase#lightest-feature-answers-the-task/user-needs-page-content-without-interaction

```console
```

## automate-cloud-browsers-browserbase#blocked-page-fallback/own-fetch-tool-returns-a-summary

```console
```

## automate-cloud-browsers-browserbase#blocked-page-fallback/platform-fetch-cannot-read-the-page

```console
$# cvedetails.com refuses a plain fetch. The script tries the Fetch API, then one cloud browser session, and stops it after the read.
$ cd .
$ bash runes/development/skills/BrowserbaseToolkit/scripts/read-page 'https://www.cvedetails.com/cve/CVE-2021-44228/'
...
[..]CVE-2021-44228[..]
...
[..]Log4j[..]
...
read-page: read through [..]
```

## automate-cloud-browsers-browserbase#read-page-arrives-as-clean-markdown/fetched-page-carries-navigation-and-a-footer

```console
```

## automate-cloud-browsers-browserbase#page-address-stays-literal/hostile-address-names-the-key-variable

```console
$# An address that is not http or https is refused before anything reaches the platform.
$ cd .
$ bash runes/development/skills/BrowserbaseToolkit/scripts/read-page 'file:///etc/passwd'
? 2
read-page: only http and https addresses are read
```

## automate-cloud-browsers-browserbase#blocked-page-stops-for-the-user/blocked-page-asks-for-a-login

```console
$# opengameart.org blocks the Fetch API and the browser session alike. The script stops the session, names the page title, and exits 3 so the session stops and asks the user.
$ cd .
$ bash runes/development/skills/BrowserbaseToolkit/scripts/read-page 'https://opengameart.org/'
? 3
read-page: the Fetch API gave [..], opening one cloud browser session
read-page: the browser session page "[..]" was blocked or empty, the site may need Proxies or a Verified session
```

## automate-cloud-browsers-browserbase#stagehand-code-matches-the-current-major-version/user-asks-for-a-stagehand-script

```console
```

## automate-cloud-browsers-browserbase#one-secret-identifies-the-project/template-asks-for-a-project-identifier

```console
```

## automate-cloud-browsers-browserbase#misleading-errors-name-their-real-cause/model-call-fails-after-the-browser-session-started

```console
```

## automate-cloud-browsers-browserbase#command-reference-stays-upstream/reviewer-lists-the-skill-directory

```console
```
