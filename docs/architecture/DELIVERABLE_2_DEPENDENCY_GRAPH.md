# Deliverable 2 — Dependency Graph Specification

This document maps the authoritative dependency topology and information flows across the five unified subsystems.

## 1. Toplogical Hierarchy & Information Flow

The architecture operates as a feed-forward information loop with continuous feedback (self-improvement):

```
       Research OS (apodex/research_os/ & apodex/ai_eos/research/)
                        ↓
       Knowledge & Evidence Ingestion (apodex/memory/models.py)
                        ↓
       World Model & Memory (apodex/world_model/ & apodex/memory/)
                        ↓
       Reasoning Engine (apodex/reasoning/)
                        ↓
       Planning Engine (apodex/planning/ & apodex/cognition/planning/)
                        ↓
       Agent Coordination (apodex/orchestration/ & apodex/aean/)
                        ↓
       Execution & Skills (apodex/skills/runner.py & implementation.py)
                        ↓
       Observation & Monitoring (apodex/evolution/self_harness/harness_observer.py)
                        ↓
       Evaluation & Quality Judges (apodex/cognition/controller.py)
                        ↓
       Learning & Self-Improvement (SelfImprovementCoordinator)
                        ↺ (Continuous Feedback)
```

## 2. Directory Mappings to the Topology

- **Research OS**: mapped to `apodex/research_os/`
- **Knowledge/Evidence**: mapped to `EvidenceCard`, `Fact`, `Belief` in `apodex/memory/models.py`
- **World Model & Memory**: mapped to `apodex/world_model/` and `apodex/memory/`
- **Reasoning**: mapped to `apodex/reasoning/` (ActiveLearning, GraphOfThought)
- **Planning**: mapped to `apodex/planning/` and `apodex/cognition/planning/`
- **Agent Coordination**: mapped to `apodex/orchestration/` and `apodex/aean/`
- **Execution**: mapped to `apodex/skills/`
- **Observation**: mapped to `apodex/evolution/`
- **Evaluation**: mapped to `CognitiveBenchmarkSuite` in `apodex/cognition/controller.py`
- **Learning**: mapped to `SelfImprovementCoordinator` in `apodex/world_model/orchestration/self_improvement_coordinator.py`
