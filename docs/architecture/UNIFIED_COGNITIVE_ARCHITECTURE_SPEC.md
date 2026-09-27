# Unified Cognitive Operating System Specification

## 1. Executive Summary & Vision

The Unified Cognitive Operating System integrates five previously disparate research and execution frameworks—**Research OS**, **EIOS**, **EOS**, **AEAN**, and **APODEX**—into a single 4-layer cognitive architecture. Rather than treating these components as independent platforms with overlapping boundary responsibilities, this specification establishes a clean, decoupled, layered hierarchy governed by **Active Inference** (Free Energy Principle) and first-principles software engineering.

```
+-------------------------------------------------------------------------------+
|                       LAYER 1: RESEARCH LAYER (Research OS)                    |
| Hypothesis Generation, Literature Mining, Statistical & Causal Validation     |
+-------------------------------------------------------------------------------+
                                      | Active Inference Hypotheses & Alpha Principles
                                      v
+-------------------------------------------------------------------------------+
|                  LAYER 2: ORCHESTRATION & EXECUTION LAYER (EIOS / EOS)        |
| Opportunity Graph Sensing, Active Inference DAG Compiler, Capital Allocation  |
+-------------------------------------------------------------------------------+
                                      | Compiled Task Graph & Resource Budgets
                                      v
+-------------------------------------------------------------------------------+
|                 LAYER 3: COGNITIVE INTELLIGENCE LAYER (AEAN Organism)         |
| HiveMind Multi-Agent Coordination, Swarm Bidding, Collective Memory (CMOS)   |
+-------------------------------------------------------------------------------+
                                      | Action Executions & Causal Updates
                                      v
+-------------------------------------------------------------------------------+
|             LAYER 4: DECISION & PLATFORM SUBSTRATE LAYER (APODEX WorldModel)   |
| WorldModel Creator (WMC), Bayesian Belief Graph, Safety & Verification Kernel  |
+-------------------------------------------------------------------------------+
```

---

## 2. Layer Taxonomy & Architectural Boundaries

### Layer 1: Research Layer (`ResearchOS`)
* **Primary Scope:** Hypothesis formation, academic/empirical corpus processing, statistical validation, and causal discovery.
* **Key Components:**
  - `LiteratureReviewEngine` / Paper Corpus Ingestion (`AI_EOS_RESEARCH_DB.yaml`, `ALPHA_ALGO_*`)
  - `StatisticalValidationEngine` (Deflated Sharpe Ratio, P-value correction, Probabilistic Sharpe)
  - `HypothesisRegistry` (Active Inference Hypotheses)
* **Explicit Outputs:** Validated hypotheses, extracted engineering/alpha principles, causal priors.

### Layer 2: Orchestration & Execution Layer (`EIOS / EOS`)
* **Primary Scope:** Systems orchestration, GTM dynamics, venture lifecycle, Active Inference DAG compilation, and resource allocation.
* **Key Components:**
  - `EIOSKernel` (Active Inference Expected Free Energy Sensing, Anomaly Detection)
  - `EOSEngine` (Opportunity Nodes, Strategic Moat Engine, Growth State Machines)
  - `DAGCompiler` (Dynamic dependency graph compilation from hypotheses)
* **Explicit Outputs:** Scheduled Active Inference Task Graphs, allocated token/capital budgets, execution policies.

### Layer 3: Cognitive Intelligence Layer (`AEAN Organism`)
* **Primary Scope:** Multi-agent collaboration, specialized role bidding, collective problem solving, and adaptive execution.
* **Key Components:**
  - `HiveMind` (Token bidding registry, task allocation, role dispatching)
  - `SwarmIntelligence` / `AgentMesh` (Domain specialist agents)
  - `CMOS` (Collective Memory & Knowledge Graph)
* **Explicit Outputs:** Task execution trajectories, step observations, candidate code rewrites, skill candidates.

### Layer 4: Decision & Platform Substrate Layer (`APODEX WorldModel`)
* **Primary Scope:** Causal world modeling, Bayesian belief updates, safety guardrails, protocol verification, and execution sandbox.
* **Key Components:**
  - `WorldModel` (CausalNode, RelationEdge graph, Bayesian belief updating)
  - `SafetyKernel` & `VerificationEngine` (Pre-flight protocol checks, credit halt, tier gating)
  - `SkillsRunner` & `ProtocolLoader`
* **Explicit Outputs:** Grounded reality state updates, verified execution artifacts, policy feedback loops.

---

## 3. Layer Interfaces & Active Inference Handoff Contracts

All inter-layer communication occurs via explicit Python data models and contract interfaces:

1. **Layer 1 -> Layer 2 Handoff:**
   `ResearchOS.export_validated_hypothesis_to_kernel(hypothesis_id)` creates a `ResearchHypothesis` entity in `EIOSKernel` with assigned prior variance $\sigma_0^2$ and initial Expected Free Energy $G(a)$.

2. **Layer 2 -> Layer 3 Handoff:**
   `EOSEngine` compiles active hypotheses into a `TaskDAG`. The tasks are posted to `HiveMind.register_task()` in `AEAN`, initiating token-based agent bidding.

3. **Layer 3 -> Layer 4 Handoff:**
   `HiveMind` agent executions emit state transitions to `WorldModel.create_node()` and `WorldModel.update_belief()`, incorporating likelihood observations into the Bayesian posterior.

4. **Layer 4 -> Layer 1/2 Feedback Loop:**
   `WorldModel` belief updates adjust hypothesis prior confidence in `ResearchOS` and trigger dynamic DAG re-plan / anomaly response in `EIOSKernel`.

---

## 4. Architectural Rationale, Trade-Offs & Complexity Analysis

* **Separation of Concerns:** Decoupling research discovery (Layer 1) from multi-agent coordination (Layer 3) prevents agent swarm degradation due to unvalidated research noise.
* **Complexity:** Time complexity for Active Inference DAG compilation is $O(V + E)$ where $V$ is the number of opportunity nodes and $E$ is dependency edges.
* **Trade-Offs:** Strict layer isolation adds minor latency overhead during cross-layer RPC/method calls, but provides $10\times$ higher testability, isolation, and system stability.
