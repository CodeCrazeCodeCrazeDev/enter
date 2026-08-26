# Unified Cognitive Operating System Architecture Specification

## Executive Summary

This document defines the authoritative architecture specification for the **Unified Cognitive Operating System**, integrating **Research OS**, **EIOS / EOS**, **AEAN**, and **APODEX** into a single, cohesive 4-layer autonomous intelligence platform.

Rather than managing five fragmented platforms with overlapping responsibilities, the architecture establishes a single, strictly layered hierarchy with non-overlapping capability ownership, typed interfaces, and explicit active inference state handoffs.

---

## 1. Architectural Principles & Taxonomy

The system is organized into a strict 4-layer hierarchy:

```
+-----------------------------------------------------------------------+
| LAYER 4: APODEX - DECISION PLATFORM & PRODUCTION EXECUTION            |
| - Safety Governance & Veto Rules    - Credit Halt & Budget Allocator |
| - Cost Tiering & Sandbox Runner    - Tool Orchestration & Runtime    |
+-----------------------------------------------------------------------+
                                  ^
                                  | Interface IV (Decision State / Approval)
                                  v
+-----------------------------------------------------------------------+
| LAYER 3: AEAN - COGNITIVE INTELLIGENCE & MULTI-AGENT SWARM             |
| - Multi-Agent Swarm & Debate        - Graph-of-Thought Planning       |
| - EMG / CMOS Memory Systems        - Skill Flywheel Registry          |
+-----------------------------------------------------------------------+
                                  ^
                                  | Interface III (Cognitive State / Handoff)
                                  v
+-----------------------------------------------------------------------+
| LAYER 2: EIOS / EOS - EXECUTION & ORCHESTRATION LAYER                 |
| - EIOS Active Inference Sensing     - EOS 13 Business Loops           |
| - Expected Free Energy (EFE) Routing - Pearl Causal Do-Calculus SCM   |
+-----------------------------------------------------------------------+
                                  ^
                                  | Interface II (Hypothesis & Sensing Bridge)
                                  v
+-----------------------------------------------------------------------+
| LAYER 1: RESEARCH OS - RESEARCH & DISCOVERY LAYER                     |
| - Scientific Literature DB (300 papers) - Falsifiable Hypothesis Gen  |
| - Reproducibility & Statistical Audit - Principle Extraction Engine   |
+-----------------------------------------------------------------------+
```

### Layer Responsibilities & Non-Overlapping Ownership

1. **Layer 1: Research OS (Research Layer)**
   - **Primary Duty**: Epistemic exploration, scientific literature ingestion, principle extraction, and hypothesis validation.
   - **Owned Modules**: `apodex/ai_eos/research/`, `apodex/research_os/`, research databases (`AI_EOS_RESEARCH_DB.yaml`, `ALPHA_ALGO_100_NEW_RESEARCH.yaml`).
   - **Explicit Non-Responsibility**: Does not execute real-world production code or allocate commercial capital.

2. **Layer 2: EIOS / EOS (Execution & Orchestration Layer)**
   - **Primary Duty**: First-principles sensing, market dynamic active inference (Expected Free Energy minimization), coupled business loop execution, and causal interventions.
   - **Owned Modules**: `apodex/arcs/kernel/`, `apodex/ai_eos/intelligence/`, `apodex/ai_eos/intelligence/eos_first_principles.py`.
   - **Explicit Non-Responsibility**: Does not perform multi-agent debate or directly invoke low-level sandbox execution tools.

3. **Layer 3: AEAN (Cognitive Intelligence Layer)**
   - **Primary Duty**: High-level reasoning, multi-agent swarm collaboration, Graph-of-Thought (GoT) planning, long-term memory management (EMG / CMOS), and skill execution.
   - **Owned Modules**: `apodex/aean/`, `apodex/cognition/`, `apodex/skills/`, `apodex/memory/`.
   - **Explicit Non-Responsibility**: Does not bypass governance vetoes or modify production runtime configurations directly.

4. **Layer 4: APODEX (Decision Platform Layer)**
   - **Primary Duty**: Institutional governance, non-bypassable safety vetoes, cost-tiering management, credit halt enforcement, and tool execution sandbox.
   - **Owned Modules**: `apodex/governance/`, `apodex/safety/`, `apodex/world_model/`, `apodex/execution/`.
   - **Explicit Non-Responsibility**: Does not synthesize scientific hypotheses or conduct literature reviews.

---

## 2. Capability Ownership Matrix

| Capability | Canonical Owner Subsystem | Deprecated / Disallowed Duplications | Interface / Contract |
| :--- | :--- | :--- | :--- |
| **Literature Ingestion & Analysis** | Layer 1 (Research OS) | Handled only via ResearchOS literature search; prohibited in AEAN/EOS | `conduct_literature_review()` |
| **Active Inference & EFE Sensing** | Layer 2 (EIOS Kernel) | No duplicate EFE math in AEAN memory; routed via EIOS Kernel | `compute_expected_free_energy()` |
| **13 Coupled Business Loops** | Layer 2 (EOS Engine) | Executed strictly in EOS engine; no duplicate loops in APODEX | `evaluate_lifecycle_stage()` |
| **Multi-Agent Swarm Debate** | Layer 3 (AEAN Hive Mind) | No separate swarm implementations; centralized in AEAN | `conduct_swarm_debate()` |
| **Memory Decay & Retrieval** | Layer 3 (AEAN CMOS/EMG) | Centralized in AEAN memory; legacy adapters use `agent_harness` bridge | `query_memory()` |
| **Skill Flywheel Registry** | Layer 3 (AEAN Skills) | 60 standard skills stored in `apodex.skills.registry` | `execute_skill()` |
| **Safety Governance & Budget Veto** | Layer 4 (APODEX Governance) | Non-bypassable Rule 6 check in `CognitiveSystemController` | `verify_governance_rules()` |
| **Sandbox Execution & Tool Call** | Layer 4 (APODEX Sandbox) | Isolated tool execution in `apodex/execution` | `run_in_sandbox()` |

---

## 3. Layer Interfaces & State Handoff Protocols

### Interface I: Research OS -> EIOS Kernel (`ResearchToSystemBridge`)
- **Data Handoff**: Validated scientific hypotheses ($H$) and extracted principles ($P$) are exported to EIOS Kernel active inference sensing.
- **Contract Schema**:
  ```python
  class ResearchHandoff(BaseModel):
      hypothesis_id: str
      domain_keyword: str
      confidence: float
      extracted_principles: List[str]
      pragmatic_value_delta: float
      epistemic_gain_delta: float
  ```

### Interface II: EIOS Kernel -> EOS Engine
- **Data Handoff**: Opportunity signals and EFE states trigger 13 coupled business loops and 9-stage lifecycle evaluation.
- **Contract Schema**:
  ```python
  class EIOSStateSignal(BaseModel):
      opportunity_id: str
      active_inference_efe: float
      causal_intervention_do: Dict[str, Any]
      recommended_capital_cents: int
  ```

### Interface III: EOS Engine -> AEAN Multi-Agent Intelligence
- **Data Handoff**: Strategic goals and business constraints are dispatched to AEAN Graph-of-Thought (GoT) planning and multi-agent swarm allocation.
- **Contract Schema**:
  ```python
  class AEANTaskAllocation(BaseModel):
      goal_id: str
      strategy_type: str  # e.g., "SWARM_DEBATE", "GOT_PLANNING"
      agent_roles: List[str]
      budget_allocation_cents: int
  ```

### Interface IV: AEAN -> APODEX Decision Platform
- **Data Handoff**: Executed plan outcomes and agent trajectories are passed to APODEX governance for Rule 6 verification, cost tiering, and sandbox tool execution.
- **Contract Schema**:
  ```python
  class APODEXDecisionRequest(BaseModel):
      task_id: str
      proposed_plan: ExecutionPlan
      cost_projection_cents: int
      safety_hash: str
  ```

---

## 4. Elimination of Technical Debt & Duplication

1. **Adapter Deduplication**: Restored 16 legacy `agent_harness` adapter modules (`agent_harness.core.memory`, `agent_harness.components`, etc.) that cleanly bridge into `apodex/` native models without logical duplication.
2. **Unified Skill Registry**: Standardized skill registration under `SkillRegistry` with alias support, eliminating competing skill registries.
3. **Probability & Metric Safeguards**: Clamped CDF/PPF probability bounds in `apodex/research_os/statistical_validation.py` to ensure numerical stability without division by zero.

---

## 5. Summary

The 4-layer taxonomy establishes structural clarity, operational isolation, and unified cognitive execution across Research OS, EIOS, EOS, AEAN, and APODEX.
