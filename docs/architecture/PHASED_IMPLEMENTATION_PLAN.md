# Phased Implementation Plan & Evaluation Criteria

## 1. Overview & Phased Rollout Roadmap

The transition of the Cognitive Operating System into a unified, 4-layer architecture follows a strict four-phase execution plan. Each phase incorporates objective evaluation criteria, strict complexity budgets, and validation gates to prevent regression.

```
+---------------------------------------------------------------------------------+
| PHASE 1: SUB-SYSTEM UNIFICATION & BOUNDARY ISOLATION (Sprint 1)                 |
| - Layer 1-4 boundary definition                                                 |
| - Cross-layer bridge integration (ResearchToSystemBridge)                       |
+---------------------------------------------------------------------------------+
                                       |
                                       v
+---------------------------------------------------------------------------------+
| PHASE 2: ACTIVE INFERENCE & GO-T REASONING HARDENING (Sprint 2)                 |
| - Expected Free Energy (EFE) minimization engine                                |
| - Graph-of-Thought (GoT) planning & Bayesian swarm debate                       |
+---------------------------------------------------------------------------------+
                                       |
                                       v
+---------------------------------------------------------------------------------+
| PHASE 3: PLATFORM EXECUTION & WORLD MODEL SYNCHRONIZATION (Sprint 3)            |
| - Skill registry harmonization (60+ production skills)                          |
| - Causal Do-Calculus & WorldModel belief update synchronization                |
+---------------------------------------------------------------------------------+
                                       |
                                       v
+---------------------------------------------------------------------------------+
| PHASE 4: CONTINUOUS AUTONOMOUS EVALUATION & FLYWHEEL EVOLUTION (Sprint 4)       |
| - Automated regression benchmarking & failure injection tests                  |
| - DSPy / MIPROv2 self-improving prompt & skill optimization                     |
+---------------------------------------------------------------------------------+
```

---

## 2. Detailed Phase Breakdown & Objective Gates

### Phase 1: Subsystem Unification & Boundary Isolation
* **Primary Focus**: Establish strict 4-layer hierarchy and eliminate architectural duplication across Research OS, EIOS/EOS, AEAN, and APODEX.
* **Key Deliverables**:
  1. `docs/architecture/UNIFIED_COGNITIVE_ARCHITECTURE_SPEC.md`
  2. `docs/architecture/UNIFIED_DEPENDENCY_GRAPH.md`
  3. Integration bridge `ResearchToSystemBridge` in `apodex/ai_eos/research/integration.py`.
* **Objective Evaluation Criteria**:
  * Zero circular dependencies in static import graphs.
  * 100% test collection and pass rate across existing unit/integration suites.

### Phase 2: Active Inference & Graph-of-Thought Hardening
* **Primary Focus**: Implement Expected Free Energy active sensing and multi-agent Graph-of-Thought reasoning.
* **Key Deliverables**:
  1. Active Inference EFE engine in `apodex/arcs/kernel/kernel.py`.
  2. Game-theoretic Bayesian Nash equilibrium clearing in `apodex/aean/coordination/hive_mind.py`.
* **Objective Evaluation Criteria**:
  * Statistical significance ($p < 0.05$) on hypothesis promotion tests.
  * $\ge 30\%$ reduction in planning uncertainty calibration error.

### Phase 3: Platform Execution & World Model Synchronization
* **Primary Focus**: Synchronize APODEX Skill Registry and Causal WorldModel state tracking.
* **Key Deliverables**:
  1. Pre-populated Skill Registry in `apodex/skills/registry.py` with 60 operational skills.
  2. Causal Do-Calculus intervention engine in `apodex/world_model/world_model.py`.
* **Objective Evaluation Criteria**:
  * 100% resolution rate for legacy skill aliases.
  * Zero failure during counterfactual policy simulation under stress injection.

### Phase 4: Continuous Autonomous Evaluation & Flywheel Evolution
* **Primary Focus**: Automated benchmarking, failure injection, and self-improving evolution.
* **Key Deliverables**:
  1. End-to-end cross-layer integration suite `tests/integration/test_unified_4layer_integration.py`.
  2. Dedicated architecture verification tools.
* **Objective Evaluation Criteria**:
  * 100% pass rate across all unit, integration, and robustness benchmarks (`pytest`).
  * Welch's t-test statistical validation ($p < 0.01$) confirming performance gains over baseline.

---

## 3. Complexity Budget & Resource Accounting

| Subsystem Layer | Maximum LOC Overhead | Memory Footprint Budget | Target Execution Latency |
| :--- | :---: | :---: | :---: |
| **Layer 1: Research OS** | $< 3,500$ LOC | $< 250$ MB | $< 100$ ms / literature query |
| **Layer 2: EIOS / EOS** | $< 5,000$ LOC | $< 500$ MB | $< 50$ ms / EFE state update |
| **Layer 3: AEAN** | $< 6,000$ LOC | $< 1.0$ GB | $< 200$ ms / GoT step |
| **Layer 4: APODEX** | $< 8,000$ LOC | $< 750$ MB | $< 20$ ms / skill invocation |
