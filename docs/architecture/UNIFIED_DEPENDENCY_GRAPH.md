# Unified Dependency Graph & Interaction Flow

## 1. Subsystem Interdependency Matrix

The Unified Cognitive Operating System enforces a strict top-down execution flow and bottom-up feedback flow across all 4 layers. Direct lateral dependencies across non-adjacent layers are routed via `ResearchToSystemBridge`.

```
                  +------------------------------+
                  |    Layer 1: Research OS      |
                  +------------------------------+
                                 |
                                 | Validated Research Hypotheses (H_val)
                                 v
                  +------------------------------+
                  |    Layer 2: EIOS / EOS       |
                  +------------------------------+
                                 |
                                 | Synthesized Intent DAGs (D_intent)
                                 v
                  +------------------------------+
                  |    Layer 3: AEAN Swarm       |
                  +------------------------------+
                                 |
                                 | Executed Agent Actions & Bids
                                 v
                  +------------------------------+
                  |    Layer 4: APODEX           |
                  +------------------------------+
                                 |
                                 | Posterior Beliefs & Causal State
                                 +------------------------+
                                                          |
                                                          v
                                        +----------------------------------+
                                        | ResearchToSystemBridge Feedback  |
                                        +----------------------------------+
```

---

## 2. Event & Data Flow Specifications

### Flow A: Literature to Active Inference Sensing
1. `ResearchOS` processes raw literature via `ResearchIngestionPipeline`.
2. Validated claims yield a `ResearchHypothesis` object with status `validated`.
3. `ResearchOS.export_to_eios()` invokes `EIOSKernel.register_research_hypothesis()`.
4. `EIOSKernel` computes Expected Free Energy ($G$):
   $$G = -D_{KL}\left(q(o|a) \,||\, p(o)\right) + \mathbb{E}_{q(s|a)}\left[H(p(o|s))\right]$$

### Flow B: Active Inference Sensing to Swarm Bidding
1. `EIOSKernel.sense_opportunity_anomalies()` identifies state discrepancies.
2. `WorkflowCompiler` compiles the task into a directed acyclic graph (`IntentDAG`).
3. `EOSOpportunityDecisionTree` submits task nodes to `HiveMind.register_research_insight()`.
4. Specialized AEAN Agents evaluate tasks and post token bids based on skill confidence.

### Flow C: Execution to World Model Grounding
1. Winning AEAN agent executes task action $a_t$.
2. Execution generates an outcome signal $o_t$.
3. Outcome is dispatched to `WorldModel.create_node()` or `WorldModel.update_belief()`.
4. Bayesian belief engine updates posterior distribution:
   $$P(\theta | o_t) = \frac{P(o_t | \theta) P(\theta)}{P(o_t)}$$
5. `ResearchToSystemBridge.handshake_and_sync()` propagates updated beliefs back to Layer 1 and Layer 2 for closed-loop iteration.

---

## 3. Class-Level Import & Invocation Hierarchy

```
apodex.ai_eos.research.research_os.ResearchOS
    └── imports: apodex.ai_eos.research.integration.CodeRewriteEngine
    └── calls: EIOSKernel.register_research_hypothesis

apodex.arcs.kernel.kernel.EIOSKernel
    └── imports: apodex.ai_eos.intelligence.eos_engine.EOSEngine
    └── calls: HiveMind.register_research_insight

apodex.aean.coordination.hive_mind.HiveMind
    └── imports: apodex.arcs.agents.executive_agents
    └── calls: WorldModel.create_node / WorldModel.update_belief

apodex.world_model.world_model.WorldModel
    └── imports: apodex.world_model.domain.beliefs
    └── synchronized by: ResearchToSystemBridge
```
