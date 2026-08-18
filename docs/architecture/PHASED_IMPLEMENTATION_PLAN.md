# Phased Implementation Plan and Evaluation Criteria
**Version:** 2026.1.0
**Implementation Methodology:** Incremental, Non-Breaking Controlled Transitions

---

## 1. Phased Roadmap Milestones

```
+---------------------------------------------------------------------------------+
| Phase 1: Architectural Baseline & Standardized Layer Boundaries               |
| Target: Establish 4-Layer Taxonomy & Deprecate Duplicate Registries           |
+---------------------------------------------------------------------------------+
                                         |
                                         v
+---------------------------------------------------------------------------------+
| Phase 2: Active Inference & Causal SCM Runtime Operationalization             |
| Target: Deploy EFE Minimization & Pearl do-calculus Engine across AEAN        |
+---------------------------------------------------------------------------------+
                                         |
                                         v
+---------------------------------------------------------------------------------+
| Phase 3: Multi-Timescale EOS Capital Shadow Pricing & Governance               |
| Target: Integrate Lagrange Shadow Price Allocation & Budget Downshifting       |
+---------------------------------------------------------------------------------+
                                         |
                                         v
+---------------------------------------------------------------------------------+
| Phase 4: Automated Research OS & Statistical Continuous Evolution              |
| Target: Activate Holm-Bonferroni Trial Execution & Provenance Tracing          |
+---------------------------------------------------------------------------------+
```

---

## 2. Detailed Phase Specifications & Evaluation Criteria

### Phase 1: Architectural Baseline & Layer Boundaries
* **Deliverables:**
  - Standardized 4-Layer taxonomy specifications.
  - Consolidated `SkillRegistry` with backwards-compatible alias forwarders.
  - Cleaned import hierarchy validated by `scripts/validate_dependencies.py`.
* **Objective Evaluation Criteria:**
  - $100\%$ pass rate across all 397+ tests (`PYTHONPATH=.:AgentHarness python3 -m pytest`).
  - Zero circular import errors and zero Core-to-Adapter dependency violations.
  - Maximum dependency depth $\le 6$.

### Phase 2: Active Inference & Causal SCM Operationalization
* **Deliverables:**
  - Active Inference Expected Free Energy (EFE) calculator integrated into `HiveMindCoordinator`.
  - Causal Structural Model (SCM) $do(X=x)$ counterfactual engine in `EIOSKernel`.
* **Objective Evaluation Criteria:**
  - EFE KL-divergence calibration accuracy improved by $\ge 0.30$.
  - Causal budget overestimation error reduced by $\ge 10\%$.
  - Execution loop latency remains under $0.005\text{ seconds}$.

### Phase 3: Multi-Timescale EOS Shadow Pricing & Governance
* **Deliverables:**
  - Lagrange shadow price capital optimization in `EIOSKernel`.
  - Dynamic budget downshifting and halting triggers in `SkillRunner`.
* **Objective Evaluation Criteria:**
  - Zero budget overflow events under adversarial high-cost scenarios.
  - Automatic downshifting to lower cost tiers upon reaching $80\%$ budget threshold.

### Phase 4: Automated Research OS & Continuous Evolution
* **Deliverables:**
  - Research ingestion pipeline supporting 200+ paper corpus.
  - Automated hypothesis formulation, power calculation, and Holm-Bonferroni correction.
* **Objective Evaluation Criteria:**
  - Rejection of $100\%$ false-positive improvement proposals.
  - End-to-end lineage provenance logged for every runtime code modification.
