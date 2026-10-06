# CAPABILITY OWNERSHIP MATRIX

## Architectural Responsibility Boundaries

To guarantee zero duplication across subsystems, the **Unified Cognitive Operating System** enforces strict capability ownership boundaries. Each layer has exclusive domain ownership over specific functions.

---

## Detailed Capability Allocation

| Subsystem / Layer | Exclusive Capability Ownership | Prohibited Capabilities (Delegated Elsewhere) |
| :--- | :--- | :--- |
| **Layer 1: Research OS** | - Scientific paper ingestion & parsing<br>- Literature synthesis & literature review<br>- Hypothesis generation & $p$-value statistical validation<br>- Transferable engineering principle extraction | - *Forbidden*: Execution scheduling (delegated to Layer 2)<br>- *Forbidden*: Agent task bidding (delegated to Layer 3)<br>- *Forbidden*: Direct world state modification (delegated to Layer 4) |
| **Layer 2: EIOS / EOS** | - Expected Free Energy (EFE) pragmatic & epistemic computation<br>- Opportunity graph construction & sensing anomaly detection<br>- Execution DAG compilation & task priority ordering<br>- Entrepreneurial company growth state machine transitions | - *Forbidden*: Literature parsing (delegated to Layer 1)<br>- *Forbidden*: Multi-agent bidding execution (delegated to Layer 3)<br>- *Forbidden*: Substrate code mutation (delegated to Layer 3) |
| **Layer 3: AEAN** | - Multi-agent token bidding & resource auction registry<br>- Specialized agent execution (Coder, Critic, Planner, Architect)<br>- Hawkes AST recursion depth verification & code self-mutation<br>- Multi-agent swarm collaboration and consensus | - *Forbidden*: Scientific literature searching (delegated to Layer 1)<br>- *Forbidden*: Company GTM state machine modeling (delegated to Layer 2)<br>- *Forbidden*: Global causal belief propagation (delegated to Layer 4) |
| **Layer 4: APODEX** | - World state node creation & causal graph updates<br>- Recursive Bayesian belief updating & evidence propagation<br>- Protocol execution runner & sandbox runtime environment<br>- Credit assignment and global system telemetry tracking | - *Forbidden*: Research hypothesis synthesis (delegated to Layer 1)<br>- *Forbidden*: Task execution DAG creation (delegated to Layer 2)<br>- *Forbidden*: Code AST parsing (delegated to Layer 3) |

---

## Enforcement Mechanisms

1. **Imports Static Audit**: Root-level audit scripts (`check_layer_imports.py`) verify that modules do not import forbidden layer cross-dependencies.
2. **Atomic Bridge Routing**: All cross-layer state handoffs must route exclusively through `ResearchToSystemBridge` or typed layer interfaces (`register_research_hypothesis`, `register_research_insight`, `create_node`, `update_belief`).
