# PHASED IMPLEMENTATION PLAN & EVALUATION CRITERIA

---

## 1. Rollout Strategy & Implementation Principles

To transition the current codebase into the unified 4-layer Cognitive Operating System without destabilizing existing functionality or breaking test suites, implementation follows a strict 5-phase progressive rollout.

Each phase is gated by **Objective Evaluation Criteria** and requires 100% test pass rates across unit, integration, and performance benchmarks.

---

## 2. Five-Phase Implementation Roadmap

```
+-----------------------------------------------------------------------------------+
| PHASE 1: LAYER BOUNDARY ENFORCEMENT & LEGACY ADAPTER CLEANUP                      |
| Goal: Eliminate capability duplication and establish strict layer import boundaries. |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
| PHASE 2: PLATFORM LAYER (L4) HARDENING                                            |
| Goal: Productionize CMOS Ebbinghaus memory, Pearl SCM counterfactual checks, sandbox|
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
| PHASE 3: COGNITIVE INTELLIGENCE LAYER (L3) EVOLUTION                              |
| Goal: Deploy Graph-of-Thought planning and Bayesian Nash swarm debate.            |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
| PHASE 4: EXECUTION & ORCHESTRATION LAYER (L2) INTEGRATION                         |
| Goal: Operationalize Active Inference EFE routing and 13 business loops.          |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
| PHASE 5: RESEARCH OS LAYER (L1) & CLOSED-LOOP FLYWHEEL                            |
| Goal: Connect Welch's t-test hypothesis promotion engine for self-improvement.    |
+-----------------------------------------------------------------------------------+
```

---

## 3. Phase Specifications & Quantitative Acceptance Thresholds

### Phase 1: Layer Boundary Enforcement & Legacy Adapter Cleanup
* **Scope**: Audit all package imports across `apodex/` and `AgentHarness`. Redirect legacy adapters to canonical Layer 1–4 modules.
* **Deliverables**: Updated import structure, capability ownership mapping.
* **Quantitative Acceptance Thresholds**:
  * $0$ direct cross-layer dependency violations.
  * $100\%$ pass rate across all existing unit tests ($390+$ tests).

### Phase 2: Platform Layer (Layer 4) Hardening
* **Scope**: Finalize `CMOSMemoryEngine` exponential decay ($S = e^{-t/\tau}$) and `CausalInterventionEngine` Pearl $do(X)$ checks.
* **Deliverables**: Hardened memory persistence and pre-execution safety filters.
* **Quantitative Acceptance Thresholds**:
  * $\ge 50.0\%$ reduction in working context memory tokens.
  * $\le 1.0\%$ false-positive abortion rate on non-destructive tool calls.
  * Zero memory leakage or unhandled database exceptions.

### Phase 3: Cognitive Intelligence Layer (Layer 3) Evolution
* **Scope**: Implement `GraphOfThoughtEngine` node branching/merging and `SwarmCoordinationEngine` Bayesian equilibrium clearing.
* **Deliverables**: Multi-agent GoT planner and sycophancy-mitigating debate engine.
* **Quantitative Acceptance Thresholds**:
  * $\ge 25.0\%$ reduction in agent sycophancy bias under conflicting initial prompts.
  * Task execution success rate improvement on multi-step reasoning benchmarks ($\ge +15.0\%$).

### Phase 4: Execution & Orchestration Layer (Layer 2) Integration
* **Scope**: Connect `EIOSKernel` active inference $EFE$ calculation ($\text{Pragmatic Value} + \text{Epistemic Gain}$) to 13 EOS business loops.
* **Deliverables**: Active inference strategic controller and Advanced Kelly capital allocator.
* **Quantitative Acceptance Thresholds**:
  * Active inference $KL$-divergence calibration accuracy boost ($\ge +30.0\%$).
  * Capital allocation protection against Simulated Portfolio Drawdown ($\le 5.0\%$ max drawdown).

### Phase 5: Research OS Layer (Layer 1) & Self-Improvement Flywheel
* **Scope**: Connect `ResearchToSystemBridge` and `StatisticalValidationEngine` to continuously monitor execution telemetry, formulate hypotheses, run experiments, and promote parameter changes.
* **Deliverables**: Autonomous self-improvement loop with automated rollback.
* **Quantitative Acceptance Thresholds**:
  * Statistical significance threshold strictly enforced ($p < 0.01$).
  * Deflated Sharpe Ratio $DSR \ge 1.0$ for parameter adjustments.
  * Zero unauthorized code promotions.
