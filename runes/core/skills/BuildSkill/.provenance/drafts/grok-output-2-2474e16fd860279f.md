UNIT: ClaudeSkill.md  
VERDICT: adapt  
WHY: Claude-specific `@`, CLAUDE.md, and `!` guidance still belong in a deck that deploys to Claude Code, but paths, naming, and discovery are forge-shaped (PascalCase `skills/MySkill/`, `plugin.json` as the only discovery story).  
REPLACEMENT:
- Title/intro: keep Claude Code scope; change “module” wording to “rune domain / deck deploy target” where it implies forge modules.
- Resolution table: replace `skills/MySkill/` → `runes/<domain>/skills/<skill-name>/` and name examples to kebab-case (`build-skill`, not `MySkill`).
- Skill Discovery section: rewrite for deck/`rune` deploy into Claude’s skills dir (still mention that Claude discovers `*/SKILL.md` under configured skill roots). Drop forge `plugin.json` as the primary deck authoring contract unless the deck’s Claude target still uses it after `rune` deploy—if it does, keep `plugin.json` only as “post-deploy Claude surface,” not “how the deck packages skills.”
- Naming Conventions table: keep patterns; drop any implication that module names are PascalCase.
- Dynamic context injection closing: keep; already points at DynamicContextInjection.md (deck-first-class).
- No network/injection danger; no cut of `@`/`!` content.

UNIT: CliToolIntegration.md  
VERDICT: keep  
WHY: Provider-agnostic authoring checklist with no forge paths, PascalCase, or INSTALL/autoMode machinery. Fits deck skills that wrap `rune` or other CLIs.

UNIT: DynamicContextInjection.md  
VERDICT: adapt  
WHY: Deck treats `!` injection as first-class; body is mostly correct for Claude-first skills, but one forge-deploy note and forge-cli issue are wrong for this destination.  
REPLACEMENT:
- Delete the parenthetical entirely: `(Note: \`forge assemble\` currently strips it for the Claude provider, forge-cli#69, until fixed, a forge-deployed skill loses the field.)`
- Keep: SKILL.md-body-only, `allowed-tools` required in frontmatter (matches deck: no SKILL.yaml sidecar), no expansions, self-guarded commands, Claude-only portability warning, secret/slow/mutate bans.
- Example frontmatter: keep `allowed-tools:`; optional rename `MySkill` → `my-skill` for deck kebab-case consistency.
- Flag (already good, keep as constraint): never inject `pass show` / secret values — retain that ban as-is.

UNIT: MultiProviderRouting.md  
VERDICT: cut  
WHY: Entire file is forge `defaults.yaml` + `forge install` provider allowlists. Deck explicitly has its own provider assembly and no skill-level multi-provider defaults.yaml routing.

UNIT: PlatformAgnostic.md  
VERDICT: adapt  
WHY: Anti-scaffold and multi-provider neutrality still apply; skill-name examples and “MemoryCapture” identifiers are old PascalCase forge convention.  
REPLACEMENT:
- Forbidden list, no-template prose, keep.
- “Use the skill name directly”: change example from `"MemoryCapture", not "/MemoryCapture"` → `"build-skill" / "memory-capture", not "/build-skill"`.
- Provider paragraph: keep multi-provider neutrality; if deck skills may be Claude-first with graceful degradation, add one sentence that Claude-only extensions (`!`, `@`, `$ARGUMENTS`) are allowed when the skill’s description/compatibility states Claude-first (align with DynamicContextInjection.md).
- No other cuts.

UNIT: SkillInstallation.md  
VERDICT: cut  
WHY: Whole convention is forge INSTALL.md + Mintlify template + `~/.config/forge/` + module INSTALL.md + forge-cli template URL. Deck has not decided an INSTALL.md convention; shipping this would invent forge process in the deck.

UNIT: SkillStructure.md  
VERDICT: adapt  
WHY: Needed as the structural companion for build-skill, but almost every concrete rule is forge (PascalCase dirs, SKILL.yaml, forge `@` assembly, vault workspace, `make install`, incomplete/wrong frontmatter vs deck).  
REPLACEMENT: replace file content with deck-aligned structure (concrete target text):

```markdown
# Skill structure (deck)

A skill is a directory under `runes/<domain>/skills/<skill-name>/` containing `SKILL.md` as the entrypoint ([Agent Skills][AGENTSKILLS] / Claude Code skills docs).

`SKILL.md` carries YAML frontmatter plus the workflow body. Companion files (templates, examples, topic guides) live alongside. Skills are lazy-loaded: `SKILL.md` is injected when the user invokes the skill or the description matches. Companions load on demand unless explicitly composed into the body.

## Deck layout

| Path | Purpose |
| ---- | ------- |
| `runes/<domain>/skills/<skill-name>/SKILL.md` | Entrypoint |
| `runes/<domain>/skills/<skill-name>/*.md` | Companions (workflows, topics, references) |
| `runes/<domain>/skills/<skill-name>/scripts/` | Optional helper scripts |
| `runes/<domain>/skills/<skill-name>/agents/` | Optional subagent prompt templates |
| `runes/<domain>/skills/<skill-name>/assets/` | Optional static assets |

There is **no** `SKILL.yaml` sidecar in the deck. `argument-hint`, `allowed-tools`, and related metadata live in SKILL.md frontmatter only.

## `@` includes vs plain references

- Use `@File.md` only for companions that must be auto-injected on every invocation (Claude Code).
- For optional/variant companions, use plain links/backticks and let the model Read on demand.
- Never write `[@File.md](File.md)` (ambiguous).
- Do not `@`-inline every mode of a multi-mode skill.

Dynamic context injection (`!`) is first-class for Claude-targeted skills; see DynamicContextInjection.md. `!` runs only in the SKILL.md body, not in `@` companions.

## SKILL.md frontmatter (deck)

```yaml
---
name: skill-name
description: >
  What it does. USE WHEN trigger one, trigger two, or trigger three.
  Not for anti-trigger cases that should route elsewhere.
argument-hint: "[optional args hint]"
allowed-tools: Bash(git *) Read
# optional: version, disallowed-tools, context, agent, model,
# when_to_use, compatibility, license
---
```

**Rules:**
- `name:` — kebab-case, 1–64 chars, **must match the directory name** (agentskills.io / deck standard). PascalCase is retired.
- `description:` — includes `USE WHEN` triggers and a `Not for` anti-trigger clause; keep within platform limits (~1024 chars where applicable).
- `argument-hint:` — optional; lives in frontmatter (not a sidecar).
- No separate `triggers:` / `workflows:` arrays; no forge `SKILL.yaml`.

Validate with the deck’s mdschema (frontmatter fields, heading depth ≤ 3, no skipped levels) and the adopt-artifact pipeline when bringing skills in.

## Body structure

```markdown
# skill-name

Brief description.

## Instructions

1. First action
2. Second action
3. Third action

## Constraints

- Boundaries and non-goals
```

Use plain numbered lists for steps (not `### Step 1:`). For multi-workflow skills, add a `## Workflow Routing` table pointing at companions; keep SKILL.md as routing + procedure, extract bulk reference into companions.

## Naming

| Component | Convention | Examples |
| --------- | ---------- | -------- |
| Skill directory | kebab-case | `build-skill`, `adopt-artifact` |
| `name` frontmatter | same as directory | `build-skill` |
| SKILL.md | always `SKILL.md` | — |

**Variants:** name the skill for stable scope; put variants in companions (`fantasy.md`), not `style-czech-fantasy` skill dirs, when siblings are plausible.

## Discovery and deploy

Authors place skills under `runes/<domain>/skills/`. Deploy and drift checks use the `rune` CLI (not `forge install` / module Makefiles). Provider-specific install roots are the deck’s assembly concern, not per-skill `defaults.yaml`.

[AGENTSKILLS]: https://agentskills.io
```

(Remove forge CC-only link-or keep Claude docs as secondary if desired; do not reintroduce SKILL.yaml, PascalCase, vault personal-skill paths, or `make install`.)

UNIT: UserConfigSchema.md  
VERDICT: cut  
WHY: Entire autoMode-mirror + `~/.config/forge/<artifact>` + `forge <artifact> config` convention is undecided for the deck; shipping it would lock forge user-config patterns into build-skill.
