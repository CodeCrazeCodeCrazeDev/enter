# World Model Creator (WMC) Core Architecture Specification
## Systems Design, Core Engines, and Multi-Horizon Roadmap

---

## 1. Introduction and Platform Positioning

The **World Model Creator (WMC)** is the simulation engine of the Apodex Cognitive Operating System. Rather than being confined to creative media generation, the WMC is built as a general-purpose world modeling platform. Its core mandate is to construct, maintain, and reason over coherent models of real or hypothetical worlds.

The WMC acts as a utility to the platform. Downstream applications (such as ARCS for revenue operations, ADE for demand engineering, and ACE for capital management) query the WMC to run counterfactual scenarios, estimate risk margins, forecast geopolitical trends, simulate market elasticities, and plan multi-modal asset generations.

### 1.1 Separation of Concerns
To prevent architectural erosion, the WMC is strictly prohibited from executing non-world-modeling operations. Specifically:
- **No General Planning:** High-level executive plans are made by the Core Cognition layer. WMC only evaluates specific scenarios or timelines proposed by the planner.
- **No Long-Term Task Memory:** General episodic memory belongs to the platform’s Memory Service. WMC only manages the structural graph representation of worlds (the World Graph) and its historical states.
- **No Direct Business Execution:** WMC does not trigger external transactions, buy ads, or execute marketing campaigns. It simulates the impact of these activities, whereas execution is managed by application engines like ARCS.

---

## 2. Global Architecture and Component Topography

The WMC is structured around a decoupled, microservices-driven architecture. The core of the system is the **World Graph**—a storage-independent, entity-relation-belief network. All operations are mediated through a high-performance, asynchronous event bus.

```
       +-------------------------------------------------------------+
       |                  Apodex Core Cognition                      |
       +------------------------------+------------------------------+
                                      | gRPC API / Queries
                                      v
+--------------------------------------------------------------------+
|                      WMC Coordinator Core                          |
|  +--------------------------------------------------------------+  |
|  |                    World Graph (Memory Layer)                |  |
|  +------------------------------+-------------------------------+  |
|                                 |                                  |
|                                 v Asynchronous Event Bus           |
|  +------------------------------+-------------------------------+  |
|  |     1. Reality Engine        |    2. World Simulation Engine |  |
|  +------------------------------+-------------------------------+  |
|  |     3. Human Cognition Engine|    4. Audience Intel Engine   |  |
|  +------------------------------+-------------------------------+  |
|  |     5. Creative Intel Engine |    6. Generative Media Engine |  |
|  +------------------------------+-------------------------------+  |
|  |     7. Distribution Intel Eng|    8. Economic Intel Engine   |  |
|  +------------------------------+-------------------------------+  |
|  |     9. Evolution Engine      |   10. Meta-World Engine       |  |
|  +--------------------------------------------------------------+  |
+---------------------------------+----------------------------------+
                                  |
                                  v
                    +-------------+-------------+
                    |   Human Governance Layer  |
                    | (Policies, Audits, Workf.)|
                    +---------------------------+
```

---

## 3. The Ten Core Engines

Every engine within the WMC is designed as a modular service communicating via the event bus. Below is the specification for each engine:

### 3.1 Reality Engine
* **Purpose:** Continuously ingests multi-modal data streams to update the foundational ground-truth state of the real world.
* **Inputs:** Real-time news feeds, economic indicators, financial tickers, regulatory updates, meteorological forecasts, and technology patent filings.
* **Outputs:** Ground-truth entity updates, newly asserted real-world relationships, and updated confidence thresholds.
* **Internal State:** Current ground-truth World Graph partition (E-K-C-T-U subgraphs).
* **Interfaces:** `IRealityEngine`
* **Events Published:** `RealityStateUpdatedEvent`, `AnomalousTrendDetectedEvent`.
* **Dependencies:** Data pipeline adapters, external scrapers, real-time vector indexes.
* **Failure Modes:** Data pollution, hallucinated correlations, ingestion pipeline saturation.
* **Evaluation Metrics:** Ingestion latency (ms), precision/recall of asserted facts, information source credibility scores.
* **Extension Points:** Custom domain-specific data connectors.

### 3.2 World Simulation Engine
* **Purpose:** Executes counterfactual projections, models timeline branching, handles state rollback, and enforces causal consistency.
* **Inputs:** Branch requests, historical timeline state checkpoints, hypothesis updates.
* **Outputs:** Branched timelines, future state predictions, step-by-step causal paths.
* **Internal State:** Multi-timeline version graph, rollback checkpoints, simulation parameters.
* **Interfaces:** `IWorldSimulationEngine`
* **Events Published:** `TimelineBranchedEvent`, `SimulationStepCompletedEvent`, `CausalInconsistencyDetectedEvent`.
* **Dependencies:** Graph database backend, casual inference solver.
* **Failure Modes:** State combinatorial explosion, timeline drift, causal loop paradoxes.
* **Evaluation Metrics:** Simulation step speed (ops/sec), timeline consistency index, predictive accuracy vs. actual historical outcomes.
* **Extension Points:** Alternate physics, economic, or geological simulation models.

### 3.3 Human Cognition Engine
* **Purpose:** Simulates the internal mental states, belief networks, cognitive biases, and psychological profiles of simulated human actors.
* **Inputs:** Human profile definitions, external stimuli, narrative scenarios.
* **Outputs:** Behavioral predictions, emotional shifts, sentiment indexes, trust evaluations.
* **Internal State:** Cognitive profiles, attention spans, emotional/motivational vector states.
* **Interfaces:** `IHumanCognitionEngine`
* **Events Published:** `CognitiveStateUpdatedEvent`, `CognitiveBiasTriggeredEvent`.
* **Dependencies:** Cognitive profile datasets, psychological model adapters.
* **Failure Modes:** Monolithic profiling, drift in simulated human logic, stereotype amplification.
* **Evaluation Metrics:** Profile fidelity score, behavioral prediction accuracy (F1), simulation diversity.
* **Extension Points:** Behavioral economics rulesets, custom cognitive bias modules.

### 3.4 Audience Intelligence Engine
* **Purpose:** Manages and updates dynamic models of aggregate demographic, psychographic, and organizational target cohorts.
* **Inputs:** Market feedback, attention logs, content consumption statistics, social trend indicators.
* **Outputs:** Evolving cohort belief vectors, trust dynamics, content fatigue curves, and segmentation definitions.
* **Internal State:** Audience cohort graph, attention decay trackers, regional language shifts.
* **Interfaces:** `IAudienceIntelligenceEngine`
* **Events Published:** `CohortBeliefShiftedEvent`, `AttentionFatigueAlert`.
* **Dependencies:** Analytics connectors, audience segmentation registers.
* **Failure Modes:** Cohort drift, over-segmentation, target tracking sample bias.
* **Evaluation Metrics:** Segments' temporal alignment score, cohort size estimation error, trend prediction horizon.
* **Extension Points:** Platform-specific attention trackers, regional cultural matrices.

### 3.5 Creative Intelligence Engine
* **Purpose:** Evaluates hundreds of candidate creations (narratives, assets, campaigns) against simulated worlds and audience models.
* **Inputs:** Asset specs, target cohorts, campaign parameters.
* **Outputs:** Pre-generation optimization indexes (estimated engagement, retention, originality, controversy).
* **Internal State:** Narrative pattern library, optimization criteria history.
* **Interfaces:** `ICreativeIntelligenceEngine`
* **Events Published:** `CreativeCandidateEvaluatedEvent`, `OptimizationIteratedEvent`.
* **Dependencies:** Audience Engine, World Simulation Engine, pattern databases.
* **Failure Modes:** Algorithmic creative homogenization, objective optimization bias.
* **Evaluation Metrics:** Expected vs. actual conversion rates, creativity originality score, optimization search convergence speed.
* **Extension Points:** Custom scoring heuristics, aesthetic evaluator plugins.

### 3.6 Generative Media Engine
* **Purpose:** Model-agnostic orchestration layer that coordinates multi-modal generations (image, video, sound, 3D assets).
* **Inputs:** Verified generative blueprints, rendering pipelines, style guides.
* **Outputs:** High-fidelity media generation plans, model-routing instructions, finalized asset packages.
* **Internal State:** Model-routing tables, rendering configurations, queue status.
* **Interfaces:** `IGenerativeMediaEngine`
* **Events Published:** `MediaGenerationPlannedEvent`, `GenerationJobRoutedEvent`, `AssetRenderCompletedEvent`.
* **Dependencies:** Model providers, rendering farm connections, vector asset caches.
* **Failure Modes:** Model provider outages, generation artifacts, aspect ratio/cross-modal sync failures.
* **Evaluation Metrics:** Generative task completion speed, rendering costs ($/job), cross-modal coherence score.
* **Extension Points:** New foundation model API adapters, asset-specific formatting post-processors.

### 3.7 Distribution Intelligence Engine
* **Purpose:** Determines optimal posting strategies, channel localizations, scheduling, and A/B configurations.
* **Inputs:** Simulation results, media metadata, platform-specific trend algorithms.
* **Outputs:** Multi-channel distribution blueprints, localization guidelines, testing matrices.
* **Internal State:** Channel engagement histories, platform algorithm updates.
* **Interfaces:** `IDistributionIntelligenceEngine`
* **Events Published:** `DistributionBlueprintCreatedEvent`, `ChannelStrategyOptimizedEvent`.
* **Dependencies:** Analytics dashboards, marketing campaign registers.
* **Failure Modes:** Algorithm changes, distribution channel blocks, timing mismatches.
* **Evaluation Metrics:** Platform CTR (click-through-rate) improvements, posting window efficiency, localization consistency.
* **Extension Points:** Platform API integration layers.

### 3.8 Economic Intelligence Engine
* **Purpose:** Computes the financial dimensions (margins, CAC, supply chain resilience, opportunity cost) of simulated worlds and strategies.
* **Inputs:** Business scenarios, price-point candidates, currency fluctuations, cloud infrastructure overhead.
* **Outputs:** Economic projections, capital allocation suggestions, unit economics reports.
* **Internal State:** Currency translation rates, infrastructure cost matrices, standard accounting tables.
* **Interfaces:** `IEconomicIntelligenceEngine`
* **Events Published:** `EconomicImpactSimulatedEvent`, `OpportunityCostAlert`.
* **Dependencies:** Financial database, cost-tracker adapters.
* **Failure Modes:** Formula discrepancies, volatile pricing drift, incorrect tax calculations.
* **Evaluation Metrics:** Forecasted vs. actual ROI discrepancy, calculation speeds, scenario evaluation throughput.
* **Extension Points:** Custom tax compliance plugins, enterprise resource planning (ERP) bridges.

### 3.9 Evolution Engine
* **Purpose:** Automates prompt, heuristic, and hyperparameter optimization over continuous simulation trajectories. For complete details on how self-improvement is organized as an internal engineering firm, see the **[Self-Improvement Flywheel Spec](WMC_SELF_IMPROVEMENT_FLYWHEEL.md)**.
* **Inputs:** Trajectory logs, system feedback metrics, prediction errors.
* **Outputs:** Updated system prompts, revised heuristic weights, updated model route configurations.
* **Internal State:** System weights history, optimization trajectories, evaluation metadata.
* **Interfaces:** `IEvolutionEngine`
* **Events Published:** `HeuristicsOptimizedEvent`, `ContinualLearningBatchProcessedEvent`.
* **Dependencies:** Database of prompt histories, weights registries.
* **Failure Modes:** Catastrophic forgetting, over-fitting, feedback loops.
* **Evaluation Metrics:** Performance improvement percentage, adaptation rate, prompt-version regression rate.
* **Extension Points:** Reinforcement learning from system feedback (RLSF) algorithms, evolutionary search models.

### 3.10 Meta-World Engine
* **Purpose:** Tracks and projects global culture, geopolitics, fashion, and macroeconomic dynamics as a universal background.
* **Inputs:** Geopolitical shifts, global news summaries, macroeconomic trends.
* **Outputs:** Civilization-scale context vectors, global cultural waves, macro trend forecasts.
* **Internal State:** Meta-world graph, global relationship map, trend trackers.
* **Interfaces:** `IMetaWorldEngine`
* **Events Published:** `MetaTrendDetectedEvent`, `GeopoliticalShiftForecastedEvent`.
* **Dependencies:** Reality Engine, macro-economic modelers.
* **Failure Modes:** Macro-model oversimplification, nationalistic or data biases.
* **Evaluation Metrics:** Trend tracking accuracy, cultural propagation speed estimation, global event association score.
* **Extension Points:** Geopolitical risk simulators, sociological trend monitors.

---

## 4. Multi-Horizon Strategy

The WMC is built with a 3-horizon plan that allows immediate implementation using today's technologies while structuring clear transition points for long-term evolution:

### 4.1 Horizon 1: Production-Ready (0–3 Years)
* **Core Technology:** Knowledge Graphs (graph-vector databases like PostgreSQL with pgvector, combined with Neo4j), discrete-event simulation engines (SimPy), standard causal Bayesian networks, and state-of-the-art LLMs (e.g., Claude 3.5, GPT-4o) using prompt-driven agent frameworks.
* **Orchestration:** Linear or DAG-based microservices, XML/JSON parsing, standard message brokers (Redis, RabbitMQ).
* **Limitations:** Higher latency, bounded context-window bottlenecks, deterministic simulation constraints.

### 4.2 Horizon 2: Advanced Cognitive Systems (3–7 Years)
* **Core Technology:** Hybrid neuro-symbolic models combining neural embeddings with symbolic graph engines. Active Inference loops replacing static planning pipelines. Continuous multi-agent simulators with agent-based reinforcement learning.
* **Orchestration:** Dynamic decentralized agents utilizing Graph-of-Thought search, semantic memory consolidation, and specialized model routing.
* **Limitations:** High compute costs, ongoing challenges in aligning continuous simulation with discrete logical constraints.

### 4.3 Horizon 3: Long-Term Frontiers (7–20 Years)
* **Core Technology:** Differentiable simulation engines (allowing gradient-based optimization over entire worlds), civilizational-scale generative simulation frameworks, and unified multi-modal world models running on specialized hardware.
* **Orchestration:** Completely autonomous agent ecosystems with self-play and self-improvement loops that require zero human intervention.
* **Limitations:** Physical hardware constraints, complex governance boundaries.
