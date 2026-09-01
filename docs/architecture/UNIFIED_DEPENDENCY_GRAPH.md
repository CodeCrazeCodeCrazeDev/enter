# Unified Dependency Graph Specification

## Overview
This document defines the acyclic dependency graph across the 4-layer cognitive operating system taxonomy.

## Directed Dependency Flows
```
[ Layer 1: Research OS ]
       |
       v  (Hypotheses & Empirical Validation)
[ Layer 2: EIOS / EOS ]
       |
       v  (Strategic Goals & Active Inference DAGs)
[ Layer 3: AEAN Multi-Agent Core ]
       |
       v  (Actions & Perception-Knowledge Chain Traces)
[ Layer 4: APODEX WorldModel & Protocols ]
```

## Layer-by-Layer Interfaces
- **Research OS -> EIOS/EOS**: Validated hypotheses export to EIOS Kernel sensing and EOS HypothesisEngine.
- **EOS -> AEAN**: Strategic goals compile into DAGs and dispatch task bids to HiveMind.
- **AEAN -> APODEX**: Trajectories update CausalNodes, RelationEdges, and Belief states in WorldModel.
