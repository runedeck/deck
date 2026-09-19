# Portable SafetyFirst discovery design

## Approach

Both entrypoints run the shared `scripts/probe_guard.py` helper.
The helper requires Python 3 and a POSIX process boundary.
The canonical entrypoint uses an available command tool with a five-second timeout and a 1024-byte output limit.
Missing runtime, missing helper, denial, or incomplete output leaves the discovery state unknown.

The helper checks `PATH` and executes the resolved program with `--version` through a subprocess argument list.
It executes no shell. It captures stdout and stderr without exposing either stream directly to the agent.
A 4.5-second internal deadline leaves time for cleanup before the five-second outer bound.
The helper sends `SIGKILL` to the probe's process group after timeout or output overflow.
It also removes remaining group members after a completed leader, including descendants that retain output pipes.
If the OS denies cleanup, the helper preserves captured results but reports `cleanup_failed` and an unknown version.
It does not retry a denied cleanup operation.

The result is one JSON record with schema `safetyfirst-guard-probe/v1`, below 1024 bytes.
Top-level lookup and version states come from actual lookup and process results.
The `process` object records the observed exit code, timeout, and truncation flags.
Untrusted path and child streams appear only as escaped strings inside `payload`.
Payload text cannot supply its own success status, including printed markers or complete fake JSON records.
An escaped-output overflow marks the version unknown, even when the executable exits successfully.

Claude injects the same helper through the supported skill-directory substitution.
An outer `timeout -s KILL 5s` also bounds executable lookup and Python startup.
Missing `timeout` produces no discovery record. The command has no unbounded fallback.
It suppresses process diagnostics so only the helper's bounded JSON can enter the injected output.
Its exact tool scope covers that command.
Native substitution and permission matching remain unverified.

Both entrypoints link to `Workflow.md` at its assembled location.
The companion preserves every byte of the old non-discovery policy after its added title.
The extraction test fixes that boundary with a digest.

## Provider assembly

The Claude variant uses explicit `mode: replace` and supplies a complete entrypoint body.
The portable base supplies Codex and the other providers.
No separate Codex variant is needed because its discovery procedure matches the portable procedure.

Shared companions pass through the existing assembly pipeline.
This change does not depend on provider-specific companion replacement or section merging.
Qualifier folders must not appear as extra skills in the assembled bundle.

## Provenance

The existing source checker updates only the entrypoint's subject digest.
Its upstream dependency digest and historical review fields remain unchanged.
The new companion and provider entrypoint have no invented adoption or reviewed-state claims.
The repository's current checker permits authored files without source sidecars.

## Validation

`tests/test_safetyfirst.py` uses standard-library unittest and temporary fixtures.
Probe tests replace `dcg` with local fixtures and never invoke the installed guard.
The fixtures cover success, absence, failure, missing runtime, missing helper, large output, timeout, and ignored termination.
Malicious fixtures print success markers, fake JSON, control characters, and padding before a failed exit.
A descendant fixture retains the output pipes after its parent exits successfully.
The tests require bounded termination and unknown version state for that process tree.
Separate fixtures stall executable lookup and runtime startup, which the outer timeout terminates.

Set `RUNE_TEST_BINARY` to a candidate Rune executable for assembly tests.
Those tests copy SafetyFirst into a temporary module and run `assemble` there.
They also require `rune validate --skill-layers` to accept the copied source and its Claude variant.
They do not deploy provider files or change user configuration.
Without that variable, assembly tests fail because required evidence is unavailable.

The assembly checker rejects a missing companion and an append variant that retains both discovery procedures.
The positive case verifies complete Claude and Codex bundles.
These tests validate commands and assembled content, not native Claude injection permission matching or model behavior.
The [proposed decision](adr.md) explains the source-only link alias and the assembled-path validation boundary.

## Risks

An installed executable does not prove that a guard intercepts this session's commands.
Native Claude invocation must separately verify its exact tool scopes and substitution behavior.
The helper controls its process group. It does not claim OS containment for a program that deliberately escapes that group.
The shared policy retains the existing denial and commit instructions for the separate authorization change.
