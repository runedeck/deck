---
name: FullSend
description: "Take one task from the owner to a merge-ready pull request while the owner reads nothing: fix it, verify the fix, open the pull request, babysit it until every check and reviewer is clean, run a last verification pass, then ask once to merge. USE WHEN full send, fix this and get it merged, take this all the way, I will not read the output, handle this end to end while I am away. NOT FOR a pull request that already exists and needs only its review loop (VersionControl BabysitPR), a survey of a whole pull-request queue (MergeTrain), or a spec-driven change that is still in planning (ForgeCycle)."
compatibility: "Requires gh with write access to the repository and the harness's blocking question tool. Without that tool, the skill stops at merge-ready and puts the question in the first line of its last message. Workflow children cannot ask and therefore never run this skill."
metadata:
    version: 0.1.0
---

# FullSend

The owner gives you a task and leaves. You fix it, prove the fix, open a pull request, and babysit it to merge-ready. Then you ask one question: may I merge this. The owner reads that question and nothing else.

## Prerequisites

- The task: an issue URL, an error, a file, or a description.
- The repository, its default branch, and `gh` with write access.

## Constraints

### The owner does not read your output

The owner who sends this prompt with full send does not expect to read your messages, now or later. A question in a message is a question nobody sees.

- When you need the owner, use the question tool. The tool notifies the owner. Prose does not.
- When the session has no question tool, stop where you need the owner. Put the question alone in the first line of your last message.
- Ask only what blocks the work: a secret, a hardware key touch, an account you have no access to, or a product decision. Decide everything else yourself. Record each such decision in the pull request body.
- Keep each question complete on its own: the pull request URL, what changed, and what each option does.

### Remote writes

- Invoking FullSend is the owner's request to push one branch and open one pull request for this task. It authorizes nothing more.
- Never merge, ready a draft, comment, label, resolve a thread, or force-push without the owner's yes in the question tool. For every other write, apply the RemoteWrites rule.
- Never weaken a check to make it pass: no skipped test, no lowered threshold, no `SKIP=`, no `--no-verify`, no new allowlist or ignore entry, no review override. When only a weaker check makes the work pass, the owner decides.

## Instructions

### Fix and verify

1. Work in an isolated workspace, per VersionControl: a jj workspace in a colocated repository, a Git worktree otherwise.
2. Reproduce the problem before you edit. A reproduction is a command, a test, or a recording that fails now.
3. Make the smallest complete fix. Keep unrelated changes out.
4. Verify the fix with the strongest evidence that the change allows. Best: drive the real app through computer use, the browser, the simulator, or a terminal session, and record it with AcceptanceTesting. Next: a test that fails before the fix and passes after it, kept in the pull request. Last: a script that exercises the changed path, named as the only evidence in the pull request body.
5. Run the repository's full local check set, per ContinuousIntegration.

### Open and babysit the pull request

1. Commit in the repository's format with the model identity, per VersionControl.
2. Push the branch. A runedeck repository opens the draft itself when the bookmark starts with `change/`, `codex/`, or `fable/`. Elsewhere, run `gh pr create`.
3. Write the body for a reader who was not here. Say what was wrong and what changed. Link the evidence of the verification. List each decision you made alone.
4. Apply the VersionControl companion `BabysitPR.md` until its merge-ready conditions hold. Fix each red check and each valid finding, push, and wait for the next round. Wait with the harness's watcher when it has one. Otherwise read the checks again no more often than every five minutes.

### Verify again on the final head

1. Read the whole diff against the base branch.
2. Run the verification from step 4 of Fix and verify again on this exact head.
3. Have a different model review the diff with fresh context, through AdversaryReview or the harness's code review. Fix each hit or reject it with a reason.
4. Rate your confidence high only when four things hold on this head. Every required check passes. No thread is open. The evidence came from this head. The second review found nothing blocking.

### Ask once

Ask one question through the question tool. Include the pull request URL, the head SHA, two sentences on what changed, the evidence, and your confidence with its reason. Ask even when you cannot run the merge yourself, so the owner's answer is one word.

- High confidence: list the exact merge command and offer "Merge it" and "Leave it open". In a repository with the sealed review ceremony, take the merge-ready step in BabysitPR first and make the key touch the merge option.
- Not high: name what is unresolved and offer "Leave it open" and the one next action you recommend.

On "Merge it", run exactly the listed command one time. Read the pull request state again and report the result in one line with the URL.

## Verification

- The question names the live head SHA and the pull request URL.
- No merge command ran before the owner's yes.
- No turn ended with a question in prose.
- The evidence in the pull request body comes from the final head.

## Troubleshooting

- A hook, a scanner, or a command guard blocks a step: read what it reports and fix that cause. When the only way past it weakens the check, ask the owner and continue with the parts that do not depend on the answer.
- A secret scanner flags a fake secret in a test fixture: change the fixture so it stops looking like a secret, or ask the owner before you add any exemption.
- BabysitPR used its last review round: stop and ask, with the open findings in the question.
- Another session moved the head: read the remote head, reconcile, and never force-push.

## References

- VersionControl companions `BabysitPR.md` and `Authorization.md`, and the RemoteWrites rule.
- ContinuousIntegration, AcceptanceTesting, AdversaryReview, and SafetyFirst.
