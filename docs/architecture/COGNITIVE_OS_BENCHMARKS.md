# Cognitive OS Phase 4 — Benchmark & Objective Metrics Definition

This document establishes the objective, quantitative metrics and rigorous acceptance criteria that govern every cognitive subsystem inside the unified Cognitive Operating System. No implementation is allowed to proceed without meeting these strict benchmarks.

---

## 1. Subsystem Performance Benchmarks & Acceptance Criteria

We define strict metrics to measure planning quality, reasoning correctness, memory persistence, coordination overhead, execution safety, and computational efficiency.

| Metric Domain | Targeted Subsystem | Defined Benchmark Metric | Exact Mathematical Formula / Evaluation Pattern | Acceptance Criteria |
| :--- | :--- | :--- | :--- | :--- |
| **Planning Quality** | Hierarchical HTN-MCTS Planner | Decomposition Efficiency & Plan Accuracy | $P_{\text{acc}} = \frac{\text{Successful primitive steps completed}}{\text{Total steps in generated plan}}$ | $P_{\text{acc}} \ge 90\%$ |
| **Reasoning Quality** | Causal SCM do-calculus Engine | Backdoor adjustment estimation error | $\text{MSE} = \frac{1}{N}\sum_{i=1}^N \left(P_{\text{sim}}(y | do(x)) - P_{\text{true}}(y | do(x))\right)^2$ | $\text{MSE} \le 0.05$ |
| **World Model Accuracy** | Unified Predictive Model | Bayesian Surprise index | $S_{\text{Bayes}} = \sum P(s | o) \log_2 \left(\frac{P(s | o)}{P(s)}\right)$ | $S_{\text{Bayes}} \le 0.15$ |
| **Memory Quality** | CMOS SQLite Retrieval | Context retrieval accuracy & Jaccard search | $J(A, B) = \frac{|A \cap B|}{|A \cup B|}$ | Match Latency $\le 2\text{ms}$; Precision $\ge 95\%$ |
| **Research Productivity** | Autonomous Research OS | Findings Reproducibility Index (RI) | $RI = w_{\text{stat}} \max(0, 1 - p_{\text{value}}) + w_{\text{effect}} E_s$ | $p_{\text{value}} < 0.05$ on $100\%$ of promoted claims |
| **Agent Coordination** | ConsensAgent Protocol | Disagreement decision entropy | $H = -\sum p_{ij} \log_2 p_{ij}$ | Turn count to consensus $\le 3$; $H \le 0.1$ |
| **Execution Reliability** | Long-horizon Controller DAG | Step failure recovery rate | $R_{\text{rec}} = \frac{\text{Trace edit repairs resolved}}{\text{Total run failures encountered}}$ | $R_{\text{rec}} \ge 95\%$ via EMG repair operators |
| **Self-Improvement Safety**| Suitability Scoring Gates | Multi-objective regression rate | $S(M) = w_q Q - w_t T - w_l L + w_s S_r$ | Quality gain $\ge 5\%$; zero safety regressions |
| **Resource Efficiency** | System-wide | Latency budget & Token-volume | Absolute CPU overhead per sub-agent transaction | Latency $\le 10\text{ms}$; Memory leakage $\le 0\text{ bytes}$ |

---

## 2. Regression Testing Protocols

Before any capability modification or prompt evolutionary sweep is promoted from the active experimental harness:
1. **Offline Benchmark Evaluation**: The candidate configuration is evaluated against 100 deterministic mock tasks.
2. **Shadow Run Evaluation**: The candidate is executed in "Shadow Mode" alongside production instances over 1,000 steps to record real-time latency and token volume metrics.
3. **Automated Rollback Verification**: If any single safety policy is violated, or if the Suitability Score is $< 1.05x$ the baseline, the transaction is rejected and the gateway triggers an automated rollback.
