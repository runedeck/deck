# Scanner Catalog

## Public Repository Deep Scan

### Task

- Task name: Public repository exposure.
- Provider: Claude Code Routine.
- Template: [PublicRepositoryExposure.md](../templates/claude/PublicRepositoryExposure.md).

### Schedule

- Daily time: 04:10.
- Model: user-selected exact Opus model identifier.
- Reasoning: provider default.

### Permissions

- Fallback: none.
- Repository: the trusted public bare mirror.
- Network: deny after environment preparation.
- Browser: deny.
- Tools: git, shasum, file, strings, rg, sed, tr, sort, uniq, wc, awk, date, and printf.
- Writes: deny.

### Preparation

- Preparation: trusted per-run refresh of one full bare mirror with all intended public refs.
- Manifest: sorted ref and object-ID lines in PUBLIC_REF_MANIFEST, with one final LF.
- Binding: repository, canonical remote URL, fetch status, UTC timestamp, and SHA-256 digest.
- Environment: [repository environment values](ScannerInputs.md#public-repository-environment).
- Activation: deny when the provider cannot run trusted preparation before every task.

### Delivery

- Notification: Claude Routine inbox.
- Device delivery: enable and verify when the provider supports it.
- Result limit: 600 characters for OK and REVIEW.
- Alert limit: 12 short lines.

### Inputs

- Inputs: [ScannerInputs.md](ScannerInputs.md#public-repository-inputs).
- Canaries: [ScannerCanaries.md](ScannerCanaries.md#public-repository-canary).

## All-Public-GitHub Sweep

### Task

- Task name: Public GitHub exposure.
- Provider: ChatGPT Work standalone Scheduled task.
- Template: [GitHubPublicExposure.md](../templates/chatgpt/GitHubPublicExposure.md).

### Schedule

- Daily time: 04:40.
- Model: `gpt-5.6-sol` as the exact identifier.
- Reasoning: Extended.

### Permissions

- Fallback: none.
- Repository: none.
- Network: configured public GitHub hosts.
- Browser: isolated signed-out cloud browser.
- Extra tools: deny.
- Writes: deny.

### Delivery

- Notification: ChatGPT Scheduled inbox.
- Device delivery: enable and verify when the provider supports it.
- Result limit: 600 characters for OK and REVIEW.
- Alert limit: 12 short lines.

### Inputs

- Inputs: [ScannerInputs.md](ScannerInputs.md#public-github-inputs).
- Canaries: [ScannerCanaries.md](ScannerCanaries.md#public-github-canary).

## Public Web Mention Monitor

### Task

- Task name: Public web exposure.
- Provider: ChatGPT Work standalone Scheduled task.
- Template: [PublicWebMentions.md](../templates/chatgpt/PublicWebMentions.md).

### Schedule

- Daily time: 06:10.
- Model: `gpt-5.6-sol` as the exact identifier.
- Reasoning: Extended.

### Permissions

- Fallback: none.
- Repository: none.
- Network: globally routable public HTTPS sources from approved searches.
- Browser: isolated signed-out cloud browser.
- Extra tools: deny.
- Writes: deny.

### Delivery

- Notification: ChatGPT Scheduled inbox.
- Device delivery: enable and verify when the provider supports it.
- Result limit: 600 characters for OK and REVIEW.
- Alert limit: 12 short lines.

### Inputs

- Inputs: [ScannerInputs.md](ScannerInputs.md#public-web-inputs).
- Canaries: [ScannerCanaries.md](ScannerCanaries.md#public-web-canary).

## Social-Network PII Monitor

### Task

- Task name: Social PII exposure.
- Provider: ChatGPT Work standalone Scheduled task.
- Template: [SocialPIIExposure.md](../templates/chatgpt/SocialPIIExposure.md).

### Schedule

- Daily time: 06:40.
- Model: `gpt-5.6-sol` as the exact identifier.
- Reasoning: Extended.

### Permissions

- Fallback: none.
- Repository: none.
- Network: configured public social hosts and one search host.
- Browser: isolated signed-out cloud browser.
- Extra tools: deny.
- Writes: deny.

### Delivery

- Notification: ChatGPT Scheduled inbox.
- Device delivery: enable and verify when the provider supports it.
- Result limit: 600 characters for OK and REVIEW.
- Alert limit: 12 short lines.

### Inputs

- Inputs: [ScannerInputs.md](ScannerInputs.md#social-pii-inputs).
- Canaries: [ScannerCanaries.md](ScannerCanaries.md#social-pii-canary).
