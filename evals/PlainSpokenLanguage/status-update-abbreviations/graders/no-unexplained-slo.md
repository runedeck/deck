---
type: regex
pattern: '^(?![\s\S]*\bservice[- ]level (objective|target|goal))[\s\S]*\bSLOs?\b'
flags: i
match: not_contains
weight: 1
---
