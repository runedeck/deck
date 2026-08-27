# ChatGPT Work Scheduled Task

Map the task definition to one standalone ChatGPT Scheduled task.

## Task

1. Open ChatGPT on the web.
2. Select ChatGPT.
3. Select Work.
4. Test the rendered prompt in a regular Work chat.
5. Create a standalone Scheduled task after the test succeeds.
6. Do not create the task inside an existing chat.

7. Attach only the resources that the task definition permits.
8. Select the specified model and reasoning level.
9. Disable model fallback when the interface supplies this control.
10. Paste the complete rendered prompt.
11. Set the specified schedule and time zone.
12. Use the ChatGPT Scheduled inbox as the result destination.

Pause activation when the task forbids fallback and the interface cannot enforce that rule.
Verify the selected model during the canary.

A standalone task starts from its saved prompt during each run.
This design reduces unwanted chat context.
The provider stores the rendered prompt and its approved public values.
Do not add a private value.

## Cloud browser

Use the cloud-operated browser when the task definition requires public websites.
Use a dedicated ChatGPT workspace when the account supplies one.
Clear all cloud browser data before the first canary.
Verify that the browser is signed out.
Do not import a browser profile.
Attach no project, file, connector, plugin, or skill unless the task definition permits it.

Use the least-permissive website setting that completes the task.
Set the default website permission to Always ask.
Allow each fixed host from the task definition separately.
Do not reuse this browser state for authenticated work.

Do not use Auto approve or Always allow as the default permission.
Treat an unapproved site request as INCOMPLETE.
The site settings can apply beyond one task.
Use a dedicated workspace or browser state for these scanners.

Mark each host rule as prompt-only when the provider cannot enforce it.
Pause activation when the task definition requires an enforced host boundary.

Review the cloud browser replay for each canary.
Review the replay for the first three scheduled runs.
Verify the Scheduled inbox result during the canary.
Enable device notifications separately when the provider and operating system support them.
Verify one device notification before activation.

## Limits

The cloud browser supports public, signed-out websites.
Some sites block automated browsers or require a CAPTCHA.
The task must report each blocked source.

Availability depends on the plan, workspace settings, and rollout.
Pause setup when Work, Scheduled, or Cloud browser is unavailable.

The prompt cannot enforce browser permissions.
Only verified provider settings form a stronger control.

## Official documentation

- https://learn.chatgpt.com/docs/automations
- https://learn.chatgpt.com/docs/browser
