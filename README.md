# runedeck

The deck: a collection of runes — markdown skills, agents, rules, and hooks — that [rune](https://github.com/runedeck/rune) deploys into AI coding harnesses (`.claude`, `.codex`, `.gemini`, `.opencode`).

The deck is growing domain by domain as artifacts pass adoption review. Today it carries the deck skeleton (`meta`, `development`, `council`, `research`) and the `rune` skill, which teaches AI agents to drive the CLI.

## Use it

```sh
brew install runedeck/tap/rune
rune config set deck <path-to-this-clone>
rune skill add rune
rune install
```

`rune skill` lists what the deck offers; `rune add --cast all` stages every published rune. The `development`, `council`, and `research` domains are scaffolding today — they fill as artifacts pass adoption review.

## Layout

| Path | Meaning |
|---|---|
| `deck.yaml` | deck marker (`schema: 1`) |
| `runes/<domain>/` | one domain of runes: `skills/`, `agents/`, `rules/`, `hooks/` |
| `casts/*.yaml` | named selections across domains |

## License

EUPL-1.2. See [LICENSE](LICENSE).
