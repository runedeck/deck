---
name: BuildAvatar
description: "Interview the user, build one canonical AGENTS.md identity file, and propagate it to every harness and provider memory system. USE WHEN build avatar, create AGENTS.md, identity interview, who am I for agents, set up AI memory, sync my profile to claude/codex/gemini/opencode, import memory to a provider, refresh my avatar. NOT FOR project-level CLAUDE.md files (init), session learnings (LearnFrom), or authoring agents (BuildAgent)."
metadata:
    version: 0.1.0
    inspiration: https://github.com/N4M3Z/forge-avatar
---

# BuildAvatar

Build the user's avatar: one canonical `AGENTS.md` that tells every AI tool who the user is, how to respond, and what the user works on. The skill runs an interview, composes the file, and propagates the content to each harness and provider memory system. The avatar is dotfiles for AI identity: write once, deploy everywhere.

## Prerequisites

- The target location for the canonical file. Default: `~/.config/rune/avatar/AGENTS.md`, a private git repository that a chezmoi external deploys next to the rune configuration. An existing file at the target starts an update interview instead of a full one. Commit and push the repository after every avatar change.
- The `AskUserQuestion` tool for the interview. Without it, use plain conversation and ask one question in each message. The round limits apply only to `AskUserQuestion`.

## Constraints

- Ask about PII before you write anything. The canonical file and local harness files default to full detail. Any content pasted into a third-party provider defaults to anonymous: no employer name, no team member names, no location beyond country.
- Never auto-apply. Present a reconciliation table of every planned write, and wait for the user's confirmation.
- Own only the managed block. Every deployed surface gets the content between `<!-- avatar:begin -->` and `<!-- avatar:end -->` markers. Never touch text outside the markers. A rerun replaces the block in place.
- Interview for facts the harness cannot discover. Do not ask about repository conventions, code style the linters enforce, or anything a `CLAUDE.md` already records.
- Run one interview round at a time. Ask at most four questions in each `AskUserQuestion` round. Push back on vague answers and ask for a concrete example. Summarize each section in one sentence before the next.
- Modality is content. Record hedges and uncertainty as the user states them.

## Instructions

### Run the interview

Run the question bank in [Interview.md](Interview.md): 20 to 30 questions across five to eight `AskUserQuestion` rounds, eight sections from profile to goals and beliefs. A short confirmation pass is not an interview. Rich session context does not cancel the interview; it converts fact questions into confirmations while the depth questions (examples, annoyances, boundaries, goals, beliefs) still run. Skip a section only when an existing avatar answers it and the user confirms the content still holds.

Without `AskUserQuestion`, ask the same question bank through plain conversation. Ask one question in each message and do not count tool rounds.

For an update interview, show the current section content and ask what changed.

### Compose the canonical AGENTS.md

Write the answers as a compact identity file at the target location:

```
# Agents brief

<!-- avatar:begin -->
## Who I am
<Profile as two or three sentences.>

## How to respond to me
<Preferences as short imperative bullets: the instructions an agent follows.>

## How I decide
<Trust order, speed-versus-proof line, risk appetite, learning style.>

## Working with me
<Standing delegation grants and their hard limits, pacing, notification triggers, parallel-session norm, working hours.>

## What I work on
<Current projects and stack, one line each, dated (month year), with each project's direction.>

## Goals (next 12 months)
<The goals agents keep in view, as one short paragraph.>

## Beliefs
<Standing technical beliefs as bullets.>

## Challenge me on
<The behaviors the user wants named when agents see them.>

## Topics I track
<Interest bullets.>

## Hobbies
<Personal interests kept distinct from work topics.>

## Never store or repeat
<Boundary bullets.>
<!-- avatar:end -->
```

Keep the file under 500 words. Every line must earn context cost in every session that loads it: cut anything only sometimes useful. Date the "What I work on" section so staleness is visible.

### Propagate to local harness memory

Deploy the managed block to each surface that exists on the machine. Check for each path first; skip absent harnesses silently.

- Claude Code global: Write the managed block to `~/.claude/CLAUDE.md`.
- Codex: Write the managed block to `~/.codex/AGENTS.md`.
- Gemini CLI: Write the managed block to `~/.gemini/GEMINI.md`.
- OpenCode: Write the managed block to `~/.config/opencode/AGENTS.md`.
- Grok: Write the managed block to `~/.grok/GROK.md`.
- Claude Code auto-memory: Write one `user`-type memory file in the active project `memory/` directory. Point it at the canonical path.

Show the reconciliation table (surface, action: append block, replace block, skip), get confirmation, then write. On first deployment, append only the managed block. On a rerun, replace the text between the markers in place. Preserve all content outside the markers byte for byte.

### Generate provider import prompts

Web providers have no file to write; the user edits their memory in the provider's own settings UI. Create a provider-safe copy of the anonymized or full block per the PII decision. Remove the complete `Never store or repeat` section from this copy, including its heading. Generate a paste-ready prompt from only the provider-safe copy:

```
Update your memory about me from this brief. Store the "Who I am" section
as my profile, "How to respond to me" as my preferences, and each "Topics"
bullet as a topic. Store only facts that appear in this brief. Do not infer
or restore omitted information.

<the provider-safe managed block>
```

Tell the user where to paste it: claude.ai Settings → Memory ("Tell Claude what to change"), ChatGPT Settings → Personalization → Memory. Providers with a memory-import flow accept the same text. Tell the user to review provider memory and delete entries that violate private boundaries. Never paste the boundary text into a provider.

### Report

List the canonical path, every surface written or skipped, and every prompt generated. Remind the user to rerun the skill when role, projects, or boundaries change, and that the dated work section is the staleness signal.

## Verification

- The canonical file exists, is under 500 words, and carries both markers.
- Every written surface contains exactly one managed block, and a diff outside the markers is empty.
- A rerun with no answer changes produces zero diffs.
- The provider prompt contains neither the `Never store or repeat` heading nor content from that section. The anonymous variant contains no employer, team member, or location detail.

## References

- [Interview.md](Interview.md): the question bank, round design, and interview method.
- [forge-avatar](https://github.com/N4M3Z/forge-avatar): the identity-layer pattern this skill compresses. Avatar files, interview round-trips, PII gates, and reconciliation before writes.
