# Unified Cognitive Operating System: Dependency Graph & Inter-Layer Contracts
**Version:** 1.0.0
**Status:** Canonical Reference Architecture

---

## 1. High-Level Directed Dependency Hierarchy

The platform enforces a strict acyclic top-down control dependency combined with bottom-up active inference observation streams. Higher layers issue strategic policies and constraints, while lower layers provide state estimates and surprise signals.

```
                  +-----------------------------------+
                  |      LAYER 1: RESEARCH OS         |
                  | Scientific Discovery & Hypotheses |
                  +-----------------------------------+
                                    |
                                    | Exposes: ResearchToSystemBridge
                                    | Ingests: Empirical Observations
                                    v
                  +-----------------------------------+
                  |        LAYER 2: EIOS / EOS        |
                  | Active Inference & EOS Lifecycle  |
                  +-----------------------------------+
                                    |
                                    | Exposes: Opportunity DAG Directives
                                    | Ingests: Swarm Execution Status
                                    v
                  +-----------------------------------+
                  |          LAYER 3: AEAN            |
                  | HiveMind Swarm & Code Synthesis   |
                  +-----------------------------------+
                                    |
                                    | Exposes: Action Tool Directives
                                    | Ingests: Skill Execution Results
                                    v
                  +-----------------------------------+
                  |         LAYER 4: APODEX           |
                  | World Model, Causal Graph & Skill |
                  +-----------------------------------+
```

---

## 2. Formal Python Module Dependency & Import DAG

To prevent cyclic dependencies and maintain clean architecture, module imports must adhere to the following layer graph:

```
apodex/ai_eos/research/ (Layer 1)
   |
   +---> Imports NO internal layers (Pure Domain Logic & Literature DB)
   |
   v
apodex/ai_eos/intelligence/ & apodex/arcs/kernel/ (Layer 2)
   |
   +---> Imports Layer 1: apodex.ai_eos.research.research_os
   |
   v
apodex/aean/ (Layer 3)
   |
   +---> Imports Layer 2: apodex.ai_eos.intelligence.eos_engine
   +---> Imports Layer 1: apodex.ai_eos.research.integration
   |
   v
apodex/world_model/ & apodex/skills/ (Layer 4)
   |
   +---> Imports Layer 3: apodex.aean.coordination.hive_mind
   +---> Imports Layer 2: apodex.arcs.kernel.kernel
   +---> Imports Layer 1: apodex.ai_eos.research.research_os
```

---

## 3. Inter-Layer Data Contracts & API Interfaces

### Interface L1 -> L2: Scientific Hypothesis Export Contract
* **Class:** `ResearchToSystemBridge` / `ResearchOS`
* **API Call:** `ResearchOS.conduct_literature_review(query: str) -> List[ResearchPrinciple]`
* **Contract Payload:**
  ```python
  {
      "hypothesis_id": "hyp_2026_042",
      "statement": "Non-Gaussian Hawkes AST mutations improve genetic optimizer convergence.",
      "confidence_interval": [0.88, 0.96],
      "dsr_score": 2.41,
      "p_value": 0.0012,
      "transferable_principles": ["P_302_NON_GAUSSIAN_HAWKES_STABILITY"]
  }
  ```

### Interface L2 -> L3: Opportunity Execution DAG Contract
* **Class:** `EOSEngine` / `EIOSKernel`
* **API Call:** `EOSEngine.ingest_validated_research(hypothesis: ValidatedHypothesis) -> StrategyDAG`
* **Contract Payload:**
  ```python
  {
      "dag_id": "dag_opt_901",
      "target_opportunity": "AUTONOMOUS_CODE_REFACTORING",
      "capital_allocated": 1500.0,
      "nodes": [
          {"id": "task_1", "action": "MUTATE_AST", "cost_limit": 50.0},
          {"id": "task_2", "action": "RUN_BENCHMARK_SUITE", "cost_limit": 100.0}
      ]
  }
  ```

### Interface L3 -> L4: Action Directive & Skill Execution Contract
* **Class:** `HiveMind` -> `SkillRunner`
* **API Call:** `HiveMind.dispatch_task(task_spec: TaskSpec) -> ExecutionResult`
* **Contract Payload:**
  ```python
  {
      "skill_id": "SKILL_014_AST_TRANSFORM",
      "protocol_id": "PROTO_CODE_REWRITE_V2",
      "token_budget": 250,
      "parameters": {
          "filepath": "apodex/cognition/brain.py",
          "hawkes_decay_rate": 0.05
      }
  }
  ```

### Interface L4 -> L1/L2/L3: Active Inference Observation & Anomaly Feedback
* **Class:** `WorldModel` / `BayesianBeliefEngine`
* **API Call:** `WorldModel.update_belief(observation: RealityObservation) -> AnomalySignal`
* **Contract Payload:**
  ```python
  {
      "node_id": "node_runtime_latency",
      "prior_belief_mean": 45.2,
      "observed_value": 112.8,
      "surprise_kl_divergence": 3.84,
      "recalibration_required": True
  }
  ```

---

## 4. Verification & Dependency Integrity

Dependency cleanliness is programmatically verified via `/home/jules/self_created_tools/check_layer_imports.py` and integration tests `tests/integration/test_unified_4layer_integration.py`.
