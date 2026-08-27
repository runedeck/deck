# Context Economy Design

## Approach

Constitution first, rewrite second, gates third. The decision records state the norms with their evidence. The rules rewrite executes the norms. The gates keep them, warning-first per the Severity Ratchet. The alternative (rewrite rules ad hoc, without decision records or gates) loses the rationale and regresses on the next adoption.

## Evidence

- Anthropic, context engineering for Claude 5 models: over 80 percent of the Claude Code system prompt removed, no measured loss. Judgment over hard rules. Progressive disclosure. One statement per instruction. Interfaces over examples.
- Zheng et al., EMNLP 2024 Findings (arXiv 2311.10054): 162 personas, 4 model families, 2410 questions. Personas do not improve performance over the no-persona control.
- Anthropic prompt guidance: state the wanted behavior. Negative phrasing can prime the behavior it names.
- Anthropic power-user guidance: verification beats instruction. Give the model a way to check its own output.
- Deck audit at main `34b08e54`: 2232 words across sixteen rules (worst: VerifyClaims 393, UseEfficientCLI 312, Deslop 256, UseSimplifiedTechnicalEnglish 255, RuneShell 222). Twenty negative constructions. Zero persona framings. 101 duplicated sentences across runes, concentrated in the scanner skill family.

## Structure

- Decision records own the norms: CORE-0013 (every instruction earns its tokens, one home per fact), CORE-0014 (no performance personas, and voice for outward text carries no capability framing), CORE-0015 (state the wanted behavior, with negation reserved for true prohibitions).
- The layer map assigns each fact one home: enforcement in hooks and CI, knowledge in skills, constraints in rules, identity in the repository brief, transient state in memory. A fact in two layers is a defect.
- The compatibility table judges forge-core CORE-0001 to CORE-0012 and ARCH-0001, ARCH-0004, ARCH-0011, ARCH-0014 against the norms. The deck records divergence in its own decisions and never edits forge-core.
- Gates: a rule-budget check (prek plus CI), a persona and negation Vale style, and a duplicated-sentence sweep. Each ships at warning severity with a declared-debt baseline and a recorded flip condition.
- Adversarial review replaces the council pattern. A consensus panel averages independent guesses and rewards fluent agreement. An adversarial reviewer attacks one claim against the source, so a plausible but wrong finding dies on evidence. The AdversarialReviewer agent owns refutation. The HarnessCouncil skill retires on the DECK-0007 path, and cross-provider fan-out stays available for research questions that want breadth, never as a gate.

## Risks

- Compression can drop a real constraint. Guard: the rewrite moves content to a skill before it deletes content, and every fact, hedge, and scope qualifier survives per the STE guard.
- A one-sentence rule can lose the example that made it unambiguous. Guard: the shape allows one example pair when the sentence alone misleads.
- The duplication sweep can flag deliberate shared boilerplate (the scanner family's safety lines). Guard: the baseline declares them with reasons, like the zizmor registry.
- Bench evidence may be thin while the bench legibility repair (artifact-review Phase 2) is open. Guard: the rewrite ships behind one before-and-after bench on a single rule. The batch follows the bench.
