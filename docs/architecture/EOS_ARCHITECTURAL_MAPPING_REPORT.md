# Cognitive OS Capability Ownership Matrix & Architectural Mapping Report (v3.0.0)
**Author:** Jules, Software Engineer
**Context:** First-Principles Subsystem Decoupling & Alignment

To eliminate technical debt, circular import pathways, and "split-brain" dual-maintenance bugs across ResearchOS, EREOS (EIOS), EOS, AEAN, and APODEX, we formally establish the following single source of truth (SSOT) Capability Ownership Matrix.

---

## 1. Subsystem Boundaries and Hierarchy
The Cognitive OS is organized as a nested directed hierarchy where higher layers represent abstract reasoning and strategic allocation, and lower layers provide transaction execution and raw persistence infrastructure.

```
       [ResearchOS]  <--- Epistemic & Scientific Grounding (SSOT: 130-paper db)
            ↓
          [EIOS]     <--- Executive Coordination & Multi-Agent Active Inference
            ↓
          [EOS]      <--- Venture Lifecycles, Financial Modeling & Multi-Timescale Filters
            ↓
          [AEAN]     <--- Action Execution, Tool Use & Bandit Optimization
            ↓
         [APODEX]    <--- Core Infrastructure, Process Scheduling & Database Substrate
```

---

## 2. Capability Ownership Matrix

### 2.1 Planners (Execution & Synthesis)
- **Problem/Technical Debt:** Planners previously existed as 4 overlapping modules (`UnifiedPlanner`, `CMOSQueryPlanner`, `StrategicPlanner`, `RecursivePlanner`).
- **Canonical Owner:**
  - **Strategic Business/Venture Planning:** Owned exclusively by `StrategicPlanner` in `apodex/planning/planner_executor.py`.
  - **Memory/Query Optimization Planning:** Owned exclusively by `CMOSQueryPlanner` in `apodex/memory/cmos/planner.py`.
  - **Hierarchical/Nested Cognitive Planning:** Owned exclusively by `UnifiedPlanner` in `apodex/cognition/planning/unified_planner.py`.
- **Migration Policy:** Obsolete/prototype planner classes in legacy pathways are deprecated.

### 2.2 Memories (Episodic, Semantic, & Learning)
- **Problem/Technical Debt:** Memory storage was fragmented across 5 interfaces (`UnifiedMemory`, `LongTermLearningMemory`, `SemanticMemory`, `InMemoryMemoryRepository`, `SQLiteMemoryRepository`).
- **Canonical Owner:**
  - **Semantic Knowledge Memory:** Owned exclusively by `SemanticMemory` in `apodex/memory/semantic_memory.py`.
  - **Episodic & Task Experience Memory:** Owned by `LongTermLearningMemory` in `apodex/memory/learning_memory.py`.
  - **System-Wide Multi-Tier State Memory:** Managed by the integrated `UnifiedMemory` in `apodex/cognition/memory/unified_memory.py`.
- **Migration Policy:** SQLite backing repositories must use `SQLiteMemoryRepository` under `apodex/memory/semantic_memory.py` as their underlying SQLite handle.

### 2.3 World Models (Environments & Predictions)
- **Problem/Technical Debt:** Fragmented representations between `WorldModel` and `WorldGraphManager`.
- **Canonical Owner:**
  - **Global Environment State & Transitions:** Owned by `WorldModel` in `apodex/world_model/world_model.py`.
  - **Causal Relationships & Event Graphs:** Managed by `WorldGraphManager` in `apodex/world_model/graph/world_graph.py`.
- **Migration Policy:** EIOS active inference loops query `WorldGraphManager` to approximate state-transition likelihoods.

---

## 3. Subsystem Interface Ownership Matrix

| Capability Category | Subsystem Owner | Canonical Module / File Path | Consumption Boundary |
| :--- | :---: | :--- | :--- |
| **Scientific Loop** | ResearchOS | `apodex/ai_eos/research/research_os.py` | Consumed by EIOS & EOS |
| **Active Inference** | EIOS | `apodex/arcs/causal/active_inference.py` | Consumed by EOS & Swarms |
| **Business Loops** | EOS | `apodex/ai_eos/intelligence/eos_first_principles.py`| Consumed by Swarms |
| **Outreach & Action** | AEAN | `apodex/aean/core.py` | Consumed by EIOS & EOS |
| **Process execution** | APODEX | `AgentHarness/agent_harness/core/` | Bottom-level Substrate |
