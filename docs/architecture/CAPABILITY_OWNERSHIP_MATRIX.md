# Capability Ownership Matrix & Single Authority Model

## Principles of Capability Single Authority

To prevent architectural duplication, split-brain logic, and ambiguous subsystem boundaries, every capability within the platform is assigned to **exactly one primary layer**.

---

## Master Capability Ownership Matrix

| Capability Category | Specific System Capability | Owning Subsystem Layer | Implementation File / Module | Duplicate Veto Invariant |
| :--- | :--- | :--- | :--- | :--- |
| **Scientific Research** | Literature Review Synthesis & Corpus Querying | **Layer 1 (Research OS)** | `apodex/ai_eos/research/research_os.py` | L2, L3, L4 MUST NOT implement standalone literature search engines. |
| **Scientific Validation**| White's Reality Check & Deflated Sharpe Ratio | **Layer 1 (Research OS)** | `apodex/ai_eos/research/research_os.py` | Statistical p-value validation logic resides exclusively in L1. |
| **Opportunity Sensing** | Market & System Anomaly Stream Sensing | **Layer 2 (EIOS / EOS)** | `apodex/arcs/kernel/kernel.py` | Real-time sensor anomaly streams are captured solely by EIOS. |
| **Workflow Compilation**| Active Inference DAG Task Compilation | **Layer 2 (EIOS / EOS)** | `apodex/arcs/kernel/kernel.py` | Task DAG creation is managed by EIOS Kernel. |
| **Opportunity Decision**| Entrepreneurial State Machine & Decision Tree | **Layer 2 (EIOS / EOS)** | `apodex/ai_eos/intelligence/eos_engine.py` | 11-section entrepreneurial stage decisions belong exclusively to EOS. |
| **Capital Allocation** | Risk-Adjusted Capital & Resource Distribution | **Layer 2 (EIOS / EOS)** | `apodex/arcs/capital/allocation_engine.py` | Treasury and capital distribution decisions belong to L2. |
| **Agent Bidding** | Token-Bidding Task Allocation & Registry | **Layer 3 (AEAN)** | `apodex/aean/coordination/hive_mind.py` | Task bidding and agent token clearing belong to AEAN HiveMind. |
| **Role Specialization** | PAEAN / ADE / AVIE / ARE Agent Roles | **Layer 3 (AEAN)** | `apodex/aean/engines/` | Specialized prompt strategies and narratives belong to AEAN engines. |
| **Epistemic Critique** | Robust Epistemic Validation (RGAE) | **Layer 3 (AEAN)** | `apodex/aean/validation/rgae.py` | Epistemic validation and counter-critique belong to AEAN. |
| **Causal World Graph** | Directed Causal Graph & Entity Relationships | **Layer 4 (APODEX Platform)**| `apodex/world_model/world_model.py` | Entity node creation and causal edge tracking belong to L4. |
| **Belief Revision** | Recursive Bayesian Belief Network Updating | **Layer 4 (APODEX Platform)**| `apodex/world_model/domain/beliefs.py` | Subject-predicate-confidence belief updating belongs to L4. |
| **Memory Substrate** | Persistent Semantic Memory & CMOS Ledger | **Layer 4 (APODEX Platform)**| `apodex/arcs/memory/unified_memory.py` | Persistent SQLite and CMOS vector memory belong to L4. |
| **Skill Execution** | Protocol Runner & Skill Execution Flywheel | **Layer 4 (APODEX Platform)**| `apodex/skills/runner.py` | Tool execution protocols and step budgets belong to L4. |
| **Safety Governance** | AST Security Linting & Security Vetoes | **Layer 4 (APODEX Platform)**| `apodex/world_model/governance/policy.py` | Platform safety and GRC policy enforcement reside in L4. |
