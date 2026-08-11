The EvalLoop companion is truncated mid-file; I'll pull the full offloaded prompt so every unit can get a decisive verdict.UNIT: SKILL.md#Red-Flags-heading
VERDICT: keep
WHY: Section heading is standard and deck-valid; no forge-specific wording.

UNIT: SKILL.md#Red-Flags-table
VERDICT: adapt
WHY: Row 1 encodes the retired forge/Obsidian rule that `argument-hint` must not live in frontmatter; in the deck it belongs in frontmatter. Other rows are still correct.
REPLACEMENT:
| Thought | Reality |
| --- | --- |
| "Put `argument-hint` in a SKILL.yaml sidecar" | Deck has no SKILL.yaml / Obsidian Linter path. Optional fields (`argument-hint`, `version`, `allowed-tools`, …) live in SKILL.md frontmatter. |
| "Use `/SkillName` inside a skill body" | Slashes are user-facing invocation syntax, not internal references. |
| "Skip the `USE WHEN` clause" | Routing depends on it. Missing trigger = skill never fires. Also include a `Not for` anti-trigger clause. |
| "Leave a stub section as a placeholder" | Skill bodies are plain prose. Delete empty sections; don't scaffold them. |
| "Inline every example in the SKILL.md" | SKILL.md should stay slim. Move static reference material to companion files. |
| "Skill directory can have any name" | Directory name must match the `name:` frontmatter field exactly (kebab-case, 1–64 chars). |
| "Put a `!` injection in a companion file" | `!` runs only in the SKILL.md body; in a companion it renders as literal text. See [@DynamicContextInjection.md](DynamicContextInjection.md). |
| "Inject a secret value with `!` (e.g. `pass show`)" | Injection lands in the transcript. Inject structure/status (names, vault list), never secret values. |
| "It ran in my sandbox, so the probe is done" | Your sandbox has tooling (uv, personal paths, aliases) the target machine lacks — resolve interpreters at preflight and assume a clean environment. |
| "I'll write custom HTML to show eval results" | `eval-viewer/generate_review.py` already renders outputs and benchmarks. Use it. |
| "The skill passed its three evals, ship it" | A handful of examples overfits. Generalize the fix; don't patch the skill to the test set. |
| "Register the skill in `defaults.yaml`" | Deck has no skill-level multi-provider `defaults.yaml` routing. Deploy with `rune`; provider assembly is deck-owned. |

UNIT: SKILL.md#Constraints-heading
VERDICT: keep
WHY: Neutral heading; structure matches mdschema-friendly H2 layout.

UNIT: SKILL.md#Constraints-list
VERDICT: adapt
WHY: PascalCase is the retired forge naming rule; deck is kebab-case per agentskills.io. Need deck frontmatter and deploy conventions.
REPLACEMENT:
- Every skill MUST have `name:` and `description:` in frontmatter
- Description MUST include `USE WHEN` trigger phrases and a `Not for` anti-trigger clause
- `name:` is kebab-case (1–64 chars), matching the skill directory name exactly
- Optional fields (`argument-hint`, `version`, `allowed-tools`, `disallowed-tools`, `context`, `agent`, `model`, …) live in SKILL.md frontmatter — no SKILL.yaml sidecar
- Prefer one SKILL.md per skill — extract reference material into companion files when body exceeds ~150 lines or contains dense static data
- Eval artifacts land in `<skill-name>-workspace/` as a sibling of the skill directory, never inside the skill
- New skills live under `runes/<domain>/skills/<skill-name>/` and deploy via `rune`, not `forge install`

UNIT: SKILL.md#Sources-heading
VERDICT: keep
WHY: Neutral; no forge coupling.

UNIT: SKILL.md#Sources-list
VERDICT: adapt
WHY: Keep Claude upstreams; add agentskills.io because deck naming/layout follows that standard, not forge INSTALL.md.
REPLACEMENT:
- <https://code.claude.com/docs/en/skills>
- <https://github.com/anthropics/skills>
- <https://agentskills.io> (naming / skill layout conventions the deck follows)

UNIT: CreateWorkflow.md
VERDICT: adapt
WHY: Paths, registration, naming, and `defaults.yaml` are pure forge module workflow; deck places skills under `runes/<domain>/skills/`, kebab-case names, `rune` deploy, frontmatter-only optional fields.
REPLACEMENT:
## Step 1: Understand the request

Determine:
1. What does this skill do?
2. What should trigger it? (intent phrases for `USE WHEN`, plus a `Not for` anti-trigger)
3. Does it wrap a CLI tool, or is it purely procedural?
4. Which deck domain should it live under (`runes/<domain>/skills/`)?

If the user hasn't specified, ask using AskUserQuestion.

## Step 2: Write the SKILL.md

Follow the structure from [SkillStructure.md](SkillStructure.md).

**Checklist while writing:**
- [ ] Frontmatter has `name:` (kebab-case) and `description:` with `USE WHEN` and `Not for`
- [ ] Description is single-line, under 1024 characters
- [ ] Optional fields that apply (`argument-hint`, `version`, `allowed-tools`, …) are in frontmatter — never a SKILL.yaml sidecar
- [ ] Body starts with `# <Human title>` (display heading; `name:` stays kebab-case)
- [ ] **Decide what live state to inject.** Ask what current machine state would orient the model on load (branch, tool status, the names of things), and open the body with a `!` injection of it. Default to injecting unless there is a reason not to; see [DynamicContextInjection.md](DynamicContextInjection.md)
- [ ] Clear step-by-step instructions (numbered steps for sequential operations)
- [ ] If wrapping a CLI tool: usage examples, intent-to-flag mapping, output format (see [CliToolIntegration.md](CliToolIntegration.md))
- [ ] Constraints section with boundary conditions
- [ ] No unnecessary complexity — minimum needed for the task
- [ ] Do **not** add skill-level `defaults.yaml` multi-provider routing (deck provider assembly is separate)
- [ ] If locale-specific (e.g., Czech tax): description mixes English action phrases ("record transaction", "validate balance") with backticked native terms (`účetní deník`, `bilance`). Avoid diacritic-stripped czenglish (`podvojne ucetnictvi`) — matches neither natural English nor natural Czech queries

## Step 3: Create the skill directory and file

```sh
mkdir -p runes/<domain>/skills/<skill-name>
```

Write the SKILL.md using the Write tool. Directory name must equal `name:`.

## Step 4: Register / deploy

Stage and deploy with the deck's `rune` CLI (not `forge install` / module `make install`). Ensure the skill path is under the domain the deck deploys.

## Step 5: Verify

1. Test invocation: does the description trigger correctly?
2. Review: does the procedure work end-to-end?
3. Self-review against this skill's Validate workflow and the deck's adoption/mdschema checks. If a skill-reviewer agent is available in the harness, dispatch it; otherwise apply the Validate checklist and fix confirmed issues before declaring done.

## Step 6: Pressure test

Apply TDD to the skill itself — write a scenario where the skill should apply but might be rationalized away, then verify it holds.

1. **Write a pressure scenario** — describe a situation where someone would think "this skill doesn't apply here" but it actually does. Example for a debugging skill: "The fix seems obvious, I'll just change it."
2. **Test the trigger** — does the description match this scenario? Would the AI load this skill?
3. **Test the procedure** — does following the skill's steps produce the right outcome in this scenario?
4. **Tighten** — if the skill would be bypassed, improve the description's `USE WHEN` / `Not for` triggers or add entries to the Red Flags table.

UNIT: ValidateWorkflow.md
VERDICT: adapt
WHY: Casing and optional-field checks must enforce deck kebab-case + frontmatter-only fields; add mdschema/`Not for` gates the deck already uses.
REPLACEMENT:
## Step 1: Read the target skill

Read the SKILL.md file.

## Step 2: Check frontmatter

- [ ] `name:` present, kebab-case (1–64 chars), equals the skill directory name
- [ ] `description:` is single-line with `USE WHEN` and a `Not for` anti-trigger clause
- [ ] `description:` is under 1024 characters
- [ ] No deprecated fields (`triggers:`, `workflows:` arrays)
- [ ] Optional fields (`argument-hint:`, `version:`, `allowed-tools:`, …) are in frontmatter and correctly formatted — no SKILL.yaml sidecar
- [ ] Passes deck mdschema checks (allowed frontmatter fields, heading depth ≤ 3, no skipped levels)

## Step 3: Check body structure

- [ ] Starts with a top-level `#` heading (human title; need not be PascalCase)
- [ ] Has clear instructions (numbered steps, usage section, or workflow routing)
- [ ] If multiple workflows: `## Workflow Routing` table present
- [ ] Constraints or rules section for boundary conditions
- [ ] No unnecessary sections or boilerplate
- [ ] `!` dynamic injections appear only in SKILL.md body, never companions

## Step 4: Check CLI tool integration (if applicable)

- [ ] Tool path is documented
- [ ] Usage examples with `bash` blocks
- [ ] Intent-to-flag mapping table (if tool has flags)
- [ ] Output format described

## Step 5: Check content quality

- [ ] Inputs and outputs stated explicitly (what the skill consumes, what artifact it produces)
- [ ] Guardrails pause rather than auto-escalate — no silent jump from read-only analysis to executing targets or installing tooling
- [ ] No authoring-environment fingerprints: stdlib-only probes use a preflight-resolved `python3`, not `uv run python`; no personal paths, package managers, or aliases the target machine may lack
- [ ] Deliverable is an artifact (table, file, verdict schema), not prose
- [ ] No skill-level multi-provider `defaults.yaml` registration requirements; no forge INSTALL.md requirement unless the skill truly needs one

## Step 6: Report

**COMPLIANT** — all checks pass.

**NON-COMPLIANT** — list failures with specific fixes. Offer to fix automatically.

UNIT: EvalLoop.md
VERDICT: adapt
WHY: Eval machinery is reusable skill-creator content and fits the deck; only naming examples and the forge deploy aside need deck language.
REPLACEMENT:
- In the sample `evals/evals.json`, change `"skill_name": "ExampleSkill"` → `"skill_name": "example-skill"`.
- In **Harness adaptations → Packaging for claude.ai upload**, replace the last sentence:
  - FROM: `Not needed for forge modules, which deploy via \`forge install\`.`
  - TO: `Not needed for deck runes, which deploy via \`rune\`.`
- Leave workspace layout, grader/comparator/analyzer wiring, `python -m scripts.*` invocation, and viewer launch verbatim (no forge coupling; local process only).
- DANGER/NOTE (document, do not cut): `generate_review.py` starts a local viewer process; description-optimization path is Claude CLI-only (`claude -p`). No secret-injection guidance in this file.

UNIT: DescriptionOptimization.md
VERDICT: adapt
WHY: Loop and assets are skill-creator eval tooling (keep); Step 4 still says "forge skills" and omits the deck `Not for` clause when merging optimized text.
REPLACEMENT:
- Steps 1–3: keep verbatim (including Claude Code-only `claude -p` requirement and `assets/eval_review.html` review flow).
- Step 4 final sentence:
  - FROM: `For forge skills, keep the \`USE WHEN\` clause convention when merging the optimized text.`
  - TO: `For deck skills, keep the \`USE WHEN\` and \`Not for\` clause conventions when merging the optimized text; do not drop anti-triggers to chase a higher trigger score.`
- DANGER/NOTE: optimization loop shells out to `claude -p` (network/API via user CLI); eval export path `~/Downloads/eval_set.json` is local-only. Not dangerous if user-gated as written.
