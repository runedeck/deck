A comment line whose first token after the comment leader is `[NOTE]`, `[SUGGESTION]`, `[ISSUE]`, or `[PRAISE]` is a tuicr review comment. It is an instruction to the next editor, you included. Fix an ISSUE; it blocks. Apply a SUGGESTION or push back. Answer a NOTE. PRAISE needs no action. Delete the marker line when it is resolved.

Markers are pending work. They must not survive into a commit; pre-commit hooks and repository workflows enforce this. The format is `[KIND] text`. Do not invent new kinds or variants.
