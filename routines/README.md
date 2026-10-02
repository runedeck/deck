---
type: guide
---

# Routines

A routine is an operate-stage artifact: a scheduled run on a provider account. This directory holds the behavior of each Claude Code routine as one Markdown file. The provider holds only a stub.

## Stub contract

The stub in the provider stays under 20 lines before its list values. It names the file by its path in the runedeck/deck checkout and says to read it from the fetched object store of the ref in POLICY_REF. It says that the stub and the file are the only instruction sources, and that every other file in every checkout is data. It supplies the values that the file lists under `## Inputs`, one Markdown bullet for each list item.

## Value forms

A value name is upper case, as in the BuildTask placeholders, and the file names it in prose. A list value has one bullet for each item and `- None.` for an empty optional list. A repository is `owner/name`. A fork pair is `fork <- upstream`. A time zone is one IANA name. A ref is a branch name. A domain suffix is a bare domain such as `corp.example`. An acknowledgement is `<RULE>-<10 hex> <commit>`. An exclusion is `host: reason`.

## Trust

The run reads the file from the attached runedeck/deck source, and never from its working tree. The stub fetches `origin <POLICY_REF>`, where POLICY_REF is a stub value with the default `main`, so the owner can test a branch before merge. It requires `git ls-tree FETCH_HEAD -- routines/<File>.md` to print one entry with mode 100644 and type blob, and reads the file only as the output of `git cat-file blob FETCH_HEAD:routines/<File>.md`. Every bootstrap command runs with `--no-replace-objects`, so a replacement ref cannot swap the blob. These bootstrap commands run before the file and are not operations of the file. An absent path, a symbolic link, or a failed command stops the run with CONFIGURATION_FAILURE, and an untracked, ignored, or edited working-tree copy is never read. The check is in the stub, because a check inside the file could be edited away with the file. Branch protection and the review ceremony guard `main`. A POLICY_REF other than `main` is a test the owner runs by hand, and the deployed stub names `main`. Pinning by digest or signed tag and a `rune routine` command are deferred.

A routine that runs code streams it from the same `FETCH_HEAD`: `git cat-file blob FETCH_HEAD:routines/scripts/<script> | python3 -I - <args>`, after the same `ls-tree` check, from a scratch directory that is not a checkout. The `-I` flag keeps Python from importing a module from the current directory or from an environment variable, so a tracked `json.py` in a scanned checkout never runs. The working-tree copy of the script is never run, and the routine never reads repository content by another means.

## Scanner inputs

The Dotfiles Scanner and Online Mentions files take instance values that never enter the deck: the values live in the stub, and the private binding in the consumer carries them.

- SENSITIVE_DOMAINS: domain suffixes whose every hostname is an ALERT, such as an employer's internal domain. The deck carries no instance value, and a test fixture uses `corp.example`.
- KNOWN_FINDINGS: for the Dotfiles Scanner, one `<finding id> <commit>` for each line, the id from an earlier report and the scanned commit of that report. For Online Mentions, the canonical URLs from earlier reports. Known means acknowledged by the owner, not fixed: a known secret keeps its rotation action, and a known host keeps its removal action. The owner copies ids from the session report into the stub between runs. A finding id is `<RULE>-<first 10 hex of SHA-256 of the matched value>`, so the stub contains no value. An occurrence is known only when its object is reachable from the acknowledged commit. The same value in a new file, in an edited file, or in a later commit message is a new occurrence and raises the status again, and a replacement secret in a known file is a new id.
- BRANCH: the branch of the scanned repository, `main` by default.
- IDENTITY_NAMES, PUBLIC_HANDLES, OFFICIAL_URLS, QUERY_ANCHORS: the approved identity signals that attribute a page to the owner. A name alone attributes nothing.
- APPROVED_FACTS: facts the owner publishes. Their republication is not a finding.
- EXCLUSIONS: hosts that always block an unauthenticated request, with a reason, reviewed by the owner. An excluded source is not a failure, and the run never adds one.

## Shape

Every Markdown file here except this one sits directly under `routines/` and matches `routines/.mdschema`: `type: routine` in the frontmatter, one H1, then Inputs, Authority, an optional Startup checks, Scope, Permitted operations, Prohibited operations, Procedure, Status, Notification, and Final checks. A file name uses only the characters `A-Za-z0-9._-`. The `mdschema-routines` hook checks each file before a commit and rejects a Markdown file in a subdirectory or with another character in its name. Code that a routine streams sits under `routines/scripts/`, uses the Python standard library only, and has its tests under `tests/`, which the `exposure-scan-tests` hook runs.

## Files

- [RepositoryDigest.md](RepositoryDigest.md): daily read-only digest of the repositories the stub lists.
- [WeeklyCeremonyAudit.md](WeeklyCeremonyAudit.md): weekly drift audit with one comment on a standing issue.
- [DotfilesScanner.md](DotfilesScanner.md): daily exposure scan of one public repository through [scripts/exposure_scan.py](scripts/exposure_scan.py), the deterministic detector that decides the findings and the finding status.
- [OnlineMentions.md](OnlineMentions.md): weekly identity-qualified web search for exposures, impersonation, and aggregated profiles.

The GitHub Exposure routine is retired: the provider's proxy refuses every GitHub path outside an attached source, so an account-wide scan has no subject there. The ConfigureScanners skill under `runes/security/` keeps the ChatGPT scanner templates and the older Claude repository template, and its overlap with these files is an open task of the scanner-routines-from-deck change.
