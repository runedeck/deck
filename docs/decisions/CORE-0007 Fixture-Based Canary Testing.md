---
title: "Fixture-Based Canary Testing"
description: "A checker is proven by fixtures: inputs that must pass and inputs that must fail, with the expected result asserted."
type: adr
category: process
tags:
    - testing
    - validation
    - fixtures
status: accepted
created: 2026-04-05
updated: 2026-10-19
author: "@N4M3Z"
project: deck
related:
    - "CORE-0021 Unified Module Validation"
responsible:
    - "@N4M3Z"
accountable:
    - "@N4M3Z"
consulted: []
informed: []
upstream:
    - "https://github.com/N4M3Z/forge-core/blob/main/docs/decisions/CORE-0012%20Fixture-Based%20Canary%20Testing.md"
change: plain-text-first-principles
---

# Fixture-Based Canary Testing

## Context and Problem Statement

The *[repository][REPOSITORY]* needs evidence that each checker still catches what it claims to catch. A checker that passes every file looks the same as a checker that checks nothing. Someone can delete an *[analysis rule][ANALYSISRULE]*, a pattern can stop matching, or a tool upgrade can alter a default, and the check still passes.

## Considered Options

1. Trust the checker, and let review catch a broken [analysis rule][ANALYSISRULE] when someone notices.
2. A manifest that maps each *[fixture][FIXTURE]* file to its expected result.
3. [Fixture][FIXTURE] inputs that must pass and inputs that must fail, where the test that runs them asserts the expected result.

## Decision Outcome

Option 3. A checker the [repository][REPOSITORY] depends on MUST have at least one input that it accepts and one input that it rejects. The test MUST assert the exact result, so a deleted or weakened [analysis rule][ANALYSISRULE] fails the test. Where [fixtures][FIXTURE] are files, the directory names `valid/` and `invalid/` state the assertion.

The ontology hook is the one example in the [repository][REPOSITORY]. It validates `ontology/smoke/instances.ttl` against the shapes and asserts the exact count of violations and warnings, so a removed shape fails the hook.

### Consequences

- [+] A new canary is one file in the right place.
- [-] Most checkers in the [repository][REPOSITORY] have no canary yet. The scripts under `scripts/` check names, record ids, record fields, and record links. The author proved each one by hand with a passing and a failing input, and nobody committed those inputs.
- [-] An exact count is fragile on purpose. A new shape alters the count, and the author updates the assertion in the same commit.

## More Information

- [JSON Schema Test Suite][JSTS]
- [markdownlint][MDLINT]
- Rewritten on 2026-10-19 in the plain spoken register. The decision is unchanged.

[JSTS]: https://github.com/json-schema-org/JSON-Schema-Test-Suite "JSON Schema Test Suite, the validator testing pattern"
[MDLINT]: https://github.com/DavidAnson/markdownlint "markdownlint, valid and invalid fixture convention"
[REPOSITORY]: ../specs/glossary/repository.md
[ANALYSISRULE]: ../specs/glossary/analysis-rule.md
[FIXTURE]: ../specs/glossary/fixture.md
