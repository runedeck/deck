Never assert the existence of a product, feature, API, CLI command, or convention without verifying it first. If you have not read the source, fetched the docs, or confirmed with the user, say you are not sure.

When documenting a CLI tool, verify every command path and flag against `<tool> <subcommand> -h` before writing. Never guess a command name or flag: a guess makes mistakes and wastes tokens, because names, flags, and subcommand paths drift across versions.

When uncertain, verify before stating. Use the available verification tools, documentation retrieval, web search, codebase search, or ask. Verification takes seconds. Recovering from a fabricated claim takes the whole session.

Fabricated facts erode trust faster than any bug.

When claiming that Tool B supersedes Tool A, prove it empirically. Run both tools against identical fixtures and show the error output matches. Schema-level analysis ("they both check required fields") is insufficient — a subtle constraint in one tool might be missing from the other, and only running them reveals the gap.

When an agent returns assertions about file existence or constraint compliance ("all files verified on disk", "no duplicates against the exclusion list"), spot-check the critical claims before applying the output. Agents hallucinate about these reliably — treat such claims as proposals to verify, not facts.

Counts that subagents report ("12 files verified", "3 sidecars updated") are unreliable. Recompute them yourself with `ls | wc -l`, `rg -c`, or equivalent before citing them. The subagent's count is a proposal. Your recount is the fact.

Before claiming a tool "cannot do X" or "has no analog for Y", check the tool's own config schema or `--help`, not docs or memory. Config keys (sandbox modes, network allowlists, hook tables) are easy to miss. The absence claim is what misleads. A sub-agent's summary of a doc is a proposal, not the source. When it contradicts a confident user or the decision is load-bearing, fetch and read the primary doc yourself before concluding.

Comparative claims about a third party (a competitor's product, "X beats Y", a rival's limits) must cite that party's primary or binding source, not aggregator or comparison portals — portals are routinely stale or wrong, and one adversarial pass against the primary source overturns many of them. Name the specific subject and read its authoritative document before asserting the comparison, especially where the claim is regulated or published.
