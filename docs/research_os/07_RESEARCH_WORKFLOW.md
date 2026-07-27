# 07. Research Workflow: Human-AI Collaborative Science

A world-class Quantitative Research Organization leverages both human intuition and automated scale. The **AlphaAlgo Research Workflow** defines how human quantitative researchers (Quants) and artificial intelligence agents (AI Assistants) collaborate, hand off tasks, and perform rigorous peer reviews.

The defining characteristic of this workflow is **structural checks and balances**: agents propose, but deterministic engines validate and log, and human/AI consensus approves.

---

## 1. Unified Research Protocol

The research process is organized into discrete steps, mapping onto our canonical pipeline:

```
[Quant / Agent]                       [Research OS Platform]
       |                                         |
       | 1. Formulate Hypothesis                 |
       |---------------------------------------->|
       |                                         | 2. Semantic Duplicate Check
       |                                         |    Pre-register in Registry
       |                                         |<-------------------------------
       |                                         |
       | 3. Construct Feature/Model              |
       |---------------------------------------->|
       |                                         | 4. Data Validation (Anti-Bias)
       |                                         |    Run Experiment in Sandbox
       |                                         |    Perform Statistical Audits
       |                                         |<-------------------------------
       |                                         |
       | 5. Submit for Review                    |
       |---------------------------------------->|
       |                                         | 6. Generate Verification Report
       |                                         |    Trigger Peer-Review Protocol
       |                                         |<-------------------------------
       |                                         |
       | 7. Review Audited Results               |
       |<----------------------------------------|
```

---

## 2. Peer Review and Collaborative Verification

No single model or research artifact is accepted into production without passing the **Peer Review Gate**. This mimics the peer-review process of major scientific journals (Nature, Science) and leading AI labs.

### Review Panel Structure
The review panel consists of:
1. **The Lead Quant (Human):** Reviews the code quality, economic rationale, and practical execution risk.
2. **The Automated Critic (LLM-as-a-Judge):** Reviews the complete experiment logs, checks for any potential leakage or data-snooping markers, and verifies that the statistical corrections (DSR, Benjamini-Hochberg) were applied correctly.
3. **The Risk Gateway:** A deterministic software contract that verifies the model satisfies basic drawdown, leverage, and liquidity constraints.

---

## 3. Review Artifacts: The Decision Record

Every peer-review process generates a **Decision Record** that is saved permanently to the institutional memory.

### Decision Record Schema
* `decision_id`: Unique UUID.
* `model_id` / `experiment_id`: Reference to the candidate model.
* `reviewers`: List of human and AI review identifiers.
* `evaluation_metrics`: Captured summary of DSR, PBO, and maximum historical drawdown.
* `status`: "APPROVED" | "REJECTED" | "REQUEST_REVISIONS".
* `rejection_rationales`: List of qualitative and quantitative issues raised.
* `hash_signature`: Cryptographic signature of the decision body to ensure audits cannot be retroactively modified.

By keeping these records transparent and permanent, AlphaAlgo establishes an immutable history of *why* choices were made, helping the system learn from past review rejections.
