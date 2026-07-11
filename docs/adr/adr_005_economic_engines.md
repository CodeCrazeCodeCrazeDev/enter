# ADR 005: Decoupled Economic Engines & ARE (ARCS) Reference Implementation

## Status
Approved

## Context
Implementing fully production-ready systems for all economic engines (ADE, APE, ARE, ACE, AOE, ATE) simultaneously is unrealistic. However, we must establish their architecture, schemas, and boundaries so they can be developed in parallel by independent teams.

## Decision
We decouple the economic platform from specific business implementations:
1. For **all engines**, we define:
   - Interface contracts
   - Shared domain models and Pydantic transport models
   - Event and command catalogs
   - Operational workflows and extension points
2. We select **ARE (Autonomous Revenue Engine / ARCS)** as our **reference implementation**.
   - ARE is fully implemented with double-entry ledgers, tenant separation, multi-rail payment integrations (Stripe, Stablecoins), and human governance.
   - It exercises every cognitive service of the platform (planning, prediction, simulation, expected value, memory, and parallel verification).
3. Skeletons for ADE, APE, ACE, AOE, and ATE are defined under `apodex/applications/` referencing the core platform interfaces.

## Alternatives Considered
- **Implement ADE only**: ADE is a specialized marketing engine. It does not exercise economic and finance-specific capabilities (like accounting ledger auditing or currency rail settlement) as comprehensively as ARE.

## Consequences
- **Pros**:
  - Clear architectural blueprints for all 6 engines.
  - Fully implemented reference engine (ARE) acts as a high-fidelity template for the others.
- **Cons**:
  - Skeletons must be fully specified to ensure they are useful development patterns.
