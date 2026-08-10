# Deliverable 1 — Unified Cognitive Architecture Specification

This report formalizes the unified cognitive topology, structural layers, data/control flows, and event-driven interfaces of the Cognitive Operating System.

## 1. Core Systems & High-Level Topology

The system unifies five major layers into a single integrated substrate:
- **Research OS**: Autonomous problem discovery, literature search, hypothesis formulation, and empirical testing.
- **EIOS**: Entrepreneurial Intelligence Operating System, managing task scheduling (Execution DAGs), multi-scale recursive planning (Time Horizons), and hierarchical active inference (variational free energy).
- **EOS**: Entrepreneurial Operating System, providing commercial capital allocation, risk-adjusted venture management, and Knowledge ROI computation.
- **AEAN**: Autonomous Economic Agent Network, driving multi-agent peer coordination, hive mind consensus, and localized capability validators.
- **APODEX**: The runtime execution, persistence, and skills-flywheel substrate containing CMOS (Cognitive Memory Operating System).

```
                      +-----------------------------------+
                      |            Research OS            |
                      +-----------------+-----------------+
                                        |
                                        v
                      +-----------------+-----------------+
                      |            EIOS / EOS             |
                      +-----------------+-----------------+
                                        |
                                        v
                      +-----------------+-----------------+
                      |               AEAN                |
                      +-----------------+-----------------+
                                        |
                                        v
                      +-----------------+-----------------+
                      |              APODEX               |
                      +-----------------------------------+
```

## 2. Structural Layer Interfaces & Contracts

### 2.1 EIOS Kernel (Execution DAGs)
The primary execution engine compiles goals to directed acyclic graphs (`ExecutionDAG` containing `ExecutionNode` items) and executes them using retries and isolation:
```python
class EIOSKernel:
    async def execute_dag(self, dag: ExecutionDAG) -> bool: ...
```

### 2.2 Hierarchical Active Inference
Calculates variational free energy at multiple company/agent timescales to drive search policies and reduce systemic entropy:
```python
class HierarchicalActiveInference:
    def calculate_layer_free_energy(self, layer: str, actual_outcome: float, expected_outcome: float) -> float: ...
```

### 2.3 Shared Multi-Tier Memory (CMOS)
Enforces data separation into transient, episodic, semantic, and procedural partitions:
- **Transient (Working Memory)**: Turn-level ReAct state.
- **Episodic**: Structured task execution trajectories and audit logs.
- **Semantic**: Persistent world graph, facts, and beliefs.
- **Procedural**: Action schemas and registered skills.

---
*Created as part of the Unified Cognitive OS Audit.*
