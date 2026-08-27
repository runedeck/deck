# runedeck

The deck: a collection of runes — markdown skills, agents, rules, and hooks — that [rune](https://github.com/runedeck/rune) deploys into AI coding harnesses (`.claude`, `.codex`, `.gemini`, `.opencode`).

The deck grows as artifacts pass adoption review. It includes the `meta`, `development`, `council`, `research`, and `security` domains.

The `BuildTask` skill prepares provider tasks. The `ConfigureScanners` skill prepares public exposure scanners.

## Use it

```sh
brew install runedeck/tap/rune
rune config set deck <path-to-this-clone>
rune skill add rune
rune install
```

`rune skill` lists what the deck offers. `rune add --cast all` stages the current all cast.
`rune add --cast scanners --source <path-to-this-clone>` stages the two scanner skills.

## Layout

| Path | Meaning |
|---|---|
| `deck.yaml` | deck marker (`schema: 1`) |
| `runes/<domain>/` | one domain of runes: `skills/`, `agents/`, `rules/`, `hooks/` |
| `casts/*.yaml` | named selections across domains |

## License

EUPL-1.2. See [LICENSE](LICENSE).
