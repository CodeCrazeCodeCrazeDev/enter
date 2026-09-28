# Prioritized Engineering ROI Roadmap
**Document Version:** 2.0.0 (2026 Edition)
**Status:** Approved

---

## 1. Effort vs. Return Ranking Framework

Engineering effort is prioritized using Expected ROI:
$$\text{ROI} = \frac{\text{Capability Impact} \times \text{Reliability Multiplier}}{\text{Implementation Complexity (Person-Weeks)}}$$

### Summary Roadmap Table

| Priority Rank | Architectural Initiative | Target Layer | Expected Capability Return | Complexity | Trade-Offs & Risks | Primary Failure Mode |
|---|---|---|---|---|---|---|
| **P0 (1)** | **Cross-Layer Active Inference Bridge Integration** | L1 <-> L2 <-> L3 <-> L4 | **High (5x):** Seamless state hand-offs, zero lost context | **Low (1-2 wks):** Standardized Pydantic schemas | Requires strict schema maintenance across releases | Stale state propagation across layers |
| **P0 (2)** | **Hawkes Process AST Recursive Call Depth Guard** | L1 Research OS | **High (4x):** Eliminates non-deterministic stack overflow in code rewrite | **Low (1 wk):** AST tree visitor implementation | May reject deep recursive ASTs | False positive rejection of valid recursive functions |
| **P1 (3)** | **Island MAP-Elites Migration Gate with Instant Population Sorting** | L1 Research OS / L3 AEAN | **Medium-High (3.5x):** Prevents genetic algorithm population stagnation | **Medium (2 wks):** Population heap tracking | Higher CPU memory during evolution loops | Diversity loss if migration rates are tuned too high |
| **P1 (4)** | **Deflated Sharpe Ratio & Bonferroni Control Engine** | L1 Research OS | **High (4x):** Guarantees zero false statistical discovery | **Medium (2 wks):** Mathematical CDF approximation | Slightly reduces hypothesis throughput | Type II error (over-conservative rejection) |
| **P2 (5)** | **Clipped Trajectory Advantage SFT Preference Collector** | L3 AEAN / L4 APODEX | **Medium (3x):** High RLHF / DPO alignment sample efficiency | **Medium (3 wks):** Advantage trajectory clipping | Requires rich episode trajectory logging | Loss of gradient signal on off-policy clipped trajectories |
| **P2 (6)** | **Budget-Decayed Active Inference Task Dispatcher** | L2 EIOS / L3 AEAN | **Medium (2.5x):** Prevents run-away API token burn | **Medium (2 wks):** Dynamic EFE decay schedules | Tasks downshift quality under tight budgets | Execution stall under zero-budget conditions |

---

## 2. Failure Mode Diagnostics & Mitigation Strategies

### 2.1 Failure Mode: Active Inference Divergence
- **Diagnostic:** Free Energy $F(q, y)$ increases monotonically across 3 consecutive cycles.
- **Mitigation:** Trigger automated fall-back to prior stable belief parameters $\theta_{t-1}$ and reset observational noisy covariance matrix $\Sigma$.

### 2.2 Failure Mode: AST Recursive Stack Overflow
- **Diagnostic:** Automated code transformation proposal introduces unbounded self-referential calls.
- **Mitigation:** Enforce `CodeRewriteEngine.verify_proposal_ast()` Hawkes AST recursive depth limits before passing code proposals to execution sandbox.
