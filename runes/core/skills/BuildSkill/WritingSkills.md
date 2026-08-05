# Writing skills

How a skill reaches the model decides what belongs where, and how it is phrased decides whether the model can generalize from it. This companion covers both.

## How a skill loads

Loading happens in three stages, and each has a different cost:

- **Name and description** are in context for every skill, all the time, before any of them trigger. This is the only text that decides whether the skill is consulted at all, so every trigger phrase belongs here and nowhere else.
- **The body** loads in full the moment the skill triggers. Everything here is paid for on every invocation, so it holds routing, constraints, and the steps that always apply.
- **Companions, scripts, and assets** load only when something reads them. Cost is paid per read, which makes this the right home for anything conditional: a workflow used by one request in five, a schema consulted once, provider-specific detail.

The practical consequence: a procedure that applies to one branch of the work belongs in a companion, and a constraint that applies to all of it belongs in the body. Moving conditional material out of the body is not tidying, it is the mechanism working as designed.

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

Today's models have good theory of mind and will do the right thing when they understand the goal. They generalize from reasoning and overfit to commands, so a rule with its rationale attached survives situations you did not anticipate, while a bare imperative does not.

Treat an all-caps ALWAYS or NEVER as a signal you have not explained something yet. Sometimes the emphasis is genuinely warranted; more often the instruction was hard to justify and force substituted for the argument.

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

When the shape of the result matters, show it rather than describing it:

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

Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication
```

Where you show a wrong form, introduce it with the reason it is wrong and never end a section on it, so the last thing read is the form to imitate.

## Drafting

Write a first pass without stopping to polish, then read it again as though you had not written it. The second read is where the padding, the instruction that restates its heading, and the step that assumes context the model will not have all become visible. Prefer the imperative for instructions, and cut any sentence whose removal costs nothing.
