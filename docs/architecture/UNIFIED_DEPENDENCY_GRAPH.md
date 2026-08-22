# Unified Cognitive Operating System Dependency Graph Specification

## Executive Summary

This document establishes the official dependency topology, data-flow model, and boundary hierarchy for the 4-layer Unified Cognitive Operating System (**Research OS**, **AEAN**, **EIOS/EOS**, and **APODEX**).

The goal of this dependency structure is to guarantee **strict unidirectional coupling**, **zero circular dependencies**, and **zero functional duplication** across layers.

---

## 1. High-Level Dependency Topology

Dependencies strictly flow from higher abstraction layers to lower implementation layers, with feedback communicated via event buses or explicit state observations.

```
       +---------------------------------------------------+
       |       Layer 1: Research OS                        |
       |       (Research & Hypothesis Subsystem)           |
       +---------------------------------------------------+
                                |
                                | Imports & References Scientific Principles
                                v
       +---------------------------------------------------+
       |       Layer 2: AEAN                               |
       |       (Cognitive Intelligence & Memory Subsystem) |
       +---------------------------------------------------+
                                |
                                | Emits Cognitive Intent & Policy Trees
                                v
       +---------------------------------------------------+
       |       Layer 3: EIOS / EOS                         |
       |       (Execution & Causal Orchestration Subsystem)|
       +---------------------------------------------------+
                                |
                                | Authorizes & Gates Execution Directives
                                v
       +---------------------------------------------------+
       |       Layer 4: APODEX                             |
       |       (Action Execution & Runtime Subsystem)      |
       +---------------------------------------------------+
```

---

## 2. Layer-by-Layer Module Mapping & Interfaces

### Layer 1: Research OS (`apodex/ai_eos/research/`)
* **Core Modules:**
  - `research_os.py`: Literature search, hypothesis ranking, and trial orchestrator.
  - `integration.py`: Converts paper findings into computable algorithms (Active Inference, Pearl Do-Calculus).
  - `experiment_framework.py`: `ExperimentRecord` engine with Welch's t-test validation.
  - `statistical_validation.py`: Hypothesis test power calculations and probability clamping.
* **Allowed Dependencies:**
  - Standard library (`math`, `typing`, `json`, `yaml`).
  - Third-party math libraries (`numpy`, `scipy`, `pydantic`).
* **Forbidden Dependencies:**
  - Cannot import Layer 2 (`aean`), Layer 3 (`arcs`, `ai_eos/intelligence`), or Layer 4 (`execution`, `harness`).

### Layer 2: AEAN (`apodex/aean/` & `apodex/cognition/`)
* **Core Modules:**
  - `apodex/cognition/brain.py`: `CognitiveBrain` operating active inference loops.
  - `apodex/aean/coordination/hive_mind.py`: Multi-agent swarm consensus and debate.
  - `apodex/memory/`: CMOS multi-tier memory with Ebbinghaus decay.
  - `apodex/planning/planner_executor.py`: Hierarchical Graph-of-Thought planning.
* **Allowed Dependencies:**
  - Layer 1 (`apodex/ai_eos/research/`).
  - Core domain models and interfaces.
* **Forbidden Dependencies:**
  - Cannot directly manipulate low-level OS tools or execution sandboxes (Layer 4).

### Layer 3: EIOS / EOS (`apodex/ai_eos/intelligence/` & `apodex/arcs/`)
* **Core Modules:**
  - `eos_first_principles.py`: 13 coupled business loops, stage-gate state machines.
  - `fourteen_layer_engine.py`: Full 14-layer computational architecture.
  - `kernel.py` (`EIOSKernel`): Do-calculus causal intervention engine and risk gating.
  - `capital_allocation.py`: Advanced Kelly Criterion portfolio optimizer.
* **Allowed Dependencies:**
  - Layer 1 (`apodex/ai_eos/research/`).
  - Layer 2 (`apodex/aean/`, `apodex/cognition/`).
* **Forbidden Dependencies:**
  - Cannot override Layer 2's belief updates directly without passing through causal filters.

### Layer 4: APODEX (`apodex/execution/` & `apodex/harness/` & `agent_harness/`)
* **Core Modules:**
  - `apodex/execution/`: Tool dispatching, API wrappers, code execution.
  - `apodex/skills/`: 60 registered operational skills and runner flywheel.
  - `agent_harness/`: Compatibility adapters and test harnesses.
* **Allowed Dependencies:**
  - Layer 1, Layer 2, Layer 3 (for type signatures and event schemas).
* **Forbidden Dependencies:**
  - Cannot issue high-level business decisions or bypass Layer 3 safety gates.

---

## 3. Data Flow & Inter-Layer Contracts

```
[ Research OS ] ──( Scientific Principle Object )──> [ AEAN ]
                                                          │
                                         ( Cognitive Policy & Intent )
                                                          │
                                                          v
[ APODEX Runtime ] <──( Gated Execution Order )── [ EIOS / EOS ]
       │                                                  ▲
       │                                                  │
       └──────────────( Telemetry / State Metrics )───────┘
```

1. **Principle Handshake Contract:**
   - Research OS exports `ScientificPrinciple(id, title, math_formulation, expected_benefit)` to AEAN.
2. **Cognitive Policy Contract:**
   - AEAN evaluates options and outputs `CognitivePolicy(intent, action_tree, expected_free_energy, confidence)`.
3. **Causal Gating Contract:**
   - EIOS/EOS checks `CognitivePolicy` against SCM do-calculus $P(Y | do(X))$ and Kelly sizing.
   - Outputs `ExecutionDirective(directive_id, approved_tools, resource_cap, risk_level)`.
4. **Execution Telemetry Contract:**
   - APODEX executes `ExecutionDirective` and returns `ExecutionTelemetry(status, execution_time, memory_delta, output, logs)`.
   - Telemetry is routed back into AEAN's Ebbinghaus memory and EIOS's state machines.

---

## 4. Architectural Verification Rules

To maintain strict structural integrity:
1. **Dependency Depth:** Maximum dependency chain depth $\le 6$.
2. **Circular Dependency Check:** Zero cycles detected in AST import analysis (`scripts/validate_dependencies.py`).
3. **Single Owner Rule:** Every capability (planner, memory, world model, scheduler) has exactly one canonical owner in `apodex/`.
