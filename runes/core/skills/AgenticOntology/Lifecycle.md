# Lifecycle

The artifact lifecycle is the SKOS scheme `rune:stages` in `ontology/rune.ttl`: capture, author, prove, measure, review, ship, operate. Each stage consumes one kind of entity and produces another, and the skill that serves a stage takes its name from that stage's verb or from an established discipline noun, plus the object.

## Stages

- **capture**: consumes an idea, produces a change proposal. Skill: IntakeIdea.
- **author**: consumes a proposal, produces a rune. Skills: BuildSkill, AdoptArtifact, BuildAvatar.
- **prove**: consumes a candidate commit, produces a `rune:Proof`. Skills: ContinuousIntegration for the checks, AcceptanceTesting for the behavior.
- **measure**: consumes a rune, produces a `rune:Verdict`. Skill: BenchArtifact.
- **review**: consumes a candidate and its proofs, produces an approval or findings. Skill: VersionControl, the BabysitPR companion.
- **ship**: consumes an approved candidate, produces a merge or a release. Skill: VersionControl.
- **operate**: consumes a deployed rune, produces a routine or a manifest. Tooling: `rune install` and routines.

## Naming rule

A skill name is the stage verb plus the object it acts on (`BenchArtifact`, `AdoptArtifact`), or the established discipline noun for the whole stage (`VersionControl`, `ContinuousIntegration`). The object is the entity the stage consumes, not the one it produces, so the name says what the skill takes in.

Skills that serve no single stage are disciplines that every stage uses: SafetyFirst, SimplifiedTechnicalEnglish, RTK, AgenticOntology. They take a discipline noun.

## Evidence per stage

The prove and measure stages each produce one evidence entity. `rune:Proof` records that a candidate commit passed a check, with the commit, the check configuration, the validators, and the exit status. `rune:Verdict` records that a rune earns its context cost, with the three bench metrics. Both are `prov:Entity`, both point at the entity they cover, and neither is stored as a state: a candidate is proven when a Proof exists for its commit, which is a query.
