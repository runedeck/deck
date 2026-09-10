## ADDED Requirements

### Requirement: Portable bounded discovery

SafetyFirst MUST provide an explicit read-only discovery procedure without Claude injection syntax in its canonical entrypoint.
Each probe MUST have a five-second timeout and a 1024-byte output limit.
The agent MUST record unknown state when the available tool cannot enforce those limits.

#### Scenario: A portable harness can bound shell commands

- **WHEN** the harness provides a bounded shell command tool
- **THEN** the agent invokes the shared Python probe helper once
- **AND** the helper checks `PATH` and invokes the resolved executable with `--version` without a shell

#### Scenario: Bounded discovery is unavailable

- **WHEN** the command tool, Python runtime, helper, or required process boundary is unavailable
- **THEN** the agent records unknown guard state without running a probe
- **AND** the shared guard constraints still apply

### Requirement: Evidence states remain distinct

SafetyFirst MUST distinguish executable presence, version evidence, and active guard enforcement.
A failed, denied, timed-out, truncated, empty, or unavailable result MUST NOT establish an observation.
Literal command text MUST NOT count as executed discovery.
The helper MUST serialize actual process status separately from escaped child output in one complete JSON record.
Child output MUST NOT establish its own process status, even when it contains success markers or fake JSON records.

#### Scenario: Lookup establishes absence from the current path

- **WHEN** a complete helper record reports top-level `lookup: absent_from_path`
- **THEN** the agent records the executable as absent from the current `PATH`
- **AND** it does not claim that the package is uninstalled

#### Scenario: The version probe fails

- **WHEN** the lookup succeeds but the version probe fails
- **THEN** the agent preserves the presence evidence and records an unknown version
- **AND** it does not claim active guard enforcement

#### Scenario: A probe is denied

- **WHEN** the harness denies a discovery probe
- **THEN** the agent records unknown evidence and does not retry that probe

#### Scenario: A failed executable prints a success marker

- **WHEN** the version executable prints a success marker or a fake successful JSON record before a failed exit
- **THEN** the helper records the actual failed exit outside the escaped payload
- **AND** the version remains unknown

#### Scenario: A descendant retains output pipes

- **WHEN** the executable exits but a descendant retains its output pipes and ignores normal termination
- **THEN** the helper forcibly terminates its process group within the discovery deadline
- **AND** the version remains unknown

### Requirement: Claude uses a complete replacement entrypoint

The Claude variant MUST use explicit `mode: replace` and retain injection inside its `SKILL.md` body.
Each injection probe MUST use the same time and output bounds as portable discovery.
Missing probe dependencies MUST produce unknown evidence without installation.
Claude's invocation MUST bound lookup and runtime startup through an outer timeout without an unbounded fallback.

#### Scenario: Claude assembles the skill

- **WHEN** Rune assembles SafetyFirst for Claude
- **THEN** one resolved entrypoint contains one bounded helper injection command
- **AND** it omits the canonical manual probe procedure and the consumed `mode` field

#### Scenario: Injection output is incomplete

- **WHEN** output lacks a complete helper envelope or remains literal injection text
- **THEN** the agent records unknown evidence

### Requirement: Shared policy remains complete

Both entrypoints MUST reference the same shared workflow at its assembled relative path.
The extracted non-discovery policy MUST remain unchanged by this change.
The assembled bundle MUST contain that companion and MUST exclude provider qualifier folders.
The Claude source links MUST resolve through an alias to the canonical companion without a copied policy body.

#### Scenario: Source lint resolves the variant links

- **WHEN** source lint checks the Claude entrypoint
- **THEN** `claude/Workflow.md` resolves to `../Workflow.md`
- **AND** assembly still emits one regular shared companion for each provider

#### Scenario: Codex assembles the portable bundle

- **WHEN** Rune assembles SafetyFirst for Codex
- **THEN** its entrypoint contains no injection commands
- **AND** its workflow link resolves to the unchanged shared companion

#### Scenario: The companion is missing

- **WHEN** assembly produces an entrypoint without its referenced shared companion
- **THEN** the content acceptance check fails

#### Scenario: Append retains two discovery procedures

- **WHEN** a Claude variant appends its changed discovery procedure to the canonical procedure
- **THEN** the content acceptance check fails
