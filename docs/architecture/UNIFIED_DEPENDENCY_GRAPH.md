# Unified Cognitive System Dependency Graph

```
+-----------------------------------------------------------------------------------+
| LAYER 4: APODEX World Model & Cognitive Brain                                      |
| (apodex.world_model.*, apodex.cognition.*)                                         |
|  - Causal Nodes, Bayesian Beliefs, Safety Governance                              |
+-----------------------------------------------------------------------------------+
                                   ^              ^
                         State     |              | Execution
                         Updates   |              | Verification
                                   |              |
+-----------------------------------+              +--------------------------------+
| LAYER 3: AEAN Multi-Agent Subsystem                                               |
| (apodex.aean.*)                                                                   |
|  - HiveMind Bidding Engine, Energy Workflows, Swarm Allocation                    |
+-----------------------------------------------------------------------------------+
                                   ^
                                   | Opportunity Nodes & Strategy Directives
                                   |
+-----------------------------------------------------------------------------------+
| LAYER 2: EIOS Kernel & EOS Engine                                                 |
| (apodex.arcs.kernel.*, apodex.ai_eos.intelligence.*)                              |
|  - EFE Sensing, Opportunity Graph, First Principles EOS                           |
+-----------------------------------------------------------------------------------+
                                   ^
                                   | Validated Hypotheses & Extracted Principles
                                   |
+-----------------------------------------------------------------------------------+
| LAYER 1: Research OS                                                              |
| (apodex.research_os.*, apodex.ai_eos.research.*)                                  |
|  - Paper Ingestion, WDL Pipelines, Statistical Controls, Principle Registry      |
+-----------------------------------------------------------------------------------+
```

## Architectural Dependency Constraints

1. **Strict Upward Layering:**
   - Layer 1 (`apodex.research_os`) MUST NOT import from Layer 2, Layer 3, or Layer 4.
   - Layer 2 (`apodex.arcs.kernel`, `apodex.ai_eos`) may import from Layer 1.
   - Layer 3 (`apodex.aean`) may import from Layer 1 and Layer 2.
   - Layer 4 (`apodex.world_model`, `apodex.cognition`) serves as the state substrate and may be referenced across orchestration loops.

2. **Cross-Layer State Handoff Adapter:**
   - All state transitions across layers MUST pass through `apodex.ai_eos.research.integration.ResearchToSystemBridge`.
