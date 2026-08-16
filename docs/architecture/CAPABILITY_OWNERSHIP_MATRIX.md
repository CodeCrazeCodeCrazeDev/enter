# Canonical Capability Ownership Matrix

## Executive Summary

This matrix establishes the authoritative, single-source-of-truth ownership mapping for all cognitive, executive, research, and substrate capabilities across the Cognitive Operating System. Every capability domain is mapped to exactly ONE canonical owning module in `apodex/`. Logical duplication in legacy adapter modules (`agent_harness/*`) is strictly deprecated, serving purely as forwarding pass-through proxies.

---

## 1. Core System Capability Ownership Table

| Capability / Subsystem | Canonical Owning Package | Primary Class / Engine | Decoupled Interface Contract | Deprecated / Duplicate Paths |
| :--- | :--- | :--- | :--- | :--- |
| **Literature Discovery & Research Ingestion** | `apodex.ai_eos.research` | `ResearchOS` | `ResearchOS.conduct_literature_review(query)` | `apodex.cognition.research` |
| **Hypothesis Generation & Statistical Power Gating** | `apodex.ai_eos.research` | `HypothesisEngine` | `HypothesisEngine.evaluate_hypothesis(h)` | `apodex.evolution.research` |
| **Multi-Agent Coordination & Swarm Consensus** | `apodex.aean.coordination` | `HiveMind` | `HiveMind.orchestrate_goal(goal)` | `agent_harness.core.runtime.orchestration` |
| **Active Inference & Expected Free Energy (EFE)** | `apodex.aean.coordination` | `ActiveInferenceEngine` | `ActiveInferenceEngine.calculate_efe(policy)` | `apodex.arcs.kernel` (duplicate copy) |
| **Graph-of-Thought (GoT) Planning** | `apodex.aean.coordination` | `GraphOfThoughtEngine` | `GraphOfThoughtEngine.plan(goal)` | `agent_harness.core.runtime.reasoning.got` |
| **Structural Causal Models & Do-Calculus** | `apodex.arcs.kernel` | `EIOSKernel` | `EIOSKernel.evaluate_causal_intervention(x, y)` | `apodex.cognition.world_model` |
| **Strategic Business Loops (EOS Flywheels)** | `apodex.ai_eos.intelligence` | `EOSManager` | `EOSManager.run_loop(loop_type)` | `agent_harness.core.loop_types` |
| **Opportunity Arbitrage & Capital Allocation** | `apodex.arcs.capital` | `CapitalAllocator` | `CapitalAllocator.allocate(opp)` | `apodex.cognition.business` |
| **Dual-Tier Memory (CMOS / EMG)** | `apodex.memory` | `CMOSEngine` | `CMOSEngine.query_memory(query)` | `agent_harness.core.memory` |
| **Skill Registry & Flywheel Runner** | `apodex.skills` | `SkillRegistry` | `SkillRegistry.execute_skill(id)` | `apodex.planning` |
| **Safety Governance & Tiered Approval** | `apodex.world_model.governance`| `ApprovalGate` | `ApprovalGate.verify_action(action)` | `agent_harness.components.rollback_manager` |
| **Backward Compatibility Adapter Substrate** | `agent_harness` | Thin Pass-throughs | Routing to `apodex.*` | Native logic implementations |

---

## 2. Invariants & Migration Governance

1. **Single Owning Module Rule**: No capability may be re-implemented or duplicated outside its canonical owning package listed above.
2. **Adapter Pass-Through Rule**: Files under `agent_harness/` MUST NOT contain business or cognitive logic; they MUST import and re-export or delegate to the corresponding `apodex/` module.
3. **Audit Verification**: Any PR or architectural evolution MUST verify compliance against this matrix via static import analysis (`scripts/validate_dependencies.py`).
