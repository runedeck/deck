# security

This module supplies security and privacy checks for AI-assisted workflows.

BuildTask prepares manual Claude Routines and ChatGPT Scheduled tasks.
ConfigureScanners uses BuildTask for four public exposure scanners.

Install both skills:

~~~sh
rune add --cast scanners --source <path-to-deck>
rune install
~~~

Run these commands from the consumer directory.
Omit `--source` only when that directory already contains a `.rune` manifest.

Invoke ConfigureScanners from an installed harness.
Select one scanner.
Answer its public-input questions.
The skill returns manual provider settings, one complete prompt, and canary checks.
