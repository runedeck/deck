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

ANSWER-ONLY. Do not use tools. Units for THIS batch: the eight topic companions below, each as ONE unit. Same output format.


===== FILE: ClaudeSkill.md =====
# Claude Code Skill Conventions

Claude Code-specific features for skills. This supplements the generic skill conventions in SKILL.md.

## @ File References

The `@` symbol in SKILL.md (and CLAUDE.md) files includes another file's content into the AI's context. This is the primary mechanism for composing instructions from multiple files.

```markdown
---
name: MySkill
description: Does something useful...
---

@conventions.md
@tools-reference.md

# MySkill
...
```

Both referenced files get expanded inline before the AI sees the skill. Resolution is always relative to the SKILL.md file's directory.

### Resolution Rules

| SKILL.md location                     | `@companion.md` resolves to             |
|---------------------------------------|-----------------------------------------|
| `skills/MySkill/SKILL.md`            | `skills/MySkill/companion.md`           |
| `~/.claude/skills/MySkill/SKILL.md`  | `~/.claude/skills/MySkill/companion.md` |

### Directory References

`@src/components/` shows the file listing of that directory -- useful for giving the AI a structural overview without reading every file.

### When to Use @ References

- **Any content the skill needs** -- conventions, reference tables, shared config, tool catalogs
- **Content shared across multiple skills** in the same module
- **Provider-specific content** that only applies to Claude Code
- **Large reference material** that would bloat the main SKILL.md

Keep inline when the section is short (<20 lines) and tightly coupled to the skill body.

## CLAUDE.md @ References

CLAUDE.md files (global or project-level) use the same `@` mechanism:

| Level         | File                          | Applies to                     |
|---------------|-------------------------------|--------------------------------|
| Global        | `~/.claude/CLAUDE.md`         | Every project, every session   |
| Project       | `<project>/CLAUDE.md`         | All sessions in this project   |
| Project-local | `<project>/.claude/CLAUDE.md` | All sessions (gitignored)      |

### When to Extract from CLAUDE.md

Extract a section into a separate `@`-referenced file when:
- **It's domain-specific** -- tool catalogs, API references, module docs
- **It's reusable across projects** -- coding conventions, commit rules
- **It exceeds ~50 lines** -- large blocks dilute surrounding instructions
- **It changes independently** -- tool docs update on different cadence than project rules

### Naming Conventions

| Pattern               | Use for                              |
|-----------------------|--------------------------------------|
| `RTK.md`, `TOOLS.md` | Uppercase -- tool/system references  |
| `conventions.md`      | Lowercase -- style and practice docs |
| `<module>.md`         | Module-specific reference            |

## Skill Discovery

Claude Code discovers skills through `plugin.json`:

```json
{
    "skills": ["./skills"]
}
```

Every directory listed is scanned for `*/SKILL.md` files. Skills in later directories override earlier ones of the same name (last wins).

## Dynamic context injection (`!`)

A Claude skill can open with live machine state via `` !`<command>` `` lines in the SKILL.md body, the output runs and is substituted before Claude sees the content. This is a first-class authoring concern with its own guide: **[@DynamicContextInjection.md](DynamicContextInjection.md)**. Reach for it whenever a skill's job starts with orienting on current state.

===== FILE: CliToolIntegration.md =====
When a skill wraps a CLI tool (Rust binary, shell script), include:

1. **Tool location** — where the binary lives
2. **Usage examples** — concrete `bash` blocks showing invocation
3. **Intent-to-flag mapping** — table translating natural language to CLI flags
4. **Output format** — what the tool returns (JSONL, plain text, etc.)

===== FILE: DynamicContextInjection.md =====
# Dynamic context injection (`!`)

A Claude Code skill can open with **live machine state** instead of stale prose. `` !`<command>` `` lines in the SKILL.md body run when the skill is invoked, and their output replaces the placeholder before Claude sees the content ("Inject dynamic context", a Claude Code extension to the Agent Skills standard).

When authoring a Claude skill, treat this as a first-class step, not an afterthought: **ask what live state would orient the model on load, and inject it.** A skill that opens with the actual situation (the current branch and diff, a tool's auth status, the names of things that exist right now) beats one that only describes how to go find it. Default to injecting unless there is a reason not to.

```markdown
---
name: MySkill
description: ...
allowed-tools: Bash(git status *) Bash(git diff *)
---

# MySkill

Current branch and changes:

!`git status --short 2>/dev/null || echo "(not a git repo)"`
```

Each `` !`<command>` `` runs once, before the rendered SKILL.md is sent to Claude; the output replaces the placeholder inline. Substitution is single-pass: injected output is not re-scanned for further placeholders.

## Hard constraints (verified by running it, not just the docs)

- **SKILL.md body only.** `!` executes only in the SKILL.md body, never in `@`-companion files (those load as plain text). Put every injected command in SKILL.md and keep companions as reference prose.
- **`allowed-tools` is required.** List the Bash scopes the injected commands need in the SKILL.md frontmatter, e.g. `allowed-tools: Bash(pass *) Bash(git *)`. It is a frontmatter field in SKILL.md itself (space-, comma-, or list-separated); there is no sidecar location. (Note: `forge assemble` currently strips it for the Claude provider, forge-cli#69, until fixed, a forge-deployed skill loses the field.)
- **No shell expansions.** The injection rejects any command containing `$(...)`, `${...}`, or backticks with a `Contains expansion` error. Keep injected commands simple and static; a guarded summary that needs command substitution will not run, inject the raw command output instead.
- **No built-in error handling.** A failing command does not degrade gracefully; it breaks or blanks the injection. Self-guard every command so a missing tool, logged-out session, or empty result cannot break skill load:

  ```markdown
  !`pass-cli vault list 2>/dev/null || echo "(proton pass: not logged in)"`
  ```

- **Claude Code only.** `!`, `@`, and `$ARGUMENTS` are Claude Code extensions, not part of the portable Agent Skills standard. In Codex / Gemini / opencode the `!` lines render as inert literal text. Use injection in skills you accept as Claude-first; it degrades to harmless text elsewhere.

## Substitutions available alongside `!`

`$ARGUMENTS`, `$ARGUMENTS[N]`, `$N`, `$name` (named args), and `${CLAUDE_SESSION_ID}` / `${CLAUDE_EFFORT}` / `${CLAUDE_SKILL_DIR}` are substituted in the SKILL.md body the same way.

## What to inject, and what never to

Inject **read-only, fast, structural state** that orients Claude: the current branch, a file listing, a tool's status, the names of things. Never inject:

- **Secret values.** For a credential skill, inject the *map* (entry names, vault list, auth status), never the *territory*. `` !`pass ls` `` is fine (entry names); `` !`pass show <x>` `` is forbidden, it would dump a live secret into the transcript and context.
- **Slow or interactive commands.** Injection blocks skill load; a command that prompts, hangs, or takes seconds makes the skill feel broken.
- **Mutating commands.** Injection should observe, not change state.

The litmus test: if the command's output appearing verbatim in the session transcript would be a problem, do not inject it.

===== FILE: MultiProviderRouting.md =====
Provider routing is controlled by the module's `defaults.yaml`, not by individual SKILL.yaml files. `forge install` reads provider-keyed allowlists to decide which skills deploy where:

```yaml
# defaults.yaml
skills:
    claude:
        SkillName:
    gemini:
        SkillName:
    codex:
        SkillName:
    opencode:
        SkillName:
```

Skills listed under a provider key are installed for that provider. Skills omitted from a provider's list are skipped. This allows Claude-only skills (e.g., those using TeamCreate or agent teams) to be excluded from Gemini/Codex/OpenCode without per-skill configuration.

===== FILE: PlatformAgnostic.md =====
Skills and agent definitions are instructions, not templates. Write them as plain prose an AI can follow — no scaffolding artifacts.

Forbidden: `{{placeholders}}`, `[REPLACE THIS]`, `<!-- TODO -->`, stub headings with no content, empty tables generated by a scaffold. If a section has nothing to say, delete it.

Keep YAML frontmatter and `@` file includes — those are structural. But never reference skills with `/` prefix inside definitions. Use the skill name directly (e.g. "MemoryCapture", not "/MemoryCapture"). The slash is user-facing invocation syntax, not an internal identifier.

A skill or agent that deploys to every provider must not assume one provider. Don't hardcode a single tool's agent identifier, CLI binary, or command syntax (`--agent claude-code`, `claude --resume`) when the artifact also runs under Codex, Gemini, or OpenCode. Parameterize the agent (`--agent <agent>`, listing the supported tools) and name actions neutrally ("the agent's resume command", not `claude --resume`). Documenting a tool's own factual default (a CLI flag that defaults to `claude-code`) is fine; that is the tool's behavior, not your assumption.

===== FILE: SkillInstallation.md =====
# Skill Installation (INSTALL.md)

## When to include

A per-skill INSTALL.md is required when the skill needs user actions the plugin system cannot automate:

- Creating a user-config file (`~/.config/forge/<artifact>.{ext}`)
- Authenticating with an external service (API tokens, OAuth flows)
- Installing a tool unique to that skill (not a module-wide shared prerequisite)

Skills that work after `make install` or plugin add need no INSTALL.md. Hooks auto-discovered via `hooks/hooks.json` need no INSTALL.md.

## What does NOT belong in per-skill INSTALL.md

- **Shared prerequisites** (gitleaks, yq, jq) belong in the module-level INSTALL.md at the repo root
- **Hook wiring** belongs in `hooks/hooks.json` (auto-discovered by the plugin system)
- **Behavioral guidance** belongs in SKILL.md

## Shape

Same Mintlify standard as the repo-level INSTALL.md. Required elements: H1 title, blockquote summary, conversational opening, OBJECTIVE, DONE WHEN (measurable), TODO checklist, Steps with shell commands, EXECUTE NOW closing.

Template at `templates/init/INSTALL.md` in [forge-cli][TEMPLATE].

## Boundary

| Content type | Lives in |
|---|---|
| "When committing, follow these rules" | SKILL.md |
| "Run this command to set up the skill" | INSTALL.md |
| "Install gitleaks" (used by multiple skills) | Module INSTALL.md |
| Hook script that fires on PreToolUse | `hooks/` + `hooks.json` |

## Related

- [InstallInstructions](../../rules/InstallInstructions.md) — the rule establishing this convention
- [UserConfigSchema](UserConfigSchema.md) — when the config file uses the autoMode-mirror pattern

[TEMPLATE]: https://github.com/N4M3Z/forge-cli/blob/main/templates/init/INSTALL.md

===== FILE: SkillStructure.md =====
A skill is a directory under `skills/` containing `SKILL.md` as the entrypoint ([Claude Code docs][CCDOCS]).

`SKILL.md` carries YAML frontmatter (`name`, `description`, and optionally `argument-hint`, `allowed-tools`, `model`, `effort`, `context`, `hooks`, `paths`, `shell`) plus the workflow body. Companion files (templates, examples, reference material) live alongside. Skills are lazy-loaded: `SKILL.md` is only injected into context when the user invokes the skill or the AI matches the description. Companion files are loaded on demand when the AI decides it needs them during execution.

## Forge additions beyond the native spec

| File          | Purpose                                        |
| ------------- | ---------------------------------------------- |
| `SKILL.yaml`  | Sidecar for reference URLs and provider hints  |
| `user/`       | Qualifier directory, flattened at assembly     |
| `@` includes  | Companion file references, resolved by forge    |

**`@` includes vs plain references**: use `@File.md` only for companions that should be auto-injected alongside SKILL.md on every invocation. For optional or variant companions (e.g. a multi-mode skill where only one mode is loaded per run), use plain filename references like `` `File.md` `` and let the AI load on demand. Over-use of `@` wastes tokens on unused companions. Never mix the forms.

```markdown
GOOD — always-loaded reference (forge inlines content into SKILL.md at parse time)
@SkillStructure.md

GOOD — load-on-demand reference (AI reads via Read tool when the workflow needs it)
See [`Linting.md`](Linting.md) for the full lint pipeline.

GOOD — same companion table, different intent
| Workflow | Companion           |
| -------- | ------------------- |
| Create   | @CreateWorkflow.md   |       <- always inline
| Validate | `ValidateWorkflow.md` |     <- load on demand

BAD — `@` inside a markdown link reads as "auto-inject", looks like a regular link, behaves like neither
[@File.md](File.md)

BAD — `@` on a multi-mode router; every variant inlines on every invocation, defeating routing
@FantasyMode.md
@SciFiMode.md
@NoirMode.md
```

## SKILL.md frontmatter

```yaml
---
name: SkillName
description: What it does. USE WHEN trigger phrase one, trigger phrase two, or trigger phrase three.
---
```

**Frontmatter rules:**
- `name:` — PascalCase for multi-word (`VaultOperations`, `DailyPlan`), natural casing for single words (`Log`, `Draft`, `Init`)
- `version:` — semantic version (required for module skills, optional for personal/vault skills)
- `description:` — single line, under 1024 characters, includes `USE WHEN` with intent-based triggers joined by commas/OR
- Optional: `argument-hint:` for skills invoked with `/SkillName <args>` (e.g., `"[natural language description]"`)
- No separate `triggers:` or `workflows:` arrays in YAML

## Body structure

```markdown
# SkillName

Brief description of what the skill does.

## Instructions (or ## Usage)

Step-by-step procedure. Use plain numbered lists for sequential operations.

1. First action
2. Second action
3. Third action

## Constraints

- Boundary conditions and rules
- What NOT to do
```

**Instruction format**: Use plain numbered lists (1, 2, 3) — not labeled steps (`### Step 1:`, `### Phase 2:`, `### Step M1:`). Headings within Instructions are for separating modes or major sections, not for individual steps.

**For skills with multiple workflows:** use a `## Workflow Routing` table pointing at companion files. Keep SKILL.md focused on flow and routing, not static data. Extract reference material (schema templates, configuration examples, lookup tables) into companion files.

## Where skills live

| Location             | Purpose                               |
| -------------------- | ------------------------------------- |
| `skills/SkillName/`  | Module skills (shipped with a module) |
| User vault workspace | Personal/experimental skills          |

All parent directories must be registered in `plugin.json` under the `skills` array for Claude Code discovery. Other providers (Gemini, Codex, OpenCode) use `make install` from the module's Makefile.

## Naming conventions

| Component         | Convention        | Examples                                      |
| ----------------- | ----------------- | --------------------------------------------- |
| Skill directory   | PascalCase        | `BuildSkill`, `DailyPlan`, `VaultOperations`  |
| Single-word skill | Natural case      | `Log`, `Draft`, `Init`, `Update`              |
| SKILL.md          | Always `SKILL.md` | —                                             |

**Naming around variants**: when a skill could plausibly spawn siblings (e.g. `StyleCzech` may want `Fantasy`, `Scifi`, `Noir`), don't bake the variant into the skill name. Name the skill for its stable scope and push variants into companion files (`Fantasy.md`, `Scifi.md`). Prefer `StyleCzech` with `Fantasy.md` over `StyleCzechFantasy`. Apply this only when variants are plausible — a truly single-purpose skill stays named for its purpose.

[CCDOCS]: https://code.claude.com/docs/en/skills

===== FILE: UserConfigSchema.md =====
# User Config Schema (autoMode mirror)

When an artifact needs per-user runtime data, follow the [UserConfig](../../rules/UserConfig.md) rule — one file per artifact at `~/.config/forge/<artifact>.{ext}`. When the config is intended to be read by an AI in the loop (skill, agent, or hook with model access), shape it after [Claude Code's `autoMode`][AM]: natural-language entries with a four-tier precedence model and a `$defaults` splice token.

## Why mirror autoMode

The pattern is already familiar to anyone configuring Claude Code. Entries are prose — descriptions a human (or AI) would naturally write — not regex or tool-pattern grammars. The `$defaults` token gives a splice-or-replace toggle for built-in defaults shipped with the artifact source. Users extend the built-ins by adding entries; they take full ownership by omitting `"$defaults"`.

## Shape

Top-level keys are tiers with strict precedence: `hard_deny` > `soft_deny` > `allow` > `environment`. Each value is an array of prose strings.

```yaml
environment:
    - "$defaults"
    - "<who I am and where I work>"

allow:
    - "$defaults"
    - "<exceptions to soft_deny — surfaces that are intentional>"

soft_deny:
    - "$defaults"
    - "<rules the user can override with explicit intent>"

hard_deny:
    - "$defaults"
    - "<rules that cannot be overridden>"
```

## Tier semantics

- `hard_deny` blocks unconditionally. No `allow` exception or user intent applies.
- `soft_deny` blocks next. `allow` exceptions and explicit user intent can override.
- `allow` overrides matching `soft_deny` entries.
- `environment` provides context: trusted infrastructure, identities, repo ownership.

Setting any tier without `"$defaults"` replaces the entire built-in list for that tier. Default entries are spliced at the position of the token, so custom entries can go before or after them.

## When NOT to use this pattern

Deterministic consumers (shell scripts, pre-commit hooks, CI gates without model access) can't interpret prose. Ship a sibling artifact for those — same `~/.config/forge/` directory, different filename — with a flat regex list or other machine-readable structure. Don't try to mix prose and regex in one file; the consumer types diverge.

Example pairing: `~/.config/forge/forensic.yaml` (prose, read by ForensicAgent) and `~/.config/forge/danger-strings` (regex, read by the pre-commit hook).

## Discovery and inspection

The artifact source documents its built-in `$defaults` inline (in `SKILL.md` body or the agent body) so users can read what they inherit before extending. A `forge <artifact> config` subcommand printing the effective merged config is recommended but not required.

## Reference

[AM]: https://code.claude.com/docs/en/auto-mode-config "Claude Code: Configure auto mode"
