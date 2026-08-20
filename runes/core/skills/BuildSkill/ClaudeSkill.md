# Claude Code skill features

Canonical skills use Agent Skills frontmatter. The directory, name, and H1 use identical casing. Providers deploy the authored casing without changes. Only the agentskills provider converts names to lowercase.

Canonical frontmatter also supports three assembly directives: `targets`, `disable-model-invocation`, and `user-invocable`. See [SkillStructure.md](SkillStructure.md) for details. Claude Code provider data supplies all other extensions during assembly. These extensions do not appear as nonstandard top-level fields in canonical `SKILL.md`.

## Feature map

- Dynamic context injection: substitutes live machine state before Claude sees the body; see [DynamicContextInjection.md](DynamicContextInjection.md).
- `allowed-tools`: an Agent Skills field that Claude Code uses to pre-approve tool scopes for the invoking turn.
- `disallowed-tools`: a Claude Code provider restriction supplied by provider data.
- `context: fork` and `agent`: Claude Code provider settings that run the skill in a subagent where interactive tools are unavailable.
- `$ARGUMENTS`, `$N`, `${CLAUDE_SKILL_DIR}`: Claude Code body substitutions; see [DynamicContextInjection.md](DynamicContextInjection.md).
- `when_to_use`: Claude Code routing text supplied by provider data.

## Companion references

Canonical skills reference companions with relative Markdown links so the model loads them on demand. Claude Code expands `@file` references inline when loading a skill, so canonical source does not use them.

## Skill discovery

Claude Code finds a skill by its directory under the provider tree. Authors write canonical identity and instructions; a deployment step owns provider paths, namespace data, and provider extensions. See [RuneDeck.md](RuneDeck.md) for how that works in a Rune deck.

## CLAUDE.md

Global and project `CLAUDE.md` files carry standing Claude Code instructions outside skills. They are harness memory, not authored artifacts, and nothing in a skill should assume their contents.
