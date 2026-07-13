# ADR 006: Abstract Execution Layer & Gateway Adapters

## Status
Approved

## Context
Core cognitive and economic logic must never depend directly on vendor-specific SDKs (like Stripe, HubSpot, Salesforce, etc.). Direct coupling introduces heavy technical debt, breaks unit testing, and makes replacing vendors impossible.

## Decision
We decouple execution through an abstract, asynchronous **Execution Layer** under `apodex/execution/`.
1. Core platforms interact exclusively with standard interfaces (such as `ExecutionGateway`, `CRMAdapter`, `TreasuryAdapter`, etc.).
2. We provide concrete, production-grade mock/simulated adapter implementations for testing.
3. Actual external providers (Stripe, HubSpot, Salesforce, stablecoin rails) are registered as plugins or dependency-injected adapters at runtime.

This guarantees:
- Complete isolation during testing (zero remote network requests).
- Easy provider replacement or multi-provider fallbacks (e.g. falling back to stablecoin payment if Stripe is down).

## Alternatives Considered
- **Direct vendor integration in agents**: Letting CFOAgent call Stripe directly. Highly rejected due to code pollution and violation of clean architecture.

## Consequences
- **Pros**:
  - Safe, predictable, mock-supported test suites.
  - Built-in graceful degradation and retry reliability.
- **Cons**:
  - Requires maintaining interface adapter layers for every vendor API.
