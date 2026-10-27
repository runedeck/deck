# Commands that work here

Verified against chezmoi 2.73 on this machine, from inside the Claude Code sandbox. An agent runs the read-only commands. The owner runs the ones that write, outside the harness sandbox.

## Read-only, allowed in an agent session

- `chezmoi source-path`: the source directory. `chezmoi source-path <target>` prints the source file of one target.
- `chezmoi diff [<target>]`: pending changes as a unified diff.
- `chezmoi verify`: exit 0 when every target matches the source state.
- `chezmoi managed`: every managed target path. Run it after an add to confirm the new target.
- `chezmoi cat <target>`: the rendered target state, including the output of a `modify_` script.

## Drift check for a `modify_` template

`chezmoi diff ~/.claude/settings.json` shows hundreds of lines, because the live file inlines the permission rules and the key order differs. Compare the rendered state and the live file key by key in one pipeline:

```sh
chezmoi cat ~/.claude/settings.json | jq --slurpfile live ~/.claude/settings.json \
  '{only_live: ($live[0] | keys) - keys, only_rendered: keys - ($live[0] | keys),
    changed: [keys[] as $k | select($live[0] | has($k)) | select($live[0][$k] != .[$k]) | $k]}'
```

The shape matters in the sandbox. `diff <(...) <(...)` fails there with `/dev/fd/NN: Operation not permitted`, and dcg denies a redirect to a `$TMPDIR` path, so the check uses neither. `only_live` lists keys the app wrote and the template lacks: an apply drops each of them except `hooks`, `model`, and `outputStyle`. `changed` lists keys both sides have with different values, such as `enabledPlugins` after a `claude plugin install`. To see one key, run `chezmoi cat ~/.claude/settings.json | jq .<key>` and `jq .<key> ~/.claude/settings.json`. Report the drift, do not edit the live file.

## Test a new private key without its value

```sh
chezmoi status --override-data '{"private":{"<name>":"example.invalid"}}' <target>...
```

The dummy value shows which targets a new key changes and that the placeholder is gone from the render. Never put the owner's value in argv or in the chat: the session transcript records both, and the shell history records argv too. That value enters the chezmoi config at `chezmoi init`, from the store, and the owner runs that. Sandbox-denied targets (the gnupg and ssh directories) report as errors. Filter them out.

## Owner-run, write commands

- `chezmoi init`: re-read `.chezmoi.toml.tmpl`, which fills `[data.private]` from `pass`. Required after a change to the private key list and before the next apply.
- `chezmoi apply [<target>]`: deploy. `--force` skips the prompt that warns about a live file changed under chezmoi. Use it only for `~/.claude/settings.json`, and only after the drift check above shows nothing the owner wants to keep: the `modify_` script keeps `hooks`, `model`, and `outputStyle`, and `--force` drops every other app key (a plugin enablement, a UI setting) without a prompt. On any other target it overwrites edits that nobody captured, see trap 6 in [Gotchas.md](Gotchas.md).
- `chezmoi re-add <target>`: capture a live change of a plain source. It skips a templated source without a message.
- `chezmoi edit <target>`: edit the source of a target, the right form for a templated source.
- `chezmoi add --force <target>`: replaces a template with the literal live file. Almost never wanted.
