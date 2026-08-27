# Capability Ownership Matrix & Architectural Unification

## Executive Overview

To eliminate architectural duplication across Research OS, EIOS, EOS, AEAN, and APODEX, the entire system is organized into a strict **4-Layer Cognitive Operating System Taxonomy**. Each capability has exactly **one canonical owner package** under `apodex/`.

---

## 4-Layer Taxonomy Definition

```
+-------------------------------------------------------------------------+
| Layer 4: APODEX Platform & Decision Runtime                             |
| Package: apodex/ai_eos/intelligence/computational_architecture.py      |
| Role: 14-Layer Computational Architecture, Multi-Objective Orchestrator|
+-------------------------------------------------------------------------+
                                    ^
                                    | High-level execution & portfolio choices
+-------------------------------------------------------------------------+
| Layer 3: AEAN Cognitive Intelligence & Memory                           |
| Packages: apodex/cognition/, apodex/aean/, apodex/skills/, apodex/memory/|
| Role: Graph-of-Thought, Active Learning, Multi-Agent Swarm, Memory      |
+-------------------------------------------------------------------------+
                                    ^
                                    | Reasoning & Active Learning Handoffs
+-------------------------------------------------------------------------+
| Layer 2: EIOS / EOS Operating Kernel                                    |
| Packages: apodex/arcs/kernel/, apodex/ai_eos/intelligence/              |
| Role: Active Inference Expected Free Energy (EFE), Business Loops       |
+-------------------------------------------------------------------------+
                                    ^
                                    | Formulated Research Hypotheses
+-------------------------------------------------------------------------+
| Layer 1: Research OS Scientific Engine                                  |
| Packages: apodex/ai_eos/research/, apodex/research_os/                 |
| Role: Literature synthesis, statistical validation, hypothesis generation|
+-------------------------------------------------------------------------+
```

---

## Complete Capability Ownership Mapping

| Subsystem Capability / Component | Canonical Layer | Primary Subsystem Module | Duplicate Wrappers (Eliminated/Refactored) |
| :--- | :--- | :--- | :--- |
| Scientific Literature Review & Paper Database | Layer 1 | `apodex/ai_eos/research/research_os.py` | Standalone unindexed bibliography scripts |
| Hypothesis Validation & Statistical Testing | Layer 1 | `apodex/research_os/statistical_validation.py` | Hardcoded p-value mocks |
| Active Inference Sensing & EFE Routing | Layer 2 | `apodex/arcs/kernel/kernel.py` | Local EFE calculators |
| Business Loop Simulation & Economics | Layer 2 | `apodex/ai_eos/intelligence/eos_engine.py` | Mock decision heuristics |
| Graph-of-Thought & Swarm Debate Reasoning | Layer 3 | `apodex/cognition/brain.py` | Hardcoded step decomposition |
| Memory Decay & Action-Decision Graph (EMG) | Layer 3 | `apodex/memory/` & `apodex/skills/` | Isolated memory tables |
| 14-Layer Entrepreneurial Engine Orchestration | Layer 4 | `apodex/ai_eos/intelligence/computational_architecture.py` | Duplicated pipeline definitions |

---

## Cross-Layer Handoff Protocols

1. **Layer 1 -> Layer 2**: `ResearchOS.export_validated_hypothesis_to_kernel()` passes verified scientific hypotheses to `EIOSKernel.register_research_hypothesis()` for Active Inference expected free energy evaluation.
2. **Layer 2 -> Layer 3**: `EIOSKernel` active inference routing triggers `AEAN CognitiveBrain` Graph-of-Thought reasoning sessions for complex strategy synthesis.
3. **Layer 3 -> Layer 4**: `AEAN` cognitive policies are passed to the `14-Layer Computational Architecture` for capital allocation, risk checks, and autonomous execution.
