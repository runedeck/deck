---
type: spec
---

## ADDED Requirements

### Requirement: Detector decides findings and status in code

The Dotfiles Scanner MUST obtain every finding, every finding id, every count, the finding status, and the scan health from `routines/scripts/exposure_scan.py`, and the run MUST NOT change them. The detector MUST read the repository through Git objects only, with `--no-replace-objects`, no hooks, no pager, no lazy fetch, no external diff, and no filters, and MUST NOT open the working tree or run repository content. The detector MUST use the Python standard library only.

#### Scenario: Working tree differs from the fetched ref

- **WHEN** an untracked file in the checkout contains a token that no reachable blob contains
- **THEN** the detector reports no finding for it and the health counts are unchanged

#### Scenario: Secret exists only in deleted history

- **WHEN** a blob with a token was committed and a later commit removed the file
- **THEN** the finding lists the path, the line, the commit that contains the blob, and the blob id

### Requirement: Finding identity hides the value

A finding id MUST be the rule code plus the first ten hexadecimal digits of the SHA-256 of the matched value, and the matched value MUST NOT appear in the detector output. Matches with the same rule and value MUST form one finding with every location, one for each path of each object. The detector MUST redact a path segment that matches a rule and MUST give each location a context line in which every match is replaced.

#### Scenario: Same host appears in several blobs

- **WHEN** one hostname matches in three blobs across two commits
- **THEN** the output has one finding with three locations and the hostname is absent from the output

#### Scenario: Same blob sits at two paths

- **WHEN** one blob with a match is tracked at two paths
- **THEN** the finding lists both paths

#### Scenario: Path contains a sensitive hostname

- **WHEN** a file named after a hostname under a SENSITIVE_DOMAINS suffix contains that hostname
- **THEN** the location path is `[REDACTED]`, the context is `[REDACTED]`, and the blob id identifies the file

### Requirement: Finding status is separate from scan health

The detector MUST report the finding status as `ALERT` when a new occurrence of a secret or of a sensitive-domain host exists, `REVIEW` when the only new occurrences are personal data or private-TLD hosts, and `NO_NEW_FINDINGS` otherwise. The detector MUST report health apart from status: commit and blob counts, the shallow boundary, binary and oversize blobs, unreadable objects, and acknowledged commits absent from the clone. A shallow clone MUST be a declared limit, and health MUST be `INCOMPLETE` only for an unreadable object, an absent acknowledged commit, or a malformed entry.

#### Scenario: Clone is shallow

- **WHEN** the repository is a depth-one clone
- **THEN** the health reports `shallow` as true and the boundary commit, and the health status is `COMPLETE`

#### Scenario: Sensitive domain appears in a known file

- **WHEN** a hostname under a SENSITIVE_DOMAINS suffix appears in an object that no acknowledgement covers
- **THEN** the status is `ALERT`, whether or not other findings in the same file are known

### Requirement: Acknowledgement binds to a commit

A KNOWN_FINDINGS entry MUST be `<finding id> <commit>`, and an occurrence MUST be known only when its object is reachable from that commit. An occurrence in any other object MUST be new and MUST raise the status by its rule. A known occurrence MUST NOT raise the status.

#### Scenario: Every finding is acknowledged at the scanned commit

- **WHEN** KNOWN_FINDINGS lists every finding id with the scanned commit
- **THEN** the status is `NO_NEW_FINDINGS`, the known count equals the finding count, and the health is unchanged

#### Scenario: Acknowledged value appears in a new file

- **WHEN** a token acknowledged at an earlier commit is committed into another file after that commit
- **THEN** the finding keeps its id, lists the earlier location as known and the new one as new, and the status is `ALERT`

#### Scenario: Acknowledged commit is absent from the clone

- **WHEN** a KNOWN_FINDINGS entry names a commit the clone does not contain
- **THEN** the health is `INCOMPLETE`, the commit is listed, and the finding is new

### Requirement: Scanner routines stream the detector from the deck

The Dotfiles Scanner MUST run the detector only as `git --no-replace-objects cat-file blob FETCH_HEAD:routines/scripts/exposure_scan.py` piped into `python3 -I -`, from a scratch directory that is not a checkout, after `git ls-tree FETCH_HEAD -- routines/scripts/exposure_scan.py` printed one entry with mode 100644 and type blob, and MUST NOT run the working-tree copy. The run MUST pass SENSITIVE_DOMAINS and KNOWN_FINDINGS as files, never as command arguments, and MUST NOT read repository content by any other means than the detector output. The run MAY add review items for personal data the rules cannot see, each with a path, a line, a commit, and a blob id, and such an item MUST NOT change the detector status.

#### Scenario: Checkout tracks a module named like the standard library

- **WHEN** the scanned checkout tracks `json.py` at its root
- **THEN** the detector imports the standard library `json` and the tracked file never runs

#### Scenario: Script is absent from the fetched ref

- **WHEN** `ls-tree FETCH_HEAD -- routines/scripts/exposure_scan.py` prints no entry
- **THEN** the run reports CONFIGURATION_FAILURE and stops

### Requirement: Stub reads the ref in POLICY_REF

The stub MUST fetch `origin <POLICY_REF>`, where POLICY_REF is a stub value whose default is `main`, and MUST read the routine file and any streamed script from that `FETCH_HEAD`. The deployed stub MUST name `main`. A routine file MUST NOT fetch again in the runedeck/deck checkout. The Dotfiles Scanner stub MUST carry BRANCH, the branch of the scanned repository, with the default `main`.

#### Scenario: Scanned repository uses another default branch

- **WHEN** the stub carries `BRANCH: trunk`
- **THEN** the run fetches `origin trunk` of REPOSITORY and scans its `FETCH_HEAD`

#### Scenario: Owner tests a branch

- **WHEN** the stub carries `POLICY_REF: routines/scanners` and the branch exists on origin
- **THEN** the run reads the routine file and the detector from that branch and reports which runedeck/deck commit it used

### Requirement: Reports separate the push from the session

A scanner MUST send a notification of at most three lines: the finding status with the health, the new and known counts, and the most urgent action, with a finding id and no value, path, URL, name, handle, or query. The session report MUST carry one table with id, new or known, rule or classification, location, and action, with every value redacted and a path or URL segment redacted only when it is itself sensitive.

#### Scenario: Path contains a sensitive value

- **WHEN** a finding's path contains a hostname under a sensitive domain
- **THEN** the table row shows `[REDACTED PATH]` with the blob id, and the notification shows the finding id only

### Requirement: Online Mentions attributes by identity signal

Online Mentions MUST run a fixed query plan built from PUBLIC_HANDLES, OFFICIAL_URLS, and each IDENTITY_NAMES item paired with each QUERY_ANCHORS item, MUST attribute a page to the owner only when it contains a handle, an official URL, or a name together with an anchor, and MUST discard every other page without recording its details or its URL. A host in EXCLUSIONS MUST be skipped and counted as excluded, not failed, for a result URL and for a redirect destination alike.

#### Scenario: Namesake page appears in the results

- **WHEN** a result page names a person with the same name and no handle, official URL, or anchor
- **THEN** the run discards it, and the ledger and the session report contain neither its details nor its URL

#### Scenario: Excluded host appears in the results

- **WHEN** a selected result's host is in EXCLUSIONS
- **THEN** the run skips it, counts it as excluded, and the health stays `COMPLETE`

### Requirement: Online Mentions identifies a finding by canonical URL

A canonical URL MUST keep the query parameters that select the resource and drop only the fragment and tracking parameters. A page that only repeats APPROVED_FACTS MUST NOT be a finding, and the exemption MUST NOT apply to a page that also exposes, aggregates, or impersonates.

#### Scenario: Copied profile links the official URL and publishes an address

- **WHEN** an attributed page links OFFICIAL_URLS and shows the owner's home address
- **THEN** the page is an ALERT finding, not an exempt republication

#### Scenario: Two paste documents differ only by a query parameter

- **WHEN** an acknowledged leak is at `view?id=1` and a new leak at `view?id=2` on the same host and path
- **THEN** the two canonical URLs differ and the second is a new finding

### Requirement: GitHub Exposure routine is retired

The deck MUST carry no GitHub Exposure routine file, and `routines/README.md` MUST record the retirement and its reason.

#### Scenario: Owner looks for the account-wide scan

- **WHEN** the owner reads `routines/README.md`
- **THEN** it says the routine is retired because the provider proxy refuses GitHub paths outside an attached source
