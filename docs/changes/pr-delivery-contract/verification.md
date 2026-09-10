# Delivery contract verification

## Owner review

The owner approved the delivery contract and requested implementation on 2026-09-10.
Deck #56 merged before implementation. Its authorization companion remains unchanged in this change.

## Source implementation

The three VersionControl files implement the approved [design](design.md).
The entrypoint and Jujutsu companion share one rebase decision.
The babysitting companion owns selection, delivery evidence, authoritative readiness, and bounded recovery.
The trusted repository checker owns attribution validation.
No routine, workflow, signing configuration, or deployed skill changed.

## Independent review

Source review covered all 16 specification scenarios.
It found two defects in the initial implementation, and the final source corrects both:

- A push error can follow remote acceptance. Delivery state now follows the remote read, with an unreadable result explicitly blocked.
- A repository can require zero approvals. The finding-response step now follows the effective approval and thread-resolution requirements.

The reviewer found no remaining concrete source defect after those corrections.
This is source coverage, not an executed behavioral replay or benchmark result.

The separate [recovery replay](behavioral-replay.md) passes eight independent decision cases.
That replay supplements source review. It does not replace paired benchmark evidence.

## Deterministic validation

- The existing attribution suites pass 37 unit tests and 31 integration tests.
- Rune source validation reports zero errors and five existing advisory warnings.
- The standalone skill schema, Markdown, and Vale checks pass.
- The guarded publication checks pass, including offline links, strict OpenSpec validation, secret scans, provenance digests, and outgoing attribution.
- A temporary Agent Skills installation contains all nine selected files without skips or warnings.
- The official `skills-ref` validator accepts the temporary Agent Skills installation.

The validator ran through isolated `uv run` with the cached official reference wheel.
This supported invocation used no global tool installation, permission change, or alternate cache path.

The validation installation does not change an owner harness deployment.
The skill still exceeds its advisory entrypoint target but remains below the 150-line limit.

## Paired benchmark evidence

The benchmark uses three composite cases and separate correctness and efficiency measures.
The owner directed execution after the three-case and 26-call request.
Historical outputs remain evidence for their original artifact only.

The [generated Sol report](sol-benchmark.md) contains three valid matched pairs, with no excluded Sol response.
Its source aggregate SHA-256 is `0f6609173a39e40c39049022106e2dbfafb49240aaa1072e3ba301fcb4f8dfed`.
The report copy retains the generated Markdown bytes.
Both conditions pass all 121 semantic checker checks across the three cases.
Those checks cover evidence completeness, fleet resumption, base updates, reviewer recovery, and attribution.
The checker has 17 passing tests, including 34 near-miss mutations.
It scores decisions and evidence against fixed opportunities, not response length or preferred phrasing.

Mean elapsed time is 70.40 seconds without the skill and 72.46 seconds with the skill.
Token telemetry is unavailable. This sample establishes no comparative improvement or token-efficiency claim.
Blind judgments and the Opus comparison remain incomplete.
The generated report covers Sol only, not the complete planned matrix.
Its word-normalized checker density remains diagnostic, not a correctness measure.

Preflight and context-canary checks pass for the explicit `sol-run@claude` route with clean state and read-only tools.
The runner preserves raw Rune output and parsed responses in the benchmark directory.
Global session archival still fails. The runner's captured output is separate from that missing archive.
Diagnostics also name `gpt-5.6-luna` for session-title generation, separate from the evaluated Sol responses.
The runner counts harness invocations. Complete backend request counts and usage are unavailable.
No Fable substitution occurred.

## Remaining evidence

The first execution stopped during route preflight before any benchmark case ran.
Codex clean-state preparation selected an absent `openai` provider configuration before its proxy wrapper could select the configured provider.
The Claude invocation exited without a provider cause in Rune's returned diagnostics.
A subsequent bounded native diagnostic reported HTTP `429`: all configured Opus credentials were cooling down after a rate-limit error.
That diagnostic confirms its own quota failure, not the missing native stdout of the earlier preflight.
No tool executed. The diagnostic also records a separate session-archive failure.
These failed preflights provide no behavioral result.

Opus execution and blind judgments remain blocked by the confirmed quota failure.

All three requested council responses exist, with their capture limits recorded in [design.md](design.md#research-status).
This change alters no harness wrapper or capture route.
