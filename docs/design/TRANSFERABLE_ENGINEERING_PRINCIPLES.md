# Transferable Engineering Principles for Autonomous Research OS

This document outlines the core engineering principles extracted from state-of-the-art research and synthesized inside the evolved `AgentHarness` framework.

---

## Principle 1: Hexagonal Isolation of Strategic Planning
- **Concept**: Never pollute the strategic planning history with task execution outputs.
- **Implementation**: The `StrategicPlanner` compiles a frozen `Roadmap`, while the `TaskExecutor` processes individual steps. Output payloads are validated by a `PlanVerifier` and kept strictly isolated from the planner's memory.

## Principle 2: Multi-Tier Memory Consolidation
- **Concept**: Distinguish short-term context window history from persistent semantic memory.
- **Implementation**: Short-term history is compacted via sliding windows, while structured evidence cards, facts, and beliefs are persisted inside a SQLite semantic memory repository. High-confidence facts are promoted, and low-confidence ones are pruned to satisfy token budgets.

## Principle 3: Model-Collapse Guard via Quality Downsampling
- **Concept**: Automatically prevent self-generated SFT training datasets from causing recursive model degradation.
- **Implementation**: The `TrajectoryDatasetCompiler` tracks the ratio of self-generated vs. real trajectory traces. In strict mode, it raises errors on threshold breach; in relaxed mode, it downsamples self-generated data, keeping only high-scoring traces.

## Principle 4: Two-Level Credit Assignment
- **Concept**: Calculate both global trajectory success and progressive step-level contribution.
- **Implementation**: The `TwoLevelCreditAssignment` engine applies positive reinforcement ($1.0 \times \frac{i}{N}$) for successful steps, and progressive penalties ($-0.2 \times \frac{i}{N}$) for steps leading to failure.

## Principle 5: Active Inference Expected Free Energy (EFE) Routing
- **Concept**: Unify pragmatic utility maximization and epistemic surprise reduction under variational free energy minimization.
- **Implementation**: `LearnableRoutingGateDispatcher` computes EFE routing scores $S = \text{epistemic\_value} + \text{pragmatic\_value} - \text{cost\_penalty}$ to assign tasks dynamically to specialized sub-agents based on budget limits and domain alignment.

## Principle 6: Non-Gaussian Hawkes Self-Exciting Process Dynamics
- **Concept**: Model asynchronous event clusters and self-exciting volatility feedback loops using continuous point processes with stability bounds.
- **Implementation**: `CodeRewriteEngine` and `EIOSKernel` compute Hawkes intensity kernels and enforce spectral radius stability matrices to bound recursive call depth and event cascades.

## Principle 7: Island MAP-Elites Behavioral Archive Illumination
- **Concept**: Maintain multi-dimensional behavioral niches to prevent premature genetic convergence and ensure sub-minute adaptation to operational failures.
- **Implementation**: `GeneticWorkflowOptimizer` sorts populations into Pareto non-dominated MAP-Elites archives, dynamically re-sorting populations upon elite insertion.

## Principle 8: On-Policy Advantage Margin Preference Distillation
- **Concept**: Compile execution trajectory traces into DPO chosen/rejected preference pairs weighted by temporal-difference advantage margins.
- **Implementation**: `SFTPreferenceCollector` computes discounted return advantages $A_t = G_t - V(s)$ and pairs trajectories to fine-tune generative agent policies without explicit reward model instability.
