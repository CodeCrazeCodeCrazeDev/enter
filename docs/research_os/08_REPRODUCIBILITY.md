# 08. Reproducibility: Elimination of Backtest Drift

Reproducibility is the foundational cornerstone of the scientific method. If an experiment cannot be reliably reproduced, its findings are statistically invalid. In quantitative finance, subtle changes in library versions, hardware configurations, or raw database contents often lead to "backtest drift," where a model's simulated performance changes over time.

The **AlphaAlgo Reproducibility Framework** guarantees absolute determinism across all experiments.

---

## 1. Environment Tracking & Locking

To eliminate "works on my machine" syndromes and silent dependency updates:

* **Strict Dependency Locking:** Every run is executed under a precise package lock file (e.g., `uv.lock` or `requirements.txt` with SHA-256 hashes).
* **Runtime Fingerprinting:** The system records and registers:
  * Operating System and kernel version.
  * Python interpreter minor and micro version (e.g., `3.12.13`).
  * System architecture (e.g., `x86_64` vs `arm64`).
  * Global environmental variables.

If any variance is detected at execution time, the runner flags an alert and records the variance in the experiment's reproducibility package metadata.

---

## 2. Configuration & Source Code Alignment

To ensure that the exact code used to generate a signal is preserved:

* **Git Commit Anchoring:** The Research OS will not execute an experiment on a dirty Git directory. All code must be committed, and the active `git_commit_hash` is recorded in the experiment metadata.
* **Declarative Parameter Hashing:** All parameters are serialized to a standardized, sorted JSON configuration. This JSON is hashed to generate the unique `config_hash`.

---

## 3. Data Replay Determinism

If the underlying historical database is updated or modified, past backtests will drift. To prevent this:

* **Dataset Versioning:** Datasets are treated as immutable snapshots. A dataset with ID `ds_market_data_v1.0` is permanently frozen. Any updates (e.g., correcting an corporate action retroactively) are published as a new version: `ds_market_data_v1.1`.
* **Seed Lockout:** All pseudo-random number generators are initialized with a seed recorded in the configuration. The engine overrides any random calls within the model to enforce this seed.

---

## 4. Reproducibility Audit Tool

The Research OS includes a CLI/API tool, `repro_replay`, which takes an `experiment_id` and:
1. Re-installs the locked package dependencies.
2. Checks out the specific Git commit hash.
3. Restores the exact immutable dataset snapshot.
4. Re-runs the model in the sandbox.
5. Verifies that the resulting metrics and trade time-series match the original registration exactly.

Any variance greater than a tiny floating-point tolerance ($10^{-12}$) triggers an automatic containment event and suspends the model from promotion.
