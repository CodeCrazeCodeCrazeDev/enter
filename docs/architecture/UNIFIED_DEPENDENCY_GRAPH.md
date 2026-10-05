# Unified Cognitive Operating System Dependency Graph & Topology

## Direct Inter-Layer Dependency Matrix

The dependency structure follows a clean acyclic directed graph (DAG). Higher abstraction layers consume capabilities from lower platform layers through standardized interfaces.

```
                      +-----------------------------+
                      |   Layer 1: Research OS      |
                      +-----------------------------+
                                     |
                                     | Ingests Research Principles
                                     v
                      +-----------------------------+
                      |   Layer 2: EIOS / EOS       |
                      +-----------------------------+
                                     |
                                     | Dispatches Task Graphs & Insights
                                     v
                      +-----------------------------+
                      |   Layer 3: AEAN Coordination|
                      +-----------------------------+
                                     |
                                     | Persists Entities & Belief Updates
                                     v
                      +-----------------------------+
                      |   Layer 4: APODEX Platform  |
                      +-----------------------------+
```

---

## Detailed Component Dependency Table

| Source Subsystem | Target Subsystem | Handoff Contract / Interface | Data Payload / Protocol |
| :--- | :--- | :--- | :--- |
| **Research OS (L1)** | **EIOS Kernel (L2)** | `register_research_hypothesis(hyp)` | `Hypothesis` object (id, title, status, metric) |
| **Research OS (L1)** | **EOS Engine (L2)** | `ingest_validated_research(hyp)` | Promoted research hypothesis for decision tree integration |
| **EIOS Kernel (L2)** | **AEAN HiveMind (L3)** | `register_research_insight(insight)` | JSON insight payload for token-bidding task creation |
| **EOS Engine (L2)** | **AEAN PAEAN/ADE (L3)** | `compile_opportunity_dag(node)` | Execution task DAG with priority scores |
| **AEAN HiveMind (L3)**| **APODEX WorldModel (L4)**| `create_node(name, node_type)` | Causal entity node added to world graph |
| **AEAN RGAE (L3)** | **APODEX WorldModel (L4)**| `update_belief(subject, predicate, confidence)`| Bayesian belief update with supporting evidence |
| **APODEX Flywheel (L4)**| **CMOS Memory (L4)** | `store_episodic_memory(trace)` | SFT/DPO trajectory step and advantage margin |

---

## Decoupling & Isolation Invariants

To guarantee platform maintainability and prevent circular dependencies:

1. **Isolation of Research OS (L1)**: Research OS operates on scientific hypothesis abstractions. It does not contain execution logic for cloud infrastructure or financial payment gateways.
2. **Isolation of Orchestration (L2)**: EIOS/EOS compiles workflows into abstract DAGs and Active Inference plans. It delegates multi-agent role execution entirely to Layer 3.
3. **Isolation of Multi-Agent HiveMind (L3)**: AEAN manages agent token bidding and reasoning strategies without embedding direct database persistence or low-level OS drivers.
4. **Platform Execution Primacy (L4)**: APODEX provides foundational services (World Graph, Belief Engine, CMOS Memory, Governance Security Gateway). L4 remains completely agnostic of upper-layer domain business rules.
