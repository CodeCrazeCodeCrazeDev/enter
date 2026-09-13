# Unified Cognitive Architecture Specification

**Author:** Jules (Autonomous System Engineer)
**Status:** Approved Architecture Standard
**Taxonomy:** Unified 4-Layer Cognitive Operating System

---

## Executive Summary

This specification establishes the authoritative **Unified Cognitive Operating System Architecture**, transforming **Research OS, EIOS, EOS, AEAN, and APODEX** into a single, seamless, multi-layer autonomous intelligence platform.

Rather than maintaining five partially overlapping or competing software boundaries, this architecture unifies all cognitive capabilities into a 4-layer functional hierarchy with zero capability duplication and single authority ownership.

```
+-----------------------------------------------------------------------------------+
|                        LAYER 4: APODEX WORLD MODEL PLATFORM                      |
| (World Model, Causal Graph, Entities, Recursive Bayesian Beliefs, Governance GRC) |
+-----------------------------------------------------------------------------------+
                                         ^
                                         | World State Updates & Beliefs
                                         v
+-----------------------------------------------------------------------------------+
|                        LAYER 3: AEAN COGNITIVE INTELLIGENCE                       |
|   (HiveMind Token Bidding, Graph-of-Thought, Swarm Execution, Skills Flywheel)    |
+-----------------------------------------------------------------------------------+
                                         ^
                                         | Task Dispatch & Swarm Execution
                                         v
+-----------------------------------------------------------------------------------+
|                     LAYER 2: EIOS / EOS EXECUTION & ORCHESTRATION                 |
| (Active Inference EFE Sensing, 14-Layer Engine, System State Machine, DAG Compiler)|
+-----------------------------------------------------------------------------------+
                                         ^
                                         | Validated Research Hypotheses
                                         v
+-----------------------------------------------------------------------------------+
|                            LAYER 1: RESEARCH OS LAYER                             |
| (Scientific Hypothesis Generation, Walk-Forward Validation, 500-Paper Corpus)     |
+-----------------------------------------------------------------------------------+
```

---

## 1. Architectural Principles & Single Authority Model

To avoid architectural duplication, split-brain state, and redundant orchestration loops, the platform adheres strictly to the **Single Authority Model**:

| Domain / Responsibility | Canonical Single Authority | Primary Module Location |
| :--- | :--- | :--- |
| **Scientific Research & Literature** | **Layer 1: Research OS** | `apodex/ai_eos/research/` |
| **Sensing, Orchestration & State Machine** | **Layer 2: EIOS / EOS Engine** | `apodex/arcs/kernel/`, `apodex/ai_eos/intelligence/` |
| **Multi-Agent Coordination & Swarms** | **Layer 3: AEAN HiveMind** | `apodex/aean/coordination/`, `agent_harness/` |
| **World Modeling & Persistent Memory** | **Layer 4: APODEX Platform** | `apodex/world_model/`, `apodex/cognition/` |

---

## 2. Layer-by-Layer Architectural Specification

### Layer 1: Research OS (Research Layer)
* **Primary Objective:** Autonomous scientific discovery, literature synthesis, hypothesis generation, and walk-forward statistical validation.
* **Core Subsystems:**
  - **Hypothesis Engine:** Manages hypothesis registration, null hypotheses, target metrics, and significance levels ($ \alpha = 0.05 $).
  - **Statistical Validation Engine:** Conducts walk-forward validation, White's Reality Check (WRC), and Deflated Sharpe Ratio (DSR) adjustments.
  - **Research Corpus Database:** Incorporates 500 peer-reviewed paper principles (Papers 1-500 in `AI_EOS_RESEARCH_DB.yaml` and `ALPHA_ALGO_*_RESEARCH.yaml`).
* **Interfaces & State Handoffs:**
  - Exports validated scientific hypotheses (`is_statistically_significant == True`) to Layer 2 via `ResearchToSystemBridge` and `export_validated_hypothesis_to_kernel()`.

---

### Layer 2: EIOS / EOS Engine (Execution & Orchestration Layer)
* **Primary Objective:** Active Inference sensing, Expected Free Energy (EFE) minimization, DAG compilation, financial budget allocation, and business state machine transitions.
* **Core Subsystems:**
  - **EIOS Kernel (`kernel.py`):** Directed Acyclic Graph (DAG) compilation, node dispatching, auto-retry failure recovery, and model routing.
  - **14-Layer Entrepreneurial Engine (`fourteen_layer_engine.py`):** First-principles computational models for reality substrate sensing, opportunity trees, customer lifecycles, unit economics, moat analysis, and failure mode prediction.
  - **Active Inference Planner (`strategic_planner.py`):** Computes policy Expected Free Energy ($ G = - \text{Pragmatic Value} - \gamma \times \text{Epistemic Value} $).
* **Interfaces & State Handoffs:**
  - Receives research hypotheses from Layer 1.
  - Compiles execution goals into DAG nodes and dispatches task bids to Layer 3 AEAN HiveMind.

---

### Layer 3: AEAN (Cognitive Intelligence Layer)
* **Primary Objective:** Multi-agent collaboration, Graph-of-Thought (GoT) reasoning, swarm execution, SFT preference collection, and skills flywheel execution.
* **Core Subsystems:**
  - **HiveMind Token Bidding (`hive_mind.py`):** Allocates compute tokens to tasks based on strategic priority, expected value, and second-price clearing.
  - **Multi-Agent Orchestrator (`hierarchical.py`):** Master -> Coordinator -> Specialized Worker execution hierarchy.
  - **Skills Flywheel Registry (`registry.py`):** Pre-populated with 60 operational and strategic skills with automated revalidation and usage attribution.
  - **Self-Improvement Engine:** On-policy advantage estimation and DPO preference dataset compilation (chosen vs rejected trajectory pairs).
* **Interfaces & State Handoffs:**
  - Receives dispatched tasks from Layer 2.
  - Executes tool actions and feeds trajectory traces and belief updates to Layer 4 APODEX.

---

### Layer 4: APODEX (Decision & Execution Platform Layer)
* **Primary Objective:** Ground truth world modeling, entity state management, recursive Bayesian belief updating, causal SCM graphs, and regulatory compliance/governance.
* **Core Subsystems:**
  - **World Model Graph (`entities.py`, `beliefs.py`):** Multi-graph storage tracking entities, relationships, timelines, environments, and uncertainty distributions.
  - **Recursive Bayesian Belief Engine (`beliefs.py`):** Continuous updating ($ P(B|E) = \frac{P(E|B) \cdot P(B)}{P(E)} $) of epistemic confidence scores.
  - **Deep Causal Engine (`brain.py`):** Judea Pearl's do-calculus ($ \text{do}(X=x) $) for counterfactual scenario analysis.
  - **Governance & Compliance Framework (`approval.py`):** Automated GRC policy evaluation and risk threshold enforcement.
* **Interfaces & State Handoffs:**
  - Serves as the authoritative source of truth for Layer 1, Layer 2, and Layer 3 queries.
  - Persists system state, lessons, and world changes across execution cycles.

---

## 3. Redesign and Elimination of Architectural Weaknesses

1. **Elimination of Duplicated Responsibilities:**
   - *Legacy Issue:* Both Research OS and AEAN maintained independent memory and reasoning stores.
   - *Superior Design:* All memory management is centralized in Layer 4 (APODEX World Model and `AdvancedMemoryEngine`), while AEAN focuses exclusively on cognitive execution and token bidding.
2. **Elimination of Split-Brain Orchestration:**
   - *Legacy Issue:* EIOS Kernel and AgentHarness each attempted to schedule top-level execution loops.
   - *Superior Design:* Layer 2 EIOS Kernel acts as the single master DAG compiler, while Layer 3 AEAN acts as the agent swarm execution framework.
3. **Closing Research Gaps:**
   - Integrated non-Gaussian Hawkes stability, MAP-Elites island migration gates, trajectory distance penalties for DPO, and do-calculus EFE task routing across all layers.

---

## 4. Institutional-Grade Reliability & Verification

- ** Hermetic Offline Replicability:** Deterministic random seeds and SHA-256 reproducibility hashes.
- **Data Leakage Safeguards:** Structural train/test set key intersection validation.
- **Syntax and GRC AST Audits:** Automated AST linting blocking `eval`, `exec`, or `os.system` injections during dynamic code mutation.
