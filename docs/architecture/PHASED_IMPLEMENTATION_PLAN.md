# Phased Implementation Plan & Evaluation Criteria

## Overview

The transformation of Research OS, EIOS, EOS, AEAN, and APODEX into a unified cognitive operating system is executed across four distinct phases. Each phase includes strict objective acceptance criteria and quantitative benchmarks.

---

## Phase 1: Core Subsystem Architecture Unification & Interface Normalization

### Objectives
- Formalize 4-Layer Cognitive Operating System taxonomy.
- Standardize cross-layer state handoffs via `ResearchToSystemBridge`, `EOSEngine.ingest_validated_research`, and `HiveMind.register_research_insight`.
- Eliminate logical duplication across legacy adapters and canonical modules.

### Objective Evaluation Criteria
- **Importability & Architecture Audit**: 100% of layer imports resolve cleanly with zero circular dependencies.
- **Corpus Overlap Audit**: Zero title or DOI overlaps across all 500 research papers.
- **Integration Test Pass Rate**: 100% pass rate across unit and integration test suites.

---

## Phase 2: Active Inference Control Loop & Market-Based Execution

### Objectives
- Implement EIOS Kernel Active Inference Expected Free Energy (EFE) sensing over research hypotheses.
- Deploy AEAN HiveMind auction-based token bidding for DAG task dispatch.
- Integrate APODEX WorldModel causal node creation and recursive Bayesian belief updates.

### Objective Evaluation Criteria
- **Task Dispatch Latency**: $\le 150\,\text{ms}$ per task node auction in HiveMind.
- **EFE Minimization Rate**: Active sensing selects highest epistemic gain tasks with $>85\%$ precision.
- **Bayesian Belief Convergence**: Recursive updates converge to steady-state confidence within $\le 5$ empirical observations.

---

## Phase 3: Meta-Reasoning, Self-Improvement & AST Safety

### Objectives
- Deploy Meta-Reasoner observer to detect and break repetitive agent tool loops.
- Implement Genetic Workflow Optimizer with island MAP-Elites migration gates.
- Implement non-Gaussian Hawkes process AST recursion depth checks for safe code mutations.

### Objective Evaluation Criteria
- **Loop Interception Rate**: $100\%$ interception of tool calls repeated $\ge 2$ times with counterfactual warning injection.
- **Optimization Uplift**: Workflow optimizer improves mean trajectory score by $\ge 15\%$.
- **Mutation Safety**: Zero false positives on non-recursive standard library calls during AST code rewrite verification.

---

## Phase 4: Institutional Governance & Production Flywheel

### Objectives
- Enforce Cost Tier budget limits, protocol downshifting, and halting in `SkillsRunner`.
- Enforce tiered multi-signature approval workflows for execution and capital re-allocation.
- Continuous benchmarking and regression-free evolution flywheel.

### Objective Evaluation Criteria
- **Budget Compliance**: $100\%$ compliance with Cost Tier token limits; downshifting/halting triggers deterministically upon budget depletion.
- **Regression Rate**: $0\%$ performance regression on existing test suites during continuous evolution runs.
