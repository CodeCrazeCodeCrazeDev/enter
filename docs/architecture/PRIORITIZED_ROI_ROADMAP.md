# Prioritized ROI Engineering Roadmap

## 1. ROI Ranking Framework

Engineering initiatives are ranked based on Expected Return on Engineering Effort (E-ROEE):

$$\text{ROI} = \frac{\Delta \text{Intelligence} \times \Delta \text{Reliability} \times \Delta \text{Scalability}}{\text{Engineering Complexity} \times \text{Maintenance Overhead}}$$

---

## 2. Ranked Implementation Priorities

| Priority | Initiative | Targeted Layer | Expected ROI | Rationale |
|---|---|---|---|---|
| **P0** | **Unified Cross-Layer Bridge Integration** | All Layers (1-4) | **10.0** | Eliminates state divergence, enables continuous closed-loop active inference, and connects literature research directly to execution. |
| **P0** | **Statistical Validation & Ast Hawkes Verification** | Layer 1 (Research OS) | **9.5** | Prevents false-positive research adoption and catastrophic code rewrite loops. |
| **P1** | **EFE Active Inference Sensing DAG Compilation** | Layer 2 (EIOS Kernel) | **8.8** | Replaces heuristic task scheduling with mathematically optimal active inference expected free energy minimization. |
| **P1** | **Token Bidding HiveMind Auction Optimization** | Layer 3 (AEAN) | **8.2** | Optimizes multi-agent task distribution and compute budget utilization. |
| **P2** | **Causal World Model Graph Pruning & Belief Decay** | Layer 4 (APODEX) | **7.8** | Prevents memory explosion and stale prior bias in long-horizon autonomous operation. |
| **P2** | **Automated Skill Abstraction Flywheel** | Layer 4 (APODEX) | **7.5** | Converts successful task execution trajectories into reusable executable protocols. |

---

## 3. Engineering Deliverables & Milestones

### Phase 1: Cross-Layer Bridge & Active Inference Integration (Immediate P0)
- Implement `ResearchToSystemBridge` in `apodex/ai_eos/research/integration.py`.
- Wire `ResearchOS.export_validated_hypothesis_to_kernel` and `promote_hypothesis_to_eos`.
- Establish joint 4-layer integration test suite (`tests/integration/test_unified_4layer_integration.py`).

### Phase 2: Active Inference & Capital Allocation Optimization (P1)
- Deepen `EIOSKernel` Expected Free Energy calculation using empirical probability updates.
- Enhance `EOSEngine` unit economics simulation and growth stage transitions.

### Phase 3: Autonomous Self-Improvement & World Model Scaling (P2)
- Integrate AST rewrite verification with automated sandbox regression testing.
- Implement graph pruning and belief decay in `APODEX WorldModel`.
