# Real before/after samples

Actual `claude-sonnet` outputs from the upstream blog experiment: the same prompt with a baseline system prompt and with the STE writing rules in context. Scores are heuristic anti-slop violations per 100 words, and lower is cleaner. Upstream measured them with an earlier version of the checker, so the bundled `scripts/lint.py` gives close but not identical numbers. Read these samples for the shape of the difference, not for exact scores.

## README intro — the hero example

**BASELINE** (191 words, 4.19/100w, 4 em-dashes):
> Traditional caches miss constantly in LLM workloads because users rarely phrase the same question identically — fluxcache solves this by embedding incoming prompts and matching them against previously cached queries within a configurable similarity threshold. [...] It ships with sensible defaults so you can get semantic caching running in a few lines of code, while exposing the knobs — similarity thresholds, TTLs, namespacing, custom scoring — that real applications need as they scale. Whether you're building a chatbot, a RAG pipeline, or an agentic workflow, fluxcache is designed to slot into your existing stack with minimal friction and no vendor lock-in.

**STE** (169 words, 1.18/100w, 0 em-dashes):
> A normal cache matches requests by exact text. A small change in wording then causes a cache miss. fluxcache compares the meaning of a new prompt with the prompts already in the cache. If two prompts are close enough in meaning, fluxcache returns the stored response instead of a new call to the model. This lowers the number of calls to the model and cuts the cost and response time of the application.

On screen: the em dash, "sensible defaults", "slot into your existing stack with minimal friction and no vendor lock-in", and the 30+ word opening sentence all light up red in the baseline. The STE version is short declaratives, no contractions, no em dash.

## Error message — the cleanest result

**BASELINE** (123 words, 3.25/100w): contractions ("You've"), a rolling-window explanation sentence, filler ("ensures fair access for all users").

**STE** (72 words, 0.00/100w — zero violations, 41% fewer words):
> The API allows a maximum of 100 requests per minute for each account. Your application sent more requests than this limit allows. The server rejected the extra requests to protect the system for all users. Check the `Retry-After` header in the response for the exact wait time. Wait for this time, then send your request again.

## PR description — density without run-ons

Baseline (347 words, 3.46/100w) stacks parentheticals into 30-40 word sentences ("surfaced immediately to callers with no retry, forcing every call site to implement its own ad-hoc retry logic"). STE (297 words, 1.35/100w) is one action per line, short sentences, same information.
