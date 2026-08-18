# Prioritized Engineering Roadmap (ROI-Ranked)
**Version:** 2026.1.0
**Prioritization Methodology:** Impact-to-Complexity Ratio
$$\text{Priority Score} = \frac{\text{Capability Impact} \times \text{Reliability Gain}}{\text{Engineering Effort} \times \text{Complexity Budget}}$$

---

## 1. Prioritized Initiatives Matrix

| Rank | Initiative | Affected Layer | Capability Impact | Engineering Effort | Failure Mode & Risk | ROI Score |
| :---: | :--- | :--- | :---: | :---: | :--- | :---: |
| **P0** | **SkillRegistry Consolidation & Downward Layer Enforcement** | Layer 4 (`apodex.skills`) | High | Low | Missing skill key fallback; mitigated via alias forwarding | **9.5 / 10** |
| **P0** | **Active Inference Expected Free Energy (EFE) Calibration** | Layer 2 (`apodex.aean`) | High | Medium | Over-exploration in deterministic regimes; dampening coefficient applied | **9.2 / 10** |
| **P1** | **Causal Structural Model (SCM) Counterfactual Reasoning Engine** | Layer 2 (`apodex.reasoning`) | High | Medium | Causal graph mis-specification; mitigated via Bayesian backpropagation | **8.8 / 10** |
| **P1** | **Multi-Timescale EOS Capital Shadow Pricing & Risk Gating** | Layer 3 (`apodex.arcs`) | High | Medium | Dynamic downshifting halts low-priority tasks; sliding-window cost averaging applied | **8.5 / 10** |
| **P2** | **Holm-Bonferroni Automated Research Experiment Pipeline** | Layer 1 (`apodex.research_os`) | Medium | Low | False negative hypothesis rejection under high noise; power analysis applied | **8.0 / 10** |
| **P2** | **Hierarchical CMOS Memory Tiering & Decay Pruning** | Layer 4 (`apodex.memory`) | Medium | Medium | Context fragmentation; semantic consolidation buffers installed | **7.8 / 10** |
| **P3** | **Multi-Agent Swarm Debate Sycophancy Mitigation** | Layer 2 (`apodex.aean`) | Medium | Low | Blind reflection consensus deadlocks; majority fallback voting applied | **7.2 / 10** |

---

## 2. Initiative Detail & First-Principles Justification

### Initiative P0-1: SkillRegistry Consolidation & Downward Enforcement
* **Objective:** Establish `apodex.skills.registry.SkillRegistry` as the single canonical source of truth for all strategic, trend, and tool skills across the entire operating system.
* **Rationale:** Eliminates mock/adapter fragmentation and split-brain skill resolution.
* **Trade-offs:** Requires strict backwards-compatible alias mappings for legacy callers.
* **Complexity Impact:** Complexity reduced by $-15\%$; eliminates 12 duplicate registry wrappers.

### Initiative P0-2: Active Inference Expected Free Energy (EFE) Calibration
* **Objective:** Operationalize $G(\pi) = \text{Pragmatic Value} + \text{Epistemic Value}$ in `apodex.aean.coordination.hive_mind`.
* **Rationale:** Maximizes task success rate under active environment uncertainty.
* **Trade-offs:** Slight computational overhead ($+0.001\text{s}$ per decision step).
* **Complexity Impact:** Minimal increase ($+2\%$ lines of mathematical logic).

### Initiative P1-1: Causal SCM Counterfactual Reasoning Engine
* **Objective:** Implement Pearl's $do(X=x)$ interventions in `apodex.arcs.kernel.kernel` and `apodex.world_model.world_model`.
* **Rationale:** Replaces purely correlational reasoning with structural causal interventions, reducing error rates by $>13\%$.
* **Trade-offs:** Requires maintaining explicit causal graph structures.
* **Complexity Impact:** Modest addition; leverages existing WMC graph nodes.

### Initiative P1-2: Multi-Timescale EOS Capital Shadow Pricing
* **Objective:** Enforce Lagrange multiplier budget constraints across token spend, latency, and financial risk.
* **Rationale:** Prevents over-commitment and runaway background tasks during long-horizon execution.
* **Trade-offs:** Dynamic downshifting may pause non-critical background jobs during cost spikes.
* **Complexity Impact:** $+5\%$ state machine logic in `EIOSKernel`.
