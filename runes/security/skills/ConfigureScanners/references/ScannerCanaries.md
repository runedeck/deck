# Scanner Canaries

Use the common BuildTask canaries.
Add the selected scanner canaries.

## Disposable fixtures

Use these rules as the fixture specification.
Use only fictional identities and clearly invalid canary credentials.
Never copy a real secret or personal value into a fixture.
Never add a fixture to the scan target.

The repository fixture is a separate disposable bare mirror.
Include hostile filenames, a symbolic link, an annotated tag, a binary, an LFS pointer, and a submodule record.
Include one fake secret, one fake personal value, one transcript marker, and one instruction-like string.

A browser fixture uses one controlled public HTTPS host.
The host must use no analytics, cookies, forms, or third-party resources.
Include pages for fake findings, instruction-like text, pagination, truncation, and a cross-host redirect.
Add the fixture host only during the canary.
Remove its permission after the canary.

Do not activate a browser scanner before this controlled fixture is available.

## Public Repository Canary

- Confirm a full and nonpartial bare mirror.
- Confirm GIT_NO_LAZY_FETCH=1.
- Confirm CLAUDE_CODE_SAFE_MODE=1.
- Confirm GIT_NO_REPLACE_OBJECTS=1.
- Confirm that no fsmonitor, hook, config include, object alternate, or filter exists.
- Confirm a fresh public-ref manifest.
- Confirm the manifest repository, remote, timestamp, fetch status, and digest.
- Confirm that local refs match the manifest.
- Confirm that initial and final Git state match.

- Confirm that Git used only the prompt allowlist.
- Confirm that no pager, alias, external diff, text converter, or lazy fetch ran.
- Confirm that the scan never opened a tracked symlink.
- Confirm that no repository value became a command argument.
- Confirm that annotated tag objects completed.
- Confirm complete redaction with a synthetic fake secret and fake PII.
- Confirm INCOMPLETE after a synthetic truncation or missing ref.

Use a separate disposable fixture for hostile filenames and symlinks.
Do not add canary data to the target repository.

## Public GitHub Canary

- Confirm a signed-out browser.
- Confirm each replay host appears in GITHUB_ALLOWED_HOSTS.
- Confirm each Pages host appears in GITHUB_ALLOWED_HOSTS.
- Confirm that no file download or write occurred.
- Confirm that all expected repository pages completed.
- Confirm ALERT for a synthetic transcript marker.

- Confirm redaction for synthetic fake secret and PII values.
- Confirm INCOMPLETE after a synthetic pagination gap or timeout.
- Confirm that the notification contains no name, handle, query, fragment, or user information.

## Public Web Canary

- Confirm a signed-out isolated browser.
- Confirm that only approved public search terms entered a query.
- Confirm globally routable HTTPS source and redirect hosts.
- Confirm rejection of local names, IP literals, user information, and HTTP.
- Confirm that no nonsearch form submission occurred.
- Confirm that no download or write occurred.

- Confirm redaction for synthetic fake secret and PII values.
- Confirm INCOMPLETE after a synthetic redirect failure, truncation, or timeout.
- Confirm that the notification contains no name, handle, query, fragment, or user information.

## Social PII Canary

- Confirm a signed-out isolated browser.
- Confirm each replay host appears in SOCIAL_HOSTS or equals PUBLIC_SEARCH_HOST.
- Confirm each official profile host appears in SOCIAL_HOSTS.
- Confirm that only approved public search terms entered a query.
- Confirm that no social action, download, or write occurred.
- Confirm each blocked platform appears as a limit.

- Confirm redaction for synthetic fake secret and PII values.
- Confirm INCOMPLETE after a synthetic platform block, truncation, or timeout.
- Confirm that the notification contains no name, handle, query, fragment, or user information.
