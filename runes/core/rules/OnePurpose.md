One action, one purpose. Apply this to every tool invocation: shell commands, file edits, agent dispatches, API calls. The user must be able to read, understand, and approve each action at a glance, and a failure must be attributable to one step.

Never chain unrelated operations (validate && stage && diff) into a single command line. Acceptable chaining: a guard and its single consequence (`mkdir -p dir && cd dir`), or a cheap probe before one action. Anything longer splits into separate invocations.

A pipeline that transforms one data stream (`cmd | filter | sort`) is one purpose and stays together. The smell is `&&` or `;` joining independent actions, not pipes.

The same discipline holds beyond the shell: one edit per concern, one commit per changeset, one agent per task. Batched unrelated work hides what happened and forces all-or-nothing review.
