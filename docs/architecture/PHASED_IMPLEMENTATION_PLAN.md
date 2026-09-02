# Phased Implementation Plan & Migration Strategy

## 1. Migration Strategy & Zero-Downtime Principles

To evolve the legacy siloed codebase into the unified 4-layer Cognitive Operating System without breaking existing execution pathways or test suites, the implementation follows three core principles:
1. **Interface-First Refactoring**: Define explicit type-annotated contracts (`pydantic.BaseModel`) before modifying underlying subsystem logic.
2. **Backwards Compatibility Wrappers**: Maintain legacy module export pathways (e.g., in `agent_harness/` and `apodex/ai_eos/`) while redirecting internal execution to canonical layer components.
3. **Continuous Regression Testing**: Run the full integration test suite (`PYTHONPATH=.:AgentHarness pytest`) after every phase transition.

---

## 2. Phased Milestone Execution Roadmap

```
+-----------------------------------------------------------------------------------+
| PHASE 1: Architectural Foundation & Boundary Consolidation (Week 1 - 2)            |
| - Standardize 4-layer directory taxonomy and import bridges.                       |
| - Eliminate duplicate planner and memory implementations.                          |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| PHASE 2: Active Inference & Sensing Integration (Week 3 - 4)                       |
| - Connect Research OS hypothesis export to EIOS Kernel EFE sensing.               |
| - Implement standard normal PPF clamping and statistical validation safeguards.    |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| PHASE 3: Cognitive Multi-Agent & Memory Synthesis (Week 5 - 6)                    |
| - Integrate HiveMind token bidding with CMOS hierarchical memory decay.            |
| - Deploy Island MAP-Elites genetic workflow optimization.                          |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| PHASE 4: World Model Causal Execution & Platform Governance (Week 7 - 8)          |
| - Connect Do-Calculus causal planning to WorldModel entity/belief updates.        |
| - Enforce Tiered Approval Governance and Credit Halt safety interlocks.           |
+-----------------------------------------------------------------------------------+
```

---

## 3. Phase Objectives, Deliverables & Evaluation Criteria

### Phase 1: Architectural Foundation & Boundary Consolidation
- **Deliverables**: Explicit layer boundary interfaces, removal of duplicate legacy classes, restored adapter modules.
- **Evaluation Criteria**: 100% test collection without `ModuleNotFoundError`, zero duplicate logical implementations across layer modules.

### Phase 2: Active Inference & Sensing Integration
- **Deliverables**: `ResearchToSystemBridge` integration, Active Inference EFE scoring in `EIOSKernel`, statistical validation mathematical edge case protection.
- **Evaluation Criteria**: EFE calculation variance $< 10^{-4}$, 0 floating point overflow errors during 10,000 Monte Carlo SPRT iterations.

### Phase 3: Cognitive Multi-Agent & Memory Synthesis
- **Deliverables**: CMOS Ebbinghaus memory decay operator, HiveMind token bidding registry with skill match routing, MAP-Elites island migration gates.
- **Evaluation Criteria**: Context token usage reduced by $\ge 30\%$, multi-agent consensus reached in $\le 3$ debate rounds on complex benchmarks.

### Phase 4: World Model Causal Execution & Platform Governance
- **Deliverables**: Do-Calculus intervention engine, `WorldModel` recursive Bayesian belief updater, Tiered Approval Governance runtime interlocks.
- **Evaluation Criteria**: Confounding planning errors reduced by $> 90\%$, 100% budget compliance under simulated cost-overrun attacks.
