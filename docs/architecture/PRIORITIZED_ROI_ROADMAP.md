# Prioritized ROI Engineering Roadmap

## 1. Return on Engineering Effort (ROI) Ranking Framework

To maximize system intelligence, reliability, performance, and maintainability, engineering enhancements are evaluated and ranked according to expected Return on Engineering Effort:

$$\text{ROI} = \frac{\text{Capability Gain} \times \text{Reliability Impact}}{\text{Implementation Complexity} \times \text{Technical Debt Risk}}$$

---

## 2. Priority Matrix

| Priority | Capability / Enhancement Area | Subsystem Layer | Expected ROI | Complexity | Primary Benefit |
|---|---|---|---|---|---|
| **P0** | **Active Inference EFE Sensing Engine** | Layer 2 (EIOS) | **9.5 / 10** | Medium | Directs agent exploration to high-uncertainty business opportunities with minimal compute waste. |
| **P0** | **Statistical Validation & Boundary Protection** | Layer 1 (Research OS) | **9.2 / 10** | Low | Ensures mathematical rigor, prevents zero-division/NaN errors in hypothesis SPRT testing. |
| **P0** | **CMOS Hierarchical Memory & Decay** | Layer 3 (AEAN) | **9.0 / 10** | Medium | Improves context window efficiency (+50%) via Ebbinghaus memory decay and re-activation triggers. |
| **P1** | **Island MAP-Elites Genetic Workflows** | Layer 3 (AEAN) | **8.6 / 10** | Medium | Maintains diverse high-performing prompt/code candidates across isolated evolution islands. |
| **P1** | **Do-Calculus Causal Graph Planner** | Layer 4 (APODEX) | **8.4 / 10** | High | Prevents non-causal confounding errors in long-horizon autonomous software engineering tasks. |
| **P2** | **Non-Gaussian Hawkes Self-Improvement** | Layer 3 (AEAN) | **7.8 / 10** | High | Optimizes prompt and code rewrite trajectory distributions based on historical cluster bursts. |
| **P2** | **Tiered Governance & Credit Halt** | Layer 4 (APODEX) | **7.5 / 10** | Low | Halts risky or out-of-budget autonomous executions before catastrophic resource depletion. |

---

## 3. In-Depth Technical Rationale & Trade-off Analysis

### Priority P0: Active Inference EFE Sensing Engine
- **Architectural Rationale**: Traditional rule-based anomaly detection lacks epistemic uncertainty estimation. Active Inference balances exploration (epistemic value) and exploitation (pragmatic value).
- **Trade-offs**: Requires real-time calculation of KL-divergence over beliefs, adding minor CPU computational overhead per cycle.
- **Failure Modes & Mitigation**: Unbounded prior beliefs could lead to infinite exploration loops; mitigated by clamping EFE score variance thresholds.

### Priority P0: Statistical Validation & Probability Clamping
- **Architectural Rationale**: Floating point underflow/overflow in standard normal PPF calculations causes silent failures in scientific literature evaluations.
- **Trade-offs**: None; clamping probability inputs to $[10^{-15}, 1 - 10^{-15}]$ guarantees mathematical safety at near-zero runtime cost.

### Priority P1: Island MAP-Elites Genetic Workflows
- **Architectural Rationale**: Prevents premature convergence in automated prompt and skill optimization by isolating candidate populations across distinct feature islands.
- **Trade-offs**: Higher memory footprint to store multi-island population archives.
- **Failure Modes & Mitigation**: Stagnant islands; mitigated by periodic cross-island migration gates controlled by HiveMind consensus.

---

## 4. Complexity Budget & Resource Accounting

| Phase | Developer Months | Compute Overhead | Memory Footprint Impact | Target Subsystems |
|---|---|---|---|---|
| **Phase 1: Foundation Cleanliness** | 0.5 | < 1% | None | All Layers |
| **Phase 2: Sensing & Memory** | 1.0 | + 3% | + 15% (CMOS Cache) | Layer 2 & Layer 3 |
| **Phase 3: Causal Execution** | 1.5 | + 5% | + 10% (Causal Graph) | Layer 3 & Layer 4 |
| **Phase 4: Autonomous Flywheel** | 2.0 | + 8% | + 20% (MAP-Elites Archives) | Layer 1, 3 & 4 |
