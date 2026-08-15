import time
import resource
import os
from apodex.cognition.controller import CognitiveBenchmarkSuite

def get_memory_mb():
    # resource.getrusage returns maxrss in kilobytes on Linux
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0

def measure_cognitive_baselines():
    mem_before = get_memory_mb()
    t0 = time.perf_counter()

    # 1. Expected Free Energy Capital Allocation (Active Inference)
    p_prior = [0.4, 0.4, 0.2]
    q_posterior = [0.1, 0.8, 0.1]
    kl_div = CognitiveBenchmarkSuite.run_expected_free_energy_evaluation(p_prior, q_posterior)

    # 2. Causal Do-Calculus Counterfactual Intervention
    causal_cost = CognitiveBenchmarkSuite.run_causal_counterfactual_intervention(10000.0, 15000.0, 0.65)

    # 3. Ebbinghaus Memory Decay Retention
    retention = CognitiveBenchmarkSuite.run_ebbinghaus_decay_retention(100.0, 10.0, 10.0)

    # 4. Swarm Debate Sycophancy Mitigation
    votes = ["AFFIRMATIVE", "AFFIRMATIVE", "AFFIRMATIVE", "AFFIRMATIVE", "NEGATIVE"]
    consensus = CognitiveBenchmarkSuite.run_multi_mind_sycophancy_mitigation(votes, 0.20)

    t1 = time.perf_counter()
    mem_after = get_memory_mb()

    latency_ms = (t1 - t0) * 1000.0
    mem_delta_mb = mem_after - mem_before

    print("=== COGNITIVE_OS_FROZEN_BASELINE_METRICS ===")
    print(f"KL-Divergence Calibrator (Active Inference): {kl_div:.4f}")
    print(f"Causal Counterfactual Cost Projection: {causal_cost:.2f}")
    print(f"Ebbinghaus Retention Rate (10-day half-life): {retention:.2f}%")
    print(f"Sycophancy-Mitigated Consensus: {consensus:.2f}")
    print(f"Loop Execution Latency: {latency_ms:.4f} ms")
    print(f"RSS Memory Delta: {mem_delta_mb:.4f} MB")
    print("===========================================")

if __name__ == "__main__":
    measure_cognitive_baselines()
