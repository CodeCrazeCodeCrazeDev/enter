# Transferable Engineering Principles for Autonomous Research OS

This document outlines the core engineering principles extracted from state-of-the-art research (across 500 cataloged publications) and synthesized inside the AEAN, EOS, EIOS, and ResearchOS architecture.

---

## Principle 1: Hexagonal Isolation of Strategic Planning (ResearchOS)
- **Concept**: Never pollute the strategic planning history with task execution outputs.
- **Implementation**: The `StrategicPlanner` compiles a frozen `Roadmap`, while the `TaskExecutor` processes individual steps. Output payloads are validated by a `PlanVerifier` and kept strictly isolated from the planner's memory.

## Principle 2: Multi-Tier Memory Consolidation (ResearchOS / AEAN)
- **Concept**: Distinguish short-term context window history from persistent semantic memory.
- **Implementation**: Short-term history is compacted via sliding windows, while structured evidence cards, facts, and beliefs are persisted inside a SQLite semantic memory repository. High-confidence facts are promoted, and low-confidence ones are pruned to satisfy token budgets.

## Principle 3: Model-Collapse Guard via Quality Downsampling (ResearchOS)
- **Concept**: Automatically prevent self-generated SFT training datasets from causing recursive model degradation.
- **Implementation**: The `TrajectoryDatasetCompiler` tracks the ratio of self-generated vs. real trajectory traces. In strict mode, it raises errors on threshold breach; in relaxed mode, it downsamples self-generated data, keeping only high-scoring traces.

## Principle 4: Two-Level Credit Assignment (ResearchOS / EOS)
- **Concept**: Calculate both global trajectory success and progressive step-level contribution.
- **Implementation**: The `TwoLevelCreditAssignment` engine applies positive reinforcement ($1.0 \times \frac{i}{N}$) for successful steps, and progressive penalties ($-0.2 \times \frac{i}{N}$) for steps leading to failure.

## Principle 5: AST Sandbox Dry-Run Verification for Self-Referential Code Rewrites (ResearchOS / EOS)
- **Concept**: Prevent unsafe code generation or execution by verifying code AST structure and simulating changes in isolated temporary sandboxes before committing to disk.
- **Implementation**: The `CodeRewriteEngine` parses proposed snippets with `ast.parse`, enforces security linting rules (vetoing dangerous functions like `eval`, `exec`, `os.system`), and runs dry-run simulations in temporary files.

## Principle 6: Island-Based MAP-Elites Behavioral Grid Decomposition (AEAN / ResearchOS)
- **Concept**: Preserve diversity in multi-agent prompt and workflow evolution through multi-island populations and behavioral feature grids.
- **Implementation**: `GeneticWorkflowOptimizer` runs island-based genome evolution with Gaussian hyperparameter mutations, prompt template transformations, and MAP-Elites migration gates to prevent premature convergence.

## Principle 7: On-Policy Advantage Estimation for DPO Preference Compilation (AEAN / ResearchOS)
- **Concept**: Compile trajectory traces into chosen vs. rejected preference pairs using temporal-difference advantage estimation.
- **Implementation**: `SFTPreferenceCollector` computes discounted step rewards against expected baseline value functions, compiling DPO preference datasets with explicit advantage margins for model alignment.

## Principle 8: Expected Free Energy (EFE) Budget-Bounded Multi-Agent Routing (EIOS / AEAN)
- **Concept**: Route complex domain tasks to specialized sub-agents by balancing pragmatic utility, epistemic curiosity, and token costs under strict financial constraints.
- **Implementation**: `LearnableRoutingGateDispatcher` computes EFE score ($V_{pragmatic} + V_{epistemic} - C_{financial}$), dynamically selecting optimal sub-agents while monitoring budget thresholds and applying fallback mechanisms.

## Principle 9: Non-Gaussian Hawkes Self-Exciting System Contagion Protection (EIOS / EOS)
- **Concept**: Model heavy-tailed event rate spikes and self-exciting task cascades to prevent systemic deadlock across distributed multi-agent pipelines.
- **Implementation**: Embedded parameter boundaries and non-linear intensity function calibrations protect high-frequency event queues from cascade failures under high-stress anomalies.

## Principle 10: Counterfactual Do-Calculus Causal Belief Updating (AEAN / EOS)
- **Concept**: Use Directed Acyclic Graphs (DAGs) and counterfactual interventions to isolate cause-and-effect relationships in complex multi-agent execution graphs.
- **Implementation**: Integrates Pearl's $do(\cdot)$ calculus operator across `WorldModel` causal nodes and `EIOSKernel` execution graphs to update recursive Bayesian beliefs upon structural changes.
