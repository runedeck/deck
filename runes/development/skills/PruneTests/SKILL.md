---
name: PruneTests
description: "Audit a repository's tests for ones that no plausible bug can make fail, delete them, repair the ones whose intent is right but whose implementation cannot fail, and take the cleanup to a pull request through FullSend. USE WHEN prune the tests, remove useless tests, tests that can never fail, clean up the test suite, tests that check a type equals itself, tests that a removed feature stays removed, audit test quality. NOT FOR writing tests for new behavior (the change's own tasks), fixing a red test in a pull request (VersionControl BabysitPR), or raising a coverage number."
compatibility: "Requires the repository's test runner. Uses the repository's mutation testing tool when it has one, for example mutmut, cargo-mutants, or Stryker. The pull request step requires FullSend."
metadata:
    version: 0.1.0
---

# PruneTests

A test earns its place when a plausible bug in the code it covers makes it fail. PruneTests deletes each test that no such bug can fail, and repairs each test that means to guard a behavior but cannot fail. The owner trusts your judgment on each test. Decide each one yourself and record the reason.

## Constraints

- One pull request carries the whole cleanup. FullSend opens it, babysits it, and asks the owner once to merge.
- Change test files, test helpers, and fixtures only. When a test is useless because the production code is dead, list that code in the pull request body for a separate change.
- Never delete a test because it is slow, flaky, or red. List it in the body as a separate problem.
- Never delete the last test of a public behavior. Repair it.
- Before you delete a file that looks unused, search the repository for each reference to it: imports, test configuration, fixtures paths, and CI files.

## Instructions

### Classify each test

Read each test beside the code it calls. Ask one question: which plausible change to the production code makes this test fail? When you find no answer, the test is a deletion candidate. Use the patterns below as the first pass.

- Type echo: asserts that a value has the type it was built as, or a type that the compiler already checks. Delete it.
- Removal guard: asserts that a removed feature, flag, route, or file is still absent. Delete it. Keep it only when a comment states a security or compatibility reason, and then consider a lint rule in its place.
- Schema echo: asserts that a migration's new column or table exists. Delete it. When no test covers the behavior that the column enables, write that test.
- Pass-through: calls a thin wrapper and asserts that it returned what its mock returned. Delete it. When the wrapper has its own logic, repair the test to cover that logic.
- Mock echo: asserts values that the test itself set on a mock or a fixture. Delete it or repair it.
- Orphan file: a helper, fixture, or snapshot that no test loads. Delete it after the reference search.

A test that matches no pattern but has no answer to the question is also a candidate. Say why in its row of the pull request body.

### Repair a weak test

1. Name the behavior the test meant to guard.
2. Rewrite it to assert that behavior through the public interface, with real inputs where the cost allows.
3. Prove the repair with a mutation: break the production code on purpose, run the test, see it fail, and revert the break. Use the repository's mutation testing tool when it has one.
4. Record the mutation and the failure line for the pull request body.

### Check the suite

1. Run the full suite before and after. The result must stay green with fewer tests.
2. When the repository measures coverage, compare it before and after. For each line that lost its only test, repair or write a test that covers it.
3. For a deletion that you are not sure of, apply one plausible mutation to the code it covers. A test that still passes is safe to delete.

### Hand off to FullSend

Write the pull request body first. Give it one table of the deleted tests with name, pattern, and reason. Give it a second table of the repaired tests with name, new assertion, and the mutation that proves it. List the slow, flaky, and red tests and the dead production code after the tables. Then run FullSend with this audit as its task. The mutation records are its verification evidence.

## Verification

- The suite passes after the change.
- Each repaired test has a recorded mutation that made it fail.
- Each deleted file has a reference search that found no user.
- The pull request body has a row for each deleted and each repaired test.

## References

- FullSend for the pull request, the babysitting, and the merge question.
- ContinuousIntegration for the repository's full local check set.
