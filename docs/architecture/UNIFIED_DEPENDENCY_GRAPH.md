# Unified Cognitive OS: Layer Dependency & State Handoff Flow Graph

## 1. Direct Architectural Graph (DAG)

```
                       +-----------------------------------+
                       |    LAYER 1: RESEARCH OS           |
                       | (Hypothesis & Empirical Corpus)   |
                       +-----------------------------------+
                                         |
                                         |  Valid Hypotheses & Alpha Principles
                                         v
                       +-----------------------------------+
                       |    LAYER 2: EIOS / EOS            |
                       | (Active Inference DAG & Sensing)  |
                       +-----------------------------------+
                                         |
                                         |  Compiled Task Graphs & Allocations
                                         v
                       +-----------------------------------+
                       |    LAYER 3: AEAN ORGANISM         |
                       | (HiveMind Bidding & Swarm Agents) |
                       +-----------------------------------+
                                         |
                                         |  Action Trajectories & Execution Signals
                                         v
                       +-----------------------------------+
                       |    LAYER 4: APODEX WORLDMODEL     |
                       | (Causal Graph & Bayesian Beliefs) |
                       +-----------------------------------+
                                         |
                                         |  Posterior Re-prioritization / Dynamic Feedback
                                         +-----------------------+
                                                                 |
                                                                 v
                                                 (Loop back to Layer 1 & Layer 2)
```

---

## 2. Component Dependency Matrix

| Owning Subsystem | Module Path | Permitted Imports | Forbidden Imports |
| :--- | :--- | :--- | :--- |
| **Layer 1 (Research OS)** | `apodex.ai_eos.research.*`, `apodex.research_os.*` | Stdlib, `pydantic`, `numpy`, `scipy` | Layer 2, Layer 3, Layer 4 |
| **Layer 2 (EIOS / EOS)** | `apodex.arcs.kernel.*`, `apodex.ai_eos.intelligence.*` | Layer 1, Stdlib, `pydantic` | Layer 3 execution state, Layer 4 WorldModel directly |
| **Layer 3 (AEAN Organism)** | `apodex.aean.*` | Layer 1, Layer 2, Stdlib, `pydantic` | Bypassing Layer 4 safety kernel |
| **Layer 4 (APODEX WorldModel)**| `apodex.world_model.*`, `apodex.cognition.*` | Layer 1, Layer 2, Layer 3, Stdlib | Business logic outside WorldModel domain |

---

## 3. Active Inference Data Flow Sequence

1. **Research OS (Layer 1):** Validates hypothesis $H_k$ with statistical confidence ($p < 0.01$, DSR $> 1.0$).
2. **EIOS Kernel (Layer 2):** Ingests hypothesis $H_k$, calculates Expected Free Energy $G(a) = \text{Ambiguity}(a) + \text{Risk}(a)$, and compiles an execution DAG.
3. **AEAN HiveMind (Layer 3):** Dispatches sub-tasks from the execution DAG to specialized agent swarms via token bidding.
4. **APODEX WorldModel (Layer 4):** Executes verified tasks, updates CausalNodes, and computes Bayesian belief updates:
   $$P(\theta \mid y) \propto P(y \mid \theta) P(\theta)$$
5. **Feedback Loop:** Updated Bayesian belief variance $\sigma_{\theta}^2$ is propagated back to Layer 1 to validate or prune hypothesis $H_k$.
