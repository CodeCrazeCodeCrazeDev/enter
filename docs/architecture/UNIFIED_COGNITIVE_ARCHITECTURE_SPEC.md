# Unified Cognitive Architecture Specification
## AEAN / EIOS / EOS / Research OS / APODEX Cognitive Operating System

### Executive Summary & First-Principles Mandate
This specification formalizes the unified, 4-layer cognitive operating system uniting Research OS, EIOS, EOS, AEAN, and APODEX into a single non-overlapping intelligence substrate. Instead of maintaining five distinct or partially redundant platforms, all capabilities are partitioned into a single layered architecture with explicit interfaces, clean data flow, and zero logical duplication.

---

## 1. The 4-Layer Cognitive OS Taxonomy

```
+-----------------------------------------------------------------------------------+
|                        LAYER 4: APODEX (Platform & Execution)                     |
|  - Personal Evolution Profiles (PEP)   - Multi-Objective Cost Router              |
|  - Tiered Governance & Safety Core    - Autonomous Software Engineering Engine   |
|  - Interactive GUI / CLI Platforms     - Runtime V&V & Introspective Critics       |
+-----------------------------------------------------------------------------------+
                                        |  Commands / Policy Invariants
                                        v
+-----------------------------------------------------------------------------------+
|                  LAYER 3: AEAN (Cognitive Intelligence Substrate)                 |
|  - Multi-Agent Swarm Orchestration     - Graph-of-Thought (GoT) Reasoning          |
|  - Continuous World Model (E-K-C-T-U)  - Shared Multi-Tier Memory (CMOS/EMG)       |
|  - Strategic & Tactical Planners      - Skill Flywheel & Tool Invention           |
+-----------------------------------------------------------------------------------+
                                        |  Active Inference Sensing / Actions
                                        v
+-----------------------------------------------------------------------------------+
|               LAYER 2: EIOS / EOS (Orchestration & Business Execution)             |
|  - Multi-Timescale Business Loops     - Active Inference EFE Sensing Engine       |
|  - Capital Allocation State Machines  - Signal-to-Hypothesis Opportunity Filter   |
|  - 14-Layer Entrepreneurial Engine    - Lifecycle Stage & Reinvention Review      |
+-----------------------------------------------------------------------------------+
                                        |  Empirical Data / Validated Hypotheses
                                        v
+-----------------------------------------------------------------------------------+
|                     LAYER 1: Research OS (Scientific Foundation)                  |
|  - Scientific Hypothesis Generator    - Reproducibility & Audit Trail Engine      |
|  - Statistical Validation & CDF/DSR    - 300-Paper Corpus Knowledge Graph          |
|  - Multi-Paradigm Code Rewrite (STOP) - Genetic Program Synthesis (ShinkaEvolve)  |
+-----------------------------------------------------------------------------------+
```

---

## 2. Layer Definitions and Core Responsibilities

### Layer 1: Research OS (Scientific Research Layer)
* **Subsystem Alignment**: `apodex/research_os/`, `apodex/ai_eos/research/`
* **Core Responsibilities**:
  1. **Hypothesis Generation & Validation**: Formulates falsifiable scientific propositions and computes Deflated Sharpe Ratios (DSR) and standard normal PPF probability bounds.
  2. **Research Knowledge Graph**: Indexes 300 transferable research principles extracted across the 200-paper core corpus (`AI_EOS_RESEARCH_DB.yaml`) and 100-paper quantitative corpus (`ALPHA_ALGO_100_NEW_RESEARCH.yaml`).
  3. **Multi-Paradigm Code Mutation**: Executes self-referential AST code rewrites with static security linting and island-based genetic program synthesis (ShinkaEvolve).
  4. **Reproducibility & Statistical Controls**: Manages experiment hashing, metric parsing, and seed-controlled multi-run verification.

### Layer 2: EIOS / EOS (Orchestration & Business Execution Layer)
* **Subsystem Alignment**: `apodex/arcs/kernel/`, `apodex/ai_eos/intelligence/`
* **Core Responsibilities**:
  1. **Active Inference EFE Sensing**: Calculates Expected Free Energy ($EFE = \text{Pragmatic Value} + \text{Epistemic Information Gain}$) over market anomalies and operational state transitions.
  2. **Multi-Timescale Loop Execution**: Runs 13 coupled business loops across short-term operational execution (minutes/hours) to long-term strategic reinvention (years).
  3. **14-Layer Computational Architecture of Entrepreneurship**: Maps reality substrates, sensory integration, cognitive world modeling, game-theoretic negotiation, dynamic capital allocation, and meta-reinvention.
  4. **Capital Allocation & Opportunity Filtering**: Manages Kelly Criterion portfolio sizing, macroeconomic shock absorption, and lifecycle state transitions (Ideation $\rightarrow$ Scaling $\rightarrow$ Reinvention).

### Layer 3: AEAN (Cognitive Intelligence Substrate Layer)
* **Subsystem Alignment**: `apodex/cognition/`, `apodex/memory/`, `apodex/world_model/`, `apodex/skills/`, `apodex/planning/`
* **Core Responsibilities**:
  1. **Hierarchical & Swarm Collaboration**: Master-Coordinator-Worker orchestration with Graph-of-Thought (GoT) branching, merging, and pruning.
  2. **Continuous Multi-Graph World Model**: Maintains unified state across Entity ($G_E$), Knowledge ($G_K$), Causal ($G_C$), Temporal ($G_T$), and Uncertainty ($G_U$) graphs.
  3. **Multi-Tier Cognitive Memory**: Integrates Working Memory, Episodic Trajectories, Semantic Knowledge (Jaccard similarity retrieval), Procedural Skills, EMG Action-Decision Graphs, and CMOS Cognitive Memory.
  4. **Skill Flywheel & Tool Invention**: Auto-discovers reusable workflow patterns, registers operational skills with decay filtering, and manages skill execution runs.

### Layer 4: APODEX (Platform Decision & Execution Layer)
* **Subsystem Alignment**: `apodex/execution/`, `apodex/governance/`, `apodex/safety/`, `apodex/meta/`
* **Core Responsibilities**:
  1. **Personal Evolution Profiles (PEP)**: User-centric preference adaptation balancing quality, token efficiency, latency, and user satisfaction ($S(M) = w_q Q - w_t T - w_l L + w_s Sat$).
  2. **Tiered Governance & Immutable Safety Core**: Four-tier approval table (Tier 1 auto-approved prompt tweaks to Tier 4 cryptographically signed tenancy policies) enforcing non-bypassable security invariants.
  3. **Autonomous Software Engineering & Verifiers**: LLM-as-a-Judge, Introspective Critics, Grounded Fact-Checkers, and parallel domain verifiers.
  4. **Multi-Objective Routing**: Learns cost-optimal agent dispatch bounded by strict financial USD budgets.

---

## 3. Inter-Layer Interface Protocols

### 3.1 Research-to-Execution Bridge (`Layer 1 -> Layer 2`)
Implemented in `apodex/ai_eos/research/integration.py` (`ResearchToSystemBridge`):
- `export_validated_hypothesis_to_kernel(hypothesis)`: Transmits statistically validated scientific hypotheses from Research OS into EIOS Kernel active inference sensing queues.
- `promote_hypothesis_to_eos(hypothesis)`: Promotes hypotheses exceeding epistemic threshold to EOS state engines for capital allocation.

### 3.2 Execution-to-Cognition Bridge (`Layer 2 -> Layer 3`)
Implemented in `apodex/arcs/kernel/kernel.py` (`EIOSKernel`):
- `sense_opportunity_anomalies(data)`: Converts market and execution anomalies into EFE active inference goal vectors dispatched to AEAN planners.
- `allocate_capital_opportunity(opportunity_id, amount)`: Triggers AEAN multi-agent strategy swarms with explicit resource constraints.

### 3.3 Cognition-to-Platform Bridge (`Layer 3 -> Layer 4`)
Implemented in `apodex/cognition/brain.py` (`CognitiveBrain`):
- `execute_cognitive_cycle(goal, pep_profile)`: Invokes multi-agent GoT planning supervised by APODEX safety cores, cost scoring, and introspective critics.

---

## 4. Single Authority Subsystem Model

To eliminate logical duplication, authority over each primary system domain is strictly assigned to one canonical module:

| Domain | Canonical Subsystem Owner | Allowed Interface Adapters |
| :--- | :--- | :--- |
| **Research & Literature** | `Layer 1: ResearchOS` (`apodex/ai_eos/research/`) | `ResearchToSystemBridge` |
| **Active Inference & Business Sensing** | `Layer 2: EIOSKernel` (`apodex/arcs/kernel/`) | `EIOSKernel.sense_opportunity_anomalies` |
| **Entrepreneurial Execution & Capital** | `Layer 2: EOSEngine` (`apodex/ai_eos/intelligence/`) | `14LayerEngine` |
| **Multi-Agent Planning & Reasoning** | `Layer 3: AEAN Planners` (`apodex/planning/`, `apodex/cognition/`) | `HierarchicalOrchestrator` |
| **World Model Representation** | `Layer 3: WorldModel` (`apodex/world_model/`) | `IWorldModelService` |
| **Cognitive & Episodic Memory** | `Layer 3: MultiTierMemory` (`apodex/memory/`) | `EMGEngine`, `CMOS` |
| **Tool & Skill Invention** | `Layer 3: SkillRegistry` (`apodex/skills/`) | `ToolInventor` |
| **Governance & Personalization** | `Layer 4: APODEX Platform` (`apodex/governance/`, `apodex/safety/`) | `SafetyCore`, `PEP` |

---

## 5. Architectural Quality Guarantees

1. **Determinism and Reproducibility**: All statistical calculations clamp probability bounds and use seed-controlled random states.
2. **Horizontal Scalability**: Event-driven asynchronous message buses allow decoupled scaling across nodes without central locks.
3. **Institutional Reliability**: Subsystem failures trigger grace-degraded fallbacks without crashing execution loops.
