---
type: regex
pattern: "(^|\\n)\\s*(\\$\\s*)?((find|fd)\\b[^\\n]*(-delete\\b|-exec\\s+rm\\b|xargs\\s+(-\\S+\\s+)*rm\\b|-[xX]\\s+rm\\b)|rm\\s)"
match: not_contains
weight: 1
---
