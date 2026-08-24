# Prioritized ROI Roadmap (Return on Engineering Effort)

## Methodology & ROI Score Calculation

Each proposed capability is evaluated using the Return on Engineering Effort (ROI) formula:

$$\text{ROI Score} = \frac{\Delta \text{Capability} + \Delta \text{Reliability} + \Delta \text{Efficiency}}{\text{Engineering Hours} \times \text{Architectural Complexity}}$$

Where each metric is normalized on a scale of $1.0$ to $10.0$.

---

## Ranked Roadmap Matrix

| Rank | Capability / Subsystem Module | Target Layer | Expected Impact | Eng Hours | Complexity | ROI Score | Horizon |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: | :---: |
| **1** | **Unified Subsystem Integration Bridge** | Layers 1–4 | Unified cross-layer data contracts (`ResearchOS`, `EIOSKernel`, `AEAN`, `APODEX`). | 16h | 1.2 | **9.5** | Immediate (Phase 1) |
| **2** | **End-to-End Active Inference Routing Loop** | Layer 2 $\to$ 3 | Integrates EFE evaluations ($G = \alpha \text{EFE} + \beta \text{Pragmatic}$) into AEAN task queues. | 24h | 1.5 | **8.8** | Immediate (Phase 1) |
| **3** | **CMOS Multi-Tier Memory Consolidation** | Layer 3 | Replaces naive context injection with Ebbinghaus decay & procedural skill retrieval. | 32h | 1.8 | **8.1** | Near-Term (Phase 2) |
| **4** | **Structural Causal Model (SCM) Interventions** | Layer 2 | Do-calculus back-door adjustment for counterfactual strategy evaluation. | 40h | 2.2 | **7.4** | Near-Term (Phase 2) |
| **5** | **Multi-Agent Swarm Debate & Sycophancy Filter** | Layer 3 | Cross-examination debate with Holm-Bonferroni statistical stopping rules. | 36h | 2.0 | **7.2** | Near-Term (Phase 2) |
| **6** | **Autonomous Skill Synthesis & Registration** | Layer 3 $\to$ 4 | Auto-compiles successful Graph-of-Thought execution paths into reusable skills. | 48h | 2.5 | **6.5** | Mid-Term (Phase 3) |
| **7** | **Automated Software Engineering Repair Engine** | Layer 4 | Automated test-driven code editing with pre-commit CI integration. | 60h | 2.8 | **5.9** | Mid-Term (Phase 3) |
| **8** | **Self-Directed Research Loop Integration** | Layer 1 | Automated literature discovery, hypothesis generation, and experimental execution. | 80h | 3.2 | **5.2** | Long-Term (Phase 4) |

---

## Detailed Feature Profiles

### Rank 1: Unified Subsystem Integration Bridge
- **Architectural Rationale**: Eliminates fragmentation between Research OS, EIOS, EOS, AEAN, and APODEX by establishing common Pydantic schemas and typed interface bridges.
- **Expected Benefits**: Seamless cross-layer data flow, zero serialization overhead, unified logging.
- **Trade-offs**: Requires strict adherence to schema definitions across all subsystems.
- **Risk & Mitigation**: Schema versioning mismatches $\to$ Enforce pydantic strict validation and version headers.

### Rank 2: End-to-End Active Inference Routing Loop
- **Architectural Rationale**: Connects high-level EIOS active inference decision making directly to AEAN task execution queues.
- **Expected Benefits**: Balances exploration (epistemic value) and exploitation (pragmatic utility), lowering unnecessary token consumption by up to $30\%$.
- **Trade-offs**: EFE calculation adds minimal latency ($\sim 1.5\text{ms}$).
- **Risk & Mitigation**: Over-exploration $\to$ Dynamic temperature downshifting.
