# Dynamic context injection (`!`)

A Claude Code skill can open with **live machine state** instead of stale prose. `` !`<command>` `` lines in the SKILL.md body run when the skill is invoked, and their output replaces the placeholder before Claude sees the content ("Inject dynamic context", a Claude Code extension to the Agent Skills standard).

Injection works only in harnesses that implement it. Claude Code implements it today. Other harnesses render the `!` lines as inert literal text. Where the harness supports it, ask what live state would orient the model on load. Then inject that state. A skill that opens with the actual situation is more useful than instructions to find it. The situation can include the current branch, diff, tool status, and existing items. Default to injection unless there is a reason not to use it.

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

Each `` !`<command>` `` runs once, before Claude receives the rendered `SKILL.md`. The output replaces the placeholder inline. Substitution is single-pass: injected output is not re-scanned for further placeholders.

## Hard constraints (verified by running it, not just the docs)

- **SKILL.md body only.** `!` executes only in the SKILL.md body, never in companion files (those load as plain text). Put every injected command in SKILL.md and keep companions as reference prose.
- **`allowed-tools` is required.** List the Bash scopes the injected commands need in the SKILL.md frontmatter, e.g. `allowed-tools: Bash(pass *) Bash(git *)`. It is a frontmatter field in SKILL.md itself (space-, comma-, or list-separated).
- **No shell expansions.** The injection rejects any command containing `$(...)`, `${...}`, or backticks with a `Contains expansion` error. Keep injected commands simple and static. A guarded summary that needs command substitution will not run. Inject the raw command output instead.
- **No built-in error handling.** A failing command can break or blank the injection. Guard each command against a missing tool, logged-out session, or empty result:

  ```markdown
  !`pass-cli vault list 2>/dev/null || echo "(proton pass: not logged in)"`
  ```

- **Claude Code only.** `!`, `@`, and `$ARGUMENTS` are Claude Code extensions, not part of the portable Agent Skills standard. In Codex, Gemini, and opencode, the `!` lines render as inert literal text. Use injection in skills that can be Claude-first. Other harnesses receive harmless literal text.
- **Test the built skill.** When authoring a skill that uses `!`, load the finished skill and confirm the lines inject in the supporting harness, and that a failing or unsupported line degrades to harmless text instead of corrupting the body.

## Substitutions available alongside `!`

`$ARGUMENTS`, `$ARGUMENTS[N]`, `$N`, `$name` (named args), and `${CLAUDE_SESSION_ID}` / `${CLAUDE_EFFORT}` / `${CLAUDE_SKILL_DIR}` are substituted in the SKILL.md body the same way.

## What to inject, and what never to

Inject **read-only, fast, structural state** that orients Claude: the current branch, a file listing, a tool's status, the names of things. Never inject:

- **Secret values.** For a credential skill, inject the *map*, never the *territory*. The map includes entry names, vault lists, and authentication status. `` !`pass ls` `` is acceptable because it lists entry names. `` !`pass show <x>` `` is forbidden because it exposes a live secret in the transcript and context.
- **Slow or interactive commands.** Injection blocks skill load. A command that prompts, hangs, or takes seconds makes the skill appear broken.
- **Mutating commands.** Injection should observe, not change state.
- **Attacker-influenced prose.** Injected output enters the model's context as trusted-looking text. Inject bounded structural data (names, counts, statuses), never file contents, commit messages, issue text, or network responses that a third party can author.

The litmus test: if the command's output appearing verbatim in the session transcript would be a problem, do not inject it.
