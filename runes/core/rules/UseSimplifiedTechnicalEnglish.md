Write all prose as Simplified Technical English (ASD-STE100). Apply this rule to docs, messages, comments, and reports.

Prefer the active voice and simple tenses. Keep natural verb forms when a simple tense changes meaning or sounds unnatural.

Use short, common words. Use one name for one thing. Use a clear pronoun when repetition sounds mechanical.

Write one instruction for each procedural sentence. Keep instructions within 20 words and descriptions within 25 words.

Combine related descriptive facts when separate sentences sound choppy. Keep one topic in each paragraph. Use six sentences or fewer.

Use a verb for an action, not a noun. Do not use phrasal verbs, semicolons, contractions, or marketing adjectives.

Prefer literal verbs. Strongly discourage `bake`, `land`, `orchestrate`, `scaffold`, `ship`, `surface`, and `wire up` as verbs. Literal noun uses stay valid.

Do not use jargon nouns such as `gate`, `arm`, or `knob` for software concepts.

Answer the question that the prompt asked. Do not add detail that the prompt did not request.

Preserve natural English. Preserve each fact, figure, condition, scope qualifier, hedge, and modal meaning before you reduce the lint score.

Keep: `We may have found an edge case.`
Reject: `We possibly found an edge case.`

Bad: `It is important to note that leveraging the new pipeline may potentially help to improve performance.`
Good: `The new pipeline makes the build faster.`

Meaning and naturalness outrank mechanical score reduction. Keep a longer sentence when compression removes precision.

Do not apply this rule to code, identifiers, or quoted output. The standard is free at https://www.asd-ste100.org.
