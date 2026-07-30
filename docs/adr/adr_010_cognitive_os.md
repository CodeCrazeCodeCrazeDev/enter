# ADR 010: Cognitive OS Service Architecture & Shared Cognitive Bus

## Status
Proposed

## Context
AEAN's legacy system contains some duplicated responsibilities and centralized control logic. A single God Object controller or isolated services would cause high architectural drift, cascading runtime failures, and make verification or continuous self-improvement difficult.

## Decision
We establish a decentralized, event-driven Cognitive Operating System (Cognitive OS) orchestrated by a light-weight `CognitiveKernel` communicating over a `Shared Cognitive Bus`. Every subsystem has exactly one authoritative owner with frozen interface contracts.

## Alternatives Considered
1. **Monolithic Brain Object (Rejected)**: Hard to test, violates separation of concerns, high regression rate.
2. **REST API Microservices (Rejected)**: Introduces heavy network/latency overhead, complex local synchronization.

## Expected Benefits
- **Zero Duplicate Ownership**: Clean routing and authorization mapping.
- **Robust Failure Propagation**: Failure states can be published as events to the Shared Cognitive Bus for automated rollback or corrective action.
- **Strict Latency Isolation**: Enables predictable latency profiles across the entire cognitive loop.

## Migration Strategy
First deploy the Shared Cognitive Bus and abstract contracts, then incrementally migrate existing capability folders.
