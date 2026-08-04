from __future__ import annotations
import ast
import os
import pytest
from typing import Dict, Set, List, Any, Optional

# 1. Layer Definitions of the target Cognitive Operating System
LAYERS = {
    "infrastructure": {
        "index": 0,
        "paths": ["apodex/common", "apodex/storage", "apodex/safety", "apodex/cognition/shared"],
        "allowed_imports": ["apodex/common", "apodex/storage", "apodex/safety", "apodex/cognition/shared"]
    },
    "memory_and_world_model": {
        "index": 1,
        "paths": ["apodex/memory", "apodex/world_model"],
        "allowed_imports": ["apodex/common", "apodex/storage", "apodex/safety", "apodex/cognition/shared", "apodex/memory", "apodex/world_model"]
    },
    "planning_and_reasoning": {
        "index": 2,
        "paths": ["apodex/planning", "apodex/reasoning", "apodex/skills"],
        "allowed_imports": ["apodex/common", "apodex/storage", "apodex/safety", "apodex/cognition/shared", "apodex/memory", "apodex/world_model", "apodex/planning", "apodex/reasoning", "apodex/skills"]
    },
    "orchestration": {
        "index": 3,
        "paths": ["apodex/orchestration", "apodex/cognition", "apodex/execution"],
        "allowed_imports": ["apodex/common", "apodex/storage", "apodex/safety", "apodex/cognition/shared", "apodex/memory", "apodex/world_model", "apodex/planning", "apodex/reasoning", "apodex/skills", "apodex/orchestration", "apodex/cognition", "apodex/execution"]
    },
    "research_and_application": {
        "index": 4,
        "paths": ["apodex/research_os", "apodex/ai_eos", "apodex/aean"],
        "allowed_imports": ["apodex/common", "apodex/storage", "apodex/safety", "apodex/cognition/shared", "apodex/memory", "apodex/world_model", "apodex/planning", "apodex/reasoning", "apodex/skills", "apodex/orchestration", "apodex/cognition", "apodex/execution", "apodex/research_os", "apodex/ai_eos", "apodex/aean"]
    },
    "evolution_and_governance": {
        "index": 5,
        "paths": ["apodex/evolution", "apodex/governance", "apodex/world_model/orchestration"],
        "allowed_imports": ["*"]  # Evolution/Governance layer can import anything.
    }
}


# 2. Authoritative Single-Ownership Capability Map (Tier-0 Capability -> Single Owning Module)
SINGLE_OWNERSHIP_CAPABILITY_MAP = {
    "PLANNER": "apodex/planning",
    "WORLD_MODEL": "apodex/world_model",
    "MEMORY": "apodex/memory",
    "SKILL_REGISTRY": "apodex/skills",
    "REASONING": "apodex/reasoning",
    "ORCHESTRATION": "apodex/orchestration",
    "RESEARCH": "apodex/research_os",
    "GOVERNANCE": "apodex/governance",
    "EVOLUTION": "apodex/evolution",
}


def get_layer_for_path(filepath: str) -> Optional[Dict[str, Any]]:
    # Gather all paths with their layer info
    all_paths = []
    for layer_name, layer_info in LAYERS.items():
        for path in layer_info["paths"]:
            all_paths.append((path, layer_info))
    # Sort by length of path descending so longer prefixes match first
    all_paths.sort(key=lambda x: len(x[0]), reverse=True)
    for path, layer_info in all_paths:
        if filepath.startswith(path):
            return layer_info
    return None


def parse_imports(filepath: str) -> Set[str]:
    """Parse all imports inside a Python file using AST."""
    imports = set()
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=filepath)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module)
    except Exception:
        pass
    return imports


def test_strict_module_decoupling_and_layering():
    """Verify that lower cognitive layers NEVER import from higher cognitive layers."""
    violating_imports = []

    for root, _, files in os.walk("apodex"):
        for file in files:
            if not file.endswith(".py"):
                continue
            filepath = os.path.join(root, file).replace("\\", "/")
            source_layer = get_layer_for_path(filepath)
            if not source_layer:
                continue

            # Parse imports in this file
            file_imports = parse_imports(filepath)
            for imp in file_imports:
                if not imp.startswith("apodex."):
                    continue
                # Map target import back to target layer
                target_path = imp.replace(".", "/")
                target_layer = get_layer_for_path(target_path)
                if not target_layer:
                    continue

                # Rule check: Sourced layer cannot import from a layer with higher index
                if source_layer["allowed_imports"] != ["*"]:
                    is_allowed = False
                    for allowed_prefix in source_layer["allowed_imports"]:
                        allowed_path_prefix = allowed_prefix.replace(".", "/")
                        if target_path.startswith(allowed_path_prefix):
                            is_allowed = True
                            break
                    if not is_allowed:
                        violating_imports.append((filepath, imp, source_layer["index"], target_layer["index"]))

    assert not violating_imports, (
        "Strict layering violations found! Lower-layer modules are importing from higher-layer modules:\n"
        + "\n".join([f"File: {filepath} imports {imp} (Layer {src_idx} -> Layer {tgt_idx})" for filepath, imp, src_idx, tgt_idx in violating_imports])
    )


def test_acyclic_dependency_and_maximum_depth():
    """Verify there are no cyclic dependencies and that maximum dependency depth does not exceed 6 layers."""
    # Build package-level dependency graph
    dependency_graph: Dict[str, Set[str]] = {}

    for layer in LAYERS.values():
        for path in layer["paths"]:
            dependency_graph[path] = set()

    all_keys = list(dependency_graph.keys())
    all_keys.sort(key=lambda x: len(x), reverse=True)

    for root, _, files in os.walk("apodex"):
        for file in files:
            if not file.endswith(".py"):
                continue
            filepath = os.path.join(root, file).replace("\\", "/")
            src_pkg = None
            for pkg in all_keys:
                if filepath.startswith(pkg):
                    src_pkg = pkg
                    break
            if not src_pkg:
                continue

            file_imports = parse_imports(filepath)
            for imp in file_imports:
                if not imp.startswith("apodex."):
                    continue
                target_path = imp.replace(".", "/")
                tgt_pkg = None
                for pkg in all_keys:
                    if target_path.startswith(pkg):
                        tgt_pkg = pkg
                        break
                if tgt_pkg and tgt_pkg != src_pkg:
                    dependency_graph[src_pkg].add(tgt_pkg)

    # Detect cycles via DFS
    visited = {}
    def dfs_cycle(node: str, path_stack: List[str]) -> bool:
        visited[node] = "visiting"
        path_stack.append(node)
        for neighbor in dependency_graph.get(node, []):
            if visited.get(neighbor) == "visiting":
                return True
            if neighbor not in visited:
                if dfs_cycle(neighbor, path_stack):
                    return True
            elif neighbor in path_stack:
                return True
        visited[node] = "visited"
        path_stack.pop()
        return False

    cycles_found = []
    for node in dependency_graph.keys():
        if node not in visited:
            stack = []
            if dfs_cycle(node, stack):
                cycles_found.append(stack)

    assert not cycles_found, f"Cyclic dependencies detected in core subsystems: {cycles_found}"

    # Calculate maximum depth
    memo_depth = {}
    def get_max_depth(node: str) -> int:
        if node in memo_depth:
            return memo_depth[node]
        neighbors = dependency_graph.get(node, [])
        if not neighbors:
            return 1
        depth = 1 + max(get_max_depth(nb) for nb in neighbors)
        memo_depth[node] = depth
        return depth

    max_depth = max(get_max_depth(node) for node in dependency_graph.keys())
    assert max_depth <= 6, f"Maximum dependency depth exceeds allowed limit (6): found depth of {max_depth}"


def test_single_ownership_tier0_capabilities():
    """Verify that every Tier-0 capability is strictly owned by exactly one authoritative module."""
    # Ensure there are no duplicated planner files outside planning directory
    for root, _, files in os.walk("apodex"):
        for file in files:
            if not file.endswith(".py"):
                continue
            filepath = os.path.join(root, file).replace("\\", "/")

            # Check for planner duplication
            if "planner" in file.lower() and not filepath.startswith("apodex/planning"):
                # Exclude database-level query planners like CMOS query planner
                if filepath.startswith("apodex/memory/cmos"):
                    continue
                # Permit thin re-exports / legacy adapters if explicitly flagged, but block raw logic duplications
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                # If file defines classes without re-exporting, it is duplication
                if "class " in content and "from apodex.planning" not in content and "from apodex.cognition.planning" not in content:
                    pytest.fail(f"Duplicated Planner capability detected at '{filepath}'. Use thin re-export adapters instead.")

            # Check for memory duplication
            if "memory" in file.lower() and not filepath.startswith("apodex/memory"):
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                if "class " in content and "from apodex.memory" not in content and "from apodex.cognition.memory" not in content:
                    pytest.fail(f"Duplicated Memory capability detected at '{filepath}'. Use thin re-export adapters instead.")

            # Check for world model duplication
            if "world_model" in file.lower() and not filepath.startswith("apodex/world_model"):
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                if "class " in content and "from apodex.world_model" not in content:
                    pytest.fail(f"Duplicated World Model capability detected at '{filepath}'. Use thin re-export adapters instead.")
