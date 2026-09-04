# Unified Cognitive Operating System Architecture Specification

## Executive Summary & Architectural Rationale

The **Unified Cognitive Operating System** integrates Research OS, EIOS/EOS, AEAN, and APODEX into a single 4-layer computational architecture. Rather than operating as five separate platforms with overlapping logic and duplicated components, each subsystem is assigned a strict single-responsibility layer within a unified cognitive stack:

```
+-----------------------------------------------------------------------+
|  LAYER 1: RESEARCH OS (Research & Knowledge Discovery Layer)          |
|  - Empirical Paper Database & Principle Extraction                     |
|  - Scientific Hypothesis Generation & Reproducibility Verification   |
+-----------------------------------------------------------------------+
                                   | (Validated Hypotheses & Research Insights)
                                   v
+-----------------------------------------------------------------------+
|  LAYER 2: EIOS / EOS (Execution & Strategic Business Orchestration)    |
|  - Entrepreneurial State Machine (11 EOS Sections / 14 CAE Layers)   |
|  - Active Inference Anomaly Sensing & Expected Free Energy (EFE) Routing|
+-----------------------------------------------------------------------+
                                   | (Opportunity Signals & Compiled Task DAGs)
                                   v
+-----------------------------------------------------------------------+
|  LAYER 3: AEAN (Cognitive Intelligence & Multi-Agent HiveMind Stack)  |
|  - Multi-Agent Bidding & Task Allocation (HiveMind Token Economy)     |
|  - Non-Gaussian Hawkes, MAP-Elites Islands, Causal Do-Calculus        |
+-----------------------------------------------------------------------+
                                   | (Strategy Execution & Action Decisions)
                                   v
+-----------------------------------------------------------------------+
|  LAYER 4: APODEX (Decision Engine, World Model & Execution Platform)  |
|  - Recursive Bayesian Belief Propagation & Causal Graph (WorldModel)  |
|  - Protocol Execution, Safety Gates, & Skill Flywheel Registry        |
+-----------------------------------------------------------------------+
```

---

## Single Responsibility & Capability-Ownership Matrix

To eliminate architectural duplication, capabilities are mapped strictly to canonical owners:

| Capability Domain | Canonical Owner Component | Scope & Interfaces | Replaced / Disallowed Legacy Equivalents |
|---|---|---|---|
| Literature Ingestion & Paper Corpus | `ResearchOS` (`apodex/ai_eos/research/research_os.py`) | Ingests research YAML DBs, extracts principles, queries literature. | Duplicate mock research parsers |
| Opportunity Sensing & Anomaly Detection | `EIOSKernel` (`apodex/arcs/kernel/kernel.py`) | Active Inference EFE sensing over market and research hypotheses. | Ad-hoc threshold sensors |
| Entrepreneurial Decision Engine | `FirstPrinciplesEOSEngine` (`apodex/ai_eos/intelligence/`) | 11-section EOS state machine & 14-layer CAE execution. | Hardcoded ROI heuristics |
| Agent Bidding & Task Dispatch | `HiveMind` (`apodex/aean/coordination/hive_mind.py`) | Priority token bidding registry & swarm task allocation. | Duplicate agent routers |
| World Representation & Belief Propagation | `WorldModel` (`apodex/world_model/world_model.py`) | Causal DAG, Recursive Bayesian belief update, protocol loader. | Isolated local memory graphs |
| Skill Execution Flywheel | `SkillRegistry` (`apodex/skills/registry.py`) | Pre-populated operational skill execution engine. | Disparate agent tool scripts |

---

## Subsystem Architecture & Interface Contracts

### Layer 1: Research OS
* **Primary Duty**: Autonomous hypothesis generation, literature review synthesis across 500+ research papers, and statistical validation of empirical principles.
* **Exports**: `export_validated_hypothesis_to_kernel()`, `promote_hypothesis_to_eos()`.

### Layer 2: EIOS & EOS
* **Primary Duty**: Translates validated research hypotheses and market anomaly signals into executable business strategies and opportunity DAGs using Active Inference Expected Free Energy (EFE) calculation.
* **Exports**: `sense_opportunity_anomalies()`, `compile_opportunity_dag()`.

### Layer 3: AEAN (Autonomous Entrepreneurial Agent Network)
* **Primary Duty**: Coordinates specialized agent swarms to execute compiled opportunity DAGs using token bidding, MAP-Elites island search, non-Gaussian Hawkes stability gates, and causal do-calculus.
* **Exports**: `bid_for_task()`, `dispatch_strategy_execution()`.

### Layer 4: APODEX
* **Primary Duty**: Serves as the substrate for world model entity state tracking, protocol execution, risk governance halt controls, and skill performance feedback flywheels.
* **Exports**: `update_entity()`, `propagate_bayesian_belief()`, `execute_protocol()`.

---

## Architectural Rationale, Trade-offs & Failure Modes

1. **Trade-off: Layered Handoff Overhead vs. Subsystem Isolation**
   - *Rationale*: Explicit cross-layer state handoffs introduce small serialization overhead (~2ms), but prevent state corruption and logical duplication across multi-agent execution paths.
2. **Failure Mode: Anomaly Drift in Active Inference**
   - *Mitigation*: Probability clamping in inverse CDF calculations (`standard_normal_ppf`) and probability bounds safeguard active inference state updates from numerical instability.
3. **Complexity Analysis**:
   - Time Complexity: Active Inference EFE sensing scales as $O(N \log N)$ where $N$ is the number of active hypotheses. Token bidding in HiveMind executes in $O(A \cdot T)$ for $A$ agents and $T$ tasks.
