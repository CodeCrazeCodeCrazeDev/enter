# Transferable Engineering Principles for Autonomous Research OS & AlphaAlgo System

This document outlines the core engineering principles extracted from state-of-the-art research (across 400 audited papers) and synthesized inside AlphaAlgo.

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

## Synthesis of Extracted Transferable Principles (Papers 301–400)

### Principle 5: Non-Gaussian Hawkes AST Call Depth Check (Papers 301–320)
- **Target Subsystem**: Research OS / CodeRewriteEngine (`apodex/ai_eos/research/integration.py`)
- **Concept**: In self-exciting Hawkes process modeling, self-excitation depth must be strictly bounded per process path. In code synthesis and AST verification, recursive function depth must be checked per-function definition rather than globally across the AST to avoid false positives on standard function calls.
- **Implementation**: `CodeRewriteEngine.verify_proposal_ast` tracks function definition call depth specifically to enforce non-recursive stability guards without vetoing harmless non-recursive AST calls.

### Principle 6: Decayed Free Energy Task Dispatching (Papers 321–340)
- **Target Subsystem**: EIOS Kernel / LearnableRoutingGateDispatcher (`apodex/ai_eos/research/integration.py`)
- **Concept**: Active inference agents minimize Expected Free Energy (EFE) by balancing pragmatic value (historical yield) and epistemic curiosity (information gain). Over time, as budget is spent and success is verified, epistemic curiosity should undergo exponential decay to prioritize pragmatic execution.
- **Implementation**: `LearnableRoutingGateDispatcher` incorporates budget-decayed epistemic curiosity multipliers, smoothly shifting task delegation from exploration to exploitation as budget thresholds are approached.

### Principle 7: Clipped Trajectory Advantage Margins (Papers 341–360)
- **Target Subsystem**: SFT/DPO Preference Collection (`apodex/ai_eos/research/integration.py`)
- **Concept**: Trajectory-level Direct Preference Optimization (DPO) can suffer from advantage scale explosion on long execution traces, leading to reward inflation and policy instability.
- **Implementation**: `SFTPreferenceCollector` applies clipped advantage margin bounds ($\text{margin} = \text{clip}(A_{\text{chosen}} - A_{\text{rejected}}, -\text{max\_margin}, \text{max\_margin})$) to stabilize preference dataset compilation.

### Principle 8: Island MAP-Elites Re-Sorting Gateways (Papers 361–380)
- **Target Subsystem**: AEAN / GeneticWorkflowOptimizer (`apodex/ai_eos/research/integration.py`)
- **Concept**: Quality diversity search (MAP-Elites) across isolated islands requires immediate population re-sorting upon elite insertion to preserve Pareto frontier dominance and prevent stale sub-optimal genomes from dominating island migrations.
- **Implementation**: `GeneticWorkflowOptimizer.insert_elite` re-sorts island populations immediately upon elite insertion and trims population size to strictly maintain top-tier genomes.

### Principle 9: Multi-Field Research Literature Querying (Papers 381–400)
- **Target Subsystem**: Research OS (`apodex/ai_eos/research/research_os.py`)
- **Concept**: Autonomous literature reviews across structured research DBs must query full multi-field namespaces (category, description, target subsystem, paper title, extracted principle, impl module) rather than single category strings to ensure complete scientific coverage.
- **Implementation**: `ResearchOS.conduct_literature_review` searches all available registered principle fields and research databases dynamically.
