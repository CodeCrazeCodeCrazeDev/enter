# Transferable Engineering Principles for Autonomous Research OS & AlphaAlgo System

This document outlines the core engineering principles extracted from state-of-the-art research (across 400 papers) and synthesized inside the evolved `AgentHarness` and `apodex` frameworks.

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

---

## Synthesis of Papers 301-400 (AlphaAlgo Advanced Quantitative Principles)

### Principle 5: Non-Gaussian Hawkes Process Self-Referential AST Call-Depth Verification
- **Paper Basis**: Papers 301-320 (Non-Gaussian Hawkes Processes & Microstructure Dynamics)
- **Concept**: Market order flow spikes and self-referential code rewrites both exhibit non-Gaussian clustering. AST verification must enforce bounded recursion call depth specifically within function definitions rather than total node counts across the file.
- **Implementation**: `CodeRewriteEngine.verify_proposal_ast` checks AST function definition nodes for recursive call depth, preventing unbounded recursion while permitting frequent standard library calls.

### Principle 6: Island MAP-Elites Migration Gate with Fitness Score Ordering
- **Paper Basis**: Papers 381-400 (Genetic Programming, Quality Diversity & MAP-Elites)
- **Concept**: Isolated island populations prevent genetic search drift. Inter-island migration must be gated by strict fitness score ordering so that only superior genomes cross island boundaries.
- **Implementation**: `GeneticWorkflowOptimizer.migrate_elites_between_islands` sorts island populations by fitness score descending and migrates top elites to neighboring islands.

### Principle 7: Clipped Trajectory Advantage Margin for SFT/DPO Preference Collection
- **Paper Basis**: Papers 341-360 (Reinforcement Learning, Advantage Bounds & DPO Alignment)
- **Concept**: Raw trajectory advantage margins can inflate under noisy reward landscapes. Advantage margins used for preference pair compilation must be clipped within a stable bounding interval $[-M_{max}, M_{max}]$.
- **Implementation**: `SFTPreferenceCollector.compile_dpo_preference_pair` clips computed advantage margins to `[-10.0, 10.0]`.

### Principle 8: Budget-Decayed Expected Free Energy (EFE) Task Routing
- **Paper Basis**: Papers 321-340 & 361-380 (Active Inference & Budget-Constrained Mechanism Design)
- **Concept**: Sub-agent routing must balance epistemic curiosity with pragmatic utility under diminishing financial budgets. As budget is depleted, epistemic curiosity weighting is dynamically scaled down by remaining budget ratio.
- **Implementation**: `LearnableRoutingGateDispatcher.route_task` decays epistemic curiosity by `(budget_limit - budget_spent) / budget_limit` when computing the EFE routing score.
