---
type: regex
pattern: '^(?![\s\S]*\bcontent (delivery|distribution) network\b)[\s\S]*\bCDNs?\b'
flags: i
match: not_contains
weight: 1
---
