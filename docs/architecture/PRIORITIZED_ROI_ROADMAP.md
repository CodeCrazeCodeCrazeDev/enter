# Prioritized Return-on-Investment (ROI) Roadmap

## Architectural Rationale & Strategy

To maximize capability expansion while minimizing engineering debt, initiatives are prioritized based on expected **Return-on-Investment (ROI)**, defined as:

$$\text{ROI Score} = \frac{\text{Capability Expansion} \times \text{Reliability Improvement}}{\text{Engineering Complexity} \times \text{Maintenance Risk}}$$

---

## Prioritized Engineering Initiatives

### Priority 1: Cross-Layer Active Inference State Handoff (`ResearchToSystemBridge`)
- **ROI Rating**: **Highest (5.0 / 5.0)**
- **Architectural Rationale**: Connects isolated scientific discovery directly into active market sensing, multi-agent bidding, and world model belief updates.
- **Expected Benefits**: Eliminates human-in-the-loop manual translation between research findings and runtime agent strategies.
- **Complexity Analysis**: Low complexity ($O(1)$ dictionary handoffs and explicit interface invocations).
- **Failure Modes & Diagnostics**: Unhandled missing hypothesis IDs. Mitigated by strict fallback default handoffs and logging.

### Priority 2: Hawkes Process Non-Gaussian AST Call Depth Security Engine
- **ROI Rating**: **High (4.7 / 5.0)**
- **Architectural Rationale**: Prevents infinite recursion and malicious self-rewrites during autonomous code modification.
- **Expected Benefits**: Guarantees AST safety during self-referential code rewrites (`CodeRewriteEngine`).
- **Complexity Analysis**: $O(N)$ AST node traversal with scope tracking.
- **Failure Modes & Diagnostics**: False positive vetoes on complex recursive algorithms. Mitigated by function-scoped depth tracking.

### Priority 3: Island MAP-Elites MAP-Elites Genetic Workflow Optimizer
- **ROI Rating**: **High (4.5 / 5.0)**
- **Architectural Rationale**: Dynamically evolves prompt templates and parameter configurations without catastrophic collapse.
- **Expected Benefits**: Automated continuous adaptation of agent prompt templates and temperature parameters.
- **Complexity Analysis**: $O(P \log P)$ population evaluation and sorting per generation.
- **Failure Modes & Diagnostics**: Premature convergence to local fitness optima. Mitigated by island migration gates and random mutation injections.

### Priority 4: Active Inference EFE Budget-Bounded Task Dispatcher
- **ROI Rating**: **High (4.4 / 5.0)**
- **Architectural Rationale**: Balances epistemic curiosity with pragmatic financial constraints (USD cost per token).
- **Expected Benefits**: Eliminates runaway API costs during long-horizon agent execution.
- **Complexity Analysis**: $O(A)$ search over $A$ registered agent profiles per task dispatch.
- **Failure Modes & Diagnostics**: All agents exceed budget ceiling. Mitigated by automatic greedy fallback to the cheapest available agent profile.

### Priority 5: On-Policy Advantage Estimation & SFT/DPO Preference Compiler
- **ROI Rating**: **Medium-High (4.2 / 5.0)**
- **Architectural Rationale**: Automatically collects chosen vs. rejected execution trajectories with temporal difference advantage margins.
- **Expected Benefits**: Continuous self-improvement dataset generation ready for fine-tuning open-weights models.
- **Complexity Analysis**: $O(T^2)$ over trajectory steps $T$ for discounted return computation.
- **Failure Modes & Diagnostics**: Zero advantage margin between choices. Mitigated by clipping minimum advantage threshold.
