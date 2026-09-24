# Unified Cognitive Architecture Specification

## Executive Summary

This specification establishes the unified, first-principles 4-layer cognitive architecture for autonomous intelligence, bringing together Research OS, EIOS, EOS, AEAN, and APODEX into a single integrated cognitive operating system. Rather than operating as isolated or overlapping platforms, each subsystem functions as a specialized layer with distinct responsibilities, explicit interfaces, and zero architectural duplication.

---

## The 4-Layer Cognitive Operating System Architecture

```
+-----------------------------------------------------------------------+
| LAYER 1: RESEARCH OS (Research Layer)                                 |
| Scientific Literature Mining | Hypothesis Generation & Testing        |
| Reproducibility Engines | Continuous Knowledge Synthesis              |
+-----------------------------------------------------------------------+
                                   |
                                   v (Validated Hypotheses & Insights)
+-----------------------------------------------------------------------+
| LAYER 2: EIOS / EOS (Execution & Orchestration Layer)                  |
| Active Inference Sensing | DAG Workflow Orchestration                 |
| GTM & Opportunity State Machine | Resource & Capital Allocation       |
+-----------------------------------------------------------------------+
                                   |
                                   v (Target Directives & Workflows)
+-----------------------------------------------------------------------+
| LAYER 3: AEAN (Cognitive Intelligence Layer)                          |
| HiveMind Multi-Agent Bidding | Specialized Agent Swarms              |
| Active Learning & Meta-Reasoning | SFT Preference Optimization       |
+-----------------------------------------------------------------------+
                                   |
                                   v (Action Proposals & Bids)
+-----------------------------------------------------------------------+
| LAYER 4: APODEX (Decision and Execution Platform Layer)               |
| World Model (Causal & Bayesian Beliefs) | Cognitive Brain             |
| Autonomous Software Engineering | Governance & Safety Verification    |
+-----------------------------------------------------------------------+
```

---

## Layer-by-Layer Subsystem Breakdown

### 1. Layer 1: Research OS (Research Layer)
* **Primary Scope**: Scientific literature discovery, continuous knowledge extraction, hypothesis formation, empirical verification, and statistical validation.
* **Core Capabilities**:
  - Corpus management (e.g. 600+ paper research database).
  - Hypothesis generation and statistical validation (`apodex/research_os/statistical_validation.py`).
  - Automated experiment execution and reproducibility tracking (`apodex/research_os/reproducibility.py`).
  - Multi-field literature querying across categories, principles, and target implementation modules.
* **Interfaces**:
  - Export: Validated scientific insights and hypotheses (`ResearchToSystemBridge.export_validated_hypothesis_to_kernel`).

### 2. Layer 2: EIOS / EOS (Execution & Orchestration Layer)
* **Primary Scope**: Strategic orchestration, opportunity sensing, workflow execution, active inference EFE calculation, and entrepreneurial dynamics.
* **Core Capabilities**:
  - `EIOSKernel`: Active inference sensing, expected free energy (EFE) minimization, DAG workflow synthesis, and adaptive task scheduling.
  - `EOSEngine`: Entrepreneurial state machine, market opportunity trees, financial runway tracking, unit economics modeling, and failure mode diagnostics.
  - `FourteenLayerEngine`: Computational architecture of entrepreneurship mapping reality substrate to meta-learning swarms.
* **Interfaces**:
  - Import: Validated hypotheses from Layer 1.
  - Export: Action directives, DAG task graphs, and capital/resource constraints to Layer 3.

### 3. Layer 3: AEAN (Cognitive Intelligence Layer)
* **Primary Scope**: Multi-agent coordination, token bidding, swarm specialization, active learning, and preference feedback.
* **Core Capabilities**:
  - `HiveMind`: Decentralized token-bidding registry for capability matching and swarm execution (`apodex/aean/coordination/hive_mind.py`).
  - Specialized Agent Roles: Research Analyst, System Architect, Code Engineer, Verification Auditor, and Growth Strategist.
  - `LearnableRoutingGateDispatcher`: Budget-decayed routing and trajectory optimization.
* **Interfaces**:
  - Import: Directives and task DAGs from Layer 2; Research insights from Layer 1.
  - Export: Action proposals, code diffs, and execution bids to Layer 4.

### 4. Layer 4: APODEX (Decision and Execution Platform Layer)
* **Primary Scope**: Causal world modeling, Bayesian belief updates, autonomous software modification, safety verification, and environment execution.
* **Core Capabilities**:
  - `WorldModel`: Graph of entities, causal relations, and recursive Bayesian beliefs (`apodex/world_model/`).
  - `CognitiveBrain`: Pydantic V2 stateful cognitive processing, memory consolidation, and action selection (`apodex/cognition/brain.py`).
  - `CodeRewriteEngine`: AST verification, Hawkes non-Gaussian recursive stability checks, and autonomous patch execution.
  - Governance & Safety: Rule-based verification, compliance checks, and approval gates (`apodex/world_model/governance/`).
* **Interfaces**:
  - Import: Action proposals and code edits from Layer 3.
  - Output: Verified state changes, updated world models, and execution telemetry fed back to Layer 1 and Layer 2.

---

## Architectural Principles & Anti-Duplication Directives

1. **Strict Capability Ownership**: No subsystem outside Layer 1 shall perform literature extraction or hypothesis statistical validation. No subsystem outside Layer 2 shall compute business state transitions or DAG orchestration. No subsystem outside Layer 3 shall manage agent token bidding. No subsystem outside Layer 4 shall execute AST code patches or modify world model belief states.
2. **Explicit State Handoffs**: Subsystems communicate exclusively through typed interface bridges (`ResearchToSystemBridge`).
3. **Institutional Reliability**: All state transitions undergo Pydantic V2 validation, timezone-aware UTC timestamps, and AST-level safety verification.
