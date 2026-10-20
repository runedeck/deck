---
type: regex
pattern: "git\\s+(add|commit)\\b[^\\n]*(&&|;)\\s*(\\\\\\s*\\n\\s*)?git\\s+(commit|push)\\b"
match: not_contains
weight: 1
---
