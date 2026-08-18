# Create workflow

> Extract the procedure from the conversation, research the gaps, write a spec-valid SKILL.md, and pressure-test its triggers.

You are turning something that already happened, or something the person can describe, into a skill another model can execute. Most of the material is usually already in front of you; the workflow below keeps you from re-asking for it.

## OBJECTIVE

A new skill directory whose `SKILL.md` passes validation, triggers on the right requests, and routes near-misses away.

## DONE WHEN

- The project validator and the section convention accept the skill with no errors.
- A should-trigger prompt loads the skill and a near-miss prompt from an adjacent skill's territory does not.
- The procedure produces the right outcome when followed literally.

## TODO

- [ ] Extract intent from the conversation; ask only about the gaps
- [ ] Research adjacent skills and tool help before interviewing
- [ ] Write the `SKILL.md` following the structure and writing companions
- [ ] Create the skill directory and file
- [ ] Verify validation, triggering, and the procedure
- [ ] Pressure-test with rationalization and near-miss scenarios

## Step 1: Capture intent

The conversation often already contains the skill. When someone says "turn this into a skill", the workflow they want captured is in the transcript above: the tools used, the order of the steps, the corrections they made along the way, the input and output formats that actually appeared. Read that first and extract it.

Present what you extracted and ask only about the gaps. An interview that re-asks what the person just demonstrated reads as not having paid attention.

Whatever the transcript cannot answer, determine:

1. What does this skill do?
2. What should trigger it? (intent phrases for `USE WHEN`, plus a `NOT FOR` anti-trigger)
3. Does it wrap a CLI tool, or is it purely procedural?
4. Where does it live, and which collection owns it?

Match your vocabulary to theirs while you ask; see [Audience.md](Audience.md).

## Step 2: Research before asking

Arrive at the interview already informed. Look for skills covering adjacent ground, so the new one gets a `NOT FOR` boundary naming them instead of duplicating what exists. Where the skill wraps a tool, read that tool's own help output rather than asking the person to recite flags.

Check what research tools are available, including any connected MCP servers, and search in parallel via subagents when the harness has them. Spend the person's attention only on what you genuinely cannot determine yourself.

If the request is still ambiguous after that, ask using AskUserQuestion.

## Step 3: Write the SKILL.md

Follow the structure from [SkillStructure.md](SkillStructure.md) and the writing guidance in [WritingSkills.md](WritingSkills.md).

While writing, check:

- [ ] Frontmatter has `name:` matching the directory, and `description:` with `USE WHEN` triggers and a `NOT FOR` clause
- [ ] Description is single-line, under 1024 characters
- [ ] Optional Agent Skills fields that apply (`license`, `compatibility`, `metadata`, `allowed-tools`) sit in frontmatter, plus the assembly directives (`targets`, `disable-model-invocation`, `user-invocable`) where the skill needs routing or invocation control
- [ ] H1, frontmatter name, and directory are identical
- [ ] Body follows the section convention with required `Instructions` and ordered optional sections
- [ ] Live state to inject is decided: what current machine state would orient the model on load (branch, tool status, the names of things). Default to injecting unless there is a reason not to; see [DynamicContextInjection.md](DynamicContextInjection.md)
- [ ] Clear step-by-step instructions or action-oriented routing beneath `Instructions`
- [ ] If wrapping a CLI tool: usage examples, intent-to-flag mapping, output format (see [CliToolIntegration.md](CliToolIntegration.md))
- [ ] Boundaries live under `Constraints`
- [ ] No unnecessary complexity; include only what the task needs

## Step 4: Create the skill directory and file

```sh
mkdir -p <skills-directory>/<skill-name>
```

Write the `SKILL.md` using the Write tool. The directory name must equal `name:`. For where that directory sits in a Rune deck, see [RuneDeck.md](RuneDeck.md).

## Step 5: Verify

1. Run the project's validator and fix anything it reports.
2. Test invocation: does the description trigger correctly? Try a should-trigger prompt AND a should-not-trigger prompt from an adjacent skill's territory.
3. Review: does the procedure work end-to-end?
4. If the harness has a skill-reviewer agent, dispatch it on the new `SKILL.md` and companions; otherwise apply the [Validate workflow](ValidateWorkflow.md) yourself. Apply confirmed fixes before declaring done.

## Step 6: Pressure test

Apply TDD to the skill itself: write a scenario where the skill should apply but might be rationalized away, then verify it holds.

1. **Write a pressure scenario**: a situation where someone would think "this skill doesn't apply here" but it actually does. Example for a debugging skill: "The fix seems obvious, I'll just change it."
2. **Write a near-miss scenario**: a request that sounds close but belongs to an adjacent skill; verify the `NOT FOR` clause routes it away.
3. **Test the trigger**: does the description match the pressure scenario? Would the AI load this skill?
4. **Test the procedure**: does following the skill's steps produce the right outcome?
5. **Tighten**: if the skill would be bypassed or misrouted, improve `USE WHEN` and `NOT FOR` or add a specific boundary under `Constraints`.

## EXECUTE NOW

Work the TODO in order, checking items off as they complete. Begin by reading the transcript for the procedure the person already demonstrated.
