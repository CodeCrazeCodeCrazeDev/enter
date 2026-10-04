# Capability Ownership Matrix
**Strict Layer Responsibility Boundaries to Eliminate Architectural Duplication**

---

## Overview

To maintain strict modularity and eliminate capability duplication across the unified cognitive operating system, every platform capability is assigned to exactly one owning layer.

---

## Capability Mapping Matrix

| Capability Category | Specific Capability | Owning Layer | Owning Module / Class | Prohibited Duplications |
| :--- | :--- | :--- | :--- | :--- |
| **Scientific Discovery** | Paper Corpus Principle Ingestion | Layer 1: Research OS | `apodex/ai_eos/research/integration.py` | Do not implement paper parsing in AEAN or APODEX |
| | Hypothesis Generation | Layer 1: Research OS | `ResearchOS.register_hypothesis` | Do not generate raw scientific hypotheses in EOS |
| | Statistical Validation (DSR, WRC) | Layer 1: Research OS | `ResearchOS.execute_experiment_simulation` | Do not re-compute statistical DSR in WorldModel |
| | Self-Referential Code Rewrite | Layer 1: Research OS | `CodeRewriteEngine` | Do not perform raw file mutation in AEAN agents |
| **Execution & Orchestration** | Active Inference Anomaly Sensing | Layer 2: EIOS / EOS | `EIOSKernel.sense_opportunity_anomalies` | Do not run duplicate sensing loops in AEAN agents |
| | DAG Computational Execution | Layer 2: EIOS / EOS | `EIOSKernel.execute_dag` | Do not create separate DAG execution engines in APODEX |
| | GTM System Dynamics & Runway | Layer 2: EIOS / EOS | `EOSEngine` | Do not track financial runway in Research OS |
| | Entrepreneurial Growth State Machine | Layer 2: EIOS / EOS | `CompanyGrowthStateMachine` | Do not implement growth state transitions in AEAN |
| **Cognitive Intelligence** | HiveMind Token Bidding | Layer 3: AEAN | `HiveMind` | Do not create token bidding mechanisms in Research OS |
| | Swarm Agent Task Allocation | Layer 3: AEAN | `LearnableRoutingGateDispatcher` | Do not implement sub-agent selection in EIOS Kernel |
| | Agent Specialization & Negotiation | Layer 3: AEAN | `HiveMind.submit_task_bid` | Do not implement multi-agent negotiation in WorldModel |
| **Decision & Platform** | Causal World Model Graph | Layer 4: APODEX | `WorldModel` | Do not maintain independent causal graphs in EOS |
| | Recursive Bayesian Belief Updating | Layer 4: APODEX | `WorldModel.update_belief` | Do not duplicate belief updating in HiveMind |
| | Skills Flywheel Protocol Execution | Layer 4: APODEX | `SkillRunner` | Do not execute tool runner loops in Research OS |
| | Cross-Layer Active Inference Bridge | Layer 4: APODEX | `ResearchToSystemBridge` | Do not bypass the unified bridge for layer handoffs |

---

## Invariant Governance Rules

1. **Layer Access Control:** Layer $N$ may only issue execution requests to Layer $N+1$ or receive feedback observations from Layer $N+1$.
2. **Interface Purity:** Direct database or state mutation across non-adjacent layers is strictly prohibited.
3. **Data Structure Standard:** All cross-layer messages must use Pydantic V2 validated models with strict type hints.
