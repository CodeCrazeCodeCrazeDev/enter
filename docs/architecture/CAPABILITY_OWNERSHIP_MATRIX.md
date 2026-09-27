# Capability Ownership Matrix: Zero-Duplication Architecture

## Capability Allocation Across the 4 Cognitive Layers

| Capability / Functionality | Owning Layer | Implementation Path | Exclusively Owned Responsibilities | Banned Duplications |
| :--- | :--- | :--- | :--- | :--- |
| **Hypothesis Generation & Validation** | **Layer 1: Research OS** | `apodex.ai_eos.research.research_os`, `apodex.research_os.*` | Literature mining, Deflated Sharpe Ratio calculation, P-value correction, empirical hypothesis formulation | Executing hypotheses directly or instantiating swarms inside Research OS |
| **Active Inference DAG & Opportunity Sensing** | **Layer 2: EIOS / EOS** | `apodex.arcs.kernel.kernel`, `apodex.ai_eos.intelligence.eos_engine` | Opportunity graph sensing, Expected Free Energy calculation, DAG compilation, venture stage machines | Raw literature ingestion or low-level agent token bidding |
| **Multi-Agent Coordination & Swarm Bidding** | **Layer 3: AEAN Organism** | `apodex.aean.coordination.hive_mind`, `apodex.aean.agents.*` | Swarm token bidding, specialized agent dispatching, agent-to-agent communication, CMOS collective memory | Direct causal world graph manipulation without going through WorldModel |
| **Causal World Modeling & Safety Substrate** | **Layer 4: APODEX WorldModel** | `apodex.world_model.world_model`, `apodex.cognition.*` | CausalNode & RelationEdge graph, Bayesian belief updating, protocol safety verification, cost tier credit halt | High-level business opportunity scoring or unverified execution |

---

## Direct Interfaces Between Layers

1. **Layer 1 -> Layer 2:** `ResearchOS` -> `EIOSKernel.register_research_hypothesis()`
2. **Layer 2 -> Layer 3:** `EOSEngine` / `EIOSKernel` -> `HiveMind.register_task()`
3. **Layer 3 -> Layer 4:** `HiveMind` -> `WorldModel.create_node()` & `WorldModel.update_belief()`
4. **Layer 4 -> Layer 1/2:** `WorldModel` -> `ResearchToSystemBridge` -> `ResearchOS` / `EIOSKernel`
