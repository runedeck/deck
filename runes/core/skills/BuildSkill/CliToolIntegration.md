# CLI tool integration

When a skill wraps a CLI tool (Rust binary, shell script), include:

1. **Tool location and dependency** — the executable's name, how its presence is checked, and any required version
2. **Verified usage examples** — concrete `bash` blocks, confirmed against the installed tool's help output
3. **Intent-to-flag mapping** — table translating natural language to CLI flags
4. **Input and output contract** — accepted inputs, output format (JSONL, plain text, etc.), exit codes, and error output
5. **Operational boundaries** — whether the tool writes files, changes external state, opens a GUI, or uses the network
