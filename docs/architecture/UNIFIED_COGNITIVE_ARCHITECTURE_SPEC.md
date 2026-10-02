# Unified Cognitive Operating System Architecture Specification
**Version:** 2026.1.0
**Status:** Authoritative Specification
**Scope:** Research OS (Layer 1), EIOS/EOS (Layer 2), AEAN (Layer 3), APODEX (Layer 4)

---

## 1. Executive Overview & Strategic Principles

Historically, autonomous AI engineering systems developed five distinct platforms: **Research OS**, **EIOS** (Entrepreneurial Intelligence Operating System), **EOS** (Entrepreneurial Operating System Engine), **AEAN** (Autonomous Entrepreneurial Agent Network), and **APODEX** (World Model & Cognitive Execution Platform).

Operating these as isolated platforms introduced significant architectural overhead, duplicated responsibilities (e.g., overlapping memory engines, parallel planners, redundant world models), and fragmenting interfaces.

This document establishes a **unified 4-layer cognitive operating system taxonomy** that eliminates logical duplication, enforces clean architectural boundaries, and establishes continuous, multi-scale active inference across all autonomous intelligence operations.

```
+-----------------------------------------------------------------------------------+
|                        LAYER 4: APODEX PLATFORM & WORLD MODEL                     |
|  - Causal World Graph (WMC)           - Bayesian Belief Propagation (EFE)         |
|  - Skills & Execution Flywheel        - Governance, Safety & Approval Gates       |
+-----------------------------------------------------------------------------------+
                                          ^
                                          | Active Inference & Belief State Updates
                                          v
+-----------------------------------------------------------------------------------+
|                     LAYER 3: AEAN COGNITIVE INTELLIGENCE LAYER                    |
|  - HiveMind Multi-Agent Bidding       - Graph-of-Thought (GoT) Reasoning          |
|  - Specialized Swarm Workers          - Episodic & Semantic Memory Fusion         |
+-----------------------------------------------------------------------------------+
                                          ^
                                          | Token Bidding & Execution DAG Dispatch
                                          v
+-----------------------------------------------------------------------------------+
|               LAYER 2: EIOS / EOS EXECUTION & ORCHESTRATION LAYER                  |
|  - Continuous Market Sensing (EIOS)   - 14-Layer Entrepreneurial Engine (EOS)     |
|  - Opportunity DAG Compilation        - Capital & Resource Allocation State Machine|
+-----------------------------------------------------------------------------------+
                                          ^
                                          | Scientific Hypotheses & Proven Principles
                                          v
+-----------------------------------------------------------------------------------+
|                         LAYER 1: RESEARCH OS (RESEARCH LAYER)                     |
|  - Automated Hypothesis Generation    - Statistical Rigor & DSR Validation        |
|  - Literature Review & Ingestion      - Code Rewrite & AST Verification           |
+-----------------------------------------------------------------------------------+
```

---

## 2. Exhaustive Subsystem Architectural Audits

### 2.1 Layer 1: Research OS (Research Layer)

#### Current State & Responsibilities
Research OS acts as the scientific engine of the system. It ingests scientific literature (such as the 500-paper AlphaAlgo research corpus), extracts transferable engineering principles, formulates falsifiable hypotheses, runs statistical experiments (with standard normal CDF/PPF and Deflated Sharpe Ratio calculation), and verifies AST code mutations (`CodeRewriteEngine`).

#### Identified Weaknesses & Gaps
- **Weaknesses:** Early versions executed hypothesis testing in isolation from active execution DAGs.
- **Duplicated Responsibilities:** Legacy implementations kept separate memory stores for literature principles instead of streaming insights into AEAN's bidding registry.
- **Missing Capabilities:** Automated closed-loop hypothesis promotion directly into Layer 2 sensing thresholds without manual human intervention.
- **Scalability Bottlenecks:** AST traversal for large codebase rewrites required linear scanning, which has been optimized via localized non-Gaussian Hawkes call-depth tracking.
- **Technical Debt:** Legacy naive datetime calls (e.g., `datetime.utcnow()`), which have been refactored to `datetime.now(timezone.utc)`.

#### Unified Superior Design
Research OS exposes a clean API:
1. `ResearchOS.conduct_literature_review()` queries the 500-paper principle database (`ALPHAALGO_301_500_PRINCIPLES`).
2. `ResearchOS.export_validated_hypothesis_to_kernel()` passes verified hypotheses to Layer 2 `EIOSKernel`.
3. `ResearchOS.promote_hypothesis_to_eos()` updates Layer 2 `EOSEngine` state machine parameters.

---

### 2.2 Layer 2: EIOS & EOS Engine (Execution & Orchestration Layer)

#### Current State & Responsibilities
- **EIOS Kernel:** Handles high-throughput continuous environment sensing, opportunity anomaly detection, Active Inference Expected Free Energy (EFE) calculation, and DAG compilation.
- **EOS Engine:** Implements the 11-section Entrepreneurial Operating System and the 14-Layer Computational Architecture of Entrepreneurship. Manages customer lifecycle, market moats, growth stage transitions, failure mode diagnostics, and economic loop coupling.

#### Identified Weaknesses & Gaps
- **Weaknesses:** EIOS and EOS previously maintained distinct opportunity node data structures.
- **Duplicated Responsibilities:** Opportunity scoring was computed independently in EIOS sensing and EOS strategy evaluation.
- **Missing Capabilities:** Unified active inference state handoffs where EIOS EFE calculations directly constrain EOS capital allocation limits.
- **Scalability Bottlenecks:** DAG compilation overhead for large-scale multi-tier workflows.
- **Technical Debt:** Mock planning wrappers in legacy harness adapters, which have been replaced with real dynamic step decomposition in `agent_harness/core/runtime/planner_executor.py`.

#### Unified Superior Design
EIOS and EOS are unified into Layer 2:
- **EIOS** operates as the *sensory & compilation pipeline* (bottom half of Layer 2).
- **EOS** operates as the *state machine & strategy evaluator* (top half of Layer 2).
- Continuous state updates are governed by `ResearchToSystemBridge` and `FourteenLayerEntrepreneurialEngine`.

---

### 2.3 Layer 3: AEAN (Cognitive Intelligence Layer)

#### Current State & Responsibilities
AEAN (Autonomous Entrepreneurial Agent Network) provides multi-agent cognitive intelligence. Key components include:
- **HiveMind Coordination:** Market-driven token bidding where specialized agents (Researcher, Architect, Coder, Verifier, Operator) bid for subtasks.
- **Graph-of-Thought (GoT) & Active Learning:** Dynamic step decomposition, uncertainty quantification via variance estimation, and contradiction verification.
- **Swarm Memory:** Integration with Action-Decision Graphs (EMG Engine) and semantic memory stores.

#### Identified Weaknesses & Gaps
- **Weaknesses:** Static token allocation models in early prototypes caused bidding starvation for long-horizon tasks.
- **Duplicated Responsibilities:** Redundant agent role definitions in `agent_harness` vs `apodex/aean`.
- **Missing Capabilities:** Dynamic budget decay in route dispatching based on Expected Free Energy (EFE).
- **Scalability Bottlenecks:** Lock contention on global token bidding registries under high worker concurrency.
- **Technical Debt:** Duplicate adapter modules, resolved by canonical mapping in `docs/architecture/CAPABILITY_OWNERSHIP_MATRIX.md`.

#### Unified Superior Design
AEAN acts as the central execution intelligence:
- Receives compiled DAGs from Layer 2.
- Decomposes DAG nodes into token-bidding auctions in `HiveMind`.
- Leverages `LearnableRoutingGateDispatcher` to route tasks based on skill requirements, cost tiers, and active learning confidence bounds.

---

### 2.4 Layer 4: APODEX (Decision Platform & World Model Layer)

#### Current State & Responsibilities
APODEX is the core decision platform and world model engine (WMC):
- **Causal World Graph:** Maintains entities, relations, and causal edges representing market, code, and operational reality.
- **Recursive Bayesian Belief Engine:** Updates probability distributions over hypothesis nodes based on real-world feedback.
- **Skills & Execution Flywheel:** Manages reusable tool routines, automated test generation, and protocol execution under strict token budgets.
- **Governance & Approval Gates:** Enforces policy compliance, safety checks, and human-in-the-loop sign-off for high-impact mutations.

#### Identified Weaknesses & Gaps
- **Weaknesses:** World state updates were previously pull-based rather than event-driven.
- **Duplicated Responsibilities:** APODEX and AEAN both tracked tool execution histories.
- **Missing Capabilities:** Closed-loop feedback where world state belief shifts immediately re-trigger Layer 1 research hypotheses or Layer 2 opportunity DAG recompilation.
- **Scalability Bottlenecks:** Bayesian belief propagation over large graph topologies.
- **Technical Debt:** Legacy JSON serialization methods in pydantic models (`event.json()` vs `model_dump_json()`).

#### Unified Superior Design
APODEX acts as the foundational reality substrate and world model:
- Subscribes to execution events emitted by Layer 3 AEAN workers.
- Performs real-time causal graph updates and recursive Bayesian belief propagation.
- Exposes immutable state interfaces to Layer 1, 2, and 3.

---

## 3. Core Cognitive Systems Integration

### 3.1 Long-Horizon Planning & Scheduling
Planning is unified across layers:
1. **Layer 2 (EOS/EIOS):** Long-horizon strategic planning (quarterly/monthly market positioning, capital runway, growth stage transitions).
2. **Layer 3 (AEAN):** Tactical task planning (Graph-of-Thought decomposition, subtask scheduling, dependency ordering).
3. **Layer 4 (APODEX):** Operational tool scheduling (execution timeouts, budget downshifting, protocol retry limits).

### 3.2 World Models & Simulation
- The **World Model Engine (WMC)** in Layer 4 serves as the single source of truth for reality state.
- **Active Inference Loop:**
  $$\text{EFE}(\pi) = \sum_\tau \mathbb{E}_{q(o_\tau, s_\tau | \pi)} \left[ \log q(s_\tau | \pi) - \log q(s_\tau | o_\tau, \pi) \right] - \sum_\tau \mathbb{E}_{q(o_\tau | \pi)} \left[ \log p(o_\tau) \right]$$
  - Pragmatic value (maximizing preferred outcomes $p(o_\tau)$) drives Layer 2 EOS decisions.
  - Epistemic value (minimizing state uncertainty $q(s_\tau | o_\tau, \pi)$) drives Layer 1 Research OS hypothesis generation.

### 3.3 Multi-Agent Coordination & Memory Systems
- **Memory Integration Taxonomy:**
  - **Working Memory:** Context windows and active GoT execution graphs in Layer 3 AEAN.
  - **Episodic Memory:** `EMGEngine` Action-Decision Graphs tracking past trajectory execution outcomes.
  - **Semantic Memory:** `LongTermLearningMemory` storing generalized concepts, principles, and software patterns.
  - **Procedural Memory:** Layer 4 APODEX `SkillsFlywheel` storing executable tools, scripts, and benchmark protocols.

---

## 4. First-Principles Technical Analysis & Rationale

### 4.1 Rationale for 4-Layer Taxonomy
By collapsing 5 independent platforms into a 4-layered architecture, we achieve:
1. **Zero Logical Duplication:** Every capability (planner, memory, world model, engine) has exactly one canonical owner.
2. **Predictable Data Flows:** Downward direction = execution/command; Upward direction = sensing/belief updates.
3. **Formal Interface Boundaries:** Clean Pydantic schemas enforce type-safe data transfer across layers.

### 4.2 Complexity Analysis
- **Layer 1 Research OS:** $O(N \cdot M)$ where $N$ is literature papers and $M$ is active code functions. Optimized to $O(N + \text{depth})$ via Hawkes depth-filtering.
- **Layer 2 EIOS/EOS:** $O(|V| + |E|)$ for DAG compilation and topological sorting.
- **Layer 3 AEAN HiveMind:** $O(K \log K)$ per auction round where $K$ is bidding agents.
- **Layer 4 APODEX World Model:** $O(|E_{causal}|)$ per Bayesian belief update step.

### 4.3 Failure Modes & Mitigation Strategies

| Failure Mode | Root Cause | Layer | Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| **Bidding Starvation** | Token depletion under high worker contention | Layer 3 | Dynamic budget downshifting & priority queuing |
| **Recursive AST Loop** | Unbounded rewrite proposals | Layer 1 | AST non-Gaussian Hawkes call-depth clamping |
| **EFE Local Minima** | Over-exploitation of early market signals | Layer 2 | Epistemic exploration forcing via active learning |
| **Causal Graph Divergence** | Stale state updates from async tools | Layer 4 | Vector-clock timestamping & strict verification gates |

---

## 5. Architectural Verification & Compliance

The unified architecture is verified through continuous automated integration tests:
- `tests/integration/test_unified_4layer_integration.py`
- `tests/integration/test_unified_cognitive_os_e2e.py`
- `tests/research_os/test_200_paper_integration.py`
- `tests/ai_eos/test_14_layer_engine.py`

All subsystems adhere strictly to zero-duplication policies and type-safe interface contracts.
