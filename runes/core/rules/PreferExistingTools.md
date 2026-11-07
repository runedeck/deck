Use an existing standard tool before you write a custom script. For a project template, use Copier. For a check that runs on commit or push, use the hook framework that the repository already runs.

A custom script is code that someone must read, test, and keep working. A standard tool has users who already found its bugs, and its documentation exists. Write a script only when no standard tool does the job. Keep it short, and say in its header which tool you looked for first.
