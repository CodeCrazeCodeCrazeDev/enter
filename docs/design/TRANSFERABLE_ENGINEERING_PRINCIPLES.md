# Transferable Engineering Principles for Autonomous Research OS

This document outlines the core engineering principles extracted from state-of-the-art research (200-paper corpus) and synthesized inside the evolved Cognitive OS architecture (`AEAN`, `EOS`, `EIOS`, and `ResearchOS`).

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

## Principle 5: Active Inference & Expected Free Energy (EFE) Routing
- **Concept**: Route tasks and sense business anomalies by evaluating Expected Free Energy ($\text{EFE} = \text{Epistemic Value} + \text{Pragmatic Value} - \text{Financial Cost Penalty}$).
- **Implementation**: Integrated into `LearnableRoutingGateDispatcher` in `apodex/ai_eos/research/integration.py` and `EIOSKernel` sensing in `apodex/arcs/kernel/kernel.py`.

## Principle 6: Pearl's Causal Do-Calculus Interventions
- **Concept**: Evaluate strategic interventions by computing structural causal model (SCM) do-interventions $P(Y \mid \text{do}(X))$ rather than observational correlations $P(Y \mid X)$.
- **Implementation**: Integrated into `EOSEngine` hypothesis verification and `ResearchOS` experimental design.

## Principle 7: Self-Referential AST Code Rewrite & AST Security Verification
- **Concept**: Enable autonomous code modification through AST syntax parsing, sandboxed dry-run simulation, and static GRC security linting.
- **Implementation**: `CodeRewriteEngine` in `apodex/ai_eos/research/integration.py`.

## Principle 8: Genetic Workflow Mutation & MAP-Elites Quality Diversity
- **Concept**: Evolve agent prompts and execution parameters via island-based genetic algorithms featuring Gaussian parameter mutation and MAP-Elites fitness scoring.
- **Implementation**: `GeneticWorkflowOptimizer` in `apodex/ai_eos/research/integration.py`.

## Principle 9: Advantage Estimation & DPO Preference Record Synthesis
- **Concept**: Compute temporal-difference advantage values across agent trajectories to synthesize high-margin chosen vs. rejected DPO preference pairs for alignment.
- **Implementation**: `SFTPreferenceCollector` in `apodex/ai_eos/research/integration.py`.

## Principle 10: Multi-Agent Swarm Debate & Sycophancy Mitigation
- **Concept**: Mitigate compliance bias by conducting structured multi-agent cross-examination debate prior to promoting research hypotheses or strategic business decisions.
- **Implementation**: Swarm debate protocols in `apodex/aean/coordination/hive_mind.py`.
