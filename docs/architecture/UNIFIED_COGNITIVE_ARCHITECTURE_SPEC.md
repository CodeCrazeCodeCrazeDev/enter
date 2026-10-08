# Unified Cognitive Architecture Specification
## AEAN / EIOS / EOS / APODEX Cognitive Operating System

### 1. Executive Summary & Architectural Vision
This document establishes the unified 4-layer Cognitive Operating System architecture integrating Research OS, EIOS/EOS Engine, AEAN HiveMind, and APODEX WorldModel into a single autonomous platform. Rather than operating as five disparate software projects, the platform is structured as a single layered cognitive engine:

1. **Layer 1: Research OS (Research Layer)** - Scientific discovery, paper corpus analysis, transferable principle extraction, hypothesis formulation, and empirical verification.
2. **Layer 2: EIOS / EOS Engine (Execution & Orchestration Layer)** - Continuous sensing, Active Inference Expected Free Energy (EFE) minimization, DAG pipeline execution, risk gateway, capital allocation, and lifecycle management.
3. **Layer 3: AEAN HiveMind (Cognitive Intelligence Layer)** - Multi-agent swarm intelligence, token-denominated task bidding, agent specialization, capability distillation, and collective consensus.
4. **Layer 4: APODEX WorldModel (Decision & Action Layer)** - Causal DAG modeling, Bayesian belief updating, active inference planning, environment simulation, and execution runtime.

---

### 2. Layer Definitions & Interface Boundaries

#### Layer 1: Research OS (Scientific Discovery)
- **Primary Responsibility**: Autonomous literature review, theoretical principle extraction from scientific publications (e.g. 600-paper corpus), hypothesis formulation, statistical significance verification ($p < 0.01$), and code rewrite proposal generation.
- **Inputs**: Academic publications, empirical benchmark logs, subsystem feedback.
- **Outputs**: Validated research hypotheses, extracted engineering principles, code rewrite AST proposals.
- **Interfaces**:
  - `conduct_literature_review(query: str) -> List[Dict]`
  - `validate_hypothesis(hypothesis_id: str) -> ResearchHypothesis`
  - `export_validated_hypotheses() -> List[ResearchHypothesis]`

#### Layer 2: EIOS Kernel & EOS Engine (Execution & Orchestration)
- **Primary Responsibility**: Event-driven continuous sensing, EIOS DAG compilation, Active Inference EFE minimization, enterprise lifecycle state machine, risk gateway monitoring, and capital allocation.
- **Inputs**: Validated research hypotheses from Layer 1, real-world telemetry, market/system signals.
- **Outputs**: Prioritized opportunity graph, executed DAG workflows, resource allocation decisions.
- **Interfaces**:
  - `ingest_validated_research(hypotheses: List[ResearchHypothesis]) -> int`
  - `sense_opportunity_anomalies(sensor_data: Dict) -> List[OpportunityNode]`
  - `evaluate_decision_tree(context: Dict) -> Dict`

#### Layer 3: AEAN HiveMind (Swarm & Cognitive Intelligence)
- **Primary Responsibility**: Autonomous multi-agent coordination, token-denominated auction bidding for task execution, agent specialization, capability distillation, and MAP-Elites evolutionary optimization.
- **Inputs**: Execution requirements from Layer 2, research insights from Layer 1.
- **Outputs**: Multi-agent task assignments, distilled prompt/parameter artifacts, consensus decisions.
- **Interfaces**:
  - `register_research_insight(insight_id: str, topic: str, priority: float)`
  - `conduct_task_auction(task_id: str, required_capability: str, budget: float) -> AgentBid`
  - `distill_capability(agent_id: str) -> CapabilityArtifact`

#### Layer 4: APODEX WorldModel (Causal World Modeling & Active Inference)
- **Primary Responsibility**: Structural Causal Modeling (SCM), counterfactual reasoning, Bayesian belief updates ($P(S|E)$), active inference planning, and environment state simulation.
- **Inputs**: Executed actions and state feedback from Layer 3 and Layer 2.
- **Outputs**: Updated world state graph, causal impact scores, epistemic and pragmatic value estimates.
- **Interfaces**:
  - `create_node(node_id: str, node_type: str, metadata: Dict)`
  - `add_edge(source: str, target: str, relationship: str, weight: float)`
  - `update_belief(node_id: str, observation: Dict) -> BeliefState`
  - `calculate_expected_free_energy(action: Dict) -> float`

---

### 3. Closed-Loop Active Inference Flywheel
The unified architecture operates as a closed-loop Active Inference flywheel across all 4 layers:
```
 [ Layer 1: Research OS ] ---> Validated Hypotheses ---> [ Layer 2: EIOS / EOS Engine ]
            ^                                                           |
            |                                                           v
  Epistemic Value & Gaps                                     Execution DAGs & Opportunities
            |                                                           |
            |                                                           v
 [ Layer 4: APODEX WorldModel ] <--- Causal Graph Updates <--- [ Layer 3: AEAN HiveMind ]
```

1. **Epistemic Exploration**: Research OS generates hypotheses to reduce epistemic ambiguity in unknown domains.
2. **Pragmatic Orchestration**: EOS Engine calculates EFE ($EFE = \text{Epistemic Value} + \text{Pragmatic Value}$) and selects actions that maximize reward while reducing uncertainty.
3. **Collective Execution**: AEAN HiveMind bids tokens to assign specialized agent teams to execute the selected DAGs.
4. **Causal Reflection**: APODEX WorldModel observes execution outcomes, updates Bayesian beliefs, adjusts causal edge weights, and identifies new research gaps fed back into Layer 1.
