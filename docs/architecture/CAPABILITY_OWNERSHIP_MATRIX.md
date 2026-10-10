# Capability Ownership Matrix (Eliminating Architectural Duplication)

## System Functionality & Layer Ownership

| Subsystem / Functional Module | Owning Layer | Exclusively Responsible For | Strictly Prohibited From |
|---|---|---|---|
| **Research OS** | **Layer 1** | Scientific paper ingestion, hypothesis generation, statistical experimentation, principle extraction | Direct agent task dispatch, capital allocation, global world state updates |
| **EIOS Kernel** | **Layer 2** | Workflow execution DAG scheduling, resource bounding, active inference anomaly sensing | Direct LLM prompt engineering, raw research ingestion, Bayesian causal graph edits |
| **EOS Engine** | **Layer 2** | Entrepreneurial capital management, unit economics simulation, SLA enforcement | AST code rewriting, multi-agent bidding resolution |
| **AEAN HiveMind** | **Layer 3** | Swarm agent capability registration, sealed-bid auctions, semantic memory retrieval, AST refactoring | Top-level research strategy definition, global Bayesian belief network updates |
| **APODEX World Model** | **Layer 4** | Causal DAG representation, Bayesian belief updates, do-calculus intervention analysis, EFE calculation | Executing terminal commands, scheduling pipeline DAG nodes |

---

## Inter-Layer Boundary Guarantees

1. **No Duplicated Memory Stores:** Single semantic memory network maintained in Layer 3 AEAN, queried by Layer 2 and Layer 1 via explicit read interfaces.
2. **No Duplicated Schedulers:** Workflow scheduling is strictly owned by Layer 2 `EIOSKernel`; Layer 3 `HiveMind` only bids on and executes scheduled tasks.
3. **No Duplicated Causal Graphs:** World state causal dependencies are strictly maintained in Layer 4 `APODEX WorldModel`.
