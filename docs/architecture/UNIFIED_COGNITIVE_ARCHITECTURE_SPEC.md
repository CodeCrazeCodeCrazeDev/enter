# Unified Cognitive Architecture Specification: AEAN / EIOS / EOS / APODEX

## 1. Executive Summary & Core Philosophy

The APODEX Cognitive Operating System integrates five historically distinct subsystems (**Research OS**, **EIOS**, **EOS**, **AEAN**, and **APODEX Core Platform**) into a unified, 4-layer cognitive architecture. Rather than treating these components as isolated or partially redundant platforms, this specification establishes a single layered taxonomy with explicit interfaces, mathematical handoffs, and zero duplicated responsibilities.

### The Unified 4-Layer Cognitive Taxonomy

1. **Layer 1: Scientific Research Layer (Research OS)**
   - **Responsibility**: Scientific discovery, literature ingestion, hypothesis formulation, statistical validation (Sequential Monte Carlo / DSR / Holm-Bonferroni), and transferable principle extraction across research corpora.
   - **Output**: Validated, statistically rigorous scientific hypotheses and transferable engineering principles.

2. **Layer 2: Strategic Sensing & System Decision Layer (EIOS / EOS)**
   - **Responsibility**: Entrepreneurial opportunity sensing, 14-layer entrepreneurial engine orchestration, capital allocation, risk modeling, and Active Inference Expected Free Energy (EFE) state reduction.
   - **Output**: Prioritized opportunity DAGs, capital allocation mandates, and strategic decision vectors.

3. **Layer 3: Multi-Agent Cognitive Intelligence Layer (AEAN)**
   - **Responsibility**: HiveMind multi-agent coordination, token-bidding task execution, specialization, credit assignment, and long-horizon strategy decomposition.
   - **Output**: Executable agent work plans, swarm consensus trajectories, and verified code/reasoning proposals.

4. **Layer 4: Decision Platform & World Engine (APODEX Platform / WorldModel)**
   - **Responsibility**: Predictive Bayesian world modeling, dynamic causal graph updates, skill execution flywheel, safety policy enforcement, and persistent state management.
   - **Output**: Grounded world state, counterfactual simulations, and safe tool execution environments.

---

## 2. Layer-by-Layer Architectural Specification

### Layer 1: Research OS (Research Layer)
- **Primary Domain**: `apodex.research_os` & `apodex.ai_eos.research`
- **Key Modules**:
  - `StatisticalValidator`: Computes Deflated Sharpe Ratio (DSR), false discovery rate control via Holm-Bonferroni, and inverse CDF probability bounds.
  - `ReproducibilityEngine`: Evaluates experimental replication fidelity and type-safe metric parsing.
  - `CodeRewriteEngine`: Evaluates non-Gaussian Hawkes stability with per-function recursion AST depth checks.
- **Explicit Interfaces**:
  - `export_validated_hypothesis_to_kernel()`: Hands off validated research hypotheses to Layer 2.
  - `register_301_500_paper_corpus_principles()`: Indexes extracted transferable principles for cross-layer query.

### Layer 2: EIOS / EOS (Execution & Orchestration Layer)
- **Primary Domain**: `apodex.arcs.kernel` & `apodex.ai_eos.intelligence`
- **Key Modules**:
  - `EIOSKernel`: Active Inference EFE engine computing epistemic value ($G_{epistemic}$) and pragmatic value ($G_{pragmatic}$).
  - `EOSEngine` / `FirstPrinciplesEOSEngine`: 11-section EOS system dynamics engine and 14-Layer Computational Engine of Entrepreneurship.
  - `GrowthStageClassifier` & `MoatAnalyzer`: Automated unit economic diagnostics and defensibility scoring.
- **Explicit Interfaces**:
  - `ingest_validated_research()`: Accepts Layer 1 hypotheses into active sensing DAGs.
  - `promote_hypothesis_to_eos()`: Converts sensed opportunity anomalies into formal strategic bets.

### Layer 3: AEAN (Cognitive Intelligence Layer)
- **Primary Domain**: `apodex.aean`
- **Key Modules**:
  - `HiveMind`: Token-bidding multi-agent coordinator allocating tasks based on agent specialization and belief alignment.
  - `SFTPreferenceCollector`: Collects trajectory advantages with clipped margin penalties.
  - `GeneticWorkflowOptimizer`: Island MAP-Elites migration gates with fitness-ranked sorting.
- **Explicit Interfaces**:
  - `register_research_insight()`: Maps Layer 1 research insights into HiveMind token bidding registry.
  - `submit_agent_plan()`: Submits swarm-verified execution steps to Layer 4 World Model.

### Layer 4: APODEX (Decision Platform & World Engine)
- **Primary Domain**: `apodex.world_model`, `apodex.cognition`, `apodex.skills`
- **Key Modules**:
  - `WorldModel`: Causal graph (`CausalNode`, `RelationEdge`) maintaining recursive Bayesian belief updates.
  - `SkillsFlywheel`: Protocol loader and budget-gated step executor.
  - `CognitiveBrain`: Central Pydantic V2 decision brain coordinating memory and world model queries.
- **Explicit Interfaces**:
  - `update_causal_graph()`: Ingests observation outcomes from Layer 3 agent actions.
  - `evaluate_counterfactual()`: Runs world model simulations before strategic commit.

---

## 3. Cross-Layer State Handoff & Active Inference Cycle

```
  +-----------------------------------------------------------------------+
  |                        LAYER 1: RESEARCH OS                           |
  |  - Ingest Research Papers   - Formulate Hypotheses   - DSR Validation |
  +-----------------------------------+-----------------------------------+
                                      | Validated Hypotheses & Principles
                                      v
  +-----------------------------------------------------------------------+
  |                        LAYER 2: EIOS / EOS                            |
  |  - Active Inference Sensing - 14-Layer Engine - Capital Allocation    |
  +-----------------------------------+-----------------------------------+
                                      | Strategic Decisions & Opportunities
                                      v
  +-----------------------------------------------------------------------+
  |                          LAYER 3: AEAN                                |
  |  - HiveMind Token Bidding  - Multi-Agent Swarm  - MAP-Elites Workflow |
  +-----------------------------------+-----------------------------------+
                                      | Verified Executable Trajectories
                                      v
  +-----------------------------------------------------------------------+
  |                   LAYER 4: APODEX WORLD MODEL                         |
  |  - Causal Graph Updates    - Bayesian Beliefs   - Skill Execution     |
  +-----------------------------------+-----------------------------------+
                                      | Grounded World Observation State
                                      +------------------(Feedback Loop)--+
```

---

## 4. Elimination of Redundant Responsibilities

1. **Unified Planning**: Planning logic is consolidated in Layer 2 (Strategic Active Inference Planning) and Layer 3 (Agent Swarm Step Execution). Legacy duplicate planner implementations in `AgentHarness` are accessed via clean adapter interfaces without duplicating core state.
2. **Unified World Modeling**: All causal graph updates and Bayesian belief updates reside strictly in Layer 4 (`apodex.world_model`).
3. **Unified Memory Hierarchy**: All persistent semantic memory and trajectory datasets are governed via Layer 4 memory managers, accessible by Layer 3 agents during execution.
