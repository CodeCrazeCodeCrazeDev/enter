# Unified Cognitive Operating System Dependency Graph

## 1. Inter-Layer Dependency Diagram (Mermaid)

```mermaid
graph TD
    %% Layer 1: Scientific Research Layer
    subgraph L1 [Layer 1: Scientific Research Layer - Research OS]
        L1_DB[(500-Paper Research Corpus)]
        L1_Val[StatisticalValidator & ReproducibilityEngine]
        L1_Extract[Principle Extractor]
        L1_DB --> L1_Val --> L1_Extract
    end

    %% Layer 2: Strategic Sensing & System Decision Layer
    subgraph L2 [Layer 2: Strategic Sensing & System Decision - EIOS / EOS]
        L2_Kernel[EIOSKernel - Active Inference EFE]
        L2_Engine[11-Section EOS Dynamics Engine]
        L2_Engine14[14-Layer Computational Engine]
        L2_Kernel --> L2_Engine --> L2_Engine14
    end

    %% Layer 3: Multi-Agent Cognitive Intelligence Layer
    subgraph L3 [Layer 3: Multi-Agent Intelligence - AEAN]
        L3_Hive[HiveMind Token-Bidding Registry]
        L3_Swarm[Multi-Agent Specialization Swarms]
        L3_Opt[Genetic MAP-Elites & SFTPreference]
        L3_Hive --> L3_Swarm --> L3_Opt
    end

    %% Layer 4: Decision Platform & World Engine
    subgraph L4 [Layer 4: Decision Platform - APODEX WorldModel]
        L4_WM[Causal Graph & Bayesian Beliefs]
        L4_Brain[CognitiveBrain & Memory Hierarchy]
        L4_Skills[SkillsFlywheel Execution Engine]
        L4_WM --> L4_Brain --> L4_Skills
    end

    %% Cross-Layer Directed Dependencies & Handoffs
    L1_Extract -->|Validated Hypotheses & Extracted Principles| L2_Kernel
    L1_Extract -->|Registered Research Insights| L3_Hive
    L2_Engine14 -->|Prioritized Opportunity DAGs & Capital Allocation| L3_Hive
    L3_Opt -->|Verified Code & Trajectory Plans| L4_Skills
    L4_Skills -->|Action Execution & State Transitions| L4_WM
    L4_WM -->|Grounded World State Feedback| L2_Kernel
```

---

## 2. Layer Data Artifact & Interface Dependency Matrix

| Source Layer | Target Layer | Data Artifact / Interface | Transport Mechanism | Synchronicity |
| :--- | :--- | :--- | :--- | :--- |
| **Layer 1** | **Layer 2** | `ValidatedHypothesis` | `export_validated_hypothesis_to_kernel()` | Asynchronous Event |
| **Layer 1** | **Layer 3** | `CorpusPrinciple` | `register_301_500_paper_corpus_principles()` | In-Memory Index |
| **Layer 1 / 2** | **Layer 3** | `ResearchToSystemBridge` | `bridge_research_to_system_state()` | Orchestrated Handoff |
| **Layer 2** | **Layer 3** | `OpportunityDAG` | `ingest_opportunity_dag()` | Active Inference Queue |
| **Layer 3** | **Layer 4** | `SwarmTrajectoryPlan` | `submit_agent_plan()` | Token Bidding Protocol |
| **Layer 4** | **Layer 2** | `WorldStateObservation` | `sense_opportunity_anomalies()` | Active Inference Sensor |
