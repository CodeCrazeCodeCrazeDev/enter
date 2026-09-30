# Capability Ownership Matrix Across Layers
**Author:** Strategic Architecture Lead & AI Engineering Core
**Version:** 4.0.0 (2026 Sovereign Edition)

---

## 1. Single Responsibility Principle (SRP) Enforcement

To prevent capability duplication, circular dependencies, and state fragmentation across Research OS, EIOS, EOS, AEAN, and APODEX, every cognitive capability is assigned strictly to **exactly one** primary layer.

---

## 2. Exhaustive Capability Allocation Matrix

| Cognitive Capability | Primary Owner Layer | Module Path | Strict Exclusions & Non-Overlapping Rules |
| :--- | :--- | :--- | :--- |
| **Paper Corpus Ingestion & Literature Querying** | **Layer 1 (Research OS)** | `apodex/ai_eos/research/research_os.py` | Layer 2, Layer 3, and Layer 4 MUST NOT query paper corpora directly; they query Layer 1 via `conduct_literature_review`. |
| **Statistical Hypothesis Validation (DSR, Hawkes)** | **Layer 1 (Research OS)** | `apodex/research_os/statistical_validation.py` | Statistical hypothesis tests (e.g. Deflated Sharpe Ratio) are strictly forbidden in downstream layers. |
| **Active Inference DAG Compilation & Scheduling** | **Layer 2 (EIOS Kernel)** | `apodex/arcs/kernel/kernel.py` | AEAN swarms MUST NOT create system-wide execution DAGs. They execute tasks inside assigned DAG nodes. |
| **Entrepreneurial Opportunity & Capital Allocation** | **Layer 2 (EOS Engine)** | `apodex/ai_eos/intelligence/eos_engine.py` | EOS Engine owns opportunity tree evaluation, financial risk modeling, and capital allocation. |
| **Multi-Agent Token Economy Bidding Registry** | **Layer 3 (AEAN HiveMind)**| `apodex/aean/coordination/hive_mind.py` | Task bidding and agent token economics exist strictly within Layer 3. |
| **Graph-of-Thought (GoT) Reasoning & Code Synthesis** | **Layer 3 (AEAN Engine)** | `apodex/aean/core.py` | Code synthesis, AST mutations, and LLM reasoning steps belong exclusively to Layer 3. |
| **Causal Bayesian Graph & Belief Propagation** | **Layer 4 (APODEX WorldModel)** | `apodex/world_model/world_model.py` | World state graph maintenance (`CausalNode`, `RelationEdge`, `BayesianBelief`) is exclusively Layer 4. |
| **Cognitive Brain & Safety/Governance Controller** | **Layer 4 (APODEX Cognition)** | `apodex/cognition/brain.py`, `controller.py` | Overall cognitive state evaluation and safety halt triggers are owned by Layer 4. |

---

## 3. Interface Access Rules

1. **Layer 1 Access:** Exposes `ResearchHypothesis` and `conduct_literature_review`.
2. **Layer 2 Access:** Exposes `register_research_hypothesis`, `compile_dag`, and `active_hypotheses`.
3. **Layer 3 Access:** Exposes `HiveMind.bid_for_task`, `register_research_insight`, and `execute_agent_workflow`.
4. **Layer 4 Access:** Exposes `WorldModel.create_node`, `WorldModel.update_belief`, and `CognitiveBrain.step_cognitive_cycle`.
