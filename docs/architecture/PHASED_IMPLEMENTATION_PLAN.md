# Phased Implementation Plan with Evaluation Criteria

**Author:** Jules (Autonomous System Engineer)
**Status:** Approved Architecture Standard

---

## Executive Summary

This document establishes the phased implementation roadmap for executing the **Unified 4-Layer Cognitive Operating System**.

Each phase defines objective quantitative evaluation criteria, target test pass metrics, capability benchmarks, and non-bypassable verification gates.

---

## Phase Overview & Milestones

```
+-------------------+     +-------------------+     +-------------------+     +-------------------+
| PHASE 1: SUBSTRATE| --> | PHASE 2: ACTIVE   | --> | PHASE 3: CAUSAL   | --> | PHASE 4: CONTINUOUS|
|  CONSOLIDATION    |     | INFERENCE ENGINE  |     |   BELIEF & GRC    |     |   EVOLUTION FLYWHEEL
+-------------------+     +-------------------+     +-------------------+     +-------------------+
  (Weeks 1 - 2)             (Weeks 3 - 4)             (Weeks 5 - 6)             (Weeks 7 - 8)
```

---

## Phase 1: Substrate Alignment & Single Authority Consolidation (Weeks 1–2)

### Core Deliverables
1. Consolidate Research OS, EIOS, EOS, AEAN, and APODEX into the 4-layer functional hierarchy.
2. Deprecate overlapping standalone memory and reasoning modules in favor of Layer 4 `AdvancedMemoryEngine` and Layer 3 `HiveMind`.
3. Establish backward-compatibility adapters in `agent_harness/` to preserve legacy test suit integration.

### Objective Evaluation Criteria & Benchmarks
- **Test Pass Rate:** 100% pass rate across all 397+ repository unit and integration tests.
- **Architectural Duplication:** Zero duplicate memory or planner registries verified via static AST audit scripts.
- **Backward Compatibility:** 100% backward compatibility maintained for legacy `agent_harness` imports.

---

## Phase 2: Active Inference & Expected Free Energy Routing (Weeks 3–4)

### Core Deliverables
1. Integrate Karl Friston's Expected Free Energy ($ G $) minimization into Layer 2 Active Inference Planner and Layer 3 HiveMind Token Bidding.
2. Implement dynamic task routing in `LearnableRoutingGateDispatcher` with epistemic curiosity and pragmatic value weighting.
3. Integrate second-price compute token arbitration across multi-agent swarms.

### Objective Evaluation Criteria & Benchmarks
- **Token Efficiency:** $ \ge 35\% $ reduction in total token consumption on standard multi-step benchmarks.
- **Uncertainty Reduction:** $ \ge 50\% $ faster convergence on epistemic curiosity targets.
- **Budget Compliance:** 100% compliance with maximum spending constraints ($ \text{budget\_limit\_usd} $).

---

## Phase 3: Causal Counterfactual Modeling & GRC Verification (Weeks 5–6)

### Core Deliverables
1. Integrate Judea Pearl's Structural Causal Models (SCM) with $ \text{do} $-calculus ($ \text{do}(X=x) $) in Layer 4 APODEX World Model.
2. Implement conjugate Beta distribution Bayesian belief updates ($ P(B|E) $) for entity and relationship states.
3. Deploy automated AST syntax and GRC security linting for self-referential code rewrites.

### Objective Evaluation Criteria & Benchmarks
- **Causal Accuracy:** $ \ge 90\% $ accuracy in counterfactual scenario projections under Gaussian noise perturbations.
- **Security Guardrail Veto:** 100% rejection rate for unsafe code mutations containing `eval`, `exec`, or `os.system`.
- **False-Positive Research Rate:** Zero false-positive scientific discoveries under Deflated Sharpe Ratio (DSR) multi-testing correction.

---

## Phase 4: Continuous Evolution & Self-Improvement Flywheel (Weeks 7–8)

### Core Deliverables
1. Deploy on-policy advantage estimation and DPO preference pair generation ($ \text{chosen} \text{ vs } \text{rejected} $) for trajectory optimization.
2. Integrate TextGrad natural language error gradient optimization for agent system prompts.
3. Establish automated benchmark regression suites with non-bypassable promotion gates.

### Objective Evaluation Criteria & Benchmarks
- **Autonomous Improvement Rate:** Measurable positive delta in trajectory success rates over 100 consecutive execution loops.
- **Zero Regression Guardrail:** Automated rollback triggered if candidate prompt/code update scores lower than baseline.
