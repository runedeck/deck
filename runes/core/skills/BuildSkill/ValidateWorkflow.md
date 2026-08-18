# Validate workflow

> Check a skill against the Agent Skills spec, the section convention, progressive disclosure, and content quality, then report a verdict with concrete repairs.

You are auditing an existing skill, not improving it. Every check below is pass or fail; opinions about style belong in the create workflow.

## OBJECTIVE

A verdict on the target skill: `COMPLIANT`, or `NON-COMPLIANT` with the file path and a concrete repair for each failure.

## DONE WHEN

- Every checklist group below has been applied to the target.
- The validation commands ran and their errors are resolved or reported.
- The verdict is stated with repairs for every failure.

## TODO

- [ ] Read the target and note its companions, scripts, references, and assets
- [ ] Check canonical frontmatter
- [ ] Check the section convention
- [ ] Check progressive disclosure, tool integration, and bundled code
- [ ] Check content quality
- [ ] Run the validators and report the verdict

## Step 1: Read the target

Read `SKILL.md` and note the companions, scripts, references, and assets it links.

## Step 2: Check canonical frontmatter

- [ ] `name` equals the skill directory and the H1. This deck authors PascalCase; the agentskills provider converts to lowercase on deployment.
- [ ] `description` is one line with concrete `USE WHEN` triggers and a useful `NOT FOR` boundary.
- [ ] Top-level fields are limited to `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`, and the assembly directives `targets`, `disable-model-invocation`, and `user-invocable`.
- [ ] `compatibility` names required providers, binaries, operating systems, or network access.
- [ ] Additional string-valued information lives under `metadata`.
- [ ] The official `skills-ref` validator accepts the skill.

## Step 3: Check the section convention

- [ ] The H1 equals the frontmatter name and directory.
- [ ] `Instructions` is present.
- [ ] Present H2 sections use this order: `Prerequisites`, `Constraints`, `Instructions`, `Verification`, `Troubleshooting`, `References`.
- [ ] No H2 falls outside that vocabulary.
- [ ] H3 appears only under `Constraints`, `Instructions`, `Verification`, or `Troubleshooting`.
- [ ] `Prerequisites` and `References` remain flat.
- [ ] Heading depth does not exceed H3 and levels are not skipped.
- [ ] More than four H3 headings beneath `Instructions` receives an advisory warning.
- [ ] Standalone `mdschema` validates the entrypoint when strict section validation is required.

A project's own schema checker may be a partial fallback that reports required sections and heading depth without covering section vocabulary, ordering, uniqueness, or subsection placement. Where that is the case, standalone `mdschema` is the strict check; see [RuneDeck.md](RuneDeck.md) for how the two relate in a Rune deck.

## Step 4: Check progressive disclosure

- [ ] Each companion link resolves inside the skill tree.
- [ ] Each companion link states when the reader should load it.
- [ ] Detailed procedures and static reference material live in companions rather than expanding the entrypoint.
- [ ] Dynamic context commands appear only in `SKILL.md` and are bounded, fast, read-only, non-interactive, and free of secrets.
- [ ] No section is empty and no authoring placeholder remains.

## Step 5: Check tool integration

When the skill wraps a CLI:

- [ ] The executable, presence check, and required version are documented.
- [ ] Every command and flag is verified against the installed tool's help output.
- [ ] Output format, exit behavior, file writes, external state changes, GUI use, and network access are stated.

## Step 6: Check bundled code

- [ ] Dependencies and interpreters are explicit.
- [ ] Scripts contain no unexpected network calls, destructive writes, or unsafe path handling.
- [ ] Validation inspects scripts without executing them.

## Step 7: Check content quality

- [ ] Inputs, outputs, and the expected result are explicit.
- [ ] Guardrails pause instead of silently escalating from analysis to execution or installation.
- [ ] Examples contain no personal paths, credentials, aliases, or undeclared tools.
- [ ] Correct and wrong examples explain the distinction.
- [ ] The entrypoint stays within its length budget and each Markdown companion stays under 150 lines.

## Step 8: Run validation

```sh
mdschema check --schema <nearest-skill-schema> <skill-path>/SKILL.md
skills-ref validate <skill-path>
```

Run the project's own validator alongside these; in a Rune deck that is `rune validate --source .` (see [RuneDeck.md](RuneDeck.md)).

Fix errors before declaring the skill valid. A breadth warning remains advisory unless another error is present.

## EXECUTE NOW

Work the TODO in order against the target skill. Report `COMPLIANT` when every required check passes, otherwise `NON-COMPLIANT` with the file path and concrete repair for each failure.
