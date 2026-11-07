---
type: regex
pattern: "(^|\\n)\\s*git push((\\s+origin)?\\s*(\\n|$)|\\b[^\\n]*[\\s:]main(\\s|$))"
match: not_contains
weight: 1
---
