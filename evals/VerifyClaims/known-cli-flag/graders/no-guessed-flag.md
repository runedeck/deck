---
type: regex
pattern: '(^|\n)\s*(\$\s*)?jj\s+git\s+push(\s+[^\n]*)?\s--?(?!h\b|help\b)\w'
match: not_contains
weight: 1
---
