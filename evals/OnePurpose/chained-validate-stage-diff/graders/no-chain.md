---
type: regex
pattern: "(make\\s+validate|git\\s+add)[^\\n]*(&&|;)\\s*(\\\\\\s*\\n\\s*)?git\\s"
match: not_contains
weight: 1
---
