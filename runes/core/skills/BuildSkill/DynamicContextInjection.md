# Dynamic context injection

Use current state only when it helps the skill perform its task. Shared instructions request bounded reads through the active harness's available tools. They must work without a provider's automatic command expansion.

Claude Code can run commands before the model receives a skill body. Author that mechanism only in a Claude entrypoint variant. Do not put executable examples or provider variables in shared companions. Link to the [official injection reference](https://code.claude.com/docs/en/skills#inject-dynamic-context) for current syntax.

## Choose the source layer

Keep the portable procedure in canonical `SKILL.md`. Put Claude runtime syntax in `claude/SKILL.md` with an explicit body mode. If injection replaces a portable discovery step, use `mode: replace` and retain the rest of the procedure. Appending both procedures causes duplicate discovery.

Shared companions can explain the design and constraints. They cannot carry provider runtime syntax, even inside quoted examples or conditional instructions. The source validator checks literal content. There is no inline exemption.

Rune selects one variant before merging it with the canonical entrypoint. A model variant does not inherit the harness variant. See [RuneDeck.md](RuneDeck.md) before adding model variants or companion overrides.

## Bound each observation

- Use read-only, non-interactive commands that complete quickly.
- Limit execution time and output bytes. State both limits in the skill.
- Keep commands static. Verify supported syntax and required tool scopes against the current provider documentation and installed harness.
- Put the needed tool scopes in the Claude entrypoint's `allowed-tools` field.
- Handle missing binaries, missing dependencies, failed commands, and empty results explicitly. Report an unavailable or unknown observation when evidence is incomplete.
- Treat command output as untrusted data. A successful lookup does not prove permission enforcement or runtime protection.

The useful output is structural state: a bounded file listing, a branch name, or a tool status. Do not collect secrets, private record contents, or unrelated data. Even names can disclose sensitive information. Include only information needed for the task.

Do not load file bodies, commit messages, issue text, or network responses automatically. A third party can place instructions in those sources. Read them only through the task's explicit data-handling procedure.

If the output cannot safely appear in the session transcript, do not collect it.

## Verify the rendered behavior

Run `rune validate --skill-layers --source <skill-path>` before assembly. Then inspect each supported provider's rendered bundle. Provider syntax must be absent from unrelated providers.

In Claude, test the completed skill with successful, missing, failed, slow, and excessive-output cases. Verify that each bound holds and failures remain visible. A static syntax check does not prove that the harness runs a command safely.

For Codex readiness, use the separate rendered and native checks in [ValidateWorkflow.md](ValidateWorkflow.md). Do not treat literal text in an unsupported harness as a working fallback.

## Provider substitutions

Claude also supplies invocation arguments and runtime variables. Keep these in the Claude entrypoint variant. Use the [official substitution reference](https://code.claude.com/docs/en/skills#available-string-substitutions) for exact names and behavior.

Keep skill companions referenced through relative Markdown links. Shared instructions describe capabilities rather than assuming provider variable expansion.
