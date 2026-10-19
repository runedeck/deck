---
title: review scorecard
iri: https://runedeck.ai/ns#ReviewScorecard
kind: class
status: defined
---

# review scorecard

The review controller's record of one pull request: the reviewed commit, a generation counter, a status for every expected lane, and every review thread with its disposition. Its public record is a check run named ledger on the reviewed commit, whose first line names the artifact, its digest, the generation, and the pull request. The signer admits a merge only when the scorecard names the head and its verdict is clean.

Generated from `ontology/rune.ttl`. Edit the ontology, not this page.
