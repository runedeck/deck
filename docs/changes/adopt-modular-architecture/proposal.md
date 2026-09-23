---
status: proposed
decisions:
    - "CORE-0020 YAML Configuration Files"
    - "CORE-0021 Unified Module Validation"
    - "CORE-0022 Verified Remote Execution"
    - "A rune is one governed instruction"
---

# Modular architecture

## Why

A deck grows by domains, and each domain brings its own instructions, defaults, and checks. Without a unit that keeps those together, every addition touches shared configuration, and every tool reads every file to find what it needs.

That unit is the *module* [MODULE]. Parnas gave the criterion for splitting a system in 1972: each module hides one design decision that is likely to change, and no other module depends on it ([Parnas][PARNAS]). Ousterhout adds the measure: a good module is deep, a small interface over a large implementation, so the cost of a caller does not grow with the module ([Ousterhout][OUSTERHOUT]). Both arguments hold for instructions as they hold for code. A domain that owns its defaults, its checks, and its instructions can be added, replaced, or removed without a change anywhere else.

Three properties make a domain a module here:

- It carries its own defaults, and a user overrides them without editing the committed file.
- Every check it needs runs through one shared hook configuration, locally and in CI, so a module cannot pass on one machine and fail on another.
- Anything it fetches from the network runs only after its digest matches one committed in the repository.

## What Changes

Define module and rune in the ontology. State the configuration overlay, one checker per concern, one validation path, and verified remote execution as the requirements of one capability. The record `adr.md` defines the parts of a rune: one canon, harness companions, variants, a provenance sidecar, and assembly.

## Capabilities

### New Capabilities

- `adopt-modular-architecture`: a module has defaults a user overlays, runs every check through one shared hook configuration, and verifies anything it fetches before it runs.

## Impact

- CORE-0020, CORE-0021, and CORE-0022 cite the requirements of this capability as their upstream.
- `ontology/rune.ttl` gains `Module`.

## Sources

- [On the Criteria To Be Used in Decomposing Systems into Modules][PARNAS], D. L. Parnas, Communications of the ACM 15(12), 1972
- [A Philosophy of Software Design][OUSTERHOUT], John Ousterhout, 2018, on deep modules

[MODULE]: https://runedeck.ai/ns#Module
[PARNAS]: https://dl.acm.org/doi/10.1145/361598.361623
[OUSTERHOUT]: https://web.stanford.edu/~ouster/cgi-bin/book.php
