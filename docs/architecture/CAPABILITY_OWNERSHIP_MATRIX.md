# Capability Ownership Matrix
## AEAN / EIOS / EOS / APODEX Layered Cognitive Operating System

| Capability Domain | Subsystem Layer Owner | Primary Module Path | Prohibited Overlaps / Duplication Rules |
|---|---|---|---|
| **Scientific Literature & Hypothesis Validation** | Layer 1 (Research OS) | `apodex/ai_eos/research/` | EIOS/EOS/AEAN/APODEX must NOT perform literature search or paper corpus extraction directly. |
| **Active Inference EFE & Opportunity DAGs** | Layer 2 (EIOS / EOS Engine) | `apodex/arcs/kernel/`, `apodex/ai_eos/intelligence/` | Research OS and AEAN must NOT construct enterprise execution trees directly. |
| **Multi-Agent Bidding & Swarm Coordination** | Layer 3 (AEAN HiveMind) | `apodex/aean/coordination/` | EOS Engine and WorldModel must NOT manage individual agent worker bidding pools directly. |
| **Causal Graph & Bayesian Belief Modeling** | Layer 4 (APODEX WorldModel) | `apodex/world_model/` | Layers 1-3 must NOT execute counterfactual SCM graph updates independently. |
