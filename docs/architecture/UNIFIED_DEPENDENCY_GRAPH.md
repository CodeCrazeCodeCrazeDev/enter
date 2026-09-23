# Unified Cognitive Operating System Dependency Graph
## Layered Topology, Import Structures, and Decoupling Constraints

---

## 1. Structural Layer Dependency Graph

The structural dependency graph below models the unidirectional flow of control, state handoffs, and data propagation across all four layers of the unified cognitive operating system:

```
===================================================================================================
LAYER 1: RESEARCH OS (Scientific Discovery & Principles)
   [ apodex.research_os ] <-----> [ apodex.ai_eos.research.integration ]
             |
             | Promotes Validated Hypotheses & Extracted Principles
             v
LAYER 2: EIOS / EOS (Execution & Strategic Orchestration Layer)
   [ apodex.arcs.kernel ] (EIOS Kernel) <-----> [ apodex.ai_eos.intelligence ] (EOS Engine)
             |
             | Compiles Opportunity DAGs & Dispatches Active Inference Directives
             v
LAYER 3: AEAN (Cognitive Intelligence & Multi-Agent Network Layer)
   [ apodex.aean.coordination ] (HiveMind) <-----> [ apodex.aean.engines ]
             |
             | Bids Tokens, Coordinates Specialized Agents & Executes Action Trajectories
             v
LAYER 4: APODEX (Decision, State & Platform Execution Layer)
   [ apodex.world_model ] <-----> [ apodex.memory.cmos ] <-----> [ apodex.cognition.brain ]
===================================================================================================
```

---

## 2. Cross-Subsystem Import Flow & Module Boundaries

To enforce institutional-grade maintainability and prevent circular import bottlenecks, module dependencies strictly follow a top-down hierarchy:

```
                      +-----------------------------+
                      |    apodex.research_os       | (Layer 1)
                      +--------------+--------------+
                                     |
                                     v
                      +-----------------------------+
                      |     apodex.arcs.kernel      | (Layer 2)
                      |   apodex.ai_eos.intelligence|
                      +--------------+--------------+
                                     |
                                     v
                      +-----------------------------+
                      |   apodex.aean.coordination  | (Layer 3)
                      +--------------+--------------+
                                     |
                                     v
                      +-----------------------------+
                      |     apodex.world_model      | (Layer 4)
                      |     apodex.memory.cmos      |
                      +-----------------------------+
```

---

## 3. Strict Boundary Constraints & Decoupling Rules

1. **Unidirectional Control Flow**:
   - Lower layers (e.g. Layer 4 WorldModel or Layer 3 AEAN) must **never** import or invoke higher-layer orchestrators (e.g. Layer 1 ResearchOS or Layer 2 EOSEngine).
   - Higher layers trigger lower layers via standardized interfaces and event callbacks.

2. **Single Canonical Ownership**:
   - Multi-Tier Memory logic belongs strictly to `apodex.memory.cmos`.
   - Multi-Graph World Model state belongs strictly to `apodex.world_model`.
   - Active Inference DAG execution belongs strictly to `apodex.arcs.kernel`.
   - Multi-Agent Token Bidding belongs strictly to `apodex.aean.coordination.hive_mind`.

3. **Stateless Integration Bridge**:
   - `ResearchToSystemBridge` in `apodex.ai_eos.research.integration` operates as a stateless glue adapter that orchestrates cross-layer method invocations without storing independent duplicate state.
