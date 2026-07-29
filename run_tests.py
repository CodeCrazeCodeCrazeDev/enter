"""Simple offline test runner for AgentHarness v2.

Runs all v2 tests using `.venv/bin/python3` directly to ensure zero dependency conflicts.
"""

from __future__ import annotations

import sys
from agent_harness.core.v2.test_v2 import (
    test_persistent_memory_and_learning,
    test_graph_of_thought_and_world_model,
    test_hierarchical_orchestration_and_plan_act,
    test_parallel_verification,
    test_meta_reasoner,
    test_active_learning,
)

if __name__ == "__main__":
    print("Starting next-gen AgentHarness v2 test suite run...")
    try:
        test_persistent_memory_and_learning()
        print("[PASS] test_persistent_memory_and_learning")

        test_graph_of_thought_and_world_model()
        print("[PASS] test_graph_of_thought_and_world_model")

        test_hierarchical_orchestration_and_plan_act()
        print("[PASS] test_hierarchical_orchestration_and_plan_act")

        test_parallel_verification()
        print("[PASS] test_parallel_verification")

        test_meta_reasoner()
        print("[PASS] test_meta_reasoner")

        test_active_learning()
        print("[PASS] test_active_learning")

        print("All v2 tests passed perfectly!")
        sys.exit(0)
    except Exception as e:
        print(f"[FAIL] Test run failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
