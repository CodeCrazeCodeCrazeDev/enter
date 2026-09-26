# Unified Cognitive Operating System Dependency Graph & Interface Protocols

## 1. System Dependency Topology

The following graph illustrates the strict directional dependency flow across the 4 layers of the Unified Cognitive Operating System.

Lower layers provide foundational capabilities to higher layers. Higher layers send feedback signals and belief updates back down to calibrate lower layer priors.

```
                  +-----------------------------------+
                  |           APODEX                  |
                  | Layer 4: Decision & Execution     |
                  +-----------------------------------+
                     ^              |              ^
                     |              | Belief       | Causal Updates
        Strategy     |              | Feedback     | & Guardrails
        Commitments  |              v              |
                  +-----------------------------------+
                  |            AEAN                   |
                  | Layer 3: Cognitive Intelligence   |
                  +-----------------------------------+
                     ^              |              ^
                     |              | Task         | Swarm Results
        Execution    |              | Signals      | & Bids
        DAGs         |              v              |
                  +-----------------------------------+
                  |         EIOS / EOS                |
                  | Layer 2: Execution & Orchestration|
                  +-----------------------------------+
                     ^              |              ^
                     |              | Anomaly      | Opportunity
        Validated    |              | Triggers     | Graph Nodes
        Hypotheses   |              v              |
                  +-----------------------------------+
                  |        Research OS                |
                  | Layer 1: Research Substrate       |
                  +-----------------------------------+
```

---

## 2. Cross-Layer Interface Contracts (`ResearchToSystemBridge`)

All cross-layer state handoffs are orchestrated through `ResearchToSystemBridge` located in `apodex.ai_eos.research.integration`.

### Contract 1: Layer 1 -> Layer 2 (Hypothesis Promotion)
- **Source:** `ResearchOS.formulate_hypothesis()`
- **Target:** `EOSEngine.ingest_validated_research()` & `EIOSKernel.register_research_hypothesis()`
- **Payload Protocol:**
  ```python
  {
      "hypothesis_id": str,
      "title": str,
      "category": str,
      "statistical_confidence": float, # e.g. DSR > 0.95
      "extracted_principles": List[str],
      "target_subsystem": "EIOS" | "EOS" | "AEAN" | "APODEX"
  }
  ```

### Contract 2: Layer 2 -> Layer 3 (Task & Opportunity Dispatch)
- **Source:** `EIOSKernel.compile_active_inference_dag()` & `EOSEngine.evaluate_opportunities()`
- **Target:** `HiveMind.register_research_insight()` & `HiveMind.submit_task_bid()`
- **Payload Protocol:**
  ```python
  {
      "opportunity_id": str,
      "expected_free_energy": float, # EFE = Pragmatic + Epistemic value
      "task_dag": List[Dict[str, Any]],
      "required_agent_specialization": List[str],
      "token_allocation": int
  }
  ```

### Contract 3: Layer 3 -> Layer 4 (Strategy Execution & Belief Update)
- **Source:** `HiveMind.resolve_bids_and_execute()`
- **Target:** `WorldModel.create_node()`, `WorldModel.update_belief()`, & `CognitiveBrain.step()`
- **Payload Protocol:**
  ```python
  {
      "execution_id": str,
      "causal_node_id": str,
      "observed_outcome": Dict[str, Any],
      "prior_belief_p": float,
      "posterior_belief_p": float,
      "approval_tier": "AUTOMATIC" | "HUMAN_REVIEW"
  }
  ```

---

## 3. Dependency Boundary Rules

To enforce modularity and eliminate technical debt, the following strict import rules are enforced by static analysis and unit tests:

1. **Rule 1 (No Inverted Imports):** `apodex.ai_eos.research` MUST NOT import `apodex.aean` or `apodex.world_model`.
2. **Rule 2 (Single Gateway):** Inter-layer communication MUST occur via `ResearchToSystemBridge` or explicitly defined re-exports in subsystem `__init__.py` files.
3. **Rule 3 (Zero Circular Dependencies):** Dependencies MUST form a Directed Acyclic Graph (DAG) across layers.
