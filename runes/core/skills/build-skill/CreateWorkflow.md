# Create workflow

## Step 1: Understand the request

Determine:

1. What does this skill do?
2. What should trigger it? (intent phrases for `USE WHEN`, plus a `NOT FOR` anti-trigger)
3. Does it wrap a CLI tool, or is it purely procedural?
4. Which `runes/<domain>/skills/` directory owns it?

If the user hasn't specified, ask using AskUserQuestion.

## Step 2: Write the SKILL.md

Follow the structure from [SkillStructure.md](SkillStructure.md).

**Checklist while writing:**

- [ ] Frontmatter has `name:` (kebab-case, matching the directory) and `description:` with `USE WHEN` triggers and a `NOT FOR` clause
- [ ] Description is single-line, under 1024 characters
- [ ] Optional Agent Skills fields that apply (`license`, `compatibility`, `metadata`, `allowed-tools`) sit in frontmatter
- [ ] H1, frontmatter name, and directory use the same kebab-case identifier
- [ ] Body follows RuneShell with required `Instructions` and ordered optional sections
- [ ] **Decide what live state to inject.** Ask what current machine state would orient the model on load (branch, tool status, the names of things), and open the body with a dynamic context command injecting it. Default to injecting unless there is a reason not to; see [DynamicContextInjection.md](DynamicContextInjection.md)
- [ ] Clear step-by-step instructions or action-oriented routing beneath `Instructions`
- [ ] If wrapping a CLI tool: usage examples, intent-to-flag mapping, output format (see [CliToolIntegration.md](CliToolIntegration.md))
- [ ] Boundaries live under `Constraints`
- [ ] No unnecessary complexity; include only what the task needs

## Step 3: Create the skill directory and file

```sh
mkdir -p runes/<domain>/skills/<skill-name>
```

Write the SKILL.md using the Write tool. The directory name must equal `name:`.

## Step 4: Register

Cast selection and provider assembly are deck-level concerns; deploy with `rune install`.

## Step 5: Verify

1. Run `rune validate --source .` and fix anything it reports.
2. Test invocation: does the description trigger correctly? Try a should-trigger prompt AND a should-not-trigger prompt from an adjacent skill's territory.
3. Review: does the procedure work end-to-end?
4. If the harness has a skill-reviewer agent, dispatch it on the new `SKILL.md` and companions; otherwise apply the [Validate workflow](ValidateWorkflow.md) yourself. Apply confirmed fixes before declaring done.

## Step 6: Pressure test

Apply TDD to the skill itself — write a scenario where the skill should apply but might be rationalized away, then verify it holds.

1. **Write a pressure scenario** — describe a situation where someone would think "this skill doesn't apply here" but it actually does. Example for a debugging skill: "The fix seems obvious, I'll just change it."
2. **Write a near-miss scenario** — a request that sounds close but belongs to an adjacent skill; verify the `NOT FOR` clause routes it away.
3. **Test the trigger** — does the description match the pressure scenario? Would the AI load this skill?
4. **Test the procedure** — does following the skill's steps produce the right outcome?
5. **Tighten**: if the skill would be bypassed or misrouted, improve `USE WHEN` and `NOT FOR` or add a specific boundary under `Constraints`.
