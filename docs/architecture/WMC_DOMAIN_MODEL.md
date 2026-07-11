# World Model Creator (WMC) Domain Model Specification
## Storage-Independent Entity-Relation-Belief (ERB) Framework

---

## 1. Domain-Driven Design and Separation of Concerns

The core of the World Model Creator (WMC) is a rich, storage-independent domain model. This design separates business, simulation, and cognitive logic from data persistence technologies. Following the principles of **Hexagonal Architecture (Ports & Adapters)**, the domain model does not import or inherit from any database drivers, ORM frameworks, or graph library classes.

```
       +-----------------------------------------------------+
       |                  Domain Layer                       |
       |  (Entities, Relationships, Beliefs, Timelines)     |
       +--------------------------+--------------------------+
                                  |
                                  v
       +-----------------------------------------------------+
       |             Repository Interfaces (Ports)           |
       +--------------------------+--------------------------+
                                  |
         +------------------------+------------------------+
         |                                                 |
         v                                                 v
+--------+----------------+                       +--------+----------------+
| SQL Adapter (Postgres)  |                       |  Graph Adapter (Neo4j)  |
| (Persistence Schema)    |                       |  (Cypher Queries)       |
+-------------------------+                       +-------------------------+
```

---

## 2. Core Entities & Graph Structures

The simulation universe is represented as a directed, attributed multi-graph known as the **World Graph**. Unlike static knowledge graphs, the WMC World Graph layers **Bayesian beliefs** and **hypotheses** directly onto graph structures to handle uncertainty and timeline branching.

### 2.1 Entity (Node)
An `Entity` is any distinct object, group, location, or concept within a simulated or real world.
* **Attributes:**
  * `entity_id`: Globally unique identifier (`UUID4`).
  * `name`: Human-readable name.
  * `entity_type`: Category classification (e.g., `PERSON`, `ORGANIZATION`, `METRIC`, `GEOGRAPHY`, `TECHNOLOGY`).
  * `properties`: Strongly typed JSON metadata specific to the type.
  * `created_at`: Timeline-specific creation timestamp.
  * `updated_at`: Last modification timeline-specific timestamp.

### 2.2 Relationship (Edge)
A `Relationship` represents a directed association, connection, or causal link between two Entities.
* **Attributes:**
  * `relationship_id`: Globally unique identifier (`UUID4`).
  * `source_id`: Source `Entity` identifier.
  * `target_id`: Target `Entity` identifier.
  * `relation_type`: Type of relation (e.g., `COMPETES_WITH`, `INFLUENCES`, `REGULATES`, `SUPPLIES`, `AFFECTS`).
  * `weight`: Float value $[0.0, 1.0]$ representing connection strength.
  * `properties`: Metadata describing the relation attributes (e.g., latency, capacity).

### 2.3 Belief (Epistemic Wrapper)
A `Belief` represents the epistemic state (confidence and uncertainty) of the system regarding the existence, strength, or relevance of a `Relationship` or `Entity`.
* **Attributes:**
  * `belief_id`: Globally unique identifier.
  * `target_id`: Identifier of the target `Entity` or `Relationship` being evaluated.
  * `probability`: Bayesian confidence score $P(B \mid E) \in [0.0, 1.0]$.
  * `evidence`: Cryptographic hashes or citations of supporting data points (e.g., news sources, telemetry data).
  * `last_validated`: Verification timestamp.

### 2.4 Hypothesis (Speculative Node)
A `Hypothesis` is a specialized, unproven belief node used to evaluate "what-if" conditions. It acts as an anchor for counterfactual reasoning.
* **Attributes:**
  * `hypothesis_id`: Globally unique identifier.
  * `description`: Textual formulation of the hypothesis.
  * `parent_belief_id`: Reference to the core belief being tested.
  * `test_conditions`: Conditions under which the hypothesis becomes a validated belief.
  * `active_simulations`: List of simulated timeline identifiers where this hypothesis is assumed true.

---

## 3. Timeline Model & Branching Architecture

To support scenario evaluation, the WMC does not modify the World Graph in place. Instead, it utilizes an immutable, branching timeline model similar to a Git version control tree.

```
                  [Timeline: Real World State (Main)]
                                  │
                       ┌──────────┴──────────┐
                       v (Branch: T_A)       v (Branch: T_B)
                 [SaaS Price +10%]     [Competitor Enters]
                       │                     │
                       v                     v
                 (Evaluation)          (Evaluation)
```

### 3.1 Timeline Branch (Branch Node)
* **Attributes:**
  * `timeline_id`: Unique identifier.
  * `parent_timeline_id`: Reference to the parent timeline (or `None` for the main reality timeline).
  * `name`: Short descriptor (e.g., `sim_fy2027_pessimistic`).
  * `created_at`: Physical system timestamp of branch creation.
  * `branch_point_sim_time`: The simulation logical time at which the branch occurred.
  * `deltas`: List of structural additions, deletions, or updates (`WorldGraphDelta`) applied to the parent graph in this timeline.
  * `is_committed`: Boolean state. Once committed, a branch becomes immutable.

### 3.2 Timeline Delta
To save storage space, child timelines only store the differences (deltas) from their parent. This delta model includes:
* **AddEntityDelta:** Adds an entity node to the current timeline view.
* **RemoveEntityDelta:** Logically removes an entity node.
* **ModifyEntityPropertiesDelta:** Modifies specific attributes of a node.
* **AddRelationshipDelta:** Adds a relation edge.
* **RemoveRelationshipDelta:** Logically removes a relation edge.
* **UpdateBeliefDelta:** Updates the probability or evidence list of a belief.

---

## 4. Environment & Context State Models

The environment defines the boundary conditions and external parameters under which a simulation is executed. It acts as the "context frame" of the World Graph.

### 4.1 Environment Vector
A high-dimensional vector representing global, slow-moving external variables that cannot be easily modeled as individual graph entities:
* **Meteorological State:** Weather anomalies, sea-level indices.
* **Macroeconomic Indicators:** Inflation index, global interest rates, liquidity metrics.
* **Regulatory Frame:** Active regional policy indices, tax brackets.
* **Geopolitical Risk Index:** Regional stability factors, trade barrier coefficients.

---

## 5. Human Cognition & Audience Segment Domains

To simulate human responses, the WMC includes a formalized domain representation of psychology and demographics.

### 5.1 Cognitive Profile
Represents the psychological configuration of an individual simulated actor:
* **Attention Matrix:** Current attention allocation across various topics $[0.0, 1.0]$.
* **Belief Vector:** Personal belief alignment coordinates mapping to core societal or political narratives.
* **Emotional State:** Vector of fundamental emotions (Anger, Fear, Joy, Sadness, Trust, Anticipation, Surprise, Disgust) scaled between $0.0$ and $1.0$.
* **Cognitive Biases:** Dictionary of active biases and their activation thresholds (e.g., `confirmation_bias: 0.8`).
* **Value System:** Priority order of core human values (Security, Self-Direction, Benevolence, Achievement).

### 5.2 Audience Segment Cohort
An aggregate representation of a group of cognitive profiles sharing demographic or psychographic characteristics:
* **Demographics:** Age group, income range, geography, primary language.
* **Psychographics:** Interests, dominant consumption channels, active cultural adaptations.
* **Content Fatigue curves:** Decay constants specifying how fast the audience tires of specific messaging vectors.
* **Trust Matrices:** Trust coefficients toward specific platforms, brands, or message sources.

---

## 6. Economic & Business Context Domains

The WMC coordinates with ARCS by modeling the physical business environment inside the simulation:
* **SaaS Unit Economics:** Customer Acquisition Cost (CAC), Lifetime Value (LTV), Monthly Recurring Revenue (MRR), Churn Rate.
* **Supply Chain Node:** Production capacity, latency constants, inventory volume, unit manufacturing costs.
* **Price Elasticity Curve:** Simulated conversion rates across proposed pricing steps.
* **Opportunity Cost Vector:** Computational value of paths not taken, scaled against resource utilization.
