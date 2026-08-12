# AgentHarness Architectural Dependency Graph (Phase 1) - Enhanced

> ### ⚠️ DOCUMENT STATUS: CONSOLIDATED & UNIFIED
> This dependency specification has been fully consolidated into the authoritative, single-source-of-truth **Unified Cognitive Operating System Architecture Specification**.
>
> All component-level dependencies, class-level imports, and system interfaces are mapped under the 4-layer taxonomy defined at:
> **[docs/architecture/UNIFIED_COGNITIVE_OS_ARCHITECTURE.md](docs/architecture/UNIFIED_COGNITIVE_OS_ARCHITECTURE.md)**

---

## 1. System Interface Dependency Diagram

The Mermaid diagram below defines how components from Research OS, EIOS, EOS, AEAN, and APODEX interact as cohesive layers without duplicated capabilities:

```mermaid
graph TD
    classDef research fill:#ffccff,stroke:#333,stroke-width:2px;
    classDef intelligence fill:#cce6ff,stroke:#333,stroke-width:2px;
    classDef execution fill:#ffffcc,stroke:#333,stroke-width:2px;
    classDef decision fill:#d9ffcc,stroke:#333,stroke-width:2px;

    subgraph Layer1 [Layer 1: Research OS (Research Layer)]
        ROS[Research OS Engine]:::research
        LitIndex[Literature Index]:::research
    end

    subgraph Layer2 [Layer 2: AEAN (Cognitive Intelligence Layer)]
        Planner[Strategic Planner]:::intelligence
        WorldModel[Continuous World Model]:::intelligence
    end

    subgraph Layer3 [Layer 3: EIOS / EOS (Execution & Orchestration Layer)]
        CompArch[14-Layer Computational Arch]:::execution
        BizLoops[13 Business Loops]:::execution
    end

    subgraph Layer4 [Layer 4: APODEX (Decision & Execution Layer)]
        ReAct[ReAct Loop Engine]:::decision
        SLA[SLA Observability Monitor]:::decision
        Sandbox[Sandbox Execution]:::decision
    end

    %% Input/Output Flow Contracts
    ROS -->|1. Promoted Theories & Evidence| WorldModel
    Planner -->|2. Active Inference Scenarios| BizLoops
    BizLoops -->|3. Playbooks & Workflows| ReAct
    ReAct -->|4. Execution Traces & Telemetry| SLA
    SLA -->|5. Rollback Controls| ReAct
    ReAct -->|6. Discrepancy Logs / Lessons| ROS
```

---

## 2. Directory & Namespace Structure Mapping

The repository is structured to isolate infrastructural mechanisms from runtime nodes:

*   `apodex/research_os/`: Houses the scientific hypothesis, literature review, and claim ingestion pipelines (Layer 1).
*   `apodex/world_model/` & `apodex/planning/`: Drives multi-graph state, causal do-calculus, and Active Inference strategic planners (Layer 2).
*   `apodex/ai_eos/` & `apodex/skills/`: Holds business model canvas generators, 14-layer computational layers, and strategic skills (Layer 3).
*   `apodex/execution/` & `apodex/evolution/`: Manages ReAct loops, live SLA telemetry, staged rollouts, and automatic canary rollback operations (Layer 4).

For typed interfaces and strict package boundary rules, refer to **[docs/architecture/UNIFIED_COGNITIVE_OS_ARCHITECTURE.md](docs/architecture/UNIFIED_COGNITIVE_OS_ARCHITECTURE.md)**.
