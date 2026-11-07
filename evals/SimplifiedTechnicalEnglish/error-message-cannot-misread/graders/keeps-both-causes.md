---
type: regex
pattern: '^(?=[\s\S]*\b(missing|not exist|does not exist|not found|cannot find)\b)(?=[\s\S]*(\b(path|location)\b[^.\n]{0,40}\b(wrong|incorrect|invalid|not correct)\b|\b(wrong|incorrect|invalid)\b[^.\n]{0,20}\b(path|location)\b))'
flags: i
match: contains
weight: 1
---
