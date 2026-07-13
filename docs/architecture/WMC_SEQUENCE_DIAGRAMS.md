# World Model Creator (WMC) Sequence Flows & State Machines
## Architectural Workflows and Lifecycle Transitions

---

## 1. High-Level Scenario Workflows

This document outlines the step-by-step interactions between the ten core engines, the Apodex Cognitive OS, and the Human Governance Layer.

### 1.1 Trend Ingestion & Causal Mapping (Reality Ingestion)
The following sequence shows how the WMC ingests real-world data, updates the World Graph, and notifies downstream applications of market opportunities:

```mermaid
sequenceDiagram
    autonumber
    participant RSS as External Data Feeds
    participant RE as Reality Engine
    participant WG as World Graph (Storage-Independent)
    participant MW as Meta-World Engine
    participant Coord as WMC Coordinator Core
    participant App as ARCS (Market Intelligence)

    RSS->>RE: Transmit News & Macro Data Streams
    RE->>RE: Parse, Deduplicate & Extract Entities
    RE->>WG: Query Existing Node Neighborhoods
    WG-->>RE: Return Entity Neighborhood Data
    RE->>RE: Run Cross-correlation & Assert Causal Links
    RE->>WG: Apply AddEntity & AssertCausalRelationship deltas
    RE->>MW: Sync Meta-World Global Context
    RE->>Coord: Publish RealityStateUpdatedEvent
    Coord->>App: Notify of Structural State Changes
    App->>App: Scan for profit/arbitrage opportunities
```

---

### 1.2 Multi-Option Scenario Simulation & Optimization
The following workflow details how the Apodex Planner requests simulation of multiple candidate strategies (such as testing different pricing levels) to optimize decisions before executing them:

```mermaid
sequenceDiagram
    autonumber
    participant Plan as Apodex Core Planner
    participant Coord as WMC Coordinator Core
    participant Sim as World Simulation Engine
    participant Cog as Human Cognition Engine
    participant Econ as Economic Intelligence Engine
    participant CIE as Creative Intelligence Engine

    Plan->>Coord: Request Scenario Optimization (Candidates A, B & C)
    Coord->>Sim: Command: CreateTimelineBranchCommand (Branch A, B, C)
    Sim->>Sim: Initialize Timeline Trees
    Sim-->>Coord: Publish TimelineBranchedEvent

    loop For each branch (A, B, C) in parallel
        Coord->>Sim: Command: StepSimulationCommand (Logical T+1 Month)
        Sim->>Cog: Request Cohort Behavioral Projections
        Cog->>Cog: Run Cognitive Bias & Attention Decays
        Cog-->>Sim: Return Cohort Response Vectors
        Sim->>Econ: Project Cash Flows, CAC & LTV
        Econ-->>Sim: Return Unit Economic Margins
        Sim->>Sim: Resolve causal feedback loops and compute final node states
    end

    Sim-->>Coord: Sim Completed (Branches A, B, C State Summaries)
    Coord->>CIE: Request Concept Selection (Compare Outcomes)
    CIE->>CIE: Score Candidates (Conversion, Originality, Controversy, Retention)
    CIE-->>Coord: Return Optimal Candidate (Candidate B selected)
    Coord-->>Plan: Return Scenario Recommendation with Causal Explanations
```

---

### 1.3 Supervised Media Generation & Governance Workflow
This sequence illustrates how media generation is planned, audited against strict safety policies, escalated to human curators if needed, and finalized:

```mermaid
sequenceDiagram
    autonumber
    participant Coord as WMC Coordinator Core
    participant GME as Generative Media Engine
    participant Pol as Policy Engine (Governance)
    participant Human as Human Approval Console (Curator)
    participant Models as Foundation Model APIs (Images, 3D, Audio)

    Coord->>GME: Command: CreateMediaGenerationPlanCommand (Candidate B)
    GME->>GME: Compile Multi-Modal Generation Blueprint & Model Route Paths
    GME->>Pol: Validate Generation Blueprint & Prompts

    alt Blueprint violates policy or flag is High Risk
        Pol->>Coord: Raise PolicyViolationDetectedEvent
        Coord->>Human: Escalate Proposal to Curators (State 2 Review)
        Human-->>Coord: Resolve Exception & Approve (curated prompt overrides)
        Coord->>GME: Re-Authorize Plan with curator overrides
    else Blueprint is compliant (Low Risk)
        Pol-->>GME: Blueprint Authorized
    end

    GME->>Models: Dispatch Parallel Generation Requests
    Models-->>GME: Return Generated Assets (Raw Images, Video, Audio)
    GME->>GME: Run Post-Processing, cross-modal sync, and alignment
    GME->>Coord: Publish AssetRenderCompletedEvent
```

---

## 2. Core State Machines & Lifecycles

The WMC maintains internal state machine transitions for timelines, hypotheses, and rendering workflows.

### 2.1 Timeline Lifecycle
Timelines represent versioned states of a simulated or real world. A timeline can transit through the following states:

```
        +---------------+
        |    Draft      |  <-- Initialized state
        +-------+-------+
                |
                | (Compile & Apply Deltas)
                v
        +---------------+
        |   Executing   |  <-- Simulation calculations active
        +-------+-------+
                |
                +-----------------------------------------+
                | (Sim step finishes)                     | (Causal failure)
                v                                         v
        +---------------+                         +---------------+
        |   Committed   |                         |    Failed     |
        |  (ReadOnly)   |                         +---------------+
        +-------+-------+
                |
                | (Merge to main / Prune)
                v
        +---------------+
        |   Archived    |  <-- Read-only archive state
        +---------------+
```

### 2.2 Hypothesis Evaluation State Machine
Hypotheses represent unproven beliefs tested inside the simulation loop:

```
                  +-----------------+
                  |   Formulated    |  <-- Initial state
                  +--------+--------+
                           |
                           | (Injected into branch)
                           v
                  +-----------------+
                  |    Testing      |  <-- Active in simulation
                  +--------+--------+
                           |
            +--------------+--------------+
            | (P(B|E) >= 0.8)             | (P(B|E) < 0.2)
            v                             v
   +-----------------+           +-----------------+
   |    Validated    |           |    Refuted      |
   | (Merge to main  |           | (Pruned /       |
   |  world beliefs) |           |  Archived)      |
   +-----------------+           +-----------------+
```
