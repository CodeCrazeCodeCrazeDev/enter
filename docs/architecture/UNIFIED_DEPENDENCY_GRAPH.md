# Unified Dependency Graph & Inter-Subsystem Communication

## Visual Architecture Diagram

```
+-----------------------------------------------------------------------------------+
| LAYER 4: APODEX Autonomous Execution Platform                                      |
| [ComputationalArchitectureOfEntrepreneurship] (14-Layer Engine)                   |
+-----------------------------------------------------------------------------------+
             ^                                                        |
             | Executive Strategy & Capital Allocation Policies        | Multi-Objective Feedback
             v                                                        v
+-----------------------------------------------------------------------------------+
| LAYER 3: AEAN Cognitive Intelligence Layer                                         |
| [CognitiveBrain] <---> [HiveMind Swarm] <---> [EMGEngine / SkillRegistry]          |
+-----------------------------------------------------------------------------------+
             ^                                                        |
             | Active Learning Task Decompositions                    | Evaluated State & EFE Beliefs
             v                                                        v
+-----------------------------------------------------------------------------------+
| LAYER 2: EIOS / EOS Operating Kernel Layer                                        |
| [EIOSKernel] <---> [ActiveInferenceEngine] <---> [EOSEngine]                      |
+-----------------------------------------------------------------------------------+
             ^                                                        |
             | Validated Hypotheses & Evidence Handoff               | Empirical Performance Signals
             v                                                        v
+-----------------------------------------------------------------------------------+
| LAYER 1: Research OS Scientific Engine Layer                                       |
| [ResearchOS] <---> [300-Paper Research DB] <---> [StatisticalValidationEngine]    |
+-----------------------------------------------------------------------------------+
```

## Direct Interface Contracts

1. **Research OS -> EIOS Kernel Contract (`Layer 1 -> Layer 2`)**:
   - Class: `apodex.ai_eos.research.integration.ResearchToSystemBridge`
   - Method: `bridge_hypothesis_to_kernel(hypothesis_id)`
   - Data Payload: Structured hypothesis schema containing prior belief parameters, expected variance, and domain tags.

2. **EIOS Kernel -> AEAN Brain Contract (`Layer 2 -> Layer 3`)**:
   - Class: `apodex.arcs.kernel.kernel.EIOSKernel`
   - Method: `trigger_cognitive_reasoning(anomaly_event)`
   - Data Payload: Anomaly signal vector, EFE score, and pragmatic value expectations.

3. **AEAN Brain -> APODEX Platform Contract (`Layer 3 -> Layer 4`)**:
   - Class: `apodex.ai_eos.intelligence.computational_architecture.ComputationalArchitectureOfEntrepreneurship`
   - Method: `execute_layer_pipeline(inputs)`
   - Data Payload: Strategic policy vector, risk tolerance metrics, and budget bounds.
