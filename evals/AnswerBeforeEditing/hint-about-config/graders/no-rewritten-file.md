---
type: regex
pattern: "database_host:\\s*[\"']?(\\$\\{|\\{\\{|<|\\$[A-Z_])"
match: not_contains
weight: 1
---
