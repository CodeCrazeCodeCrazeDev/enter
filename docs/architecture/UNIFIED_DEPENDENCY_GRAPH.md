# Unified Cognitive Operating System Dependency Graph

**Author:** Jules (Autonomous System Engineer)
**Status:** Approved Architecture Standard

---

## 1. High-Level Subsystem Interaction Flow

The following diagram details the directional flow of scientific hypotheses, strategic goals, execution tasks, world state queries, and recursive belief updates across the 4 integrated layers of the Cognitive Operating System:

```
                  +----------------------------------------------+
                  |         LAYER 1: RESEARCH OS LAYER           |
                  | (Hypothesis Generation & Statistical Check) |
                  +----------------------------------------------+
                                         |
                                         | Validated Scientific
                                         | Hypotheses (DSR & WRC)
                                         v
                  +----------------------------------------------+
                  |       LAYER 2: EIOS / EOS ENGINE LAYER       |
                  |  (Active Inference Sensing & DAG Compiler)   |
                  +----------------------------------------------+
                                         |
                                         | Task Bids & Compiled
                                         | Execution DAG Nodes
                                         v
                  +----------------------------------------------+
                  |       LAYER 3: AEAN COGNITION LAYER          |
                  | (HiveMind Bidding, Swarm & Skills Execution) |
                  +----------------------------------------------+
                                         |
                                         | Action Trajectories,
                                         | Tool Evidence & Claims
                                         v
                  +----------------------------------------------+
                  |     LAYER 4: APODEX WORLD MODEL PLATFORM     |
                  | (Entity Graph, Bayesian Beliefs, GRC Audit)  |
                  +----------------------------------------------+
```

---

## 2. Detailed Data Handoff and Interface Protocol

```mermaid
graph TD
    subgraph L1["Layer 1: Research OS"]
        R1[Literature Review & Synthesis] --> R2[Hypothesis Registration]
        R2 --> R3[Sandbox Walk-Forward Simulation]
        R3 --> R4[Statistical Validation: DSR & White's Reality Check]
    end

    subgraph L2["Layer 2: EIOS / EOS Engine"]
        E1[Active Inference Sensing Loop]
        E2[Strategic Goal Compiler - 14-Layer Engine]
        E3[Execution DAG Builder]
        E4[Expected Free Energy Policy Selection]
    end

    subgraph L3["Layer 3: AEAN Cognitive Intelligence"]
        A1[HiveMind Compute Token Bidding]
        A2[Hierarchical Multi-Agent Master/Coordinator]
        A3[Graph-of-Thought Reasoning & MCTS]
        A4[Skills Flywheel Execution Engine]
    end

    subgraph L4["Layer 4: APODEX World Model"]
        W1[Entity & Relationship Multi-Graph]
        W2[Recursive Bayesian Belief Updater]
        W3[Deep Causal Model - Pearl do-calculus]
        W4[Governance & GRC Audit Verification]
    end

    %% State Handoffs
    R4 -->|export_validated_hypothesis_to_kernel| E1
    E1 --> E2
    E2 --> E3
    E3 --> E4
    E4 -->|Task Bids| A1
    A1 --> A2
    A2 --> A3
    A3 --> A4
    A4 -->|Trajectory Trace & Evidence| W2
    W2 --> W1
    W1 --> W3
    W3 --> W4
    W4 -->|Feedback Signals & World Entropy| E1
```

---

## 3. Directional Module Call Hierarchy

| Source Layer & Module | Direction | Target Layer & Module | Interface Method / Protocol | Handoff Payload |
| :--- | :--- | :--- | :--- | :--- |
| **Layer 1:** `research_os.py` | $ \longrightarrow $ | **Layer 2:** `kernel.py` | `ResearchToSystemBridge.export_validated_hypothesis_to_kernel()` | Registered Hypothesis, P-value, Deflated Sharpe Ratio |
| **Layer 1:** `research_os.py` | $ \longrightarrow $ | **Layer 2:** `eos_engine.py` | `EOSEngine.ingest_validated_research()` | Validated scientific theory, effect size, statistical confidence |
| **Layer 2:** `kernel.py` | $ \longrightarrow $ | **Layer 3:** `hive_mind.py` | `HiveMind.arbitrate(bids)` | `TaskBid(task, priority, expected_value, token_cost)` |
| **Layer 3:** `hive_mind.py` | $ \longrightarrow $ | **Layer 3:** `hierarchical.py` | `HierarchicalOrchestrator.orchestrate()` | Granted task execution spec, role assignment |
| **Layer 3:** `hierarchical.py` | $ \longrightarrow $ | **Layer 4:** `beliefs.py` | `Belief.update_confidence()` | Likelihood score, prior probability, evidence hash |
| **Layer 4:** `beliefs.py` | $ \longrightarrow $ | **Layer 4:** `brain.py` | `CognitiveBrain.run_strategic_cycle()` | Bayesian belief state, Pearl do-calculus causal query |
| **Layer 4:** `brain.py` | $ \longrightarrow $ | **Layer 2:** `kernel.py` | `HierarchicalActiveInference.calculate_layer_free_energy()` | Variational Free Energy, world entropy, state feedback |

---

## 4. Active Inference Feedback Loops and State Verification

1. **Epistemic Feedback Loop:**
   - Unresolved uncertainty in Layer 4 World Model generates an epistemic curiosity demand signal.
   - Layer 2 Active Inference Planner routes curiosity demand to Layer 1 Research OS for literature review and hypothesis formulation.
2. **Pragmatic Feedback Loop:**
   - Layer 3 swarm action execution produces empirical outcomes.
   - Outcomes update Layer 4 Bayesian Belief distributions ($ P(B|E) $).
   - Reduced entropy stabilizes Layer 2 EIOS state machine transitions.
3. **Governance and Safety Guardrail:**
   - Before any Layer 3 action reaches Layer 4 persistence or real-world execution, Layer 4 Governance Framework evaluates Hendrycks safety constraints and GRC thresholds ($ \text{risk\_score} < 0.85 $).
