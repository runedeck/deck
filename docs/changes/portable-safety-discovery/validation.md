# Validation record

The 23 SafetyFirst tests pass against the isolated architecture candidate in 54.529 seconds.
They include the strict generic and harness source-layer gate.
They cover content, bounded fake-guard probes, and Claude/Codex assembly.
Missing candidate executables fail the required assembly checks.

The probe controls reject printed success markers, fake JSON, padding, control characters, and failed process exits.
They also terminate hung leaders, processes that ignore normal termination, and descendants that retain output pipes.
Outer-command fixtures bound stalled executable lookup and Python startup.
Missing Python, timeout, or helper produces no usable discovery record.

Run the focused suite from the Deck root:

```sh
RUNE_TEST_BINARY=../cli/target/debug/rune PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_safetyfirst.py -v
```

The tested executable has SHA-256 `451eff3d339e286421f9ee254a6bfeeb2b87c8794e1a8d9546ebcdee578eba16`.
The shared helper has SHA-256 `6eebc7f0c541b6467f58fd7dd1f0ea5709a05f1e95580d87a26a5c94b9e40d5d`.
The unchanged workflow has SHA-256 `5fad19f70e2e5d6eb65bf285f003fe86405ca2654927bc76a994ec072c05ef31`.
Its non-discovery policy digest remains `5ecac2914fd8a9e041cd61228e06af64b1888cd8da2f4de76a6adf71e9e19a8e`.

Changed-file checks pass for schema, prose, local bundle links, provenance, Python, and native specification validation.
Strict STE scores for the six checked instruction and design files range from 0.27 to 1.41 per 100 words.
Technical terms and the ordered evidence conditions remain unchanged where the advisory checker flags them.
The local schema-copy gate fails because unchanged Deck and sibling CLI skill schemas differ.
Full `make validate` also reports existing prose and Markdown failures outside this change.
These failures remain visible. This change does not alter shared schemas or lint configuration.

Native Claude injection and Codex companion execution remain unverified.
Passing static checks does not establish a native runtime result.
The PR records its exact candidate revision and publication-gate results.

The content CI builds the architecture revision pinned in its workflow.
The architecture PR must merge before this change becomes ready to merge.
