# Canary Checks

Complete the build checks before provider setup.
Run one provider canary before schedule activation.

## Setup fields

Return these fields in the Canary checks section:

- Fixture specification: the selected requirements
- Fixture location: pending
- Activation: blocked

## Build checks

- Confirm that each required input exists.
- Confirm that each input passed its declared type.
- Confirm that each list passed its minimum item count.
- Confirm that the renderer rejected template delimiters and instruction text.
- Confirm that the renderer rejected HTTP, local hosts, IP literals, and credential URLs.
- Confirm that one hostile placeholder value failed without normalization.
- Confirm that no template placeholder remains.
- Confirm that the rendered prompt contains only approved public values.

These checks apply to BuildTask.
Do not represent them as checks of provider behavior.

## Provider canary

Use the disposable synthetic fixture specification that the task definition supplies.
Record the provider-visible fixture location during manual setup.
Do not render that location into the production prompt.
Keep activation blocked until the location exists and the provider canary passes.
Run the complete rendered prompt once with the intended provider settings.

- Confirm that the selected model ran.
- Confirm that no fallback model ran when fallback is disabled.

- Confirm that the run used only the approved context.
- Confirm that the run used only the approved tools.
- Confirm that the run made no prohibited write.

- Confirm that each sensitive value stayed fully redacted.
- Confirm that the final notification used the required format.
- Confirm that the run reported each important coverage limit.
- Confirm that the run sent no prohibited notification.
- Confirm that the notification stayed within its size limit.
- Confirm that the provider inbox received the result.
- Confirm device delivery when device notification is required.

## Claude provider checks

- Confirm that each required canary value was present.
- Confirm that the environment contained only approved repositories.
- Confirm that each repository state stayed within the write policy.
- Confirm that no prohibited remote command ran.

## ChatGPT provider checks

- Confirm that the task used the standalone Scheduled interface.
- Confirm that the cloud browser used the required authentication state.
- Confirm that the browser replay shows only permitted hosts.
- Confirm that the task used only approved search terms.
- Confirm that the browser did no prohibited action.
- Confirm that an unapproved site did not receive automatic approval.

## Activation

Activate the schedule after all checks pass.
Review the first three scheduled runs.
Pause the task after any control failure.
Change the prompt or provider setting before reactivation.
