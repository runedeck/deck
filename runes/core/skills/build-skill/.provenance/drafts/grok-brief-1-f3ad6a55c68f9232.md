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

ANSWER-ONLY. Do not use tools. Units for THIS batch: SKILL.md blocks 9-14 (shown below as the tail of SKILL.md from "## Red Flags" on) and the four workflow companions, each as one unit. Same output format as described above.


===== FILE: SKILL.md =====
---
name: build-skill
version: 0.1.0
description: Create, validate, evaluate, and iterate skills for forge modules. USE WHEN create skill, new skill, write skill, validate skill, check skill, skill structure, skill conventions, test a skill, run skill evals, benchmark a skill, skill not triggering, optimize skill description. Not for adopting community skills (AdoptArtifact) or shipping artifacts downstream (PublishArtifact).
upstream: https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md
---
# ForgeSkill

Create, validate, evaluate, and iterate skills following forge conventions. Skills are markdown files (`SKILL.md`) with YAML frontmatter that teach AI coding tools new capabilities. Load only the companion relevant to the current task.

The evaluation machinery (grader/comparator/analyzer prompts, eval scripts, browser viewer) lives in `agents/`, `scripts/`, `references/`, `eval-viewer/`, and `assets/`. Scripts run with `python -m scripts.<name>` from this skill's directory (`${CLAUDE_SKILL_DIR}` when deployed). The files under `agents/` are worker prompt templates this skill feeds to generic subagents during the eval loop, not standalone agent definitions; harness-discoverable agents belong in the module-level `agents/` directory.

## Workflow Routing

| Workflow           | Trigger                                                      | Companion                                                 |
| ------------------ | ------------------------------------------------------------ | --------------------------------------------------------- |
| Create             | "create a skill", "new skill", "write a skill"               | [@CreateWorkflow.md](CreateWorkflow.md)                     |
| Validate           | "validate skill", "check skill structure"                    | [@ValidateWorkflow.md](ValidateWorkflow.md)                 |
| Evaluate           | "test this skill", "run skill evals", "benchmark the skill"  | [@EvalLoop.md](EvalLoop.md)                                 |
| Optimize triggering | "skill doesn't trigger", "improve the skill description"     | [@DescriptionOptimization.md](DescriptionOptimization.md)  |

## Topics

| Topic                                                       | Companion                                                |
| ----------------------------------------------------------- | -------------------------------------------------------- |
| SKILL.md structure, frontmatter, body layout, naming        | [@SkillStructure.md](SkillStructure.md)                    |
| **Dynamic context injection (`!`): open a Claude skill with live state** | [@DynamicContextInjection.md](DynamicContextInjection.md) |
| Multi-provider routing via `defaults.yaml`                  | [@MultiProviderRouting.md](MultiProviderRouting.md)        |
| Wrapping a CLI tool in a skill                              | [@CliToolIntegration.md](CliToolIntegration.md)            |
| Platform-agnostic writing — no placeholders or `/` prefix   | [@PlatformAgnostic.md](PlatformAgnostic.md)                |
| User-config schema for AI-first artifacts (autoMode mirror) | [@UserConfigSchema.md](UserConfigSchema.md)                |
| Claude-only features: `@` refs, skill discovery, `allowed-tools` | [@ClaudeSkill.md](ClaudeSkill.md)              |
| When to author a per-skill INSTALL.md                       | [@SkillInstallation.md](SkillInstallation.md)              |
| Eval JSON structures (evals.json, grading.json, benchmark.json) | [@references/schemas.md](references/schemas.md)        |

## Red Flags

| Thought                                                  | Reality                                                                              |
| -------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| "Put argument-hint in SKILL.md frontmatter"              | Obsidian Linter reformats frontmatter. Provider-specific fields go in SKILL.yaml.     |
| "Use `/SkillName` inside a skill body"                   | Slashes are user-facing invocation syntax, not internal references.                    |
| "Skip the `USE WHEN` clause"                             | Claude uses it to route. Missing trigger = skill never fires.                         |
| "Leave a stub section as a placeholder"                  | Skill bodies are plain prose. Delete empty sections, don't scaffold them.             |
| "Inline every example in the SKILL.md"                   | SKILL.md should stay slim. Move static reference material to companion files.         |
| "Skill directory can have any name"                      | Directory name must match the `name:` frontmatter field exactly.                      |
| "Put a `!` injection in a companion file"                | `!` runs only in the SKILL.md body; in a companion it renders as literal text. See [@ClaudeSkill.md](ClaudeSkill.md). |
| "Inject a secret value with `!` (e.g. `pass show`)"      | Injection lands in the transcript. Inject structure/status (names, vault list), never secret values. |
| "It ran in my sandbox, so the probe is done"             | Your sandbox has tooling (uv, personal paths, aliases) the target machine lacks — resolve interpreters at preflight and assume a clean environment. |
| "I'll write custom HTML to show eval results"            | `eval-viewer/generate_review.py` already renders outputs and benchmarks. Use it.      |
| "The skill passed its three evals, ship it"              | A handful of examples overfits. Generalize the fix; don't patch the skill to the test set. |

## Constraints

- Every skill MUST have `name:` and `description:` in frontmatter
- Description MUST include `USE WHEN` trigger phrases
- PascalCase for multi-word skill names, natural case for single words
- Skill directory name must match the `name:` field
- Prefer one SKILL.md per skill — extract reference material into companion files when body exceeds ~150 lines or contains dense static data
- Eval artifacts land in `<skill-name>-workspace/` as a sibling of the skill directory, never inside the skill

## Sources

- <https://code.claude.com/docs/en/skills>
- <https://github.com/anthropics/skills>

===== FILE: CreateWorkflow.md =====
## Step 1: Understand the request

Determine:
1. What does this skill do?
2. What should trigger it? (intent phrases for `USE WHEN`)
3. Does it wrap a CLI tool, or is it purely procedural?
4. Which module should it live in?

If the user hasn't specified, ask using AskUserQuestion.

## Step 2: Write the SKILL.md

Follow the structure from [SkillStructure.md](SkillStructure.md).

**Checklist while writing:**
- [ ] Frontmatter has `name:` and `description:` with `USE WHEN`
- [ ] Description is single-line, under 1024 characters
- [ ] Body starts with `# SkillName` heading
- [ ] **For a Claude skill, decide what live state to inject.** Ask what current machine state would orient the model on load (branch, tool status, the names of things), and open the body with a `!` injection of it. Default to injecting unless there is a reason not to; see [DynamicContextInjection.md](DynamicContextInjection.md)
- [ ] Clear step-by-step instructions (numbered steps for sequential operations)
- [ ] If wrapping a CLI tool: usage examples, intent-to-flag mapping, output format (see [CliToolIntegration.md](CliToolIntegration.md))
- [ ] Constraints section with boundary conditions
- [ ] No unnecessary complexity — minimum needed for the task
- [ ] Skill listed in module's `defaults.yaml` under each target provider (see [MultiProviderRouting.md](MultiProviderRouting.md))
- [ ] If locale-specific (e.g., Czech tax): description mixes English action phrases ("record transaction", "validate balance") with backticked native terms (`účetní deník`, `bilance`). Avoid diacritic-stripped czenglish (`podvojne ucetnictvi`) — matches neither natural English nor natural Czech queries

## Step 3: Create the skill directory and file

```sh
mkdir -p skills/SkillName
```

Write the SKILL.md using the Write tool.

## Step 4: Register

For Claude Code: ensure the skill's parent directory is listed in `plugin.json` under `skills`.

For other providers: run `make install` from the module's Makefile.

## Step 5: Verify

1. Test invocation: does the description trigger correctly?
2. Review: does the procedure work end-to-end?
3. Dispatch the **SkillReviewer** agent on the new `SKILL.md` (and any companion files). It catches trigger weaknesses, czenglish descriptions, broken cross-references, body bloat, and convention drift that self-review misses. Apply confirmed fixes before declaring done.

## Step 6: Pressure test

Apply TDD to the skill itself — write a scenario where the skill should apply but might be rationalized away, then verify it holds.

1. **Write a pressure scenario** — describe a situation where someone would think "this skill doesn't apply here" but it actually does. Example for a debugging skill: "The fix seems obvious, I'll just change it."
2. **Test the trigger** — does the description match this scenario? Would the AI load this skill?
3. **Test the procedure** — does following the skill's steps produce the right outcome in this scenario?
4. **Tighten** — if the skill would be bypassed, improve the description's USE WHEN triggers or add entries to the Red Flags table.

===== FILE: ValidateWorkflow.md =====
## Step 1: Read the target skill

Read the SKILL.md file.

## Step 2: Check frontmatter

- [ ] `name:` present and uses correct casing
- [ ] `description:` is single-line with `USE WHEN` clause
- [ ] `description:` is under 1024 characters
- [ ] No deprecated fields (`triggers:`, `workflows:` arrays)
- [ ] Optional fields (`argument-hint:`, `version:`) are correctly formatted

## Step 3: Check body structure

- [ ] Starts with `# SkillName` heading (matches `name:` frontmatter)
- [ ] Has clear instructions (numbered steps, usage section, or workflow routing)
- [ ] If multiple workflows: `## Workflow Routing` table present
- [ ] Constraints or rules section for boundary conditions
- [ ] No unnecessary sections or boilerplate

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

## Step 6: Report

**COMPLIANT** — all checks pass.

**NON-COMPLIANT** — list failures with specific fixes. Offer to fix automatically.

===== FILE: EvalLoop.md =====
# Eval Loop

Run test cases against a skill, review results with the user, improve, repeat. This is one continuous sequence; don't stop partway through.

Results live in `<skill-name>-workspace/` as a sibling of the skill directory, organized by iteration (`iteration-1/`, `iteration-2/`), with one directory per test case named `eval-<ID>-<descriptive-name>`. The aggregator discovers only `eval-*` directories, and each config directory must contain `run-<R>/` subdirectories holding `outputs/`, `grading.json`, and `timing.json`; files placed directly in the config directory are ignored. Create directories as you go, not upfront.

## Write test cases

Draft 2-3 realistic test prompts, the kind a real user would type. Confirm them with the user before running. Save to `evals/evals.json` (prompts only; assertions come later):

```json
{
    "skill_name": "ExampleSkill",
    "evals": [
        {
            "id": 1,
            "prompt": "User's task prompt",
            "expected_output": "Description of expected result",
            "files": []
        }
    ]
}
```

Full schema, including the `assertions` field: [references/schemas.md](references/schemas.md).

Skills with objectively verifiable outputs (file transforms, data extraction, code generation, fixed workflows) benefit from assertions. Subjective skills (writing style, design) are better judged qualitatively; don't force assertions onto human-judgment outputs.

## Step 1: Spawn all runs in the same turn

For each test case, spawn two subagents in the same turn, one with the skill and one baseline, so everything finishes together.

With-skill run prompt:

```
Execute this task:
- Skill path: <path-to-skill>
- Task: <eval prompt>
- Input files: <eval files if any, or "none">
- Save outputs to: <workspace>/iteration-<N>/eval-<ID>-<name>/with_skill/run-1/outputs/
- Outputs to save: <what the user cares about>
```

Baseline run, same prompt:

- New skill: no skill at all; save to `without_skill/outputs/`.
- Improving an existing skill: snapshot first (`cp -r <skill-path> <workspace>/skill-snapshot/`), point the baseline at the snapshot, save to `old_skill/outputs/`.

Write an `eval_metadata.json` per test case (assertions may be empty for now):

```json
{
    "eval_id": 0,
    "eval_name": "descriptive-name-here",
    "prompt": "The user's task prompt",
    "assertions": []
}
```

## Step 2: Draft assertions while runs are in progress

Good assertions are objectively verifiable and have descriptive names that read clearly in the benchmark viewer. Update `eval_metadata.json` and `evals/evals.json` once drafted, and explain to the user what they'll see in the viewer.

## Step 3: Capture timing as each run completes

Each subagent completion notification carries `total_tokens` and `duration_ms`. Save immediately to `timing.json` in the run directory; the notification is the only place this data exists. Process notifications as they arrive, never batch.

```json
{
    "total_tokens": 84852,
    "duration_ms": 23332,
    "total_duration_seconds": 23.3
}
```

## Step 4: Grade, aggregate, launch the viewer

1. **Grade each run.** Spawn a grader subagent (instructions: [agents/grader.md](agents/grader.md)) evaluating each assertion against the outputs; save `grading.json` in each `run-<R>/` directory. The expectations array MUST use the fields `text`, `passed`, `evidence`, and the file MUST carry a `summary` object (`passed`, `failed`, `total`, `pass_rate`); the aggregator and viewer depend on these exact names. Check programmatically verifiable assertions with a script, not by eyeballing.
2. **Aggregate.** From this skill's directory: `python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>`. Produces `benchmark.json` and `benchmark.md` (pass rate, time, tokens, mean, stddev, delta). Put each with_skill version before its baseline counterpart.
3. **Analyst pass.** Read the benchmark data for patterns the aggregates hide: non-discriminating assertions, high-variance evals, time/token tradeoffs. See the "Analyzing Benchmark Results" section of [agents/analyzer.md](agents/analyzer.md).
4. **Launch the viewer** before doing your own revision pass; get outputs in front of the human first:

    ```bash
    nohup python <skill-dir>/eval-viewer/generate_review.py \
        <workspace>/iteration-N \
        --skill-name "<name>" \
        --benchmark <workspace>/iteration-N/benchmark.json \
        > /dev/null 2>&1 &
    VIEWER_PID=$!
    ```

    For iteration 2+, add `--previous-workspace <workspace>/iteration-<N-1>`. Headless or no-display environments: pass `--static <output_path>` to write standalone HTML instead of serving; feedback then downloads as `feedback.json`, which you copy into the workspace. Always use `generate_review.py`; never hand-write viewer HTML.

5. **Tell the user** the viewer is open: the Outputs tab collects per-case feedback, the Benchmark tab shows the quantitative comparison.

## Step 5: Read the feedback

When the user says they're done, read `feedback.json`. Empty feedback on a case means it was fine; focus on cases with specific complaints. Kill the viewer: `kill $VIEWER_PID 2>/dev/null`.

## Improve the skill

- **Generalize from the feedback.** The skill must work across many prompts, not just the test set. Avoid fiddly overfit patches and rigid MUSTs; if an issue is stubborn, try a different framing or working pattern instead.
- **Keep the prompt lean.** Read the transcripts, not just outputs. If the skill makes the model do unproductive work, cut the part causing it and re-measure.
- **Explain the why.** Reframe all-caps imperatives as reasoning the model can apply; that generalizes better than rote instruction.
- **Bundle repeated work.** If every test run independently wrote the same helper script, move that script into `scripts/` and reference it from the skill.

Then rerun everything into `iteration-<N+1>/` (baselines included), launch the viewer with `--previous-workspace`, and read the new feedback. Stop when the user is happy, the feedback is all empty, or progress stalls.

## Blind comparison (optional)

For a rigorous "is the new version actually better?" answer: give two outputs to an independent agent without revealing which is which, let it judge, then analyze why the winner won. Instructions: [agents/comparator.md](agents/comparator.md) and [agents/analyzer.md](agents/analyzer.md). Requires subagents; the human review loop is usually sufficient.

## Harness adaptations

- **No subagents** (e.g. claude.ai): run test cases yourself, one at a time, skill instructions in context. Skip baselines and quantitative benchmarking; present outputs inline and gather feedback conversationally.
- **No browser or display**: skip the viewer server, use `--static`, present file outputs by path.
- **Description optimization** requires `claude -p` (Claude Code only): see [DescriptionOptimization.md](DescriptionOptimization.md).
- **Packaging for claude.ai upload**: `python -m scripts.package_skill <path/to/skill-folder>` produces a `.skill` file; works anywhere with Python. Not needed for forge modules, which deploy via `forge install`.
- **Updating an existing skill**: preserve the original `name` and directory name unchanged; copy read-only installs to a writable location before editing.

===== FILE: DescriptionOptimization.md =====
# Description Optimization

The `description` field is the primary triggering mechanism: Claude sees only name + description when deciding whether to consult a skill. Claude tends to undertrigger, so descriptions should be a little pushy, naming both what the skill does and the concrete contexts that should invoke it, even when the user doesn't use the skill's own vocabulary.

Triggering mechanics worth knowing: Claude only consults skills for tasks it can't easily handle directly. Simple one-step queries ("read this PDF") may not trigger a skill even with a perfect description match; complex, multi-step, or specialized queries trigger reliably. Eval queries must be substantive enough that consulting a skill would actually help.

## Step 1: Generate trigger eval queries

Create 20 queries, a mix of should-trigger and should-not-trigger, saved as JSON:

```json
[
    {"query": "the user prompt", "should_trigger": true},
    {"query": "another prompt", "should_trigger": false}
]
```

Queries must be realistic: concrete and specific, with file paths, personal context, column names, company names, typos, casual speech, mixed lengths. Favor edge cases over clear-cut ones; the user signs off before the run.

- **Should-trigger (8-10)**: different phrasings of the same intent, formal and casual; cases where the user never names the skill or file type but clearly needs it; uncommon use cases; cases where this skill competes with another but should win.
- **Should-not-trigger (8-10)**: near-misses that share keywords or concepts but need something different: adjacent domains, ambiguous phrasing a naive keyword match would catch, contexts where another tool is more appropriate. Obviously irrelevant negatives test nothing.

## Step 2: Review with the user

Render the eval set for review using the bundled template:

1. Read `assets/eval_review.html`
2. Replace `__EVAL_DATA_PLACEHOLDER__` (the JSON array, unquoted), `__SKILL_NAME_PLACEHOLDER__`, `__SKILL_DESCRIPTION_PLACEHOLDER__`
3. Write to a temp file and open it in the browser
4. The user edits queries, toggles should-trigger, and clicks "Export Eval Set"
5. The export lands in `~/Downloads/eval_set.json`; take the most recent if there are duplicates

Bad eval queries produce bad descriptions; this review step is load-bearing.

## Step 3: Run the optimization loop

Warn the user it takes a while, then run in the background from this skill's directory:

```bash
python -m scripts.run_loop \
    --eval-set <path-to-trigger-eval.json> \
    --skill-path <path-to-skill> \
    --model <model-id-powering-this-session> \
    --max-iterations 5 \
    --verbose
```

Use the model ID powering the current session so the triggering test matches what the user experiences. The loop splits 60% train / 40% held-out test, measures the current description (each query 3 times), proposes improvements from the failures, and re-evaluates up to 5 iterations. It reports per-iteration results and returns JSON with `best_description`, selected by test score to avoid overfitting. Tail the output periodically to report progress.

Requires the `claude` CLI (`claude -p`); Claude Code only.

## Step 4: Apply the result

Update the skill's frontmatter with `best_description`, show the user before/after, and report the scores. For forge skills, keep the `USE WHEN` clause convention when merging the optimized text.
