# Prioritized Engineering ROI Roadmap

## 1. Prioritization Framework

All engineering initiatives are evaluated and ranked based on **Expected Return on Engineering Effort (ROI)**:

$$\text{ROI} = \frac{\Delta \text{Capability} + \Delta \text{Reliability} + \Delta \text{Safety}}{\text{Engineering Hours} \times \text{Architectural Complexity}}$$

---

## 2. Priority Tiers

### Tier 1: Core System Unification & Active Inference Control Loop (Highest ROI)
- **Objective**: Redesign Research OS, EIOS, EOS, AEAN, and APODEX into the 4-layer taxonomy with zero capability duplication and unified EFE control loop.
- **Expected ROI**: $10\times$ baseline.
- **Key Deliverables**:
  1. Integration of `ResearchToSystemBridge` across Layer 1 to Layer 4.
  2. EIOS Active Inference EFE sensing and topological DAG compiler.
  3. AEAN HiveMind token bidding multi-agent task dispatch.
  4. WorldModel causal graph and recursive Bayesian belief updates.

### Tier 2: Institutional-Grade Safety, Governance & Meta-Reasoning (High ROI)
- **Objective**: Guarantee zero runaway loops, strict token budget enforcement, and multi-signature execution safety.
- **Expected ROI**: $5\times$ baseline.
- **Key Deliverables**:
  1. Meta-Reasoner loop intervention observers.
  2. Cost Tier Enforcer & budget downshifting/halting mechanics in `SkillsRunner`.
  3. Tiered approval workflows for live execution and capital allocation.
  4. AST non-Gaussian Hawkes stability verification for automated code rewrites.

### Tier 3: Long-Horizon Execution, SFT Preference & Workflow Optimization (Medium-High ROI)
- **Objective**: Extend continuous agent execution window to $100+$ turns and enable automated workflow hyper-parameter evolution.
- **Expected ROI**: $3\times$ baseline.
- **Key Deliverables**:
  1. Genetic Workflow Optimizer with island MAP-Elites migration gates.
  2. SFT Preference Collector with clipped advantage margin calculation.
  3. Learnable routing gate dispatcher with budget decay.
  4. CMOS hierarchical memory retrieval optimization (epistemic + semantic + working memory).

### Tier 4: Continuous Research Ingestion & 1000-Paper Corpus Scaling (Medium ROI)
- **Objective**: Continuously synthesize SOTA academic literature into executable runtime principles.
- **Expected ROI**: $2\times$ baseline.
- **Key Deliverables**:
  1. Automated research ingestion pipeline with zero duplicate title/DOI enforcement.
  2. Direct injection of research insights into AEAN HiveMind bidding registry.
  3. Automated statistical validation (DSR, P-value clamping) on incoming research benchmarks.

---

## 3. Engineering Allocation Matrix

| Initiative / Subsystem | Target Layer | Estimated Effort (Person-Weeks) | Expected Capability Uplift | Priority Tier |
|---|---|---|---|---|
| **Unified 4-Layer Control Loop** | Layers 1-4 | 2 | $+40\%$ Cross-Layer Task Throughput | **Tier 1** |
| **Meta-Reasoner Observer** | Layer 3 | 1 | $-95\%$ Repetitive Tool Call Loops | **Tier 2** |
| **Recursive Bayesian World Model**| Layer 4 | 2 | $+35\%$ Decision Precision Under Uncertainty| **Tier 1** |
| **Genetic Workflow Optimization** | Layer 3 | 2 | $+25\%$ Agent Trajectory Efficiency | **Tier 3** |
| **500-Paper Principle Registry** | Layer 1 | 1 | $+30\%$ Automated Hypothesis Rigor | **Tier 4** |
