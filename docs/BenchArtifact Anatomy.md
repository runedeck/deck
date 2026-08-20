# BenchArtifact Anatomy

How one artifact benchmark moves from a configuration file to a pull-request table. The diagrams record the system as built for the Simplified Technical English iteration-4 run (2026-08-19). Decision records: [DECK-0001](decisions/DECK-0001%20Artifact%20Benchmarking%20Skill.md), [DECK-0002](decisions/DECK-0002%20Benchmark%20Execution%20Ladder.md), [DECK-0003](decisions/DECK-0003%20Three-Metric%20Verdict%20and%20Cross-Vendor%20Judging.md).

## The execution ladder

Four setups, one method. Each rung buys more isolation and more models for more time. The manifest, assertions, checker, and verdict rule stay identical on every rung, so results stay comparable as you climb.

```mermaid
flowchart LR
    A["minimal<br/>current harness agents<br/>NativeBench.md<br/><i>no subprocesses, minutes</i>"]
    B["value / time<br/>claude -p and codex exec<br/>rune run when available<br/><i>2x2 grade-only, ~5 min</i>"]
    C["maximal<br/>cross-harness rune matrix<br/>clean state, canaries, blind judging<br/><i>hours, full verdict</i>"]
    D["runedeck/bench<br/>suites, registries, repeats<br/>custom judge dimensions<br/><i>future home</i>"]
    A -->|more isolation| B -->|more models| C -->|configs migrate| D
```

The absolutely minimal setup runs inside the current harness. The best value-for-time setup drives Claude and Codex directly. The maximal setup is the full matrix. The best evaluations will run from runedeck/bench.

## The pipeline

Every consumer reads files, never memory. Records freeze as they land: the manifest freezes per iteration, results never get overwritten, and each output feeds exactly one consumer.

```mermaid
flowchart LR
    CFG["bench.json<br/><i>one per artifact</i>"] --> RUN["run_benchmark.py<br/><i>frozen manifest</i>"]
    RUN -->|writes| RES["result.json + raw stdout<br/><i>one per run</i>"]
    RES --> GRADE["grade<br/><i>assertions + checker</i>"]
    RES --> JUDGE["judge<br/><i>blind pairs</i>"]
    GRADE --> AGG["aggregate<br/><i>matched pairs only</i>"]
    JUDGE --> AGG
    AGG --> HTML["report.html<br/><i>pair browser</i>"]
    AGG --> MD["benchmark.md<br/><i>PR table</i>"]
```

## Six models, four authentication mechanisms

Every lane ends in the `rune run` JSON envelope, but each harness authenticates differently. Keychain-backed authentication only works outside the agent sandbox, so the whole pipeline runs through one excluded wrapper command.

```mermaid
flowchart LR
    W["bench wrapper<br/><i>unsandboxed</i>"] --> R["rune run<br/><i>Seatbelt + clean state</i>"]
    R --> CL["claude -p<br/>opus, sonnet, grok"]
    R --> CX["codex exec<br/>sol"]
    R --> OC["opencode run<br/>lumo"]
    R --> AG["agy --print<br/>gemini"]
    CL -->|env token + local CA| P["CLIProxyAPI"]
    CX -->|own config| P
    OC -->|auth.json copied into clean state| OK1[" "]
    AG -->|keychain + OAuth token bridge| OK2[" "]
```

The baseline arm gets no artifact. Gemini's agy lane still fails on real-length prompts; the failure signature is recorded in the iteration-4 and iteration-5 records.

## One pair, three verdicts

Each case runs twice per model: identical prompt, files, and mode; only the artifact differs. Judging is blind and cross-vendor so no model grades its own vendor's output.

```mermaid
flowchart LR
    CASE["case + files<br/><i>frozen assertions</i>"] --> BA["baseline arm<br/><i>no artifact</i>"]
    CASE --> TA["treatment arm<br/><i>--system-prompt-file snapshot</i>"]
    BA --> RA["response A<br/><i>assertions, lint /100w</i>"]
    TA --> RB["response B<br/><i>assertions, lint /100w</i>"]
    RA -->|shuffled A/B| J["blind judge<br/><i>Sol judges five models,<br/>Opus judges Sol</i>"]
    RB -->|shuffled A/B| J
    J --> V["clarity - fluency - directness<br/><i>winner + reason per pair</i>"]
```

The verdict rule reads the three signals together: assertions must hold (meaning), checker density must fall (the claimed behavior), and blind preference must stay acceptable (prose). Iteration-4: true for Opus and Sonnet, neutral for Sol, inverted for Grok and Lumo.

## Where things live

```mermaid
flowchart LR
    DECK["runedeck/deck<br/>BenchArtifact skill + scripts<br/>report template, schemas<br/>STE skill, checker, rule<br/><i>the method and the artifact</i>"]
    CLI["runedeck/cli<br/>rune run: Seatbelt, clean state<br/>auth bridges per provider<br/>final-message extraction<br/><i>the execution layer</i>"]
    WS["~/Data/Benchmarks<br/>bench wrapper + bench.json<br/>manifests, route registries<br/>immutable iteration records<br/><i>the working layer, never in git</i>"]
    DECK -->|shells out| CLI -->|writes into| WS
```

When runedeck/bench exists, the workspace wrapper and its configurations move there. The deck keeps the method definition; the cli keeps execution.
