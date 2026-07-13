# World Model Creator (WMC) Event Model & Message Catalogs
## Message-Driven Integration Architecture

---

## 1. Overview of Event-Driven Integration

The World Model Creator (WMC) uses an event-driven architecture to keep its systems decoupled. The ten core engines do not call each other directly via synchronous remote procedure calls (RPC). Instead, they communicate using an asynchronous event bus (such as RabbitMQ or Redis Streams). This event model uses **Domain Commands** for requests that change state and **Domain Events** for publishing those state changes, ensuring high scalability and fault tolerance.

```
       +----------------------------------------------------+
       |                   WMC Coordinator                  |
       +-------------------------+--------------------------+
                                 |
                        Dispatches Command
                                 |
                                 v
       +----------------------------------------------------+
       |                   Event Bus                        |
       |  (Durable Queue / Event Store / Message Broker)    |
       +-------------------------+--------------------------+
                                 |
                         Publishes Event
                                 |
                                 v
       +----------------------------------------------------+
       |                Subscribing Engines                 |
       |     (Reality, Simulation, Economic, etc.)          |
       +----------------------------------------------------+
```

---

## 2. Domain Command Catalog

Domain Commands are direct requests sent to a specific engine to perform an action. They represent intents and can be accepted or rejected based on validation and policy constraints.

### 2.1 Reality Ingestion Commands
* `IngestRealWorldDataCommand`
  * **Recipient:** `RealityEngine`
  * **Payload:** `source_url: str`, `payload_type: str`, `raw_payload: str`, `timestamp: datetime`
  * **Description:** Requests the Reality Engine to parse, validate, and extract entities/relationships from an external data source.

### 2.2 Simulation Commands
* `CreateTimelineBranchCommand`
  * **Recipient:** `WorldSimulationEngine`
  * **Payload:** `parent_timeline_id: UUID`, `branch_name: str`, `simulation_logical_time: datetime`, `hypotheses_to_apply: List[UUID]`
  * **Description:** Requests a new, isolated timeline branch to run counterfactual experiments.
* `StepSimulationCommand`
  * **Recipient:** `WorldSimulationEngine`
  * **Payload:** `timeline_id: UUID`, `step_duration_logical_hours: float`, `environmental_adjustments: Dict[str, Any]`
  * **Description:** Moves a simulated timeline forward by a specified duration, triggering event propagation.
* `RollbackTimelineCommand`
  * **Recipient:** `WorldSimulationEngine`
  * **Payload:** `timeline_id: UUID`, `rollback_to_logical_time: datetime`
  * **Description:** Rewinds a branch to a previously saved checkpoint.

### 2.3 Cognitive Simulation Commands
* `SimulateAudienceResponseCommand`
  * **Recipient:** `HumanCognitionEngine` / `AudienceIntelligenceEngine`
  * **Payload:** `timeline_id: UUID`, `candidate_creative_id: UUID`, `target_cohort_ids: List[str]`, `exposure_context: Dict[str, Any]`
  * **Description:** Requests simulation of how target cohorts will react to a specific asset or campaign.

### 2.4 Generative Media Commands
* `CreateMediaGenerationPlanCommand`
  * **Recipient:** `GenerativeMediaEngine`
  * **Payload:** `creative_concept_id: UUID`, `target_formats: List[str]`, `visual_style_guidelines: Dict[str, Any]`, `maximum_budget_usd: float`
  * **Description:** Directs the media engine to generate a multi-modal rendering and execution plan.
* `ExecuteMediaGenerationPlanCommand`
  * **Recipient:** `GenerativeMediaEngine`
  * **Payload:** `generation_plan_id: UUID`, `target_model_routing_overrides: Dict[str, str]`
  * **Description:** Directs the media engine to coordinate with underlying foundation model APIs to render and finalize the required assets.

### 2.5 Economic Optimization Commands
* `SimulateCampaignEconomicsCommand`
  * **Recipient:** `EconomicIntelligenceEngine`
  * **Payload:** `timeline_id: UUID`, `candidate_creative_id: UUID`, `pricing_tiers: List[Dict[str, Any]]`, `distribution_cost_estimates: Dict[str, float]`
  * **Description:** Requests unit economics projection (CAC, LTV, margins) of a simulated strategy.

---

## 3. Domain Event Catalog

Domain Events represent historical facts—they indicate actions that have already completed. Events are immutable, versioned, and can be consumed by multiple subscribing engines.

### 3.1 Reality & Tracking Events
* `RealityStateUpdatedEvent`
  * **Publisher:** `RealityEngine`
  * **Subscribers:** `WMCCoordinator`, `WorldSimulationEngine`, `MetaWorldEngine`
  * **Payload:** `update_id: UUID`, `affected_entity_ids: List[UUID]`, `new_relationships_asserted: List[UUID]`, `timestamp: datetime`
  * **Description:** Published when the ground-truth model of the real world is updated with fresh observations.
* `AnomalousTrendDetectedEvent`
  * **Publisher:** `RealityEngine`
  * **Subscribers:** `WMCCoordinator`, `MetaWorldEngine`, `CoreCognitionPlanner`
  * **Payload:** `trend_id: UUID`, `description: str`, `signal_strength: float`, `affected_sectors: List[str]`
  * **Description:** Published when an ingestion pattern exceeds statistical variance thresholds, indicating a new trend or market disruption.

### 3.2 Simulation Events
* `TimelineBranchedEvent`
  * **Publisher:** `WorldSimulationEngine`
  * **Subscribers:** `WMCCoordinator`, `EconomicIntelligenceEngine`, `HumanCognitionEngine`
  * **Payload:** `new_timeline_id: UUID`, `parent_timeline_id: UUID`, `branch_name: str`, `creation_timestamp: datetime`
  * **Description:** Published when a branched simulation environment is successfully initialized.
* `SimulationStepCompletedEvent`
  * **Publisher:** `WorldSimulationEngine`
  * **Subscribers:** `WMCCoordinator`, `HumanCognitionEngine`, `EconomicIntelligenceEngine`
  * **Payload:** `timeline_id: UUID`, `current_logical_time: datetime`, `applied_deltas_count: int`
  * **Description:** Published when a timeline advances, signaling down-stream engines to evaluate consequences.
* `CausalInconsistencyDetectedEvent`
  * **Publisher:** `WorldSimulationEngine`
  * **Subscribers:** `WMCCoordinator`, `GovernanceAuditor`
  * **Payload:** `timeline_id: UUID`, `offending_node_ids: List[UUID]`, `inconsistency_score: float`, `error_details: str`
  * **Description:** Published when causal validation fails, triggering an automated rollback or adjustment.

### 3.3 Cognitive & Audience Events
* `CohortBeliefShiftedEvent`
  * **Publisher:** `AudienceIntelligenceEngine`
  * **Subscribers:** `WMCCoordinator`, `CreativeIntelligenceEngine`
  * **Payload:** `cohort_id: str`, `affected_beliefs: Dict[str, float]`, `catalyst_event_id: UUID`
  * **Description:** Published when simulation results show a shift in a target segment's beliefs or values.
* `AttentionFatigueAlert`
  * **Publisher:** `AudienceIntelligenceEngine`
  * **Subscribers:** `WMCCoordinator`, `CreativeIntelligenceEngine`, `DistributionIntelligenceEngine`
  * **Payload:** `cohort_id: str`, `theme_or_creative_id: UUID`, `fatigue_coefficient: float`
  * **Description:** Published when an audience's response to specific content drops below performance thresholds, indicating content saturation.

### 3.4 Creative & Media Events
* `CreativeCandidateEvaluatedEvent`
  * **Publisher:** `CreativeIntelligenceEngine`
  * **Subscribers:** `WMCCoordinator`, `GenerativeMediaEngine`
  * **Payload:** `candidate_id: UUID`, `estimated_engagement: float`, `estimated_conversion: float`, `risk_score: float`, `score_metadata: Dict[str, float]`
  * **Description:** Published when a creative concept has completed simulation testing and is ready for rendering optimization.
* `MediaGenerationPlannedEvent`
  * **Publisher:** `GenerativeMediaEngine`
  * **Subscribers:** `WMCCoordinator`, `EconomicIntelligenceEngine`
  * **Payload:** `plan_id: UUID`, `creative_concept_id: UUID`, `required_models: List[str]`, `estimated_tokens_or_dollars: float`
  * **Description:** Published when a multi-modal generation and model-routing path is compiled.
* `AssetRenderCompletedEvent`
  * **Publisher:** `GenerativeMediaEngine`
  * **Subscribers:** `WMCCoordinator`, `DistributionIntelligenceEngine`, `GovernanceAuditor`
  * **Payload:** `asset_id: UUID`, `plan_id: UUID`, `media_url: str`, `checksum_sha256: str`, `generation_metadata: Dict[str, Any]`
  * **Description:** Published when rendering finishes and media assets are safely stored in the platform cache.

### 3.5 Governance & System Events
* `PolicyViolationDetectedEvent`
  * **Publisher:** `GovernanceAuditor`
  * **Subscribers:** `WMCCoordinator`, `SecurityMonitor`, `HumanApprovalConsole`
  * **Payload:** `violation_id: UUID`, `violating_agent_id: str`, `policy_id: str`, `severity_level: str`, `evidence_context: Dict[str, Any]`
  * **Description:** Published when a simulation path or generation proposal violates safety, ethical, regulatory, or brand-protection policies.
