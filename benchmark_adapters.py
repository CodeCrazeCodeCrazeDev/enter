"""
Micro-benchmarking script to measure latency and overhead of the compatibility adapter layers.
"""

from __future__ import annotations

import time
import sys


def benchmark_imports() -> dict:
    results = {}

    # 1. Benchmark cost_tier
    t0 = time.perf_counter_ns()
    from apodex.skills.models import CostTier as CanonicalCostTier
    t_canonical_cost = time.perf_counter_ns() - t0

    t0 = time.perf_counter_ns()
    from agent_harness.core.cost_tier import CostTier as AdapterCostTier
    t_adapter_cost = time.perf_counter_ns() - t0
    results["cost_tier"] = {"canonical_ns": t_canonical_cost, "adapter_ns": t_adapter_cost}

    # 2. Benchmark emg_engine
    t0 = time.perf_counter_ns()
    from apodex.memory.emg_engine import EMGEngine as CanonicalEMGEngine
    t_canonical_emg = time.perf_counter_ns() - t0

    t0 = time.perf_counter_ns()
    from agent_harness.core.memory.emg_engine import EMGEngine as AdapterEMGEngine
    t_adapter_emg = time.perf_counter_ns() - t0
    results["emg_engine"] = {"canonical_ns": t_canonical_emg, "adapter_ns": t_adapter_emg}

    # 3. Benchmark parallel verification
    t0 = time.perf_counter_ns()
    from apodex.governance.parallel_verification import MetaVerifier as CanonicalMetaVerifier
    t_canonical_meta = time.perf_counter_ns() - t0

    t0 = time.perf_counter_ns()
    from agent_harness.core.runtime.verification.parallel import MetaVerifier as AdapterMetaVerifier
    t_adapter_meta = time.perf_counter_ns() - t0
    results["parallel_verification"] = {"canonical_ns": t_canonical_meta, "adapter_ns": t_adapter_meta}

    return results


def benchmark_instantiation() -> dict:
    results = {}

    # Measure EMGEngine build_graph_from_trajectory overhead via adapter
    steps = [
        {"step_id": "s1", "node_type": "tool_execution", "tool_name": "web_search", "status": "success", "timestamp": 100},
    ]

    from apodex.memory.emg_engine import EMGEngine as CanonicalEMGEngine
    from agent_harness.core.memory.emg_engine import EMGEngine as AdapterEMGEngine

    # Warm-up
    CanonicalEMGEngine.build_graph_from_trajectory("t1", steps)
    AdapterEMGEngine.build_graph_from_trajectory("t2", steps)

    # 1. Canonical run
    t0 = time.perf_counter()
    for i in range(1000):
        CanonicalEMGEngine.build_graph_from_trajectory(f"t_can_{i}", steps)
    t_canonical = time.perf_counter() - t0

    # 2. Adapter run
    t0 = time.perf_counter()
    for i in range(1000):
        AdapterEMGEngine.build_graph_from_trajectory(f"t_ad_{i}", steps)
    t_adapter = time.perf_counter() - t0

    results["emg_execution_1k_runs"] = {"canonical_sec": t_canonical, "adapter_sec": t_adapter}
    return results


if __name__ == "__main__":
    print("=== COGNITIVE OS ADAPTER OVERHEAD BENCHMARK ===")

    import_results = benchmark_imports()
    print("\n1. Import Latency (Nanoseconds):")
    for k, v in import_results.items():
        overhead = v["adapter_ns"] - v["canonical_ns"]
        ratio = v["adapter_ns"] / v["canonical_ns"] if v["canonical_ns"] > 0 else 1.0
        print(f"  - {k}:")
        print(f"    Canonical: {v['canonical_ns']:,} ns")
        print(f"    Adapter:   {v['adapter_ns']:,} ns")
        print(f"    Overhead:  {overhead:+,} ns ({ratio:.2f}x)")

    exec_results = benchmark_instantiation()
    print("\n2. Execution Benchmark (1,000 Iterations):")
    for k, v in exec_results.items():
        overhead = v["adapter_sec"] - v["canonical_sec"]
        ratio = v["adapter_sec"] / v["canonical_sec"] if v["canonical_sec"] > 0 else 1.0
        print(f"  - {k}:")
        print(f"    Canonical: {v['canonical_sec']:.6f} sec")
        print(f"    Adapter:   {v['adapter_sec']:.6f} sec")
        print(f"    Overhead:  {overhead:+.6f} sec ({ratio:.2f}x)")
