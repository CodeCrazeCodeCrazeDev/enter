# Transferable Engineering Principles for Autonomous Research OS & Cognitive Systems

This document synthesizes transferable engineering principles extracted across 500 published research papers, providing explicit design abstractions, theoretical foundations, and direct subsystem mappings for **AEAN**, **EOS**, **EIOS**, and **Research OS**.

---

## Part 1: Core Subsystem Architectural Mappings

### Subsystem 1: AEAN (Autonomous Entrepreneurial Agent Network)
- **Principle 5: Token-Bidding Task Allocation & Shapley Credit Attribution**
  - *Theoretical Source*: Papers 341-380 (Sandholm, Conitzer, Wooldridge)
  - *Concept*: Decentralized swarm intelligence coordinates via token bidding, where agents bid based on domain suitability, epistemic curiosity, and cost. Task outcomes are attributed back using Shapley value calculation.
  - *Target Subsystem*: `apodex/aean/coordination/hive_mind.py` (`HiveMind.register_research_insight` and token bidding).

- **Principle 6: Quality Diversity Island Migration Gates**
  - *Theoretical Source*: Papers 421-460 (Mouret, Clune, Real)
  - *Concept*: MAP-Elites population grids are partitioned into isolated islands. When elite programs are inserted, island populations immediately re-sort and apply migration gates to prevent premature convergence.
  - *Target Subsystem*: `apodex/ai_eos/research/integration.py` (`GeneticWorkflowOptimizer`).

---

### Subsystem 2: EOS (Entrepreneurial Operating System)
- **Principle 7: Active Inference Research Hypothesis Ingestion & Capital Allocation**
  - *Theoretical Source*: Papers 301-340 & 461-500 (Friston, Parr, Bacry, Cont)
  - *Concept*: EOS ingests scientifically validated hypotheses from Research OS into its active hypotheses ledger, using Expected Free Energy (EFE) and non-Gaussian Hawkes market impact risk bounds to optimize unit-economic capital allocation.
  - *Target Subsystem*: `apodex/ai_eos/intelligence/eos_engine.py` (`EOSEngine.ingest_validated_research`).

- **Principle 8: Non-Gaussian Heavy-Tailed Risk Boundaries**
  - *Theoretical Source*: Papers 461-500 (Cont, Bacry, Gatheral)
  - *Concept*: Financial and operational parameters enforce non-Gaussian heavy-tailed risk boundaries, protecting execution against liquidity traps and latency spikes.
  - *Target Subsystem*: `apodex/ai_eos/intelligence/eos_engine.py` and `eos_first_principles.py`.

---

### Subsystem 3: EIOS (Entrepreneurial Intelligence Operating Subsystem / Kernel)
- **Principle 9: Expected Free Energy (EFE) Anomaly Sensing**
  - *Theoretical Source*: Papers 301-340 (Friston, Millidge, Sajid)
  - *Concept*: EIOS Kernel senses anomalies by evaluating epistemic value (curiosity/entropy reduction) and pragmatic value (expected reward) over research hypotheses exported from Research OS.
  - *Target Subsystem*: `apodex/arcs/kernel/kernel.py` (`EIOSKernel.sense_opportunity_anomalies`).

- **Principle 10: Multi-Horizon Active Inference DAG Execution**
  - *Theoretical Source*: Papers 328-340 (Da Costa, Parr)
  - *Concept*: Hierarchical task graphs are compiled into directed acyclic execution graphs with EFE-decayed resource budgets across Day, Week, Quarter, and 1Y horizons.
  - *Target Subsystem*: `apodex/arcs/kernel/kernel.py` (`EIOSKernel.register_research_hypothesis`).

---

### Subsystem 4: Research OS
- **Principle 11: AST Recursion Depth Verification in Self-Referential Rewriting**
  - *Theoretical Source*: Papers 421, 427, 451, 460 (Real, Bacry, Romera-Paredes)
  - *Concept*: AST static linting inside `CodeRewriteEngine` enforces recursive call-depth checks within function definitions to prevent unbounded stack overflows and non-Gaussian Hawkes instabilities.
  - *Target Subsystem*: `apodex/ai_eos/research/integration.py` (`CodeRewriteEngine.verify_proposal_ast`).

- **Principle 12: Clipped Margin Trajectory Preference Collection (DPO)**
  - *Theoretical Source*: Papers 381-420 (Rafailov, Lambert, Mitchell)
  - *Concept*: Trajectory step advantage estimation applies clipped margin bounds ($|A_t| \le C$) and edit-path distance penalties to prevent reward inflation during on-policy preference dataset compilation.
  - *Target Subsystem*: `apodex/ai_eos/research/integration.py` (`SFTPreferenceCollector`).

- **Principle 13: Multi-Field Literature Synthesis & Corpus Principle Querying**
  - *Theoretical Source*: Papers 1-500 (200-Paper Corpus Integration)
  - *Concept*: `ResearchOS.conduct_literature_review` queries registered principles across domain category, description, paper title, target subsystem, and extracted principle fields to provide zero-hallucination research retrieval.
  - *Target Subsystem*: `apodex/ai_eos/research/research_os.py` (`ResearchOS.conduct_literature_review`).

---

## Part 2: Baseline Principles

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
