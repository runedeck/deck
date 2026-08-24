Start each shell command chain with `cd` to an absolute path. The shell working directory persists between commands and does not follow your attention. An inherited working directory sends relative paths into the wrong tree.

Before a mutating command in a repository with several worktrees, confirm the target: `git rev-parse --show-toplevel`. Never run a state change from an assumed working directory.
