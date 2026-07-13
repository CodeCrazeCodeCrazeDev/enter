# ADR 002: Inverted Integration & Adapter Pattern for AgentHarness

## Status
Approved

## Context
AgentHarness was previously treated as the primary execution engine, with cognitive features implemented directly within it. Continuing to expand AgentHarness couples Apodex's core logic with the evaluation harness, making it difficult to run Apodex independently or deploy it in different runtime environments (such as remote cloud workers).

## Decision
We invert the relationship between Apodex and AgentHarness.
- **Apodex** becomes the primary, root-level package containing all cognitive, economic, execution, and simulation services.
- **AgentHarness** is treated strictly as an adapter and compatibility layer.
- Submodule files in `AgentHarness/agent_harness` are implemented as thin wrappers/adapters that delegate to the clean, production-grade APIs defined inside `from apodex import ...`.

This inversion ensures:
1. **Historical Decoupling**: Legacy evaluation requirements do not restrict the architecture of the production platform.
2. **Ease of Verification**: Existing test suites run against the harness adapters seamlessly, validating that the underlying Apodex platform exhibits correct behavioral compatibility.

## Alternatives Considered
- **Inline Refactoring inside AgentHarness**: Keeping the code inside the submodule. Rejected because submodule modifications are difficult to track, deploy, and package across parent projects.

## Consequences
- **Pros**:
  - Extremely clean package separation.
  - Zero pollution of production platform code with test harness/benchmark specifics.
- **Cons**:
  - Requires maintaining adapter files inside the `AgentHarness/` submodule directory.
