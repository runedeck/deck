# Contributing

Runes enter the deck through adoption review: `rune adopt` records provenance (SLSA sidecars with upstream digests), and each artifact is reviewed section by section before it lands. Until that pipeline is public, the deck grows by maintainer adoption; issues and suggestions are welcome.

Ground rules for content:

- Skills follow the [agentskills.io](https://agentskills.io) standard: kebab-case `name` matching the directory, `SKILL.md` with frontmatter.
- `rune validate` passes before any commit.
- Synthetic data only in examples; no real names, addresses, or credentials.
- Four-space indentation, LF line endings, files end with a newline.
