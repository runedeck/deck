## ADDED Requirements

### Requirement: Owner Gets Only Questions

FullSend is the *[skill][SKILL]* that takes one task to a merge-ready pull request while the owner reads nothing. A *[model][MODEL]* that runs FullSend MUST put every question to the owner through the *[harness][HARNESS]*'s question tool, which notifies the owner, and never in prose. It MUST ask only what blocks the work: a secret, a key touch, an account it cannot reach, or a product decision. It records every other decision in the pull request body.

#### Scenario: Work needs a secret

- **WHEN** a model that runs FullSend needs a secret that it does not have
- **THEN** it asks through the question tool in a question that is complete on its own, and no turn ends on a question in prose

### Requirement: Merge Waits For The Owner's Yes

Starting FullSend lets the model push one branch and open one pull request for the task, and nothing more. The model MUST NOT merge, mark a draft ready, comment, label, resolve a thread, or force-push before the owner says yes in the question tool. At merge-ready it MUST ask one question with the pull request URL, the head commit, the evidence, and its confidence. On a yes it runs the listed merge command one time.

#### Scenario: Pull request reaches merge-ready

- **WHEN** the pull request of a FullSend task meets every merge-ready condition
- **THEN** the model asks one question that names the URL and the live head commit, and no merge runs before the owner's yes

### Requirement: Fix Is Reproduced And Proven

A model that runs FullSend MUST reproduce the problem before it edits, with a command, a test, or a recording that fails. It MUST prove the fix with the strongest evidence the change allows. The real app driven and recorded is strongest. A test that fails before the fix and passes after it comes next. A script, named in the pull request body as the only evidence, comes last.

#### Scenario: Fix changes what a user can drive

- **WHEN** a fix changes behavior that a user can drive in the real app
- **THEN** the pull request links a recording of the real app with the fix, and a passing test alone does not count as the evidence

### Requirement: Confidence Rests On The Final Head

Before it asks to merge, the model MUST run the verification again on the final head. A different model MUST review the diff with fresh context. The model rates its confidence high only when all of these hold on that head: every required check passes, no review thread is open, the evidence comes from it, and the second review found nothing blocking. The model MUST NOT weaken a check to make it pass: no skipped test, lowered threshold, bypassed hook, or review override.

#### Scenario: Pull request gets a new commit after verification

- **WHEN** the pull request gets a new commit after the last verification
- **THEN** the model runs the verification again on the new head before it rates its confidence high

### Requirement: Tests Earn Their Place

PruneTests is the skill that cleans a test suite. A model that runs it MUST delete a test when no plausible change to the production code makes the test fail. It MUST repair a test that means to guard a behavior but cannot fail. It MUST NOT delete a test because it is slow, flaky, or red, and MUST NOT delete the last test of a public behavior. It changes tests, test helpers, and fixtures only, and one pull request through FullSend holds the whole cleanup.

#### Scenario: Test only echoes a type

- **WHEN** a test asserts only that a value has the type it was built as
- **THEN** the model deletes the test and gives it a row in the pull request body with the pattern and the reason

### Requirement: Repairs Are Proven By Mutation

A mutation is a deliberate break in the production code. A model that runs PruneTests MUST prove each repaired test with a mutation: it breaks the code, runs the test, sees the test fail, and reverts the break. The pull request body MUST record the mutation and the failure line for each repaired test. The full test suite MUST pass after the cleanup with fewer tests.

#### Scenario: Repaired test survives its mutation

- **WHEN** a repaired test still passes after the model breaks the code that the test guards
- **THEN** the repair does not count, and the model rewrites the test until the break makes it fail

[SKILL]: ../../../../specs/glossary/skill.md
[MODEL]: ../../../../specs/glossary/model.md
[HARNESS]: ../../../../specs/glossary/harness.md
