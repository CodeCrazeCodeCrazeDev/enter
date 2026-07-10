# AgentHarness Technical Debt Analysis (Phase 1)

This document maps out areas of legacy structures, refactoring opportunities, and modules that should under no circumstances be changed during the upgrades.

---

## 1. Legacy Structural Patterns

### Coarse-Grained Checkpoint/State Payload
- **Problem**: Large task state fields (like `evidence_cards` or long text variables) are written as a single monolithic block to SQLite during phase transitions.
- **Debts**: Leads to databasebloat and potential I/O bottlenecks.

### Raw Observer Mutations
- **Problem**: Rollback and normalization observers (e.g., `ToolCallArgsNormalizer`, `DuplicateQueryRollbackObserver`) interact with the message list using direct pop/append operations.
- **Debts**: A change in the shape of standard LLM return objects could cause silent index errors in observers, leading to unstable runs.

---

## 2. Refactoring Opportunities

- **Abstract Memory Base**: Establish a formal interface for memories (`SemanticMemory`, `LongTermMemory`) rather than letting nodes directly manage local state variables.
- **Structured Verification Contract**: Formalize an abstract domain verifier signature so that parallel multi-verifier execution is uniform and easily mockable.

---

## 3. Safe Harbor: Modules to NOT Modify

To ensure benchmark reproducibility and baseline integrity, the following modules must not be altered:
1. **`benchmarks/`** (all files): The scoring, dataset fetching, and evaluation logic are sacred and must not be touched to guarantee that benchmark results are not artificially inflated or deflated.
2. **`workflows/react_base/`**: This is the legacy baseline control workflow against which new architecture variants will be compared.
3. **Core Registry & Schemas**: The standard `PipelineSpec` schemas must support backward compatibility, meaning legacy fields like `phases` must still function properly.
