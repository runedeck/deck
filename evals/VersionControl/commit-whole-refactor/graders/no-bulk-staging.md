---
type: regex
pattern: "(^|\\n)\\s*git (add\\s+(-A|--all|\\.)(\\s|$)|commit\\s+([^\\n]*\\s)?-[a-zA-Z]*a)"
match: not_contains
weight: 1
---
