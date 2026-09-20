## Purpose

Define observable delivery evidence for PR babysitting, so owners can distinguish published repairs, incomplete reviews, and merge-ready work.

## ADDED Requirements

### Requirement: Complete selection with preserved ownership

A babysit pass MUST record its selected pull requests, observation time, exclusions, and known concurrent owners in one local state record.
An organization-wide selection MUST cover every currently open pull request unless the user narrows the scope.
Each mutable head MUST have at most one modifying agent within the pass.
The pass MUST preserve explicit ownership restrictions after delegation, interruption, or compaction.

#### Scenario: A selected PR belongs to another session

- **WHEN** the user reserves a selected PR for another session
- **THEN** the pass records that reservation and limits itself to the authorized observation scope

#### Scenario: An organization-wide pass resumes

- **WHEN** a paused organization-wide pass resumes after repositories gain or lose open PRs
- **THEN** the pass refreshes its selection and reports additions, completed items, and exclusions

### Requirement: Delivery claims have current evidence

Each selected PR MUST have an explicit local-only, published, reviewing, blocked, or merge-ready state.
The record MUST distinguish the local repair revision from the last verified remote head.
Each unfinished item MUST identify its next authorized action or its specific external blocker.
Evidence requirements from the user and repository MUST remain visible until fulfilled or explicitly waived by the owner.

#### Scenario: A validated repair never reaches the remote

- **WHEN** a commit exists locally but publication fails or does not occur
- **THEN** the pass reports the repair as local-only with the cause and next action

#### Scenario: Benchmark execution has no valid result

- **WHEN** a selected PR requires benchmark evidence and only a plan or failed route attempt exists
- **THEN** the pass records the missing evidence as a blocker and preserves the attempt as a separate fact

### Requirement: Readiness derives from authoritative requirements

The pass MUST obtain effective requirements from repository policy, applicable branch protections and rulesets, live workflows, and explicit owner decisions.
It MUST compare each requirement with evidence for the current head and the policy's required review scope.
Absent required evidence MUST remain unsatisfied.
An unreadable requirement source MUST produce an unknown state with its cause.
The pass MUST distinguish substantive review, skipped review, provider failure, and an approved override.
An optional review MUST remain optional unless the user or repository makes it required.

#### Scenario: A check listing omits a required check

- **WHEN** policy requires a check that does not appear in the check listing
- **THEN** the pass identifies that missing check and reports the PR as not merge-ready

#### Scenario: An optional provider reports a skipped review

- **WHEN** an optional provider reports success without performing a review
- **THEN** the pass records the skip without treating it as approval or inventing a mandatory review requirement

#### Scenario: The head changes during readiness assessment

- **WHEN** a final remote read differs from the assessed head
- **THEN** the pass discards the stale readiness result and reconciles ownership before further work

### Requirement: Main movement preserves conflict-free heads

After main changes or a queued PR merges, the pass MUST verify each remaining PR's merge state before choosing a repair.
It MUST preserve a conflict-free head unless effective policy or an explicit owner instruction requires a base update.
A required update MUST receive a scoped repair under the existing publication and history-rewrite authorization rules.

#### Scenario: An unrelated PR merges

- **WHEN** main advances and another selected PR remains MERGEABLE without a policy or owner requirement to update its base
- **THEN** the pass leaves that PR's head unchanged

#### Scenario: Policy requires a clean PR to update its base

- **WHEN** a selected PR remains MERGEABLE but effective policy requires an updated base
- **THEN** the pass records that requirement and applies the existing authorization contract before changing the head

#### Scenario: A surviving PR has a conflict

- **WHEN** the platform confirms a conflict on a selected PR
- **THEN** the pass isolates its repair and applies the existing authorization contract before publication

### Requirement: Reviewer recovery has a bounded budget

The pass MUST distinguish expected reset rounds from adjudication results and provider failures using the live workflow and terminal evidence.
It MUST record the head, run, observed failure, and attempt count before another summon.
An explicit owner budget MUST control recovery.
When no budget exists, the pass MUST permit at most one retry for the same unresolved failure on an unchanged head.
Retrying a known permanent failure MUST require corrective action regardless of the remaining budget.
After that budget is exhausted, a new attempt MUST require a corrected cause, new diagnostic evidence, or an explicit owner instruction.
A blocked reviewer MUST leave unaffected PRs eligible for continued work.

#### Scenario: The same unresolved failure repeats

- **WHEN** a required reviewer fails without a verdict and its recovery budget is exhausted
- **THEN** the pass stops summons for that failure and reports the head, run, observed cause, and required next action

#### Scenario: A wrapper rejects a required option

- **WHEN** a wrapper fails before provider execution because the CLI rejects an option
- **THEN** the pass records the incompatibility and requires an authorized corrective action before another attempt

#### Scenario: A reset round completes as designed

- **WHEN** terminal evidence confirms an expected reset round
- **THEN** the pass follows the workflow's next review step and keeps the reset distinct from a provider-failure retry

#### Scenario: Logs do not reveal the provider cause

- **WHEN** a failed run omits the underlying provider error
- **THEN** the pass reports the cause as unknown instead of inferring authentication, quota, model access, or network failure

### Requirement: Attribution follows the trusted contract

The pass MUST apply the repository's trusted attribution contract and checker to the outgoing range.
It MUST use declared model identity accurately without treating an obsolete exact-model catalog as authority.
It MUST preserve the distinction between syntax validation and proof of model execution.

#### Scenario: A future model satisfies trusted policy

- **WHEN** an accurately declared future model identifier passes the trusted checker
- **THEN** the pass proceeds without adding an unnecessary model-catalog entry

#### Scenario: An identity violates trusted policy

- **WHEN** the outgoing identity fails the trusted checker
- **THEN** the pass repairs the declaration or reports the policy conflict without weakening the checker
