# 02. System Architecture: The AlphaAlgo Research Pipeline

This document describes the high-level system architecture of the **AlphaAlgo Research Operating System (Research OS)**.

The core architecture is designed as a **deterministic, non-agent-centric research pipeline**. AI agents and human researchers interact with the system via stable interfaces, but the sequence of execution, statistical gates, and state persistence are managed by strict, deterministic system boundaries.

---

## 1. High-Level System Architecture Topology

The Research OS is built around a series of state-retaining **Registries** and a central **Research Pipeline Orchestrator**.

```
                           +------------------------------------------+
                           |        Research Question Registry        |
                           +--------------------+---------------------+
                                                |
                                                v
                           +--------------------+---------------------+
                           |            Hypothesis Registry           |
                           +--------------------+---------------------+
                                                |
                                                v
                           +--------------------+---------------------+
                           |           Data Validation Engine         |
                           +--------------------+---------------------+
                                                |
                                                v
                           +--------------------+---------------------+
                           |               Feature Registry           |
                           +--------------------+---------------------+
                                                |
                                                v
                           +--------------------+---------------------+
                           |            Experiment Sandbox Engine     |
                           +---+-------------+-------------+-------+--+
                               |             |             |       |
                               v             v             v       v
                           [Experiment Registry] <--- [Artifacts / Weights]
                                                |
                                                v
                           +--------------------+---------------------+
                           |         Statistical Validation Layer     |
                           +--------------------+---------------------+
                                                | (Deflated Sharpe, Multi-Test Correction)
                                                v
                           +--------------------+---------------------+
                           |         Robustness & Bootstrap Layer     |
                           +--------------------+---------------------+
                                                | (Block Bootstrap, Monte Carlo)
                                                v
                           +--------------------+---------------------+
                           |           Scientific Review Gate         |
                           +--------------------+---------------------+
                                                | (Human / AI Consensus Audit)
                                                v
                           +--------------------+---------------------+
                           |         Non-bypassable Promotion Gate    |
                           +--------------------+---------------------+
                                                | (Cryptographic Verification)
                                                v
                           +--------------------+---------------------+
                           |               Model Registry             |
                           +--------------------+---------------------+
                                                |
                                                v
                           +--------------------+---------------------+
                           |          Production & Live Monitor       |
                           +--------------------+---------------------+
                                                |
                                                + - - - (Feedback Loop) - - - -> [Hypothesis Engine]
```

---

## 2. Component Overviews

### 2.1 Research Question Registry
* **Purpose:** The entry point for scientific inquiry. Defines high-level research objectives (e.g., "Is there cross-sectional momentum in cryptocurrency markets under high-volatility regimes?").
* **Properties:** Deduplicated, structured, and prioritized based on potential information gain and corporate objectives.

### 2.2 Hypothesis Registry
* **Purpose:** Every potential alpha model or signal *must* be registered as a formal hypothesis ($H_1$) against a null hypothesis ($H_0$) *before* any backtesting occurs.
* **Properties:** Immutable, versioned. Prevents post-hoc hypothesis formulation (fitting the hypothesis to the backtest).

### 2.3 Data Validation Engine
* **Purpose:** Verifies that raw datasets comply with scientific standards.
* **Properties:** Performs non-leakage analysis, walk-forward calendar alignment, look-ahead checks, and survivorship bias validation before data is handed to feature pipelines.

### 2.4 Feature Registry
* **Purpose:** A centralized, versioned repository of validated mathematical features.
* **Properties:** Every feature is assigned a unique SHA-256 configuration hash, lineage/provenance tracking, and statistical health metrics (e.g., missing values, stationarity).

### 2.5 Experiment Sandbox Engine
* **Purpose:** Runs strategy backtests and simulations in completely isolated, reproducible, and resource-bounded sandboxes.
* **Properties:** Seed-locking, library isolation, strict time bounds, outputting standardized performance time-series to the **Experiment Registry**.

### 2.6 Statistical Validation Layer
* **Purpose:** Filters out random anomalies and overfitted backtests.
* **Properties:** Implements multiple hypothesis testing corrections (Bonferroni, Holm, Benjamini-Hochberg) and computes the **Deflated Sharpe Ratio (DSR)** to account for the number of trials executed.

### 2.7 Robustness & Bootstrap Layer
* **Purpose:** Evaluates the stability of the model across alternative histories and market regimes.
* **Properties:** Block bootstrapping, Monte Carlo perturbations, walk-forward parameter stability audits.

### 2.8 Scientific Review & Promotion Gate
* **Purpose:** Dual-factor validation (human expert and LLM-as-a-judge system audit) verifying code correctness, adherence to risk policies, and theoretical backing before a model goes live.
* **Properties:** Audits are signed, hash-logged, and immutable. No model can bypass this gate.

### 2.9 Model Registry
* **Purpose:** The final catalog of ready-to-deploy, production-ready trading models.
* **Properties:** Immutable, versioned, traceably linked to the original hypothesis, training data, and statistical reports.

---

## 3. Communication and Data Exchange Schema

Subsystems communicate via clean, strongly-typed domain schemas. All registrations, experiments, and validations generate standard JSON-LD or structured model schemas stored in a lightweight SQLite/PostgreSQL relational database.

For example, when an experiment completes, it generates an `ExperimentRecord` which references:
1. `hypothesis_id`: Link to the pre-registered hypothesis.
2. `dataset_id`: Link to the exact immutable dataset version used.
3. `feature_ids`: List of specific features used.
4. `config_hash`: SHA-256 hash of the model code and hyperparameters.
5. `reproducibility_package`: Exact package versions, environment lock-file, and seed values.

This strict schemas and registries framework eliminates file-system drift, undocumented modifications, and "voodoo" research practices.
