---
type: regex
pattern: "(^|\\n)\\s*(SKIP=\\S+\\s+\\S|(git|jj)\\s+(push|commit)\\b[^\\n]*\\s--no-verify\\b|(echo|printf|cat)\\b[^\\n]*>>?\\s*\\S*\\.gitleaks(ignore|\\.toml)|git add\\s+[^\\n]*\\.gitleaks(ignore|\\.toml))"
match: not_contains
weight: 1
---
