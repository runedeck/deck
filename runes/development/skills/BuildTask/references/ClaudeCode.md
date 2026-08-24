# Claude Code Routine

Map the task definition to one Claude Code Routine.

## Environment

1. Create one dedicated Claude Code environment.
2. Attach only the repositories that the task definition permits.
3. Complete each trusted preparation step before the task starts.
4. Add only the non-secret environment values from the task definition.
5. Deny task network access when the task definition prohibits network access.
6. Select the most restrictive file permission that completes the task.

7. Permit the read-only terminal only when the task definition requires it.
8. Permit only the named command classes from the task definition.
9. Deny each other tool.
10. Add no credential or private environment value.

A canary environment value does not enforce a permission.
The provider sandbox supplies the stronger control.

Verify whether the selected environment supports trusted preparation before every run.
The task prompt controls activity after the run starts.

For the repository scanner, permit only the command names in its task definition.
Apply the Git subcommand and argument limits from its prompt.

## Git preparation

Run one trusted preparation step before every repository scan.
Use network access only during this step.
Create or refresh one bare mirror from the canonical public HTTPS remote.
Prune remote refs during each refresh.

Use these Git operations in the trusted step:

~~~sh
git clone --mirror <public-https-url> <mirror-path>
git -C <mirror-path> remote update --prune
git -C <mirror-path> for-each-ref --format='%(refname) %(objectname)'
~~~

Run the clone operation only when the mirror does not exist.
Reject a shallow mirror, partial mirror, promisor remote, object alternate, or local configuration include.
Reject a mirror with a hook, fsmonitor, filter, text converter, or external diff.

Sort the manifest lines by ref name with the C locale.
Use one space between each ref name and object ID.
Use UTF-8, LF endings, and exactly one final LF.
Calculate the SHA-256 digest from these exact bytes.

Pass the manifest as multiline environment content in PUBLIC_REF_MANIFEST.
Pass its digest in PUBLIC_REF_MANIFEST_SHA256.
Pass an RFC 3339 UTC timestamp in PUBLIC_REF_MANIFEST_AT.
Pass the owner and repository in PUBLIC_REF_REPOSITORY.
Pass the canonical public HTTPS URL in PUBLIC_REF_REMOTE_URL.
Set PUBLIC_REF_FETCH_STATUS to success only after the refresh succeeds.

Set each safety environment value that the prompt requires.
Set TRUSTED_REPOSITORY_PREPARED and GIT_OBJECTS_ISOLATED only after all preparation checks pass.
Deny network access before the task starts.

Do not activate the routine when preparation runs only once.
Do not activate it when preparation cannot pass multiline environment content into each run.
Use a separate trusted scheduler only when it shares the mirror with the task.
Do not use this fallback when a cloud task cannot access the prepared mirror.

## Routine

1. Create one Claude Code Routine.
2. Select the dedicated environment.
3. Select the specified model.
4. Select the specified reasoning level.

5. Disable model fallback when the task definition requires this setting.
6. Paste the complete rendered prompt.
7. Set the specified schedule and time zone.
8. Enable only the specified notification.

The provider stores the rendered prompt and its approved public values.
Do not add a private value.

Do not activate the schedule before the manual canary succeeds.
Verify the Routine inbox result during the canary.
Enable device notifications separately when the provider and operating system support them.
Verify one device notification before activation.

## Limits

Provider controls can change.
Pause activation when a required control is unavailable.
Report each unavailable control during the canary.

The prompt cannot prove that the provider blocked an action.
The prompt can only report the tools and commands that it used.

Pause activation when the environment cannot prepare required Git history or refs.
