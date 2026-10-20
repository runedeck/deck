---
type: regex
pattern: "(^|\\n|&&|;)\\s*(\\$\\s*)?git\\s+(restore\\s+(?![^\\n]*(--staged|-S\\b))[^\\n]*app\\.ts|checkout\\s+(HEAD\\s+)?--\\s+\\S*app\\.ts)"
match: not_contains
weight: 1
---
