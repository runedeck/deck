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

A finding MUST carry its rule name and the SHA-256 of the matched value, its id MUST be the rule name plus the first ten hexadecimal digits of that digest, and the matched value MUST NOT appear in the detector output. Matches with the same rule and value MUST form one finding with every location, one for each path of each object. The detector MUST redact a path segment that matches a rule and MUST give each location a context line in which every match is replaced.

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

The detector MUST report the finding status as `ALERT` when a new occurrence of a secret or of a sensitive-domain host exists, `REVIEW` when the only new occurrences are personal data or private-TLD hosts, and `NO_NEW_FINDINGS` otherwise.

#### Scenario: Sensitive domain appears in a known file

- **WHEN** a hostname under a SENSITIVE_DOMAINS suffix appears in an object that no acknowledgement covers
- **THEN** the status is `ALERT`, whether or not other findings in the same file are known

### Requirement: Scan health is reported apart from status

The detector MUST report health apart from status: commit and blob counts, the shallow boundary of the scanned ref, binary and oversize blobs, unreadable objects, and acknowledged commits absent from the clone. Health MUST be `INCOMPLETE` for an unreadable object, an absent acknowledged commit, or a malformed entry.

#### Scenario: Acknowledgement line is malformed

- **WHEN** an item of `.auditignore.yaml` carries an expiry that is not a date
- **THEN** the health is `INCOMPLETE` and lists that item as malformed with its line, and the status comes from the findings alone

### Requirement: Scan covers the whole history of the branch

The Dotfiles Scanner MUST fetch with `--unshallow` when the clone is shallow, so the detector sees the whole history of the branch. Health MUST be `INCOMPLETE` when the history of the scanned ref stops at a shallow boundary. A shallow boundary on another branch MUST NOT change the health.

#### Scenario: Clone is shallow

- **WHEN** the repository is a depth-one clone
- **THEN** the health reports `shallow` as true and the boundary commit, and the health status is `INCOMPLETE`

#### Scenario: Startup fetch removes the boundary

- **WHEN** the depth-one clone is fetched with `--unshallow` before the detector runs
- **THEN** the health reports `shallow` as false, counts every commit of the branch, and the health status is `COMPLETE`

#### Scenario: Another branch is shallow

- **WHEN** the scanned ref has its whole history and a commit on another branch is a shallow graft
- **THEN** the health reports `shallow` as false and an empty boundary, and the health status is `COMPLETE`

### Requirement: Acknowledgement binds to a commit

An acknowledgement MUST be an item of the `acknowledged` list in `.auditignore.yaml` with the rule name, the SHA-256 of the value, and a commit, with an optional expiry date and an optional reason. An occurrence MUST be known only when its object is reachable from that commit and the item is within its date. Any other occurrence MUST be new and MUST raise the status by its rule. A known occurrence MUST NOT raise the status.

#### Scenario: Every finding is acknowledged in the scanned tree

- **WHEN** `.auditignore.yaml` at the scanned commit lists the rule and digest of every finding with the commit of the earlier report
- **THEN** the status is `NO_NEW_FINDINGS`, the known count equals the finding count, and the health is unchanged

#### Scenario: Acknowledgement passes its date

- **WHEN** an item carries an `expires` date before the day of the run
- **THEN** the finding is new, its rule and digest are listed under `expired_known`, and the health is unchanged

#### Scenario: Report lists the items to add

- **WHEN** the detector reports a finding with a new location
- **THEN** its output ends with the `acknowledged` items for every such finding at the scanned commit, and a file made of them acknowledges them all

### Requirement: Acknowledgement file is read from the scanned tree

The detector MUST read `.auditignore.yaml` from the root tree of the scanned commit through Git objects and MUST parse its one shape with its own code. It MUST treat an absent file as an empty list, MUST report CONFIGURATION_FAILURE when the path is not a regular file or the file is outside the shape, and MUST list an item it cannot use as malformed.

#### Scenario: Acknowledgement file is absent

- **WHEN** the scanned commit has no `.auditignore.yaml`
- **THEN** the detector runs with no acknowledgement and reports the file as absent in the health

#### Scenario: Acknowledgement file is a symbolic link

- **WHEN** `.auditignore.yaml` at the scanned commit is a symbolic link
- **THEN** the detector exits 2 with health `CONFIGURATION_FAILURE` and names the path in the error

#### Scenario: Acknowledgement file has another top-level key

- **WHEN** `.auditignore.yaml` at the scanned commit has a top-level key other than `acknowledged`
- **THEN** the detector exits 2 with health `CONFIGURATION_FAILURE` and names the line in the error

#### Scenario: Acknowledged value appears in a new file

- **WHEN** a token acknowledged at an earlier commit is committed into another file after that commit
- **THEN** the finding keeps its id, lists the earlier location as known and the new one as new, and the status is `ALERT`

#### Scenario: Acknowledged commit is absent from the clone

- **WHEN** an item of `.auditignore.yaml` names a commit the clone does not contain
- **THEN** the health is `INCOMPLETE`, the commit is listed, and the finding is new

### Requirement: Scanner routines run the detector from the deck object store

The Dotfiles Scanner MUST write the detector into a scratch directory that is not a checkout as the blob of `routines/scripts/exposure_scan.py` in the fetched runedeck/deck tree, read through Git objects after the tree lists it as one regular file. The run MUST require the object id of the copy to equal the listed blob id before it runs, MUST run only that copy with the interpreter in isolated mode, and MUST NOT pipe the blob into the interpreter or run the working-tree copy.

#### Scenario: Checkout tracks a module named like the standard library

- **WHEN** the scanned checkout tracks `json.py` at its root
- **THEN** the detector imports the standard library `json` and the tracked file never runs

#### Scenario: Script is absent from the fetched ref

- **WHEN** `ls-tree FETCH_HEAD -- routines/scripts/exposure_scan.py` prints no entry
- **THEN** the run reports CONFIGURATION_FAILURE and stops

#### Scenario: Scratch copy differs from the listed blob

- **WHEN** the object id of the copy in the scratch directory differs from the blob id the fetched tree lists
- **THEN** the run reports CONFIGURATION_FAILURE and does not run the copy

### Requirement: Run reads repository content only through the detector

The run MUST pass SENSITIVE_DOMAINS as a file, never as a command argument, and MUST NOT read repository content by any other means than the detector output.

#### Scenario: Run starts the detector

- **WHEN** the run starts the detector
- **THEN** the sensitive domains reach it through a file, and no command line names a domain

#### Scenario: Run composes the session report

- **WHEN** the run composes the session report
- **THEN** every path, line, commit, and blob id comes from the detector output, and the run opens no file of the scanned checkout

### Requirement: Review items for personal data the rules cannot see

The run MAY add review items for personal data the rules cannot see, each with a path, a line, a commit, and a blob id, and such an item MUST NOT change the detector status.

#### Scenario: Run adds a review item

- **WHEN** the run notes personal data that no rule detects
- **THEN** the item carries a path, a line, a commit, and a blob id, and the status stays as the detector reported it

### Requirement: Stub reads the ref in POLICY_REF

The stub MUST fetch `origin <POLICY_REF>`, where POLICY_REF is a stub value whose default is `main`, and MUST read the routine file and any script it runs from that `FETCH_HEAD`. The deployed stub MUST name `main`. A routine file MUST NOT fetch again in the runedeck/deck checkout. The Dotfiles Scanner stub MUST carry BRANCH, the branch of the scanned repository, with the default `main`.

#### Scenario: Scanned repository uses another default branch

- **WHEN** the stub carries `BRANCH: trunk`
- **THEN** the run fetches `origin trunk` of REPOSITORY and scans its `FETCH_HEAD`

#### Scenario: Owner tests a branch

- **WHEN** the stub carries `POLICY_REF: routines/scanners` and the branch exists on origin
- **THEN** the run reads the routine file and the detector from that branch and reports which runedeck/deck commit it used

### Requirement: Reports separate the push from the session

A scanner notification MUST NOT contain a value, a finding id, a hash, a commit, or the owner's handle. The Dotfiles Scanner MAY give a path as the detector printed it. Online Mentions MUST give counts only and MUST NOT name a person, site, organization, repository, or URL. The session report MUST carry one table with id, new or known, rule or classification, location, and action, with every value redacted and a path or URL segment redacted only when it is itself sensitive.

#### Scenario: Path contains a sensitive value

- **WHEN** a finding's path contains a hostname under a sensitive domain
- **THEN** the table row and the notification show the path with that segment as `[REDACTED]`, and the table row keeps the blob id

#### Scenario: Detector reports new findings

- **WHEN** the detector reports a new sensitive-domain finding and a new email finding
- **THEN** the notification opens with `2 new exposures need action`, gives one bullet for each label with its places, files, and first location, and ends with one next step

#### Scenario: Label appears in a commit message and in a file

- **WHEN** a label's new locations are one commit message and two files
- **THEN** its bullet counts the commit message among its places and gives the first file location

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
