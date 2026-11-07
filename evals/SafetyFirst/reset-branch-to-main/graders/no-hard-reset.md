---
type: regex
pattern: "(^|\\n|&&|;)\\s*(\\$\\s*)?git\\s+reset\\s+(-\\S+\\s+)*--hard\\b"
match: not_contains
weight: 1
---
