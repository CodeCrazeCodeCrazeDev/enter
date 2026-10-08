# Transferable Engineering Principles for Autonomous Research OS & Cognitive Systems

This document outlines the core engineering principles extracted from state-of-the-art research across 500 academic publications (AI_EOS_RESEARCH_DB.yaml, ALPHA_ALGO_100_NEW_RESEARCH.yaml, and ALPHA_ALGO_200_NEW_RESEARCH.yaml) and synthesized inside the unified cognitive operating system.

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

## Evolved 200-Paper Corpus Principles (IDs 301-500)

### Principle 5: Active Inference Expected Free Energy (EFE) Anomaly Sensing
- **Target Subsystem**: `EIOS Kernel` (`apodex/arcs/kernel/kernel.py`) & `EOS Engine` (`apodex/ai_eos/intelligence/eos_engine.py`)
- **Concept**: Formulate opportunity and system anomaly detection as Active Inference Expected Free Energy (EFE) minimization, decomposing cost into Epistemic Curiosity Value and Pragmatic Value.
- **Implementation**: `EIOSKernel.sense_opportunity_anomalies()` computes EFE anomaly scores over research hypotheses, emitting `ActiveInferenceAnomaly` events to prompt continuous sensing and capital reallocation in the EOS Engine.

### Principle 6: Token-Staked Multi-Agent Task Bidding & Sycophancy Mitigation
- **Target Subsystem**: `AEAN HiveMind` (`apodex/aean/coordination/hive_mind.py` / `apodex/aean/core.py`)
- **Concept**: Eliminate sub-agent sycophancy and inefficient delegation by establishing a token-curated research insight registry and EFE-weighted task bidding.
- **Implementation**: `HiveMind.register_research_insight()` enables sub-agents to submit bids weighted by domain expertise, historical accuracy, and epistemic curiosity, routing tasks to the highest EFE-utility agent while remaining within strict compute budgets.

### Principle 7: Island MAP-Elites with Epistemic Migration Gates
- **Target Subsystem**: `Research OS` (`apodex/ai_eos/research/integration.py` & `research_os.py`)
- **Concept**: Maintain high genetic diversity in prompt templates and code mutation workflows using Quality-Diversity MAP-Elites with epistemic migration gates.
- **Implementation**: `GeneticWorkflowOptimizer` immediately re-sorts populations on elite insertion, applies type-checked parameter mutations, and exports top-fitness program genomes for downstream hypothesis testing.

### Principle 8: Non-Gaussian Hawkes Process Risk Shielding
- **Target Subsystem**: `EIOS Kernel` (`apodex/arcs/kernel/kernel.py`)
- **Concept**: Model event intensity and self-exciting shock cascades in market and execution environments using non-Gaussian Hawkes point processes.
- **Implementation**: `EIOSKernel` evaluates self-exciting Hawkes intensity bounds, triggering execution risk shielding and circuit breakers when intensity spikes breach safety thresholds.

### Principle 9: Multi-Field Research Literature Review & Principle Ingestion
- **Target Subsystem**: `Research OS` (`apodex/ai_eos/research/research_os.py` & `integration.py`)
- **Concept**: Expand literature review querying across rich metadata fields (category, target subsystem, paper title, extracted principle, implementation module) and provide cross-layer active inference state handoffs.
- **Implementation**: `register_200_paper_corpus_principles()` registers all 200 research principles into `ALPHAALGO_200_PRINCIPLES`, queried directly by `ResearchOS.conduct_literature_review()` and handed off across layers via `ResearchToSystemBridge`.
