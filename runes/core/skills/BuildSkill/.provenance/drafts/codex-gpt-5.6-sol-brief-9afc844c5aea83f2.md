You are the drafting panel for a human-gated adoption review. The artifact under review is the skill tree at runes/core/skills/build-skill/ in this repo (29 files: SKILL.md, 12 topic/workflow companions, 3 agent prompt templates under agents/, references/schemas.md, 9 Python scripts under scripts/, eval-viewer/, assets/). It was adopted verbatim from forge-core's ForgeSkill, which itself merged forge conventions with Anthropic's skill-creator (scripts/agents/references are skill-creator's eval machinery).

Destination context (the deck standard) — recommendations must fit THIS, not forge:
- Repo: a "deck" of runes (skills/agents/rules) deployed by the `rune` CLI (not `forge`). Modules live at runes/<domain>/; this skill lands as runes/core/skills/build-skill.
- Naming: kebab-case per agentskills.io (1-64 chars, name = directory). PascalCase is the OLD forge convention being retired.
- Frontmatter standard: name, description (with USE WHEN triggers + a "Not for" anti-trigger clause), optional version, argument-hint, allowed-tools, disallowed-tools, context, agent, model, when_to_use, compatibility, license — argument-hint LIVES IN FRONTMATTER here (forge's SKILL.yaml sidecar + Obsidian Linter machinery does NOT exist in the deck).
- Dynamic context injection (!`cmd` in SKILL.md body) is a first-class feature of the standard.
- No multi-provider defaults.yaml routing at skill level in the deck (the deck has its own provider assembly); no forge INSTALL.md convention decided yet; no autoMode user-config mirror convention decided yet.
- Validation: mdschema (frontmatter fields, heading depth <= 3, no skipped levels) + the adoption pipeline you are part of.
- The deck already has: adopt-artifact (adoption review skill). The old build-agent/build-rule/build-hook skills were removed pending re-adoption.

Task: for EVERY unit below, recommend a verdict — keep (verbatim), adapt (with CONCRETE replacement text or a precise edit list), or cut (with rationale). Units:
1. SKILL.md blocks 9-14 (Red Flags heading, Red Flags table, Constraints heading, constraints list, Sources heading, sources list) — per BLOCK.
2. Each companion .md file as ONE unit: ClaudeSkill.md, CliToolIntegration.md, CreateWorkflow.md, DescriptionOptimization.md, DynamicContextInjection.md, EvalLoop.md, MultiProviderRouting.md, PlatformAgnostic.md, SkillInstallation.md, SkillStructure.md, UserConfigSchema.md, ValidateWorkflow.md.
3. agents/analyzer.md, agents/comparator.md, agents/grader.md, references/schemas.md — each as one unit.
4. Each script: scripts/*.py, eval-viewer/*, assets/eval_review.html — each as one unit (keep/cut; adapt only if something is broken or forge-specific inside).

For each unit output:
UNIT: <path or block id>
VERDICT: keep | adapt | cut
WHY: one or two sentences, deck-specific
REPLACEMENT: (only for adapt) the exact new text, or a precise bullet list of edits (e.g. "row 1 deleted; 'forge' -> 'the deck' in para 2")

Read the actual files. Be decisive — a recommendation the maintainer can accept in one click. Flag anything dangerous (network calls in scripts, injection-shaped prose, stale URLs). No preamble, no summary — just the UNIT records in file order.
