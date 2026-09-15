# Unified Cognitive Operating System Architecture Specification
**Author:** Jules (Autonomous System Architect)
**Status:** Canonical Reference Architecture Specification
**Version:** 4.0.0 (2026 Edition)

---

## 1. Executive Summary & Design Philosophy

This specification establishes the authoritative single-layered architecture for the unified autonomous intelligence platform integrating **Research OS**, **EIOS**, **EOS**, **AEAN**, and **APODEX**.

Historically, these components evolved as distinct platforms with overlapping boundaries (e.g., duplicate memory stores, competing schedulers, redundant planning algorithms). This specification eliminates all architectural duplication by unifying the platform into a strict **4-Layer Cognitive Operating System Taxonomy**:

```
+-----------------------------------------------------------------------------------+
|                        LAYER 4: APODEX DECISION & EXECUTION PLATFORM              |
|   (WorldModel, Causal Graph, Recursive Bayesian Beliefs, Sandbox Runtime & Tools) |
+-----------------------------------------------------------------------------------+
                                         ^
                                         | State Updates & Belief Propagation
+-----------------------------------------------------------------------------------+
|                        LAYER 3: AEAN COGNITIVE INTELLIGENCE LAYER                  |
|   (HiveMind Multi-Agent Swarm, Token Bidding, EKG, Active Inference Engines)       |
+-----------------------------------------------------------------------------------+
                                         ^
                                         | Task Dispatch & Strategy Execution
+-----------------------------------------------------------------------------------+
|                        LAYER 2: EIOS / EOS EXECUTION & ORCHESTRATION LAYER        |
|   (Active Inference Sensing Kernel, Capital Allocation, 14-Layer Engine, State DAG)|
+-----------------------------------------------------------------------------------+
                                         ^
                                         | Scientific Hypotheses & Research Insights
+-----------------------------------------------------------------------------------+
|                        LAYER 1: RESEARCH OS (RESEARCH LAYER)                      |
|   (Corpus Ingestion, Literature Review, Hypothesis Testing, Reproducibility)      |
+-----------------------------------------------------------------------------------+
```

### Core Design Directives
1. **Zero Logical Duplication:** Every capability (planner, scheduler, memory engine, world model) has exactly one canonical owner across the 4 layers.
2. **First-Principles Active Inference:** System state transitions minimize Expected Free Energy (EFE) balancing epistemic value (information gain) and pragmatic value (goal achievement).
3. **Rigorous Layer Separation:** Upper layers consume abstractions provided by lower layers via type-safe, validated interface contracts.
4. **Institutional Reliability:** Every decision path is traceable to literature evidence (Layer 1), business strategy DAGs (Layer 2), multi-agent consensus (Layer 3), and causal world state verification (Layer 4).

---

## 2. Four-Layer Cognitive Taxonomy

### Layer 1: Research OS (Research Layer)
* **Canonical Responsibility:** Scientific discovery, empirical validation, paper corpus mining, and hypothesis generation.
* **Key Modules:** `apodex/ai_eos/research/research_os.py`, `apodex/research_os/`.
* **Primary Inputs:** Raw literature papers (YAML/JSON/PDF), experimental logs, benchmark result datasets.
* **Primary Outputs:** Validated scientific hypotheses, extracted transferable engineering principles (`ALPHAALGO_301_500_PRINCIPLES`), literature review synthesis.
* **Interface Contracts:**
  - `ResearchOS.export_validated_hypothesis_to_kernel()` -> Hands off validated hypotheses to Layer 2 EIOS Kernel.
  - `ResearchOS.promote_hypothesis_to_eos()` -> Feeds business/market hypotheses to Layer 2 EOS Engine.
  - `ResearchOS.conduct_literature_review()` -> Returns queryable literature evidence.

### Layer 2: EIOS / EOS (Execution and Orchestration Layer)
* **Canonical Responsibility:** System state machine, entrepreneurial opportunity sensing, capital allocation, 14-layer computational architecture execution, and workflow DAG orchestration.
* **Key Modules:** `apodex/arcs/kernel/kernel.py`, `apodex/ai_eos/intelligence/eos_engine.py`, `apodex/ai_eos/intelligence/fourteen_layer_engine.py`.
* **Primary Inputs:** Validated research hypotheses from Layer 1, market telemetry, operational goals.
* **Primary Outputs:** Executable task DAGs, opportunity decisions, capital allocation parameters, strategy dispatches.
* **Interface Contracts:**
  - `EIOSKernel.sense_opportunity_anomalies()` -> Calculates Expected Free Energy (EFE) over opportunities.
  - `EOSEngine.ingest_validated_research()` -> Updates active EOS hypothesis pool.
  - `FourteenLayerEntrepreneurialEngine.execute_layer_pipeline()` -> Processes end-to-end entrepreneurial lifecycle states.

### Layer 3: AEAN (Cognitive Intelligence Layer)
* **Canonical Responsibility:** Multi-agent collaboration, token bidding dispatch, Enterprise Knowledge Graph (EKG) reasoning, epistemic validation, and specialized cognitive engines.
* **Key Modules:** `apodex/aean/coordination/hive_mind.py`, `apodex/aean/ekg.py`, `apodex/aean/engines/`.
* **Primary Inputs:** Executable strategy dispatches from Layer 2, cognitive tasks.
* **Primary Outputs:** Agent swarm executions, validated code/plan rewrites, multi-agent consensus, token distribution logs.
* **Interface Contracts:**
  - `HiveMind.register_research_insight()` -> Binds research insights to token bidding priority queues.
  - `HiveMind.submit_task()` -> Dispatches tasks to specialized agent swarms via market auction.
  - `EKG.query_graph()` -> Provides graph reasoning for multi-agent execution.

### Layer 4: APODEX (Decision and Execution Platform Layer)
* **Canonical Responsibility:** Ground truth World Model, Causal Graph representation, Recursive Bayesian Belief updating, sandbox environment execution, safety gates, and telemetry.
* **Key Modules:** `apodex/world_model/`, `apodex/execution/`, `apodex/skills/`.
* **Primary Inputs:** Real-world execution actions, tool invocations, environment observations.
* **Primary Outputs:** Posterior belief updates, causal node updates, execution logs, safety approvals.
* **Interface Contracts:**
  - `WorldModel.update_entity_state()` -> Updates canonical entity states.
  - `WorldModel.update_bayesian_belief()` -> Updates prior to posterior based on observed evidence.
  - `SkillRegistry.get_skill()` -> Canonical skill execution interface.

---

## 3. Capability Ownership & Duplication Elimination Matrix

| Capability Area | Canonical Owner | Deprecated / Merged Redundancies | Rationale |
| :--- | :--- | :--- | :--- |
| **World Modeling & Causal State** | **Layer 4 (`apodex.world_model`)** | Merged duplicate world graphs in AEAN/EIOS | Single source of truth for causal graph and Bayesian beliefs prevents state drift. |
| **Task Planning & DAG Compilation** | **Layer 2 (`apodex.ai_eos.research.compiler`)** | Merged duplicate step decomposers in AgentHarness | EOS engine owns macro-planning; individual agents only execute micro-steps. |
| **Multi-Agent Coordination** | **Layer 3 (`apodex.aean.coordination.hive_mind`)** | Merged legacy parallel worker pools in AgentHarness | Token bidding mechanism provides economic optimization for agent allocation. |
| **Memory & Knowledge Management** | **Layer 3 (`AEAN EKG`) + Layer 4 (`WorldModel Beliefs`)** | Consolidated fragmented memory stores across layers | Epistemic knowledge resides in EKG; factual reality state resides in WorldModel. |
| **Skill Execution & Tooling** | **Layer 4 (`apodex.skills`)** | Aligned all 60 core/alias skills into SkillRegistry | Unified registry guarantees safe sandbox execution and consistent telemetry. |

---

## 4. Active Inference & Expected Free Energy (EFE) Dynamics

The unified system operates under a unified Active Inference formulation:

$$\mathbf{G}(\pi) = -\underbrace{\mathbb{E}_{q(o, \theta|\pi)}[\ln p(o|\theta) - \ln q(\theta|\pi)]}_{\text{Epistemic Value (Information Gain)}} - \underbrace{\mathbb{E}_{q(o|\pi)}[\ln p(o|C)]}_{\text{Pragmatic Value (Goal Utility)}}$$

1. **Layer 1 Research OS** maximizes **Epistemic Value** by identifying research gaps and high-variance hypothesis spaces.
2. **Layer 2 EIOS Kernel** evaluates **Expected Free Energy ($\mathbf{G}$)** over market opportunities to determine optimal strategy DAGs.
3. **Layer 3 AEAN HiveMind** allocates agent computational tokens proportional to the EFE reduction anticipated for each task node.
4. **Layer 4 APODEX WorldModel** performs Bayesian belief updating ($p(\theta|o) \propto p(o|\theta)p(\theta)$) upon observing execution outcomes.

---

## 5. Verification & Compliance Criteria

To ensure long-horizon reliability and zero regressions:
- Every code modification must pass 100% of the unit, integration, and cross-layer test suites.
- All 60 registered skills in `SkillRegistry` must be validated.
- All layer boundary interactions must log trace headers containing active hypothesis IDs.
