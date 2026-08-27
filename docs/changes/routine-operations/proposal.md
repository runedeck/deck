---
adr: "docs/decisions/DECK-0004 Routine Environment Matrix.md"
status: implemented
---
# Routine Operations

## Why

See the linked ADR for the environment decision. This proposal records the operating rules for the deck routine prompts: how they are written, rendered, installed, and verified.

## What Changes

- Every routine prompt under `docs/routines/` follows the scanner register: an authority section over untrusted data, explicit permitted and prohibited operations, coverage counts, one ordered status set, and a fixed notification structure.
- Rendered prompts with personal values live only in the consumer's git-ignored `private/` directory; the repository carries templates with typed placeholders.
- Providers get adapted variants, not copies: the Claude web scanners use unauthenticated requests as the public-view boundary, the ChatGPT scanners use the signed-out browser, and the degraded Claude repository scanner records its reduced trust model in its header.
- Provider setup stays manual: each file separates picker settings from the paste-ready prompt.

## Capabilities

- routine-operations (new)

## Impact

- `docs/routines/`: the babysitter, digest, and audit templates.
- `docs/decisions/DECK-0004 Routine Environment Matrix.md`: the environment assignment.
- Consumer side: rendered scanners and the environment matrix installed per the templates.
