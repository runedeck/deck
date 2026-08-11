# Writing skills

How a skill reaches the model decides what belongs where, and how it is phrased decides whether the model can generalize from it. This companion covers both.

## How a skill loads

The frontmatter description is always in context; the body lazy-loads when the skill triggers; companions load only when something reads them. So: trigger phrases live in the description, always-apply routing and constraints in the body, conditional material in companions.

State the load condition wherever you link:

```markdown
Read [ValidateWorkflow.md](ValidateWorkflow.md) when checking an existing skill.
```

Not this, because the reader cannot tell when it matters:

```markdown
There is also a validate workflow.
```

## Organizing by variant

When a skill covers several interchangeable targets, give each its own reference file so only the relevant one loads:

```text
cloud-deploy/
    SKILL.md            the workflow, and how to choose
    references/
        aws.md
        gcp.md
        azure.md
```

A reference file past roughly 300 lines earns a table of contents at the top, so a model can decide whether to keep reading.

## Explaining why

A rule with its rationale attached survives situations you did not anticipate; a bare imperative holds only in the cases you enumerated. Upstream skill authoring guidance draws the same conclusion: reframe all-caps imperatives as reasoning the model can apply.[SKILLCREATOR]

Treat an all-caps ALWAYS or NEVER as a signal you have not explained something yet.

Weak, because it only holds in the cases you enumerated:

```markdown
NEVER put the trigger phrases in the body. ALWAYS put them in the description.
```

Stronger, because the reason applies to cases you did not:

```markdown
Trigger phrases go in the description. The body is not in context when the
model decides whether to consult the skill, so a trigger written there is
never read at the moment it would matter.
```

## Defining an output format

Show the result shape as a template, not a description of it:

```markdown
## Report structure

Use this template:

# [Title]
## Executive summary
## Key findings
## Recommendations
```

## Showing examples

Paired examples teach a transformation faster than prose about it:

```markdown
## Commit message format

Do:
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication

Don't:
Output: Updated some auth stuff
```

Introduce a wrong form with the reason it is wrong, and end on the form to imitate.

## Drafting

Draft without polishing, then reread as a stranger. Cut padding, instructions that restate their heading, and steps that assume context the model lacks. Use the imperative. Cut any sentence whose removal costs nothing.

[SKILLCREATOR]: https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md "Anthropic skill creator"
