# Transferable Engineering Principles for Autonomous Research OS & Evolved Cognitive Architecture

This document outlines the core engineering principles extracted from state-of-the-art research (across 500 published publications) and synthesized inside the APODEX AI-EOS, AEAN, EIOS, and Research OS architecture.

---

## Baseline Principles (1-4)

### Principle 1: Hexagonal Isolation of Strategic Planning
- **Concept**: Never pollute the strategic planning history with task execution outputs.
- **Implementation**: The `StrategicPlanner` compiles a frozen `Roadmap`, while the `TaskExecutor` processes individual steps. Output payloads are validated by a `PlanVerifier` and kept strictly isolated from the planner's memory.

### Principle 2: Multi-Tier Memory Consolidation
- **Concept**: Distinguish short-term context window history from persistent semantic memory.
- **Implementation**: Short-term history is compacted via sliding windows, while structured evidence cards, facts, and beliefs are persisted inside a SQLite semantic memory repository. High-confidence facts are promoted, and low-confidence ones are pruned to satisfy token budgets.

### Principle 3: Model-Collapse Guard via Quality Downsampling
- **Concept**: Automatically prevent self-generated SFT training datasets from causing recursive model degradation.
- **Implementation**: The `TrajectoryDatasetCompiler` tracks the ratio of self-generated vs. real trajectory traces. In strict mode, it raises errors on threshold breach; in relaxed mode, it downsamples self-generated data, keeping only high-scoring traces.

### Principle 4: Two-Level Credit Assignment
- **Concept**: Calculate both global trajectory success and progressive step-level contribution.
- **Implementation**: The `TwoLevelCreditAssignment` engine applies positive reinforcement ($1.0 \times \frac{i}{N}$) for successful steps, and progressive penalties ($-0.2 \times \frac{i}{N}$) for steps leading to failure.

---

## Evolved Subsystem Transferable Principles (200-Paper Corpus, IDs 301-500)

### Principle 5: AEAN - Clipped Trajectory Advantage Alignment & Bidding Consensus
- **Concept**: In decentralized multi-agent token bidding and strategy exchanges, raw preference advantages can explode or suffer sycophantic drift.
- **Implementation**: `SFTPreferenceCollector` applies clipped trajectory advantage margins $A_{clip} = \text{clip}(A_{chosen} - A_{rejected}, -\epsilon, +\epsilon)$ and `HiveMind` implements sycophancy-proof voting with counterfactual credit assignment.

### Principle 6: EOS - Hawkes Non-Gaussian Volatility Jump Control & Unit Economic Stress Testing
- **Concept**: Entrepreneurial venture capital deployment and customer lifetime value decay follow non-Gaussian heavy-tailed jump-diffusion processes.
- **Implementation**: `EOSEngine` and `CodeRewriteEngine` incorporate Hawkes process intensity limits and non-Gaussian AST call depth bounds to safeguard against catastrophic drawdown regimes and infinite recursion.

### Principle 7: EIOS - Active Inference Expected Free Energy (EFE) Sensing over Execution DAGs
- **Concept**: Operating system execution DAGs must balance pragmatic action (fulfilling goals) with epistemic exploration (reducing uncertainty).
- **Implementation**: `EIOSKernel` computes Expected Free Energy $G(\pi) = \text{Epistemic Uncertainty} + \text{Pragmatic Cost}$ over opportunity nodes and dynamically routes tasks using budget-decayed routing gates in `LearnableRoutingGateDispatcher`.

### Principle 8: Research OS - Self-Referential Code Rewrite, Island MAP-Elites, & Multi-Field Literature Review
- **Concept**: Automated scientific discovery requires verified self-referential code rewrites, diverse genetic program mutation, and broad cross-field literature synthesis.
- **Implementation**: `ResearchOS.conduct_literature_review` performs multi-field queries across categories, descriptions, target subsystems, paper titles, and extracted principles, while `GeneticWorkflowOptimizer` applies island MAP-Elites re-sorting gates upon elite insertion.
