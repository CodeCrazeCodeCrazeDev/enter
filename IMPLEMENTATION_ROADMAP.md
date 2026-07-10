# AgentHarness Architectural Upgrade Implementation Roadmap

To avoid massive, unstable refactors, we divide the 10 upgrades into clean, independently-reversible, and fully testable pull requests.

---

## Phased Pull Request Schedule

### PR 1: Hierarchical Multi-Agent Orchestration
- **Deliverables**: `HierarchicalOrchestrator`, `CoordinatorAgent`, and `WorkerAgent` implementations.
- **Verification**: Dedicated multi-agent routing unit tests and baseline smoke tests.

### PR 2: Planner / Executor Separation
- **Deliverables**: Separation of planning strategy nodes from sequential tool executors.
- **Verification**: Mock planner execution verification and flow validation.

### PR 3: Persistent Semantic Memory
- **Deliverables**: Fact, belief, and unresolved question storage module.
- **Verification**: Persistence tests writing and loading context cards.

### PR 4: World Model
- **Deliverables**: Entity, causal, and temporal graph representation structures.
- **Verification**: Graph query correctness assertions.

### PR 5: Parallel Verification
- **Deliverables**: Parallel Domain Verifier execution with Meta Verifier synthesis.
- **Verification**: Parallel mock task execution timings and verification.

### PR 6: Meta-Reasoner
- **Deliverables**: Live token monitor and logic duplication analyzer.
- **Verification**: Loop trap detection test cases.

### PR 7: Long-Term Learning Memory
- **Deliverables**: Cross-session strategies registry.
- **Verification**: Inter-session strategy cache reload testing.

### PR 8: Self-Improvement Flywheel
- **Deliverables**: Trajectory validator and training dataset generation pipeline.
- **Verification**: High-fidelity trace file parsing tests.

### PR 9: Graph-of-Thought Reasoning
- **Deliverables**: Branching/Merging thought-node manager.
- **Verification**: Non-linear reasoning traversal testing.

### PR 10: Active Learning
- **Deliverables**: Entropy and uncertainty threshold engine.
- **Verification**: Confidence query triggered test routines.
