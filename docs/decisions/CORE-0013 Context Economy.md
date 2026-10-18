---
title: Context Economy
description: Every instruction earns its resident tokens, each fact lives in one artifact, and judgment replaces rulebooks for Claude 5 generation models
type: adr
category: architecture
tags:
    - architecture
    - context
    - rules
status: accepted
created: 2026-08-27
updated: 2026-10-19
author: "@N4M3Z"
project: deck
related:
    - "CORE-0014 No Performance Personas"
    - "CORE-0015 Positive Instruction"
upstream:
    - "https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: []
informed: []
change: economy-measure-context-efficiency
---

# Context Economy

## Context and Problem Statement

Anthropic removed over 80 percent of the Claude Code system prompt for the Claude 5 generation with no measured loss. The owner wrote the *[deck][DECK]* under the older assumption that more guidance means more control. The audit at main `34b08e54` counts 2232 words across sixteen core *[rules][RULE]* and 101 duplicated sentences across *[runes][RUNE]*. Every deployed session pays for this text, and every duplicate is a future conflict.

## Considered Options

1. Keep long [rules][RULE] and rely on a reviewer to prune them.
2. Adopt context economy as a decided norm, with deterministic checks that refuse an overrun.

## Decision Outcome

Option 2, context economy as a decided norm.

- Each piece of guidance stays only when its effect is worth the tokens it occupies in every session. A [rule][RULE] states one imperative statement within 50 words.
- Each fact has one home. Enforcement goes in *[hooks][HOOK]* and continuous integration, knowledge in *[skills][SKILL]*, and constraints in [rules][RULE]. Identity and gotchas go in the *[repository][REPOSITORY]* brief, and transient state in memory. A fact in two layers is a defect.
- The author trusts the judgment of the *[model][MODEL]* over a rulebook. The author gives it context and intent, and reserves a hard constraint for an invariant or for safety.
- Progressive disclosure: situational content loads on demand, through [skills][SKILL] and *[companions][COMPANION]*, and never up front.
- Interfaces over examples: an expressive tool or schema shows correct use better than a usage example.
- A way to check the output is worth more than another paragraph of guidance, so the author adds a check instead of a paragraph.

### Consequences

- [+] The [rule][RULE] corpus shrinks toward a 900-word budget, and checks that refuse an overrun keep it there.
- [+] Duplicated guidance retires instead of drifting.
- [-] Compression can drop a real constraint, so the author moves displaced content to a [skill][SKILL] before deleting it.

## More Information

Compatibility of the forge-core decisions with this norm:

| Record | Verdict | Note |
| --- | --- | --- |
| [CORE-0001 Markdown as System Language][FC-CORE-0001] | affirmed | unchanged |
| [CORE-0002 Metadata Inside Files][FC-CORE-0002] | affirmed | [deck][DECK] *[sidecars][SIDECAR]* for sealed evidence stay a recorded exception |
| [CORE-0003 YAML Frontmatter][FC-CORE-0003] | affirmed | unchanged |
| [CORE-0004 Adopt ADRs][FC-CORE-0004] | affirmed | this pass exercises it |
| [CORE-0005 ADR Template Choice][FC-CORE-0005] | affirmed | compact bodies preferred under this norm |
| [CORE-0006 Directories Direct][FC-CORE-0006] | affirmed | naming as configuration matches interfaces over examples |
| [CORE-0007 Forge MADR Extensions][FC-CORE-0007] | affirmed | unchanged |
| [CORE-0008 Variables in Markdown][FC-CORE-0008] | affirmed | unchanged |
| [CORE-0009 YAML Configuration][FC-CORE-0009] | affirmed | unchanged |
| [CORE-0010 Unified Module Validation][FC-CORE-0010] | amended | gains the chosen *[linter][LINTER]* set on migration: one [linter][LINTER] for each concern, one binary, offline on the commit path, revisions by record |
| [CORE-0011 Verified Remote Execution][FC-CORE-0011] | affirmed | the [repository][REPOSITORY]'s CI pins action references by commit and verifies release binaries by SHA-256. Reusable workflow references and package installs remain compliance gaps |
| [CORE-0012 Fixture-Based Canary Testing][FC-CORE-0012] | affirmed | the ontology smoke *[fixture][FIXTURE]* follows it |
| [ARCH-0001 Skills Agents and Rules][FC-ARCH-0001] | amended | *[agents][AGENT]* are containers, never personas, per CORE-0014 |
| [ARCH-0002 Skills Companion Files][FC-ARCH-0002] | affirmed | progressive disclosure in practice |
| [ARCH-0004 Rules as Shared Conventions][FC-ARCH-0004] | amended | shared stays, the shape becomes one imperative statement within 50 words |
| [ARCH-0011 Hook Design Principles][FC-ARCH-0011] | affirmed | strengthened: prose demotes to [hooks][HOOK] wherever a check can be code |
| [ARCH-0014 Per-Tool Memory Files][FC-ARCH-0014] | diverged | the owner authors the [deck][DECK] once and the *[assembler][ASSEMBLER]* assembles it per tool, so accepted duplication ends |

- Rewritten on 2026-10-19 in the plain spoken register. The decision is unchanged.

[DECK]: ../specs/glossary/deck.md
[RULE]: ../specs/glossary/rule.md
[RUNE]: ../specs/glossary/rune.md
[HOOK]: ../specs/glossary/hook.md
[SKILL]: ../specs/glossary/skill.md
[REPOSITORY]: ../specs/glossary/repository.md
[MODEL]: ../specs/glossary/model.md
[COMPANION]: ../specs/glossary/companion.md
[ASSEMBLER]: ../specs/glossary/assembler.md
[SIDECAR]: ../specs/glossary/sidecar.md
[LINTER]: ../specs/glossary/linter.md
[FIXTURE]: ../specs/glossary/fixture.md
[AGENT]: ../specs/glossary/agent.md
[FC-CORE-0001]: https://github.com/N4M3Z/forge-core/blob/main/docs/decisions/CORE-0001%20Markdown%20as%20System%20Language.md
[FC-CORE-0002]: https://github.com/N4M3Z/forge-core/blob/main/docs/decisions/CORE-0002%20Metadata%20Inside%20Files.md
[FC-CORE-0003]: https://github.com/N4M3Z/forge-core/blob/main/docs/decisions/CORE-0003%20YAML%20Frontmatter%20for%20Machine%20Readability.md
[FC-CORE-0004]: https://github.com/N4M3Z/forge-core/blob/main/docs/decisions/CORE-0004%20Adopt%20Architecture%20Decision%20Records.md
[FC-CORE-0005]: https://github.com/N4M3Z/forge-core/blob/main/docs/decisions/CORE-0005%20ADR%20Template%20Choice.md
[FC-CORE-0006]: https://github.com/N4M3Z/forge-core/blob/main/docs/decisions/CORE-0006%20Directories%20Direct.md
[FC-CORE-0007]: https://github.com/N4M3Z/forge-core/blob/main/docs/decisions/CORE-0007%20Forge%20MADR%20Extensions.md
[FC-CORE-0008]: https://github.com/N4M3Z/forge-core/blob/main/docs/decisions/CORE-0008%20Variables%20in%20Markdown%20Instructions%20and%20Templates.md
[FC-CORE-0009]: https://github.com/N4M3Z/forge-core/blob/main/docs/decisions/CORE-0009%20YAML%20Configuration%20Files.md
[FC-CORE-0010]: https://github.com/N4M3Z/forge-core/blob/main/docs/decisions/CORE-0010%20Unified%20Module%20Validation.md
[FC-CORE-0011]: https://github.com/N4M3Z/forge-core/blob/main/docs/decisions/CORE-0011%20Verified%20Remote%20Execution.md
[FC-CORE-0012]: https://github.com/N4M3Z/forge-core/blob/main/docs/decisions/CORE-0012%20Fixture-Based%20Canary%20Testing.md
[FC-ARCH-0001]: https://github.com/N4M3Z/forge-core/blob/main/docs/decisions/ARCH-0001%20Skills%20Agents%20and%20Rules.md
[FC-ARCH-0002]: https://github.com/N4M3Z/forge-core/blob/main/docs/decisions/ARCH-0002%20Skills%20Companion%20Files.md
[FC-ARCH-0004]: https://github.com/N4M3Z/forge-core/blob/main/docs/decisions/ARCH-0004%20Rules%20as%20Shared%20Ecosystem%20Conventions.md
[FC-ARCH-0011]: https://github.com/N4M3Z/forge-core/blob/main/docs/decisions/ARCH-0011%20Hook%20Design%20Principles.md
[FC-ARCH-0014]: https://github.com/N4M3Z/forge-core/blob/main/docs/decisions/ARCH-0014%20Per-Tool%20Memory%20Files.md
