# Write the title and body of a pull request

A reviewer reads the title in a list and reads the body once. Write both so that a person who has not seen the code
understands the change on one reading. The text goes out under the owner's name, so write it in the owner's voice:
casual and brief. These rules apply to GitLab merge requests too.

## Title

- Say what changes for the person who uses the software. Keep the conventional prefix and the scope that the
  repository uses.
- Do not use identifiers: config keys, functions, modules, flags, or names of internal mechanisms. Describe the
  effect instead.
- Keep the title under 70 characters.
- Use the same rules for the first line of a commit message.

Examples:

- Bad: `feat(proton): claim jj's new-commit exports in the untraced-commit fixup`
- Good: `feat(proton): attribute commits made with jj`
- Bad: `feat(proton): notes_sync_repositories decides where notes travel, apart from attribution`
- Good: `feat(proton): record data for every repo, but push notes only to Proton remotes`

## Body

Use these sections in this order. Add the sections that the repository's checks require, such as the deck's
`## Release Notes`.

- `## Summary`: bullets. The first bullet says what changes and which problem that solves for the user. The next
  bullets give the behavior a reviewer must check, such as what is now allowed and how to turn it off. One bullet
  lists each edit to shared or upstream code that a later merge can conflict with.
- `## Proof`: when the change has a recorded proof, embed the video with the build it ran on. Then list the scenes in
  order in one sentence.
- `## Not covered`: one bullet for each known gap. Link a known upstream issue instead of explaining it again.
- The last line gives the pull request that this one stacks on, if any.

Leave out:

- A list of files. The diff shows the files.
- Local test counts, checksums, and checkboxes. CI shows the results.
- Any account of the agents, sessions, drafts, and reviews behind the change.
- Generation footers, tool badges, and session links.

Use an identifier only when the reviewer must type it, such as the config key that turns a feature off. Explain an
internal term at first use, or describe it instead.

## Check before posting

- Run vale and rumdl over the body file, and fix every finding.
- Read the title alone. If a reviewer from another team cannot tell what changes, write it again.
