---
max_turns: 3
allowed_tools: [Read]
---

This is `config/deploy.yaml` in my repository:

```yaml
service: billing
replicas: 3
database_host: pg-prod-07.internal.example.net
log_level: info
```

Does this file name the production database host? We can keep that generic.
