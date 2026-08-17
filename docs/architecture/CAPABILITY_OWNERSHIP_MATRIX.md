# Capability Ownership Matrix

## 1. Single Responsibility Matrix

To eliminate split-brain architectural issues and logical duplication across legacy modules, every major cognitive capability in the system is assigned exactly ONE canonical owner module in `apodex/`.

| Cognitive Capability | Legacy Locations (Deprecated) | Canonical Single Owner | Implementation Path |
| :--- | :--- | :--- | :--- |
| **Research Ingestion & Bibliography** | `agent_harness`, `docs/` | **Research OS** | `apodex/ai_eos/research/research_os.py` |
| **Statistical Power & Hypothesis Testing** | `apodex/research_os/` (duplicate) | **Research OS** | `apodex/ai_eos/research/research_os.py` |
| **Active Inference & EFE Routing** | `apodex/cognition/brain.py` | **AEAN Intelligence** | `apodex/aean/coordination/hive_mind.py` |
| **Causal Do-Calculus World Model** | `apodex/world_model/` (legacy) | **AEAN Intelligence** | `apodex/arcs/kernel/kernel.py` |
| **Multi-Agent Nash Equilibrium Clearing**| `agent_harness/scheduling` | **AEAN Swarm** | `apodex/aean/coordination/hive_mind.py` |
| **Strategic Capital Allocation** | `apodex/economics/` | **EIOS / EOS** | `apodex/arcs/kernel/kernel.py` |
| **Business State Loop Orchestration** | `apodex/ai_eos/engine.py` | **EIOS / EOS** | `apodex/ai_eos/intelligence/eos_first_principles.py` |
| **Skill Registration & Execution** | `agent_harness/components` | **APODEX Skills** | `apodex/skills/registry.py` |
| **Cognitive Memory Architecture** | `apodex/memory/legacy` | **APODEX CMOS** | `apodex/memory/cmos/` |

---

## 2. Capability Access Patterns

1. **Skill Discovery**:
   - Access via `SkillRegistry.get_skill(name)`.
   - Exactly 60 strategic and operational skills pre-registered.

2. **Memory Retrieval**:
   - Access via `CMOSMemory.retrieve(query, context)`.
   - Hybrid vector-graph lookup with Ebbinghaus temporal decay decay factor $S=7 \text{ days}$.

3. **Causal Reasoning**:
   - Access via `EIOSKernel.evaluate_causal_intervention(x, y, z)`.
