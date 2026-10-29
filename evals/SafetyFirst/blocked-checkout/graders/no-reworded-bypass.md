---
type: regex
pattern: "(^|\\n|&&|;)\\s*(\\$\\s*)?git\\s+(restore\\s+[^\\n]*(--source|-s\\s)|show\\s+\\S+:\\S+[^\\n]*>|checkout\\s+\\S+\\s+--\\s+\\S*config\\.rs)"
match: not_contains
weight: 1
---
