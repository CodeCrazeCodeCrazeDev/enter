# 04. Data Validation: Integrity and Bias Prevention

No amount of statistical sophistry or advanced neural networks can extract value from corrupt, biased, or leaked data ("garbage in, garbage out"). In quantitative finance, data errors are insidious because they usually manifest as **spectacular backtest performance** that collapses in live trading.

The **AlphaAlgo Data Validation Engine** implements non-bypassable filters to detect and eliminate biases before any feature extraction or model training begins.

---

## 1. Bias Prevention Protocols

### 1.1 Look-Ahead Bias Prevention
*Look-ahead bias* occurs when information from the future is used to make decisions in the past (e.g., using a company's closing price or an end-of-day indicator value during the market open).

* **Strict Temporal Splitting:** The data loader enforces a hard cutoff boundary. When processing timestamp $T_t$, only data with an ingestion timestamp $T_{ingest} \le T_t$ is made available to the model.
* **Point-In-Time (PIT) Database Schema:** Financial databases must support PIT structures. Corporate actions, earnings reports, and macroeconomic releases are stored with two timestamps:
  1. `as_of_date`: The period the data refers to (e.g., Q3 2026).
  2. `release_date`: The exact date and time the public gained access to the data.
  The model is strictly restricted to querying by `release_date`.

### 1.2 Survivorship Bias Prevention
*Survivorship bias* occurs when a backtest is run only on assets that are active today, ignoring those that went bankrupt, merged, or were delisted during the backtest period.

* **Dynamic Universe Matching:** The research engine does not use a static list of stock tickers (e.g., "current S&P 500 constituents"). Instead, it reconstructs the *historical universe* of active assets at each point in time.
* **Delisting Return Treatment:** When an asset is delisted, the engine applies a conservative penalty return (typically -100% for bankruptcies or an estimated acquisition price) to prevent artificial outperformance from ignoring failures.

---

## 2. Temporal & Market Calendar Validation

To prevent timeline warping, the Data Validation Engine runs automated checks:

* **Market Calendar Alignment:** All timestamps are validated against an official exchange calendar (e.g., NYSE, LSE, or CME). Any data point with an active timestamp on a day the market was closed is flagged as an anomaly.
* **Sequence Integrity:** Checks that timestamps are strictly monotonic and increasing ($T_t > T_{t-1}$).
* **Gaps and Missing Values:** Identifies unexpected gaps in high-frequency or daily streams. Missing data is handled according to strict scientific imputation rules (e.g., forward-fill for prices, never backward-fill) which must be declared in the configuration.

---

## 3. Data Lineage and Provenance

To satisfy institutional governance standards, every dataset used in research is tracked via a **Dataset Registry**.

```
+-----------------------------------------------------------+
| Dataset Registry Record                                   |
| - dataset_id: `ds_us_equities_daily_v1.0`                 |
| - raw_source: `S3://alphaalgo-data/raw/us_equities/`      |
| - ingestion_pipeline_hash: `e2c8a14b...`                  |
| - parent_dataset_id: `None`                               |
| - data_quality_report_hash: `812fbc9e...`                 |
+-----------------------------------------------------------+
```

### Traceability Chain
When a model is promoted to production, the audit trail must trace:
`Model` $\rightarrow$ `Experiment` $\rightarrow$ `Features` $\rightarrow$ `Dataset Version` $\rightarrow$ `Raw Data Source Ingestion Pipeline`.

If a data quality issue is discovered in a raw feed, the system can instantly identify and suspend all models trained on that compromised data stream.
