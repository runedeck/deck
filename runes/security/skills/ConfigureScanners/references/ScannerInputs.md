# Scanner Inputs

Use only approved public values.
Apply the BuildTask placeholder rules.

## Common Inputs

TIME_ZONE is required.
Use the time-zone type.
Use Europe/Prague when the user accepts the default.

ACCEPTED_PUBLIC_FACTS is optional.
Use a public-fact list.
Set the minimum item count to zero.
Render an empty list as `- None.`.

## Public Repository Inputs

GITHUB_REPOSITORY is required.
Use the repository type.

GITHUB_OWNER is required.
Use one GitHub login.
Require the repository owner to match this login.

## Public Repository Environment

Set these static values:

- CLAUDE_CODE_SAFE_MODE=1
- GIT_NO_LAZY_FETCH=1
- GIT_OPTIONAL_LOCKS=0
- GIT_NO_REPLACE_OBJECTS=1
- GIT_ATTR_NOSYSTEM=1
- GIT_TERMINAL_PROMPT=0

- GIT_CONFIG_COUNT=0
- GIT_CONFIG_PARAMETERS is empty
- GIT_CONFIG_NOSYSTEM=1
- GIT_CONFIG_GLOBAL=/dev/null
- GIT_PAGER=cat
- PAGER=cat

- GIT_EXTERNAL_DIFF is empty
- GIT_DIR, GIT_WORK_TREE, GIT_COMMON_DIR, and GIT_INDEX_FILE are empty
- GIT_OBJECT_DIRECTORY and GIT_ALTERNATE_OBJECT_DIRECTORIES are empty
- GIT_NAMESPACE, GIT_SHALLOW_FILE, and GIT_REPLACE_REF_BASE are empty

Set these values only after trusted preparation succeeds:

- TRUSTED_REPOSITORY_PREPARED=1
- GIT_OBJECTS_ISOLATED=1
- PUBLIC_REF_FETCH_STATUS=success

Set these dynamic public values during every preparation step:

- PUBLIC_REF_MANIFEST contains sorted ref and object-ID lines
- PUBLIC_REF_MANIFEST_SHA256 contains the lowercase SHA-256 digest
- PUBLIC_REF_MANIFEST_AT contains an RFC 3339 UTC timestamp
- PUBLIC_REF_REPOSITORY contains the owner and repository
- PUBLIC_REF_REMOTE_URL contains the canonical public HTTPS GitHub URL

## Public GitHub Inputs

GITHUB_OWNER is required.
Use one GitHub login.

GITHUB_ALLOWED_HOSTS is required.
Use a host list with at least four items.
Include github.com, api.github.com, raw.githubusercontent.com, and gist.github.com.

GITHUB_PAGES_URLS is optional.
Use an HTTPS URL list.
Set the minimum item count to zero.
Require each URL host in GITHUB_ALLOWED_HOSTS.

PUBLIC_HANDLES is optional.
Use a handle list.
Set the minimum item count to zero.

## Public Web Inputs

PUBLIC_SEARCH_HOST is required.
Use one host.

IDENTITY_NAMES is optional.
Use a public-name list.
Set the minimum item count to zero.

PUBLIC_HANDLES is optional.
Use a handle list.
Set the minimum item count to zero.

Require at least one nonempty list.
Require two public identity signals for each ambiguous name.

OFFICIAL_URLS is optional.
Use an HTTPS URL list.
Set the minimum item count to zero.

## Social PII Inputs

SOCIAL_HOSTS is required.
Use a host list with at least one item.

PUBLIC_SEARCH_HOST is required.
Use one host.

IDENTITY_NAMES is optional.
Use a public-name list.
Set the minimum item count to zero.

PUBLIC_HANDLES is optional.
Use a handle list.
Set the minimum item count to zero.

Require at least one nonempty list.
Require two public identity signals for each ambiguous name.

OFFICIAL_SOCIAL_PROFILES is optional.
Use an HTTPS URL list.
Set the minimum item count to zero.
Require each profile host in SOCIAL_HOSTS.
