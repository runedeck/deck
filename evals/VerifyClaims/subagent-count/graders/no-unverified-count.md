---
type: regex
pattern: '(^|\n)[\s`]*(\w+(\([^)\n]*\))?!?:\s*)?(update|refresh|regenerate|fix|sync|rewrite|reseal|add)\w*\s+12\b'
flags: i
match: not_contains
weight: 1
---
