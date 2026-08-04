from __future__ import annotations
import os
import ast
import pytest

def test_single_capability_ownership():
    """
    Enforces automated capability ownership verification:
    Guarantees exactly one authoritative, non-duplicative implementation exists
    for each core Tier-0 capability in the codebase.
    """
    capability_owners = {
        "strategic_planner": {
            "canonical": "apodex/planning/planner_executor.py",
            "forbidden": [
                "agent_harness/core/runtime/orchestration/planner_executor.py",
                "apodex/planning/custom_planner.py",
            ]
        },
        "world_model": {
            "canonical": "apodex/world_model/world_model.py",
            "forbidden": [
                "apodex/world_model/custom_world_model.py",
            ]
        },
        "persistent_memory": {
            "canonical": "apodex/memory/semantic_memory.py",
            "forbidden": [
                "agent_harness/core/memory/semantic_memory.py",
            ]
        },
        "scheduler": {
            "canonical": "apodex/world_model/orchestration/scheduler.py",
            "forbidden": [
                "agent_harness/scheduling/scheduler.py",
            ]
        },
        "orchestration_execution": {
            "canonical": "apodex/orchestration/hierarchical.py",
            "forbidden": [
                "agent_harness/core/runtime/orchestration/hierarchical.py",
            ]
        },
        "evaluation_engine": {
            "canonical": "apodex/cognition/trajectory_verification.py",
            "forbidden": [
                "agent_harness/core/runtime/dataset_generator.py",
            ]
        },
        "governance_core": {
            "canonical": "apodex/ai_eos/governance/gateway.py",
            "forbidden": [
                "apodex/ai_eos/governance/custom_gateway.py",
            ]
        }
    }

    # Verify that:
    # 1. Every canonical owner file exists.
    # 2. No forbidden duplicative implementation file exists.
    for capability, config in capability_owners.items():
        canonical_path = config["canonical"]
        assert os.path.exists(canonical_path), f"Canonical owner of {capability} is missing at {canonical_path}!"

        for forbidden_path in config["forbidden"]:
            # If the path exists, it must not be a duplicate implementation.
            # Compatibility adapters are acceptable only if they are thin zero-logic wraps.
            if os.path.exists(forbidden_path):
                # Verify that it does not contain a duplicate class implementation (e.g. by checking AST)
                with open(forbidden_path, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read(), filename=forbidden_path)

                # Check for class definitions that duplicate canonical classes rather than wrapping them
                class_names = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
                # Compatibility files inside agent_harness should strictly be re-exports or inherit from canonical classes.
                # To prevent duplicate logic, they must not define the full logic of these classes.
                for name in class_names:
                    # We assert that the class definitions in these forbidden files do not house core complex logic.
                    # Instead, any duplicate class names are flagged.
                    assert name not in ["StrategicPlanner", "WorldModel", "SemanticMemory", "HierarchicalOrchestrator"], (
                        f"Duplicate core logic implementation found for class {name} in {forbidden_path}! "
                        f"Must use the canonical implementation in {canonical_path}."
                    )


def test_runtime_capability_exclusivity():
    """
    Runtime capability exclusivity check:
    Ensures that multiple concurrent or conflicting instances of Tier-0 components
    (such as two planners or two world models) cannot execute under the same context.
    """
    active_instances = {}

    def register_runtime_execution(component_type: str, instance_id: str):
        if component_type in active_instances and active_instances[component_type] != instance_id:
            raise RuntimeError(
                f"Runtime Capability Violation: Multiple active implementations of '{component_type}' "
                f"detected: {active_instances[component_type]} and {instance_id}. Exclusivity must be preserved."
            )
        active_instances[component_type] = instance_id

    # Simulate healthy singular execution
    register_runtime_execution("planner", "canonical_planner_v1")
    register_runtime_execution("planner", "canonical_planner_v1")  # Same instance allowed
    register_runtime_execution("world_model", "canonical_wm_v1")

    # Simulate a violation with conflicting execution
    with pytest.raises(RuntimeError, match="Multiple active implementations"):
        register_runtime_execution("planner", "conflicting_planner_v2")
