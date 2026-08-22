# Unified Cognitive Operating System: Prioritized ROI Roadmap

## Executive Summary

This roadmap ranks architectural and engineering initiatives for the Unified Cognitive Operating System (**Research OS**, **AEAN**, **EIOS/EOS**, **APODEX**) based on expected Return on Engineering Investment (**ROI = Capability Gain / Engineering Effort**).

Rather than pursuing speculative feature bloat, every task in this roadmap targets clear, measurable improvements in **Intelligence**, **Reliability**, **Performance**, **Scalability**, or **Maintainability**.

---

## 1. ROI Ranking Matrix

| Rank | Initiative Name | Target Layer | Expected Impact | Eng Effort (Story Points) | Target Metric Improvement | ROI Score |
| :---: | :--- | :---: | :--- | :---: | :--- | :---: |
| **1** | **EFE Active Inference Loop Unification** | AEAN (L2) | +34.6% Decision Precision | 13 | EFE KL-Divergence Calibration ($< 0.05$) | **9.5** |
| **2** | **Pearl Do-Calculus Causal Gating** | EIOS/EOS (L3) | -13.2% Budget Overestimation | 21 | Intervention Error Reduction | **9.1** |
| **3** | **Multi-Tier Ebbinghaus Memory Synthesis** | AEAN (L2) | +50.0% Context Efficiency | 13 | Context Retention vs Token Consumption | **8.8** |
| **4** | **Sycophancy-Proof Swarm Deliberation** | AEAN (L2) | -25.0% Blind Compliance | 8 | Adversarial Debate Consensus Robustness | **8.6** |
| **5** | **Advanced Kelly Portfolio Risk Allocation** | EIOS/EOS (L3) | Zero Drawdown Catastrophes | 13 | Risk-Adjusted Capital Growth Rate | **8.4** |
| **6** | **Self-Correcting Genetic Program Synthesis**| APODEX (L4) | +42.0% Code Generation Success | 34 | Automated Test Pass Rate | **8.0** |
| **7** | **Continuous Automated Empirical Ingestion** | Research OS (L1) | 100% Corpus Traceability | 21 | Paper-to-Code Mapping Coverage | **7.8** |

---

## 2. Phase-by-Phase Execution Roadmap

### Phase 1: Cognitive Core Hardening & Deduplication (Weeks 1-4)
- **Objective:** Consolidate memory, planning, and active inference into AEAN (Layer 2). Eliminate legacy adapter duplicate definitions.
- **Key Deliverables:**
  1. Standardize `CognitiveBrain` on Active Inference with Expected Free Energy formulation.
  2. Implement Ebbinghaus memory decay $R(t) = \exp(-t/S)$ across episodic and semantic memory.
  3. Enforce single-source ownership for all 60 core skills in `SkillRegistry`.
- **Target Metrics:**
  - 100% pass rate on unit, integration, and flywheel test suites.
  - Zero duplicate class declarations across `agent_harness/` and `apodex/`.

### Phase 2: Causal Orchestration & Risk Gating (Weeks 5-8)
- **Objective:** Operationalize Structural Causal Models (SCMs) and fractional Kelly capital allocation in EIOS/EOS (Layer 3).
- **Key Deliverables:**
  1. Complete 14-Layer Computational Architecture engine (`fourteen_layer_engine.py`).
  2. Integrate Judea Pearl's do-calculus intervention operator $P(Y | do(X))$.
  3. Implement macroeconomic shock and decision fatigue metrics in portfolio sizing.
- **Target Metrics:**
  - Intervention error reduction by $\ge 12\%$.
  - Execution speed under 0.005s per causal evaluation.

### Phase 3: Autonomous Research & Empirical Ingestion (Weeks 9-12)
- **Objective:** Scale Research OS (Layer 1) to continuously ingest, validate, and hypothesis-test frontier AI papers.
- **Key Deliverables:**
  1. Expand bibliography to 300+ peer-reviewed and pre-print publications (`AI_EOS_RESEARCH_DB.yaml` + `ALPHA_ALGO_100_NEW_RESEARCH.yaml`).
  2. Implement automated Welch's t-test and Holm-Bonferroni statistical power verification engine.
  3. Dynamic principle extraction pipeline updating Layer 2 knowledge bases.
- **Target Metrics:**
  - Zero DOI or title duplications across research DB.
  - Automated hypothesis validation with statistical power $1 - \beta \ge 0.80$.

### Phase 4: Self-Improving Code Execution Engine (Weeks 13-16)
- **Objective:** Enhance APODEX (Layer 4) with genetic program synthesis and real-time execution telemetry.
- **Key Deliverables:**
  1. AST-level code rewriting and self-repair loops for automated software engineering.
  2. Resource-bounded sandbox runtime with memory delta ($\le 1.0$ MB) and execution latency ($\le 0.002$s) limits.
  3. End-to-end telemetry feedback loop reporting back to Layer 2/3.
- **Target Metrics:**
  - First-pass code generation success rate $\ge 90\%$.
  - 100% containment of unsafe or boundary-exceeding tool calls.

---

## 3. Resource Allocation & Complexity Budgeting

| Layer | Dedicated Engineering Resource Allocation | Maximum Latency Budget | Maximum Memory Delta |
| :--- | :---: | :---: | :---: |
| **Layer 1: Research OS** | 15% | 0.010 s | 2.5 MB |
| **Layer 2: AEAN** | 35% | 0.005 s | 1.5 MB |
| **Layer 3: EIOS / EOS** | 30% | 0.003 s | 1.0 MB |
| **Layer 4: APODEX** | 20% | 0.002 s | 0.8 MB |
