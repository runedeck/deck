## ADDED Requirements

### Requirement: Later steps read the frozen plan

The benchmark wrapper MUST give the grading, judging, and aggregation steps the manifest that the run step froze into the iteration directory. The source manifest has no run plan, and each of those steps rejects a manifest without one.

#### Scenario: Wrapper grades an iteration after the run step

- **WHEN** the wrapper grades, judges, or reports an iteration whose source manifest has no run plan
- **THEN** each step reads the frozen manifest of that iteration and validates its run plan without a manual path change

### Requirement: Example routes use supported options

The cross-*[harness][HARNESS]* companion MUST build its example route only from options that the installed command accepts. An author copies the example into a route registry, and an unknown option fails every route check before the matrix starts.

#### Scenario: Author copies the example route

- **WHEN** an author copies the example route into a registry and runs the route checks
- **THEN** the command that starts each route accepts every option in the copied route

### Requirement: One assertion accepts several wordings

The grader MUST offer a required assertion kind that matches regular expressions with the case-insensitive and multiline flags. Every expression must match for the assertion to pass. One expression can then accept two correct wordings of the same fact. The literal assertion kinds MUST keep their plain-text matching.

#### Scenario: Response uses the second correct wording

- **WHEN** a required expression accepts "home-manager" and "Home Manager", and the response says "Home Manager"
- **THEN** the grader passes the assertion

### Requirement: Forbidden checks match usage

The grader MUST offer a forbidden assertion kind that fails when any of its regular expressions matches the response. An author can then match the use of a command and ignore a warning that quotes the same command.

#### Scenario: Treatment warns against the forbidden flag

- **WHEN** the response warns against a forbidden flag in prose, and its command block omits the flag
- **THEN** a forbidden expression that matches only a command line passes the assertion

### Requirement: Invalid expressions stop the benchmark early

The manifest validator MUST compile every regular expression of every assertion. It MUST reject the manifest before the first provider call when one expression is invalid, and name the case, the kind, and the pattern.

#### Scenario: Author writes an unbalanced bracket

- **WHEN** a manifest has a regular expression with an unbalanced bracket
- **THEN** the benchmark stops with an error that names the pattern, and no provider receives a call

### Requirement: Short answers stay comparable

The aggregator MUST keep a graded run valid when the checker reports that the run has too few prose words for a reliable density. It MUST record the checker density of that run as null, and it MUST pair the run on its assertion results. A code-only or one-line answer then counts as a matched pair, and the verdict reports missing checker data instead of no pairs.

#### Scenario: Baseline and treatment give one-line answers

- **WHEN** the baseline run and the treatment run of a case each give a one-line answer, and the grader scores all their assertions
- **THEN** the aggregator counts the pair as matched and reports its assertion delta, with a null density for both runs

[HARNESS]: ../../../../specs/glossary/harness.md
