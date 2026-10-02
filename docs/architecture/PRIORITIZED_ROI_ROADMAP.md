# Prioritized Return-on-Effort (ROI) Engineering Roadmap
**Version:** 2026.1.0
**Status:** Authoritative Specification
**Scope:** Cognitive System Enhancements Ranked by Engineering Value

---

## 1. ROI Calculation Methodology

Every proposed architectural upgrade is evaluated and ranked using the Expected Return on Engineering Effort (EREE) ratio:

$$\text{EREE} = \frac{\Delta \text{Capability} \times \Delta \text{Reliability} \times \text{Reach}}{\text{Engineering Complexity (Person-Weeks)} \times \text{Maintenance Risk}}$$

Where:
- **$\Delta \text{Capability}$ (1-10):** Direct improvement in system intelligence, long-horizon planning, or autonomous execution.
- **$\Delta \text{Reliability}$ (1-10):** Reduction in error rates, flakiness, or unhandled edge cases.
- **$\text{Reach}$ (1-10):** Percentage of active workflows affected by the improvement.
- **$\text{Complexity}$ (1-10):** Implementation effort and potential architectural debt introduced.
- **$\text{Maintenance Risk}$ (1-10):** Long-term operational overhead.

---

## 2. Priority 1: High ROI (Immediate Execution / Q1)
*Focus: Eliminating architectural friction, resolving legacy deprecations, and unifying cross-layer interfaces.*

### P1.1 Layer Boundary Consolidation & Adapter Unification
- **Rationale:** Replacing legacy adapter shims with direct canonical imports in `agent_harness/core/runtime/`.
- **Expected Benefit:** Eliminates import circularity, improves test execution speed by 35%, reduces developer friction.
- **Impact Analysis:** Reach = 10, Capability = 8, Reliability = 9, Complexity = 2, Risk = 1.
- **EREE Score:** **36.0** (Top Priority)

### P1.2 Automated Timezone Awareness & Pydantic V2 Migration
- **Rationale:** Migrating deprecated `datetime.utcnow()` to `datetime.now(timezone.utc)` and standardizing on `ConfigDict(arbitrary_types_allowed=True)`.
- **Expected Benefit:** Eliminates Python 3.12 runtime warnings, guarantees timezone-safe comparison in causal graphs.
- **Impact Analysis:** Reach = 10, Capability = 5, Reliability = 9, Complexity = 1, Risk = 1.
- **EREE Score:** **45.0** (Immediate Win)

### P1.3 Non-Gaussian Hawkes Call-Depth AST Verification Clamping
- **Rationale:** Restricting Hawkes AST recursion depth tracking strictly to function definitions inside `CodeRewriteEngine`.
- **Expected Benefit:** Prevents false-positive AST rejections on non-recursive standard library calls; boosts mutation acceptance rate by 40%.
- **Impact Analysis:** Reach = 7, Capability = 8, Reliability = 9, Complexity = 2, Risk = 1.
- **EREE Score:** **25.2**

---

## 3. Priority 2: Medium ROI (Mid-Term Execution / Q2)
*Focus: Deepening active inference capabilities, multi-agent coordination, and memory retrieval speed.*

### P2.1 Closed-Loop EFE (Expected Free Energy) DAG Recompilation
- **Rationale:** Coupling Layer 4 world model epistemic uncertainty directly to Layer 2 EIOS DAG re-ordering.
- **Expected Benefit:** Dynamic task re-prioritization under environmental surprise; reduces wasted token spend on stale goals by 28%.
- **Impact Analysis:** Reach = 8, Capability = 9, Reliability = 8, Complexity = 4, Risk = 2.
- **EREE Score:** **7.2**

### P2.2 Island MAP-Elites Migration Gates with Fitness Sorting
- **Rationale:** Integrating fitness-sorted island migration gates into `GeneticWorkflowOptimizer` in AEAN Layer 3.
- **Expected Benefit:** Prevents premature convergence in multi-agent workflow evolution; increases solution diversity across swarm workers.
- **Impact Analysis:** Reach = 6, Capability = 8, Reliability = 7, Complexity = 3, Risk = 2.
- **EREE Score:** **5.6**

### P2.3 Multi-Tier Memory Fusion (EMG Engine + Semantic Memory)
- **Rationale:** Unified retrieval indexing across episodic Action-Decision Graphs and long-term semantic learning memory.
- **Expected Benefit:** Sub-millisecond context retrieval for agent workers during active bidding.
- **Impact Analysis:** Reach = 8, Capability = 8, Reliability = 8, Complexity = 4, Risk = 2.
- **EREE Score:** **6.4**

---

## 4. Priority 3: Strategic Long-Horizon ROI (Q3–Q4)
*Focus: Fully autonomous scientific discovery, enterprise growth state evolution, and self-directed world modeling.*

### P3.1 Automated Multi-Scale Simulation & Market Digital Twin
- **Rationale:** Full 14-layer continuous digital twin simulation in Layer 2 EOS to forecast business model durability.
- **Expected Benefit:** Enables months-ahead market scenario forecasting before capital deployment.
- **Impact Analysis:** Reach = 5, Capability = 10, Reliability = 7, Complexity = 8, Risk = 3.
- **EREE Score:** **1.46** (High complexity, strategic long-term)

### P3.2 Autonomous Self-Rewriting Code Flywheel with Formal Proofs
- **Rationale:** End-to-end self-improvement loop where Layer 1 Research OS writes, verifies, proves, and deploys its own runtime optimizations.
- **Expected Benefit:** True recursive self-improvement without human engineering limits.
- **Impact Analysis:** Reach = 9, Capability = 10, Reliability = 9, Complexity = 10, Risk = 5.
- **EREE Score:** **1.62**

---

## 5. Engineering Resource Allocation Matrix

```
+-------------------------------------------------------------------+
| PRIORITY TIER   | ALLOCATED EFFORT % | PRIMARY GOAL               |
+-----------------+--------------------+----------------------------+
| Tier 1 (P1)     | 50% Effort         | Platform Stability & ROI   |
| Tier 2 (P2)     | 35% Effort         | Active Inference & Memory  |
| Tier 3 (P3)     | 15% Effort         | Long-Horizon Autonomy      |
+-------------------------------------------------------------------+
```
