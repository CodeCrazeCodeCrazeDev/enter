# Unified Dependency Graph & Inter-Layer Topology

## 1. System Interaction Topology

```
                                +-------------------------------------------+
                                |               User / Event                |
                                +---------------------+---------------------+
                                                      |
                                                      v
+-------------------------------------------------------------------------------------------------------------------+
| LAYER 4: APODEX PLATFORM EXECUTION & GOVERNANCE ENGINE                                                             |
|                                                                                                                   |
|  +-------------------------+     +--------------------------+     +-----------------------------------+          |
|  | Personal Evolution (PEP)| --> | Multi-Objective Router   | --> | Governance & Tiered Approval      |          |
|  +-------------------------+     +--------------------------+     +-----------------------------------+          |
|               |                              |                                      |                             |
|               +------------------------------+--------------------------------------+                             |
+----------------------------------------------|--------------------------------------------------------------------+
                                               | Policy Directives & Goal Invariants
                                               v
+-------------------------------------------------------------------------------------------------------------------+
| LAYER 3: AEAN COGNITIVE INTELLIGENCE SUBSYSTEM                                                                    |
|                                                                                                                   |
|  +-------------------------+     +--------------------------+     +-----------------------------------+          |
|  | Hierarchical Planner    | <-> | Graph-of-Thought (GoT)   | <-> | Multi-Agent Swarm Coordinator     |          |
|  +-------------------------+     +--------------------------+     +-----------------------------------+          |
|               ^                              ^                                      ^                             |
|               |                              |                                      |                             |
|               v                              v                                      v                             |
|  +-------------------------+     +--------------------------+     +-----------------------------------+          |
|  | Multi-Tier Memory       | <-> | Continuous World Model   | <-> | Skill Registry & Tool Invention   |          |
|  | (Working/Episodic/CMOS) |     | (E-K-C-T-U Graphs)       |     | (Flywheel & Dynamic Execution)    |          |
|  +-------------------------+     +--------------------------+     +-----------------------------------+          |
+----------------------------------------------^--------------------------------------------------------------------+
                                               | Active Inference Goal State & Sensed Anomalies
                                               v
+-------------------------------------------------------------------------------------------------------------------+
| LAYER 2: EIOS / EOS ORCHESTRATION & BUSINESS EXECUTION LAYER                                                      |
|                                                                                                                   |
|  +-------------------------+     +--------------------------+     +-----------------------------------+          |
|  | EIOS Active Inference   | --> | EOS Business Loops       | --> | 14-Layer Computational Engine    |          |
|  | (EFE Sensing)           |     | (13 Coupled Loops)       |     | (Capital & Opportunity Allocation)|          |
|  +-------------------------+     +--------------------------+     +-----------------------------------+          |
+----------------------------------------------^--------------------------------------------------------------------+
                                               | Validated Hypotheses & Epistemic Signals
                                               v
+-------------------------------------------------------------------------------------------------------------------+
| LAYER 1: RESEARCH OS SCIENTIFIC FOUNDATION LAYER                                                                  |
|                                                                                                                   |
|  +-------------------------+     +--------------------------+     +-----------------------------------+          |
|  | Scientific Hypothesis   | --> | Statistical Validation   | --> | 300-Paper Corpus Knowledge Graph  |          |
|  | Engine                  |     | (CDF/DSR Math Protection)|     | & Code Rewrite Engine (STOP)      |          |
|  +-------------------------+     +--------------------------+     +-----------------------------------+          |
+-------------------------------------------------------------------------------------------------------------------+
```

---

## 2. Unidirectional Data & Control Flow Mechanics

### 2.1 Top-Down Directive Downsampling (`Layer 4 -> Layer 3 -> Layer 2`)
1. **APODEX Platform (L4)** receives external task requests or scheduled triggers. It inspects the active **Personal Evolution Profile (PEP)** and applies governance policies (Tier 1-4 approvals).
2. **APODEX Platform (L4)** dispatches the goal specification to **AEAN Cognitive Intelligence (L3)**.
3. **AEAN Planners (L3)** query the **Continuous World Model ($G_E, G_K, G_C, G_T, G_U$)** and **Multi-Tier Memory (CMOS/EMG)** to decompose the goal into strategic paths via **Graph-of-Thought (GoT)** reasoning.
4. **AEAN Swarm Coordinators (L3)** invoke **EIOS / EOS Execution (L2)** to evaluate economic feasibility, calculate opportunity costs, and perform Kelly Criterion capital allocations.

### 2.2 Bottom-Up Epistemic Uplink (`Layer 1 -> Layer 2 -> Layer 3`)
1. **Research OS (L1)** generates scientific hypotheses, extracts transferable principles from the 300-paper corpus, and validates statistical significance ($DSR > 0.0, PPF \text{ bounds}$).
2. Validated hypotheses are handed off via `ResearchToSystemBridge` to **EIOS Kernel (L2)**.
3. **EIOS Kernel (L2)** performs Expected Free Energy ($EFE$) active inference calculations to quantify pragmatic utility and epistemic surprise.
4. High-EFE opportunities trigger anomaly alerts that update **AEAN World Models (L3)** and inform long-term memory consolidation.

---

## 3. Communication Protocol Standards

### 3.1 Event Bus Schema
All inter-layer signals are transmitted via an asynchronous, typed Event Bus:
- `HypothesisValidatedEvent` (`Layer 1 -> Layer 2`): Emitted when Research OS completes statistical verification.
- `OpportunitySensedEvent` (`Layer 2 -> Layer 3`): Emitted when EIOS Kernel detects market/operational anomalies with EFE scores above threshold.
- `PlanExecutionCompletedEvent` (`Layer 3 -> Layer 4`): Emitted when AEAN multi-agent swarms complete execution trajectories.
- `PolicyViolationEvent` (`Layer 4 -> All Layers`): Emitted when APODEX Safety Core halts execution due to governance veto.

### 3.2 Error Handling & Fallback Circuit Breakers
- **Layer 1 Failure**: If code mutation or genetic synthesis fails AST parsing, Research OS reverts to baseline code and logs audit telemetry.
- **Layer 2 Failure**: If capital allocation triggers market liquidity limits, EOS falls back to conservative non-leveraged execution modes.
- **Layer 3 Failure**: If GoT planning exceeds iteration depth or budget limits, AEAN downshifts to single-agent ReAct fallback plans.
- **Layer 4 Failure**: If governance rules flag unapproved actions, APODEX executes a 1-click rollback to the last verified checkpoint.
