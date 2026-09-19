# Portable skill authoring

## Why

Shared skills still prescribe native tool names and syntax from particular harnesses.
The authoring guide permits those instructions and can declare compliance without the source-layer lint.
These instructions conflict with the new portability contract.

## What Changes

- Use capability-based instructions in shared skills and companions.
- Keep Claude tool scopes in explicit Claude metadata variants.
- Preserve the interview question count and use each harness's actual question capacity.
- Remove the shared-injection exception from the authoring guide.
- Require source-layer validation before an author declares a changed skill compliant.
- Route skill creation and validation through the repeatable artifact implementation loop.
- Align three shared rules with nested model variants and portable file reading.

## Capabilities

### New Capabilities

- `portable-skill-authoring`: Keep shared instructions and their authoring checks consistent across harnesses.

### Modified Capabilities

None.

## Impact

This change covers AdoptArtifact, BenchArtifact, BuildAvatar, BuildSkill, and SimplifiedTechnicalEnglish.
It also covers the SkillLayout, ArtifactLength, and UseEfficientCLI rules.
The separate `portable-safety-discovery` change covers SafetyFirst in the same content PR.
The CLI architecture PR supplies the validator. This change adds no validator bypass or new deployment route.
The active Claude issue run retains its own schemas, hooks, and consumer work.

BuildSkill uses [one loop companion](../../../runes/core/skills/BuildSkill/ImplementationLoop.md).
