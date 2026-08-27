---
name: ConfigureScanners
description: "Configure prompt-only public exposure scanners with BuildTask. USE WHEN configuring a public repository, GitHub, web mention, or social PII scanner. NOT FOR running scans, accessing private sources, interpreting findings, fixing exposures, or adding deterministic scanner services."
license: EUPL-1.2
metadata:
    version: 0.1.0
---

# ConfigureScanners

Prepare one public exposure scanner.
Use BuildTask to produce the provider setup package.

## Prerequisites

- BuildTask is installed and available.
- The user selects one scanner.
- The user has access to the selected provider.

If BuildTask is unavailable, stop and give the scanners cast installation command.

## Constraints

- Configure only one scanner during each invocation.
- Never run the scan.
- Never access a public or private source.
- Never create or change a provider task.
- Never write user input to a file.

- Never write a rendered prompt to a local file.
- Never use account memory as input.
- Never infer a missing identity value.
- Never request a private email address, phone number, home address, or government identifier.
- Never request a credential, recovery phrase, private hostname, or private account identifier.

- Use only values that the user approves as public search terms.
- Explain that each search term reaches the selected provider.
- Explain that the provider stores each rendered public value.
- Never claim that a prompt or task definition enforces a provider permission.
- Keep deterministic scanners outside this task package.

## Instructions

### Select the scanner

Read references/ScannerCatalog.md.
Use one scanner definition from that catalog.

Ask the user to select a scanner when the request does not identify one.
Read only the selected template.
Ask for an exact model identifier when the catalog requires user selection.
Reject `current` and `latest` as model identifiers.

### Collect approved values

Read [ScannerInputs.md](references/ScannerInputs.md).
Ask only for required inputs and missing optional inputs.
Validate each value before rendering.
Use `- None.` only for an optional empty list.

### Create the task definition

Use the selected definition for the provider, template, and daily time.
Use the user time zone.
Use no model fallback.
Set the write policy to deny.

Set external scanners to deny.
Set connectors, plugins, skills, and uploads to deny.
Set one final notification.
Use the selected input schema.
Use the selected checks from [ScannerCanaries.md](references/ScannerCanaries.md).

### Use BuildTask

Use the installed BuildTask skill.
Pass it the task definition and the selected complete template.
Pass it the approved placeholder values.
Pass it the typed input schema.
Pass it the selected scanner canaries and fixture specification.

BuildTask owns provider guidance, rendering, placeholder checks, output structure, and canary instructions.

## Verification

- Confirm that BuildTask received one complete task definition.
- Confirm that no placeholder remains.
- Confirm that the result contains no unapproved private value.
- Confirm that the task definition denies writes.

- Confirm that the task definition denies external scanners.
- Confirm that the rendered prompt requires complete redaction.
- Confirm that the rendered prompt reports coverage limits.
- Confirm that the task definition permits one final notification.

## References

- BuildTask supplies provider setup and common canary checks.
- [ScannerCatalog.md](references/ScannerCatalog.md) defines each scanner task.
- [ScannerInputs.md](references/ScannerInputs.md) defines typed inputs.
- [ScannerCanaries.md](references/ScannerCanaries.md) defines behavior checks.
- Each template supplies the complete scanner prompt.
