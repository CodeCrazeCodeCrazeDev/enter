# Transferable Engineering Principles for Autonomous Research OS

This document outlines the core engineering principles extracted from state-of-the-art research (spanning the 500-paper corpus) and synthesized inside the evolved AI-EOS, AEAN, EIOS, Research OS, and APODEX WorldModel framework.

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

## Synthesized Principles from 200 New Papers (IDs 301-500)

### Principle 5: Active Inference Expected Free Energy (EFE) Sensing (Target: EIOS)
- **Concept**: Active Inference balances epistemic exploration (uncertainty reduction) and pragmatic exploitation (value realization) through Expected Free Energy (EFE) bounds.
- **Implementation**: Implemented in `EIOSKernel` and `ResearchToSystemBridge`. Prioritizes task routing by calculating $EFE = \alpha \cdot E[\text{Value}] + \beta \cdot \text{InfoGain} + \gamma \cdot \text{OptionValue}$.

### Principle 6: HiveMind Adaptive Token Bidding & Consensus Weighting (Target: AEAN)
- **Concept**: Multi-agent task allocation utilizes convex capacity bounds, dynamic token inflation deflators, and precision-weighted consensus bidding.
- **Implementation**: Implemented in `HiveMind` (`apodex/aean/coordination/hive_mind.py`). Bids are evaluated against skill availability, token budget thresholds, and agent consensus weights.

### Principle 7: Non-Gaussian Hawkes Process Anomaly Sensing (Target: EOS & EIOS)
- **Concept**: Event streams in high-frequency opportunity sensing exhibit mutually exciting non-Gaussian jump dynamics and self-excitation kernels.
- **Implementation**: Implemented in `AnomaliesAndSensingEngine` and `CodeRewriteEngine`. Tracks event intensity rates and applies non-Gaussian variance decay to detect market and system anomalies.

### Principle 8: Self-Referential Code Rewrite & AST Depth Guards (Target: Research OS)
- **Concept**: Code mutation and self-improvement require formal AST safety bounds, non-recursive depth limits, and static Gödel verification gates to eliminate unhandled recursion and arbitrary code execution.
- **Implementation**: Implemented in `CodeRewriteEngine` (`apodex/ai_eos/research/integration.py`). Enforces per-function recursion depth tracking and GRC security linting.

### Principle 9: System Dynamics GTM Lifecycle & Moat Expansion (Target: EOS)
- **Concept**: B2B GTM lifecycles, customer acquisition/retention physics, and network effect moats follow non-linear differential dynamics.
- **Implementation**: Implemented in `EOSEngine` and `EOSFirstPrinciples` (`apodex/ai_eos/intelligence/eos_first_principles.py`). Simulates multi-stage growth state transitions and calculates moat scaling factors.

### Principle 10: Multi-Field Literature Review Querying & Statistical Controls (Target: Research OS)
- **Concept**: Autonomous literature synthesis must query across multiple paper attributes (title, extracted principle, target subsystem, category) and enforce Bonferroni / Deflated Sharpe Ratio statistical controls.
- **Implementation**: Implemented in `ResearchOS.conduct_literature_review` (`apodex/ai_eos/research/research_os.py`) and `StatisticalValidator`.

### Principle 11: Causal Structure Discovery & Bayesian Belief Updates (Target: WorldModel)
- **Concept**: Causal graph compilation enables counterfactual do-calculus reasoning and recursive Bayesian belief updates under heavy-tailed noise.
- **Implementation**: Implemented in `WorldModel` (`apodex/world_model/world_model.py`) and `AdvancedCausalEngine`.

### Principle 12: Fault-Tolerant Task DAG Execution & Resilient Queues (Target: EIOS)
- **Concept**: Asynchronous agent execution queues utilize budget-decayed task routing, SLA threshold enforcement, and automated compensation workflows.
- **Implementation**: Implemented in `EIOSKernel` (`apodex/arcs/kernel/kernel.py`).

### Principle 13: Neural-Symbolic Graph Planning & Node Routing (Target: AEAN & EOS)
- **Concept**: Opportunity graph traversal combines neural embedding similarity with symbolic constraint checking.
- **Implementation**: Implemented in `EntrepreneurialIntelligenceOrchestrator` and `OpportunityGraph`.

### Principle 14: Multi-Tier Memory Context Compaction (Target: AEAN & Research OS)
- **Concept**: Long-running agent executions maintain multi-tier context windows with selective retention, fact verification, and token budget decay.
- **Implementation**: Implemented in `HiveMind` and `ResearchOS`.
