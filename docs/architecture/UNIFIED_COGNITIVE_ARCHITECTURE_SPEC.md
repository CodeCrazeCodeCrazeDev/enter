# Unified Cognitive Operating System Specification
## AEAN / EIOS / EOS / APODEX / Research OS Architectural Redesign

---

## 1. Executive Summary & First-Principles Rationale

Modern autonomous AI systems frequently suffer from architectural bloat and logical duplication when subsystems (such as research engines, decision orchestrators, multi-agent networks, and world models) are built as standalone, isolated platforms.

This specification establishes a **Single Layered Cognitive Operating System Taxonomy** that unifies five formerly separate paradigms—**Research OS**, **EIOS**, **EOS**, **AEAN**, and **APODEX**—into four strictly delineated runtime layers with zero duplicated capabilities and explicit, unidirectional interfaces:

```
+-------------------------------------------------------------------------------+
| LAYER 1: RESEARCH OS (Scientific Discovery & Empirical Validation Layer)      |
| Ingestion -> Hypothesis Generation -> Empirical Probing -> Statistical Control |
+---------------------------------------+---------------------------------------+
                                        | Validated Hypotheses & Research DB
                                        v
+-------------------------------------------------------------------------------+
| LAYER 2: EIOS / EOS (Execution, Sensing & Strategic Orchestration Layer)      |
| DAG Compiler -> Active Inference Sensing -> EFE Optimization -> Capital Allocation|
+---------------------------------------+---------------------------------------+
                                        | Opportunity DAG & Token Directives
                                        v
+-------------------------------------------------------------------------------+
| LAYER 3: AEAN (Cognitive Intelligence & Multi-Agent Network Layer)            |
| HiveMind Token Bidding -> Strategy Negotiation -> Agent Specialization       |
+---------------------------------------+---------------------------------------+
                                        | Action Trajectories & Tool Invocations
                                        v
+-------------------------------------------------------------------------------+
| LAYER 4: APODEX (Decision, State & Platform Execution Layer)                  |
| Multi-Graph WorldModel -> CMOS Memory Tiering -> Verification -> Safety Core |
+-------------------------------------------------------------------------------+
```

---

## 2. Layered Architecture Taxonomy & Subsystem Responsibilities

### Layer 1: Research OS (Research & Discovery Layer)
- **Canonical Owner**: `apodex.research_os` & `apodex.ai_eos.research`
- **Core Function**: Continuous ingestion of academic literature, mathematical theorem extraction, active scientific probing, and statistical hypothesis testing.
- **Key Capabilities**:
  - Paper Corpus Parsing & Principle Indexing (`ALPHAALGO_301_500_PRINCIPLES`)
  - Hypothesis Engine (`HypothesisEngine`)
  - Statistical Validation & Control (`StatisticalValidator`, probability clamping, Deflated Sharpe Ratio calculation)
  - Self-Referential AST Code Rewrite Engine (`CodeRewriteEngine`)
- **Strict Boundary**: Layer 1 generates and validates scientific hypotheses and research principles. It never manages runtime agent execution or state storage directly.

### Layer 2: EIOS / EOS (Execution & Strategic Orchestration Layer)
- **Canonical Owner**: `apodex.arcs.kernel` (EIOS Kernel) & `apodex.ai_eos.intelligence` (EOS Engine)
- **Core Function**: Active inference sensing, Directed Acyclic Graph (DAG) compilation, Expected Free Energy (EFE) minimization, and entrepreneurial opportunity & capital allocation.
- **Key Capabilities**:
  - Active Inference Sensing (`EIOSKernel.sense_opportunity_anomalies`)
  - EFE Task Routing & Optimization (`ActiveInferencePlanner`)
  - 14-Layer Entrepreneurial Operating Engine (`FourteenLayerEntrepreneurialEngine`)
  - Capital & Resource Allocation (`CapitalAllocationEngine`)
- **Strict Boundary**: Layer 2 evaluates trade-offs, allocates capital, and compiles execution graphs. It delegates multi-agent negotiation and token bidding to Layer 3.

### Layer 3: AEAN (Cognitive Intelligence & Multi-Agent Network Layer)
- **Canonical Owner**: `apodex.aean.coordination` (HiveMind) & `apodex.aean.engines`
- **Core Function**: Multi-agent coordination, auction-based task bidding, peer-to-peer strategy negotiation, specialized agent role dispatching, and collective reasoning.
- **Key Capabilities**:
  - HiveMind Token Bidding Registry (`HiveMind.bid_for_task`)
  - Learnable Routing Gate Dispatcher (`LearnableRoutingGateDispatcher`)
  - Island MAP-Elites Genetic Optimizer (`GeneticWorkflowOptimizer`)
  - Peer-to-Peer Agent Negotiation Protocols (`INegotiationProtocol`)
- **Strict Boundary**: Layer 3 coordinates specialized agents and negotiates action trajectories. It relies on Layer 4 for persistent world state storage and runtime memory.

### Layer 4: APODEX (Decision, State & Platform Execution Layer)
- **Canonical Owner**: `apodex.world_model`, `apodex.memory.cmos`, `apodex.cognition.brain`
- **Core Function**: Central state-of-truth, persistent multi-graph world modeling, multi-tier memory (CMOS), safety verification, and hardware-isolated execution sandbox.
- **Key Capabilities**:
  - Persistent Multi-Graph World Model ($G_E, G_K, G_C, G_T, G_U$)
  - CMOS Multi-Tier Memory (Working, Episodic, Semantic, Procedural)
  - Cognitive Brain & Safety Core (`CognitiveBrain`, immutable governance filters)
  - Introspective Critics & Verification Sandbox (`Verifier`, AST static linting)
- **Strict Boundary**: Layer 4 maintains state, manages memory, and enforces safety rollbacks. It does not perform market simulation or scientific research generation directly.

---

## 3. Explicit Subsystem Interfaces & Active Inference State Handoffs

The four layers interact via a strictly typed Active Inference State Handoff Protocol implemented by `ResearchToSystemBridge`:

1. **Research OS -> EIOS Kernel Handoff**:
   - `ResearchOS` validates a scientific hypothesis $H = (\text{claim}, p\text{-value}, \text{confidence})$.
   - Calls `ResearchToSystemBridge.promote_hypothesis_to_kernel(H)`.
   - `EIOSKernel` registers $H$ into its Active Inference state, generating an anomaly sensing event if $H$ alters Expected Free Energy calculations.

2. **EIOS / EOS -> AEAN HiveMind Directives**:
   - EOS Engine computes optimal opportunity allocation and DAG steps.
   - Calls `ResearchToSystemBridge.dispatch_dag_to_hivemind(DAG)`.
   - `HiveMind` auctions DAG step execution tokens to registered specialized agents based on domain capability and token bid.

3. **AEAN -> APODEX State & Belief Updates**:
   - Specialized agents complete ReAct tool execution trajectories.
   - Calls `ResearchToSystemBridge.update_world_model_state(trajectory, outcome)`.
   - APODEX `WorldModel` updates causal edges ($G_C$) and performs recursive Bayesian belief updating ($G_U$), while `CMOSMemory` consolidates episodic traces into semantic skills.

---

## 4. Failure Modes, Trade-Offs & Complexity Analysis

| Subsystem Component | Failure Mode | Mitigation Strategy | Complexity |
|---|---|---|---|
| AST Code Rewrite | Malformed syntax or dangerous function calls | AST static analysis + isolated dry-run compilation sandbox | $O(N)$ AST nodes |
| Active Inference Routing | EFE score divergence or token budget exhaustion | Fallback to parsimonious cheapest agent + conjugate Bayesian update | $O(K)$ candidate agents |
| Multi-Agent Bidding | Deadlocks or agent collusion | Dynamic auction ceiling + timeout arbitration protocol | $O(M)$ bids |
| Bayesian Belief Update | Numerical instability or probability bounds error | Clamped log-odds math + conjugate Dirichlet priors | $O(E)$ edges |

---

## 5. Summary & System Verification Criteria

The unified cognitive operating system guarantees:
- **Zero Capability Duplication**: Single canonical owner for planners, memories, world models, and schedulers.
- **Deterministic Traceability**: Every execution trace maps directly from Layer 1 hypothesis to Layer 4 state update.
- **Institutional-Grade Reliability**: Full verification sandbox, AST static analysis, and automated rollback triggers.
