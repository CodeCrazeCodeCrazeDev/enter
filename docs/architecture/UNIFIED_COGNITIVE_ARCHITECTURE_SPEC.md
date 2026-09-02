# Unified Cognitive Architecture Specification

## 1. Architectural Vision & First Principles

The APODEX Cognitive Operating System integrates five historically distinct subsystems—**Research OS**, **EIOS**, **EOS**, **AEAN**, and **APODEX**—into a unified, 4-layer cognitive platform. Rather than operating as isolated silos or duplicate platforms, each component occupies a precise functional layer with strict interface boundaries, zero duplicated capabilities, and explicit cross-layer active inference state transitions.

```
+-----------------------------------------------------------------------------------+
| LAYER 1: RESEARCH OS (Research & Scientific Validation)                           |
| - Literature ingestion (500+ paper corpus), hypothesis generation, DSR testing    |
| - Statistical validation (E-values, sequential probability ratio tests, alpha)    |
+-----------------------------------------------------------------------------------+
                                         |  (Hypothesis Export & E-Value Handshake)
                                         v
+-----------------------------------------------------------------------------------+
| LAYER 2: EIOS / EOS (Execution, Sensing & Strategic Orchestration)               |
| - EIOS Kernel: Active Inference Expected Free Energy (EFE) anomaly sensing         |
| - EOS Engine: 14-Layer Computational Architecture, 11-section business dynamics   |
+-----------------------------------------------------------------------------------+
                                         |  (Opportunity DAG & EFE Priority Vector)
                                         v
+-----------------------------------------------------------------------------------+
| LAYER 3: AEAN (Cognitive Intelligence & Multi-Agent Layer)                        |
| - HiveMind token bidding, Swarm debate, Island MAP-Elites genetic workflows       |
| - CMOS hierarchical memory (Episodic, Semantic, Working, Action-Decision Graph)   |
+-----------------------------------------------------------------------------------+
                                         |  (Bidded Execution Tasks & Skill Commands)
                                         v
+-----------------------------------------------------------------------------------+
| LAYER 4: APODEX (Decision Engine, World Model & Platform Execution)               |
| - WorldModel: Causal graph, Entity/Relation state, Bayesian belief updates        |
| - ProtocolLoader, Tiered Approval Governance, Credit Halt & Cost Cutting Safeguards|
+-----------------------------------------------------------------------------------+
```

---

## 2. Layer Definitions & Capability Allocation

| Layer | System | Scope of Responsibility | Key Modules & Classes |
|---|---|---|---|
| **Layer 1** | **Research OS** | Scientific literature review, hypothesis generation, empirical experiment design, DSR statistical validation, publication tracking. | `apodex/ai_eos/research/research_os.py`, `apodex/research_os/statistical_validation.py` |
| **Layer 2** | **EIOS / EOS** | Opportunity sensing via Active Inference EFE, 14-layer business dynamics modeling, state machine strategy formulation, market coupling. | `apodex/arcs/kernel/kernel.py`, `apodex/ai_eos/intelligence/eos_engine.py`, `fourteen_layer_engine.py` |
| **Layer 3** | **AEAN** | Multi-agent coordination, HiveMind token bidding, swarm debate consensus, genetic workflow optimization, non-Gaussian Hawkes code rewrite, CMOS memory. | `apodex/aean/coordination/hive_mind.py`, `apodex/memory/cmos.py`, `agent_harness/core/runtime/` |
| **Layer 4** | **APODEX** | World state persistence, causal belief networks, tool/protocol execution, cost governance, risk halting, safety verification. | `apodex/world_model/world_model.py`, `apodex/skills/runner.py`, `apodex/governance/approval.py` |

---

## 3. Redesign of Core Cognitive Systems

### 3.1 Planning and Long-Horizon Execution
- **Mechanisms**: Integrates Do-Calculus Causal Planning (`AdvancedCausalEngine`) with Active Inference EFE minimization. Plans are decomposed into directed acyclic graphs (DAGs) in Layer 2 and executed via token bidding in Layer 3.
- **Uncertainty Quantification**: Expected Free Energy $EFE = \text{Epistemic Value} + \text{Pragmatic Value}$ prioritizes exploration of high-uncertainty parameters.

### 3.2 Multi-Agent Coordination & Specialization
- **HiveMind Token Bidding**: Specialized agents (Planner, Worker, Reviewer, Verifier) bid compute tokens based on skill match scores and current memory context.
- **Swarm Debate & MAP-Elites**: Conflicting agent outputs trigger structured N-way debate with counterfactual verification and MAP-Elites island migration.

### 3.3 Memory & Knowledge Management
- **CMOS Architecture**: Unified memory subsystem spanning Episodic Trajectories, Semantic Vector Indexing, Working Context, and Action-Decision Graph (ADG).
- **Ebbinghaus Memory Decay**: Context efficiency is optimized by applying exponential decay with re-activation triggers upon recall.

### 3.4 World Modeling & Simulation
- **Causal Graph State**: Maintains entity-relation topologies in `WorldModel` with recursive Bayesian belief updating.
- **Counterfactual Forecasting**: Simulates environmental interventions before executing high-impact real-world operations.

### 3.5 Research Workflows & Self-Improvement
- **Closed-Loop Scientific Feedback**: Research OS continuously evaluates empirical execution metrics, updates paper corpus principles, and refines system prompt strategies through non-Gaussian Hawkes Hawkes processes.

---

## 4. Cross-Layer Interface Contracts & Protocols

1. **Layer 1 -> Layer 2**: `ResearchToSystemBridge.export_hypothesis(hypothesis)` transfers validated scientific hypotheses with E-value bounds to `EIOSKernel`.
2. **Layer 2 -> Layer 3**: `EOSEngine.dispatch_opportunity(opportunity)` converts business opportunities into executable multi-agent execution tasks for `HiveMind`.
3. **Layer 3 -> Layer 4**: `HiveMind.execute_task_via_skill(task_id)` dispatches validated tool protocols to `SkillRunner` and records updates in `WorldModel`.
4. **Layer 4 -> Layer 1**: `WorldModel.export_telemetry()` provides empirical performance data back to `ResearchOS` for literature hypothesis testing.

---

## 5. Institutional-Grade Reliability & Governance

- **Safety Interlocks**: Cost Tier Budget Enforcement, Tiered Approval Governance (`apodex/governance/approval.py`), and Credit Halt Mechanisms (`apodex/world_model/credit_halt.py`).
- **Mathematical Integrity**: Standard normal PPF bounds clamping $[10^{-15}, 1 - 10^{-15}]$ and safe probability calculation in statistical validation engines.
