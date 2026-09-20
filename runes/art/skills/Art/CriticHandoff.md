# Critic handoff

Use this procedure when Art requests independent palette review.
PaletteCritic is a separate agent supplied by the art module, not another skill invocation.

## Resolve the agent

Find PaletteCritic in the installed agent catalog.
If named invocation is unavailable, read its canonical definition from the art module's `agents/PaletteCritic.md`.
Send that definition as the role instructions through the available task tool.
Do not infer a provider-specific tool identifier or assume that a skill-only installation includes the agent.

If the definition or delegation tool is unavailable, state that limitation and perform a labeled self-review when useful.
Do not report independent validation from that fallback.
If the user requires independence, return supported work and identify the missing review.

## Send a complete review packet

Provide the actual content the agent needs. A companion name alone does not transfer its instructions.
For relevant methods, include the loaded painting and technique guidance or accessible files with an explicit reading instruction.
Ensure that reference images are accessible to the agent. State when it receives only a description.

```text
Scope: the specific palette or material claim to challenge.
Brief: subject, reference type, variant, desired appearance, and intentional departures.
State: current preparation, existing color layers, tools, and finish.
Materials: available paints, chosen inks, metallic or NMM preference, and current budget with exclusions.
Proposal: paint-to-area mapping, method, sequence, and candidate mixtures.
Evidence: images, direct source pages, supplied test results, relevant technique guidance, and access limits.
Question: what evidence could make this proposal wrong, and what is the smallest supported correction?
Boundary: return findings only. Do not edit collections or start more reviewers.
```

Do not include a preferred verdict or reward disagreement for its own sake.
A sound plan can pass without changes.

## Split independent challenges

For explicit multiple-agent review, give each reviewer the same brief and proposed plan.
Split material behavior, values and application method, and reference identity into bounded checks.
Keep the first reviews independent. Let the coordinator reconcile their findings afterwards.
Use separate research tasks for missing artwork. Do not make PaletteCritic own a collection search.

Judge findings by inspected evidence and their effect on the plan, not by votes.
Retain disagreement that evidence cannot resolve and name the smallest useful physical test.
Do not let review postpone an immediate answer beyond the checks that can change it.

## Integrate the findings

Verify each accepted correction against the current brief.
Retain correct preparation, chosen materials, and deliberate reference departures.
Update the guide and authorized notes once, after reconciling findings.
State the scope of review and distinguish it from physical testing or measured benchmark performance.
