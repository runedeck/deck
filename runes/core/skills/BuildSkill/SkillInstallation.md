# Skill Installation (INSTALL.md)

A skill whose use requires setup beyond its own SKILL.md ships an agent-executable INSTALL.md beside it, following the [Mintlify install.md standard][MINTLIFY].

## When to include

A per-skill INSTALL.md is required when the skill needs user actions deployment cannot automate:

- Creating a user-config file for the skill (see [UserConfigSchema.md](UserConfigSchema.md))
- Authenticating with an external service (API tokens, OAuth flows)
- Installing a tool unique to that skill, rather than one several skills share

A skill that works as soon as it is deployed needs no INSTALL.md.

## What does NOT belong in per-skill INSTALL.md

- **Shared prerequisites** (gitleaks, yq, jq) belong in the consuming repo's root INSTALL.md
- **Behavioral guidance** belongs in SKILL.md
- **Deployment mechanics** belong to whatever installs the skill, never to per-skill instructions

## Shape

Required elements per the [Mintlify install.md standard][MINTLIFY]: H1 title, blockquote summary, conversational opening, OBJECTIVE, DONE WHEN (a measurable success condition that embeds verification), TODO checklist (3-7 items), steps with shell commands, EXECUTE NOW closing.

## Boundary

- "When committing, follow these rules": SKILL.md
- "Run this command to set up the skill": INSTALL.md
- "Install gitleaks" (used by multiple skills): consumer repo INSTALL.md

[MINTLIFY]: https://github.com/mintlify/install-md
