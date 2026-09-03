# Unified Cognitive Architecture Specification

## 1. Vision & Architecture Overview

The Unified Cognitive Operating System integrates five historically distinct subsystems—**Research OS**, **EIOS**, **EOS**, **AEAN**, and **APODEX**—into a single, 4-layer cognitive architecture. Rather than operating as isolated or partially redundant platforms, these subsystems represent specific vertical layers of a unified autonomous intelligence lifecycle:

```
+-----------------------------------------------------------------------------------+
|                        LAYER 1: RESEARCH OS (Research Layer)                      |
| Scientific Literature Mining | Hypothesis Generation | Empirical Validation       |
+-----------------------------------------------------------------------------------+
                                          | Validated Hypotheses & Insights
                                          v
+-----------------------------------------------------------------------------------+
|                   LAYER 2: EIOS / EOS (Execution & Orchestration Layer)           |
| Active Inference Sensing | 14-Layer Business Engine | Opportunity DAG Dispatch|
+-----------------------------------------------------------------------------------+
                                          | Bidded Execution Tasks
                                          v
+-----------------------------------------------------------------------------------+
|                 LAYER 3: AEAN (Cognitive Intelligence Layer)                       |
| HiveMind Bidding | Graph-of-Thought Reasoning | Swarm Debate | Memory Consolidation|
+-----------------------------------------------------------------------------------+
                                          | Protocol Decisions & Trajectories
                                          v
+-----------------------------------------------------------------------------------+
|                 LAYER 4: APODEX (Decision & Execution Platform Layer)             |
| WorldModel Causal Graph | Recursive Bayesian Beliefs | Skill Registry Flywheel   |
+-----------------------------------------------------------------------------------+
```

---

## 2. Layer Taxonomy & Responsibilities

### Layer 1: Research OS (Research Layer)
* **Responsibility**: Scientific hypothesis formulation, literature synthesis, statistical validation, and academic knowledge extraction.
* **Key Components**: Literature review engine, hypothesis generator, reproducibility verifier, statistical validation module (`standard_normal_ppf`, DSR calculation).
* **Guiding Invariant**: Research OS never executes operational tasks or mutates environment states directly. It produces verified empirical hypotheses and statistical confidence bounds.

### Layer 2: EIOS / EOS (Execution & Orchestration Layer)
* **Responsibility**: Real-time environmental sensing (EIOS) and strategic computational entrepreneurship orchestration (EOS).
* **Key Components**: `EIOSKernel` (Active Inference Expected Free Energy sensing), `EOSEngine` (14-layer business computational state machine), coupled business loop compilers, risk & ROI monitors.
* **Guiding Invariant**: EIOS/EOS translates research hypotheses and raw market signals into executable task Directed Acyclic Graphs (DAGs) using Expected Free Energy minimization ($\Delta EFE = \Delta \text{Risk} + \Delta \text{Ambiguity}$).

### Layer 3: AEAN (Cognitive Intelligence Layer)
* **Responsibility**: Multi-agent coordination, cognitive task execution, reasoning under uncertainty, and skill synthesis.
* **Key Components**: `HiveMind` token-bidding coordinator, `GraphOfThoughtEngine` (GoT decomposition), island MAP-Elites workflow optimizer, `SFTPreferenceCollector`, and episodic memory consolidation.
* **Guiding Invariant**: AEAN agents bid for and execute DAG nodes allocated by EOS/EIOS without maintaining redundant enterprise state machines or duplicating causal world models.

### Layer 4: APODEX (Decision & Execution Platform Layer)
* **Responsibility**: Causal world modeling, recursive Bayesian belief updating, skill registry execution, and safety/governance enforcement.
* **Key Components**: `WorldModel` (CausalNode & RelationEdge graph), `SkillRegistry` (60 pre-populated operational skills), `ApprovalGate`, safety harness, and protocol runners.
* **Guiding Invariant**: APODEX serves as the single source of truth for reality state representations and physical/virtual execution.

---

## 3. Active Inference & Cross-Layer State Handoffs

Cross-layer state progression strictly obeys unidirectional active inference loops:

1. **Hypothesis Handoff ($L_1 \rightarrow L_2$)**: `ResearchOS` validates empirical principles (e.g., non-Gaussian Hawkes process stability) and exports a `ValidatedHypothesis` to `EIOSKernel`.
2. **Sensing & Opportunity Dispatch ($L_2 \rightarrow L_3$)**: `EIOSKernel` senses environmental anomalies against $L_1$ hypotheses, calculates Expected Free Energy (EFE), and compiles opportunity DAGs into `EOSEngine` tasks dispatched to `HiveMind`.
3. **Agent Coordination & Strategy ($L_3 \rightarrow L_4$)**: `HiveMind` agents bid for execution tasks using specialized capabilities, execute Graph-of-Thought reasoning, and issue protocol execution requests to `APODEX`.
4. **Belief Update & Reality State Mutation ($L_4 \rightarrow L_1$)**: `APODEX` executes actions via `SkillRegistry`, performs recursive Bayesian belief updates on `WorldModel`, and feeds observational residuals back to `ResearchOS` for hypothesis re-validation.

---

## 4. Architectural Invariants & Zero-Duplication Directives

* **Single World Model Invariant**: Only APODEX (`apodex/world_model`) maintains entity and belief state representations. All other layers query APODEX via read-only views.
* **Single Task Bidding Invariant**: Only AEAN HiveMind (`apodex/aean/coordination`) manages agent bidding and multi-agent coordination.
* **Single Business Loop Invariant**: Only EOS (`apodex/ai_eos/intelligence`) computes 14-layer entrepreneurial dynamics.
* **Single Hypothesis Invariant**: Only Research OS (`apodex/ai_eos/research`) performs literature review synthesis and statistical confidence validation.
