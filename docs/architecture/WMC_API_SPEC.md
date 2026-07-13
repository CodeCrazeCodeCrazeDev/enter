# World Model Creator (WMC) API & Service Specifications
## Integration Protocols, Interface Contracts, and gRPC Definitions

---

## 1. Overview of Integration Interfaces

The World Model Creator (WMC) exposes high-performance, strongly typed interfaces to the rest of the Apodex Cognitive OS. While internal service communication is primarily asynchronous and event-driven (using domain events), direct queries, simulation setup, and resource requests from the Core Cognition Planner use **gRPC over HTTP/2** to minimize latency and ensure strict type validation.

```
       +-----------------------------------------------------+
       |               Apodex Core Cognition                 |
       +--------------------------+--------------------------+
                                  |
                           gRPC / mTLS Calls
                                  |
                                  v
       +-----------------------------------------------------+
       |                WMC API Gateway                      |
       |  (Port 50051 - gRPC / Protobuf v3 Protocol)         |
       +--------------------------+--------------------------+
                                  |
                        Internal Routing
                                  |
                                  v
       +-----------------------------------------------------+
       |             WMC Coordinator Core                    |
       |    (Registry, Factory, Engine Delegation)           |
       +-----------------------------------------------------+
```

---

## 2. Protocol Buffers & gRPC Interface Contracts

Below are the Protobuf v3 definitions for the core WMC services.

```protobuf
syntax = "proto3";

package apodex.world_model.v1;

import "google/protobuf/struct.proto";
import "google/protobuf/timestamp.proto";

// Main World Model Creator service contract
service WorldModelCreatorService {
    // Queries the active World Graph state
    rpc QueryWorldGraph(QueryWorldGraphRequest) returns (QueryWorldGraphResponse);

    // Creates an isolated timeline branch for simulation
    rpc CreateTimelineBranch(CreateTimelineBranchRequest) returns (CreateTimelineBranchResponse);

    // Drives a simulated timeline forward by logical steps
    rpc StepSimulation(StepSimulationRequest) returns (StepSimulationResponse);

    // Computes behavioral reactions for a set of target cohorts
    rpc SimulateAudienceResponse(SimulateAudienceResponseRequest) returns (SimulateAudienceResponseResponse);

    // Generates optimal media plans and routes to downstream model APIs
    rpc OrchestrateMediaGeneration(OrchestrateMediaGenerationRequest) returns (OrchestrateMediaGenerationResponse);
}

// Request to query node/edge/belief structures
message QueryWorldGraphRequest {
    string timeline_id = 1;
    string query_string = 2; // Graph-query representation (e.g., Cypher-like syntax)
    google.protobuf.Struct filter_properties = 3;
}

message QueryWorldGraphResponse {
    string timeline_id = 1;
    repeated EntityNode nodes = 2;
    repeated RelationshipEdge edges = 3;
    repeated BeliefNode beliefs = 4;
}

message EntityNode {
    string entity_id = 1;
    string name = 2;
    string entity_type = 3;
    google.protobuf.Struct properties = 4;
    google.protobuf.Timestamp created_at = 5;
}

message RelationshipEdge {
    string relationship_id = 1;
    string source_id = 2;
    string target_id = 3;
    string relation_type = 4;
    float weight = 5;
    google.protobuf.Struct properties = 6;
}

message BeliefNode {
    string belief_id = 1;
    string target_id = 2;
    float probability = 3;
    repeated string evidence = 4;
    google.protobuf.Timestamp last_validated = 5;
}

// Timeline branching requests
message CreateTimelineBranchRequest {
    string parent_timeline_id = 1;
    string branch_name = 2;
    google.protobuf.Timestamp simulation_time = 3;
    repeated string hypothesis_ids_to_apply = 4;
}

message CreateTimelineBranchResponse {
    string timeline_id = 1;
    string parent_timeline_id = 2;
    google.protobuf.Timestamp created_at = 3;
}

// Simulation step execution
message StepSimulationRequest {
    string timeline_id = 1;
    double duration_hours = 2;
    google.protobuf.Struct external_forces = 3;
}

message StepSimulationResponse {
    string timeline_id = 1;
    google.protobuf.Timestamp current_simulation_time = 2;
    int32 modified_elements_count = 3;
    bool has_causal_anomalies = 4;
}

// Audience response simulation requests
message SimulateAudienceResponseRequest {
    string timeline_id = 1;
    string creative_concept_id = 2;
    repeated string cohort_ids = 3;
}

message SimulateAudienceResponseResponse {
    string timeline_id = 1;
    repeated CohortReaction reactions = 2;
}

message CohortReaction {
    string cohort_id = 1;
    float attention_score = 2;
    float sentiment_score = 3;
    float purchase_intent_shift = 4;
    google.protobuf.Struct emotional_profile_deltas = 5;
}

// Media generation request
message OrchestrateMediaGenerationRequest {
    string creative_concept_id = 1;
    repeated string target_formats = 2;
    float maximum_budget_usd = 3;
}

message OrchestrateMediaGenerationResponse {
    string plan_id = 1;
    repeated GeneratedAsset assets = 2;
    float final_computed_cost_usd = 3;
}

message GeneratedAsset {
    string asset_id = 1;
    string format = 2;
    string uri = 3;
    string checksum_sha256 = 4;
}
```

---

## 3. Dependency Injection & Service Registry Design

To maintain strict modular decoupling, WMC uses a standard Dependency Injection (DI) framework. Classes never instantiate their dependent engines directly. Instead, they reference interfaces, which are resolved at runtime by a central container.

### 3.1 Container Registry Interfaces (Python Contract)

```python
from abc import ABC, abstractmethod
from typing import Type, TypeVar, Dict

T = TypeVar('T')

class IDependencyContainer(ABC):
    """Core contract for the WMC Dependency Injection container."""

    @abstractmethod
    def register_singleton(self, interface: Type[T], implementation_instance: T) -> None:
        """Register a globally persistent singleton service instance."""
        pass

    @abstractmethod
    def register_transient(self, interface: Type[T], implementation_factory) -> None:
        """Register a transient service factory resolved freshly on each request."""
        pass

    @abstractmethod
    def resolve(self, interface: Type[T]) -> T:
        """Resolve and return an instance satisfying the requested interface contract."""
        pass
```

### 3.2 Service Registration Setup
When the WMC service boots up, the service bootstrap script initializes the DI container and binds mock, staging, or production adapters based on the environmental configuration:

```python
# Bootstrapping snippet
container = DependencyContainer()

# Bind persistent storage repository ports
container.register_singleton(IWorldGraphRepository, PostgresNeo4jHybridRepository())

# Bind the 10 Engines to their production implementations
container.register_singleton(IRealityEngine, ProductionRealityEngine())
container.register_singleton(IWorldSimulationEngine, ProductionWorldSimulationEngine())
# ... (all other engines registered)
```
This ensures that mock implementations can be injected in unit test suites, while high-performance storage and GPU-backed clusters are injected in production, without requiring any modifications to the core engine code.
