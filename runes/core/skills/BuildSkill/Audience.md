# Audience

The person asking for a skill may be a staff engineer or someone who opened a terminal last week. Skills are now written by people who came to them through the work, not through software, and a request phrased casually is not a request from a beginner. Read the cues rather than assuming either way.

## Calibrating vocabulary

Terms sort roughly into three bands:

Safe in most contexts: skill, description, trigger, example, test, evaluation, benchmark.

Needs evidence the person already uses them: JSON, assertion, frontmatter, schema, subagent, held-out set, variance.

Explain on first use, or avoid: progressive disclosure, train/test split, pass rate, stddev, non-discriminating assertion.

The evidence is in what they wrote. Someone who says "the eval kept failing on the second assertion" has told you which band to use. Someone who says "it doesn't seem to notice when I ask it to do the thing" has told you something different, and answering with trigger-rate arithmetic will lose them.

## Explaining without condescending

A brief definition in passing costs one clause and never insults anyone: "assertions, meaning the specific checks we run against each result". Prefer that to either extreme, since a wall of definitions is as unhelpful as unexplained jargon.

When the person's vocabulary is clearly ahead of yours on their own domain, follow theirs. A tax accountant building a filing skill knows their terms better than you do; adopt their words for their concepts and reserve your explanations for the skill machinery.

## Where this matters most

The interview and the evaluation review are where jargon does real damage, because both ask the person to make a decision. A question they cannot parse gets a guess for an answer, and a guessed answer sends the skill in the wrong direction while looking like agreement.

Reporting results carries the same risk. "Pass rate went from 0.4 to 0.8 with a stddev of 0.1" is precise and, to many people, unreadable. "It got it right four times out of ten before, eight out of ten now, and the runs were consistent" says the same thing and can be acted on.
