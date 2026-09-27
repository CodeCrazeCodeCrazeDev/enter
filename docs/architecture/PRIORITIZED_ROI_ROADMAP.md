# Prioritized ROI Engineering Roadmap

## Overview & Evaluation Framework
Engineering effort is prioritized based on **Expected Return on Investment (ROI)**, defined as:

$$\text{ROI} = \frac{\text{Capability Gain} \times \text{Reliability Improvement}}{\text{Engineering Effort} \times \text{System Risk}}$$

---

## Roadmap Phases

### Phase 1: High ROI (Months 1–3) — Core Integration & Closed-Loop Active Inference
* **1.1 Cross-Layer Active Inference State Handoff Engine (`ResearchToSystemBridge`)**
  - **Effort:** Low (1–2 weeks)
  - **ROI Score:** 9.8 / 10
  - **Impact:** Eliminates isolated manual data transfers between Research OS hypotheses and EIOS/EOS execution pipelines.
* **1.2 Deprecation Warning Removal & Pydantic V2 Standardization**
  - **Effort:** Low (1 week)
  - **ROI Score:** 9.5 / 10
  - **Impact:** Zero warnings during test runs, full compatibility with Python 3.12+ datetime UTC and Pydantic V2 ConfigDict.
* **1.3 Unified Architectural Specification & Verification Suite**
  - **Effort:** Low (1 week)
  - **ROI Score:** 9.2 / 10
  - **Impact:** Formalizes system boundaries and prevents architectural regression across future PRs.

---

### Phase 2: Medium-High ROI (Months 4–6) — Autonomous Self-Improvement & Multi-Agent Swarms
* **2.1 Island MAP-Elites Genetic Workflow Optimizer Acceleration**
  - **Effort:** Medium (3–4 weeks)
  - **ROI Score:** 8.7 / 10
  - **Impact:** Enables $5\times$ faster agent prompt and strategy evolution across HiveMind roles.
* **2.2 Non-Gaussian Hawkes AST Code Rewrite Stability**
  - **Effort:** Medium (2–3 weeks)
  - **ROI Score:** 8.4 / 10
  - **Impact:** Guarantees zero infinite recursive call loops during autonomous agent code rewrite proposals.

---

### Phase 3: Medium ROI (Months 7–9) — Institutional World Modeling & Continuous Learning
* **3.1 Dynamic Causal Node Discovery in APODEX WorldModel**
  - **Effort:** High (6 weeks)
  - **ROI Score:** 7.9 / 10
  - **Impact:** Automatically discovers hidden structural causal variables from environment trajectories.
* **3.2 CMOS Multi-Tier Memory Index Compression**
  - **Effort:** Medium (3 weeks)
  - **ROI Score:** 7.6 / 10
  - **Impact:** Reduces memory retrieval latency by $60\%$ for long-horizon task execution.
