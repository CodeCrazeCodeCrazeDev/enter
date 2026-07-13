# ADR 001: Cognitive Operating System (OS) Architecture Pattern

## Status
Approved

## Context
Traditional LLM frameworks typically follow a monolithic, flat ReAct loop or single-agent orchestration model. This couples strategy, low-level execution, memory, and business logic into a single context, causing rapid token decay, cognitive overload, and limits long-horizon scalability. To evolve Apodex into a General Cognitive Platform capable of running multiple Domain Intelligence Platforms, we need a clean separation of concerns.

## Decision
We select a layered **Cognitive Operating System (OS)** architectural pattern. Everything in the platform fits into distinct, well-defined vertical and horizontal layers of responsibility:

```text
Infrastructure Layer
    Cloud, Storage, Messaging, Networking
Execution Layer
    External gateways and platform adapters (CRM, ERP, Treasury)
Cognitive Platform (Apodex Core)
    Memory, Planning, Reasoning, World Model, Simulation, Prediction
Economic Platform (AEAN Foundation)
    Markets, Contracts, Capital, Resource Allocation
Application Layer
    Economic Engines: ADE, APE, ARE (ARCS), ACE, AOE, ATE
```

By structuring Apodex as a Cognitive OS:
1. **Separation of Concerns**: Core cognition is domain-agnostic; economic engines implement business workflows; execution adapters interact with the outside world.
2. **Horizontal Extensibility**: New applications or specialized organs (e.g. ADE, APE) can be added cleanly as plugins without rewriting the core cognitive subsystems.
3. **Pluggability**: The underlying model or API can be changed or simulated without altering the higher layers.

## Alternatives Considered
- **Monolithic Agent Loop**: Direct extension of `agent_loop.py`. Rejected due to high coupling and poor extensibility for complex corporate multi-agent workflows.
- **Microservices Architecture**: Separate processes for each service. Rejected for initial implementation due to high IPC/RPC latency and infrastructure complexity, though the interfaces are designed to support future distribution.

## Consequences
- **Pros**:
  - High long-term maintainability and robust code separation.
  - Standardized cognitive interfaces can be reused across economic domains (software engineering, cybersecurity, finance).
- **Cons**:
  - Requires explicit translation and mapping between layers.
  - Marginally higher initialization latency due to interface instantiation, which is mitigated via dependency injection/caching.
