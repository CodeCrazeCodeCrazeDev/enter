# Unified Dependency Graph & Cross-Layer Interface Specification

## 1. Topographic Subsystem Dependency Diagram

```
+-------------------------------------------------------------------------------+
|                      LAYER 1: RESEARCH OS                                     |
|  - Literature Analysis (600 Paper Corpus)                                     |
|  - Statistical Validation (DSR, FDR)                                         |
|  - Code Rewrite Engine (AST Hawes Depth Checks)                               |
+-------------------------------------------------------------------------------+
                                      |
                                      | ResearchToSystemBridge
                                      v
+-------------------------------------------------------------------------------+
|                      LAYER 2: EIOS / EOS KERNEL                               |
|  - EIOS Kernel (Active Inference, EFE Sensing DAGs)                          |
|  - EOS Engine (Entrepreneurial State Machine, Capital Allocation)             |
+-------------------------------------------------------------------------------+
                                      |
                                      | EOSToHiveMindBridge
                                      v
+-------------------------------------------------------------------------------+
|                      LAYER 3: AEAN HIVEMIND                                   |
|  - HiveMind Coordination & Token Bidding Registry                             |
|  - Specialized Agent Clusters (Researcher, Planner, Coder, Auditor)           |
+-------------------------------------------------------------------------------+
                                      |
                                      | HiveMindToWorldModelBridge
                                      v
+-------------------------------------------------------------------------------+
|                      LAYER 4: APODEX WORLD MODEL                              |
|  - Causal Engine (Causal DAG, Relation Edge)                                  |
|  - Bayesian Belief Engine (Prior/Posterior Updates)                           |
|  - Safety Governance & Tiered Approval Engine                                 |
+-------------------------------------------------------------------------------+
                                      |
                                      +--- Feedback Loop to Layer 1 (Research Refinement)
```

---

## 2. Explicit Cross-Layer Interfaces

### Layer 1 -> Layer 2 Interface (`ResearchToSystemBridge`)
* **Input:** `ResearchHypothesis` (from Layer 1 `ResearchOS`).
* **Method:** `handoff_research_to_kernel(hypothesis, kernel)`
* **Output:** Instantiates Active Inference EFE sensing node in `EIOSKernel`.
* **Method:** `promote_hypothesis_to_eos(hypothesis, eos_engine)`
* **Output:** Ingests validated hypothesis into `EOSEngine.active_hypotheses`.

### Layer 2 -> Layer 3 Interface (`EOSToHiveMindBridge`)
* **Input:** `Opportunity` (from Layer 2 `EOSEngine`).
* **Method:** `handoff_eos_to_hive_mind(opportunity, hive_mind)`
* **Output:** Registers execution opportunity task in `HiveMind`, triggering token auctions for agent assignment.

### Layer 3 -> Layer 4 Interface (`HiveMindToWorldModelBridge`)
* **Input:** Execution results, tool outputs, and telemetry from Layer 3 agents.
* **Method:** `handoff_hive_mind_to_world_model(agent_results, world_model)`
* **Output:** Performs causal node creation (`CausalNode`), relation edge insertion (`RelationEdge`), and updates recursive Bayesian belief state (`BeliefNode`) in Layer 4 `WorldModel`.

---

## 3. Strict Module Import Boundaries

To prevent circular dependencies and capability duplication, module imports follow strict directional constraints:
1. `apodex.world_model` (Layer 4) imports only core utility/common types. It **NEVER** imports from Layer 1, 2, or 3.
2. `apodex.aean` (Layer 3) imports from Layer 4 models for state reporting, but never imports Layer 1 or 2 orchestration engines.
3. `apodex.arcs` and `apodex.ai_eos.intelligence` (Layer 2) import from Layer 4 for world state queries.
4. `apodex.ai_eos.research` (Layer 1) interacts with Layer 2, 3, and 4 exclusively via `ResearchToSystemBridge` in `apodex/ai_eos/research/integration.py`.
