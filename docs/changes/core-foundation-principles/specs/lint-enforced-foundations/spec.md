## ADDED Requirements

### Requirement: Checker Coverage

The checker map MUST name, for every requirement in the plain-text-wins, markdown-first-authoring, and harness-independent-authoring capabilities, the enforcing check (mdschema, `rune validate`, a commit hook, or a Vale style) or the declared gap. A gap closes with a checker that starts as a warning with a declared baseline.

#### Scenario: Foundation requirement has no checker

- **WHEN** the checker map lists a requirement with neither an enforcing check nor a declared gap
- **THEN** verification fails until the map names one

#### Scenario: Plain Text Representation has its checker

- **WHEN** the checker map reaches Plain Text Representation
- **THEN** it names the declared gap, because representability stays a review judgment

#### Scenario: Lossless Derived Forms has its checker

- **WHEN** the checker map reaches Lossless Derived Forms
- **THEN** it names the declared gap until a regeneration drift check exists

#### Scenario: Markdown System Language has its checker

- **WHEN** the checker map reaches Markdown System Language
- **THEN** it names the `rune validate` artifact checks

#### Scenario: Metadata Inside Files has its checker

- **WHEN** the checker map reaches Metadata Inside Files
- **THEN** it names the declared gap, because no mechanical check detects an external metadata index

#### Scenario: Flat Frontmatter has its checker

- **WHEN** the checker map reaches Flat Frontmatter
- **THEN** it names the mdschema frontmatter checks and the declared gap for nested-value detection

#### Scenario: Directories Direct has its checker

- **WHEN** the checker map reaches Directories Direct
- **THEN** it names the terminology Vale style for the term and the declared gap for routing judgment

#### Scenario: Runtime Variables has its checker

- **WHEN** the checker map reaches Runtime Variables
- **THEN** it names the declared gap, because no check detects a hardcoded configurable value

#### Scenario: Template Placeholders has its checker

- **WHEN** the checker map reaches Template Placeholders
- **THEN** it names the declared gap, because no check parses placeholder syntax yet

#### Scenario: Configuration Defaults has its checker

- **WHEN** the checker map reaches Configuration Defaults
- **THEN** it names the `rune validate` module defaults check

#### Scenario: One Checker Per Concern has its checker

- **WHEN** the checker map reaches One Checker Per Concern
- **THEN** it names the shared lint configuration as the roster of record

#### Scenario: Reference Citations has its checker

- **WHEN** the checker map reaches Reference Citations
- **THEN** it names the citations Vale style, which starts as a warning

#### Scenario: One Validation Path has its checker

- **WHEN** the checker map reaches One Validation Path
- **THEN** it names the declared gap, because nothing diffs the CI steps against the shared configuration

#### Scenario: Author Once has its checker

- **WHEN** the checker map reaches Author Once
- **THEN** it names the declared gap, because authoring location stays a review judgment

#### Scenario: Assembled Instances has its checker

- **WHEN** the checker map reaches Assembled Instances
- **THEN** it names the deployment manifest fingerprints and `rune drift`

#### Scenario: Portable Instructions has its checker

- **WHEN** the checker map reaches Portable Instructions
- **THEN** it names the declared gap, because portability review stays human judgment

### Requirement: External links are checked on a schedule

A scheduled workflow MUST fetch every external URL in the documents and the runes one time each week. The commit path MUST stay offline, so it checks only local links and fragments. The workflow MUST install its tool through the shared installer, so that one pinned version and one archive digest serve every path.

#### Scenario: External page disappears

- **WHEN** a cited page returns an error on the weekly run
- **THEN** the Links workflow fails and names the file and the URL

#### Scenario: Commit path has no network

- **WHEN** a commit adds a link to an external page
- **THEN** the commit stage checks its form only, and the weekly run checks that it resolves
