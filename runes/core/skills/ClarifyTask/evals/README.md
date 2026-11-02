# ClarifyTask trigger cases

Use these cases to evaluate skill selection, not task execution.
Both JSON files use BuildSkill's trigger format: arrays of `query` and `should_trigger` objects.

- `trigger-eval.json`: four positive cases and two near-misses for description changes.
- `trigger-eval-held-out.json`: two positive cases and two near-misses reserved for final evaluation.

Do not use the held-out cases to tune the description.
Keep both files unchanged during a comparison.
These fixtures have no measured routing score until an evaluation runs.

The training near-misses belong to WorkflowInterface and IntakeIdea, in that order.
The held-out near-misses belong to AdversaryReview and ReviewChange, in that order.
