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
updated: 2026-09-20
author: "@N4M3Z"
project: deck
related:
    - "CORE-0007 Unified Module Validation"
responsible:
    - "@N4M3Z"
accountable:
    - "@N4M3Z"
consulted: []
informed: []
upstream: []
change: core-foundation-principles
---

# Fixture-Based Canary Testing

## Context and Problem Statement

A checker that passes every file looks the same as a checker that checks nothing. A rule can be deleted, a pattern can stop matching, or a tool upgrade can change a default, and the check stays green. The deck needs proof that each checker still catches what it claims to catch.

## Considered Options

1. Trust the checker. Review catches a broken rule when someone notices.
2. A manifest that maps each fixture file to its expected result.
3. Fixture inputs that must pass and inputs that must fail, with the expected result asserted by the test that runs them.

## Decision Outcome

Option 3. A checker the deck depends on MUST have at least one input that it accepts and one input that it rejects. The test MUST assert the exact result, so that a deleted or weakened rule fails the test. Where fixtures are files, `valid/` and `invalid/` directory names state the assertion.

The ontology hook is the instance in the deck. It validates `ontology/smoke/instances.ttl` against the shapes and asserts the exact count of violations and warnings, so a removed shape fails the hook.

## Consequences

- A new canary is one file in the right place.
- Most checkers in the deck have no canary yet. The scripts under `scripts/` that check names, record ids, record fields, and record links were each proven by hand with a passing and a failing input, and those inputs are not committed.
- An exact count is brittle on purpose. A new shape changes the count, and the author updates the assertion in the same commit.

## More Information

- [JSON Schema Test Suite][JSTS]
- [markdownlint][MDLINT]

[JSTS]: https://github.com/json-schema-org/JSON-Schema-Test-Suite "JSON Schema Test Suite, the validator testing pattern"
[MDLINT]: https://github.com/DavidAnson/markdownlint "markdownlint, valid and invalid fixture convention"
