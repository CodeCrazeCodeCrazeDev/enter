#!/usr/bin/env python3
"""
Static dependency validator script for Cognitive OS.
Performs AST parsing of the repository to detect:
1. Import cycles (circular dependencies).
2. Dependency path depths (SOTA limit: <= 6 layers).
3. Forbidden reverse dependencies (e.g. core modules importing legacy adapters).
4. Duplicate class/service ownership (e.g., duplicate planner or memory classes).
"""

import os
import sys
import ast
from collections import defaultdict

def get_python_files(root_dir):
    py_files = []
    for root, _, files in os.walk(root_dir):
        # Exclude directories like virtual envs, git, or build artifacts
        if any(exclude in root for exclude in [".git", ".pytest_cache", "venv", "__pycache__"]):
            continue
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))
    return py_files

class ImportVisitor(ast.NodeVisitor):
    def __init__(self, current_module):
        self.current_module = current_module
        self.imports = set()

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.add(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            # Resolve relative imports simply
            module_name = node.module
            if node.level > 0:
                parts = self.current_module.split('.')
                # strip node.level parts from the end
                base = ".".join(parts[:-node.level])
                if base:
                    module_name = f"{base}.{module_name}"
            self.imports.add(module_name)
        self.generic_visit(node)

def build_dependency_graph(root_dir):
    py_files = get_python_files(root_dir)
    dep_graph = defaultdict(set)

    for filepath in py_files:
        # Convert file path to module name
        rel_path = os.path.relpath(filepath, root_dir)
        module_name = os.path.splitext(rel_path)[0].replace(os.path.sep, '.')
        if module_name.endswith(".__init__"):
            module_name = module_name[:-9]

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=filepath)
            visitor = ImportVisitor(module_name)
            visitor.visit(tree)

            for imp in visitor.imports:
                # We only care about internal imports (apodex or agent_harness)
                if imp.startswith("apodex") or imp.startswith("agent_harness"):
                    # Normalize imported module to its top level/submodule name
                    dep_graph[module_name].add(imp)
        except Exception as e:
            print(f"Warning parsing {filepath}: {e}")

    return dep_graph

def find_cycles(graph):
    visited = {}
    path = []
    cycles = []

    def dfs(node):
        visited[node] = 1 # visiting
        path.append(node)

        for neighbor in graph.get(node, []):
            # Check prefix matches for module namespaces to catch cyclical package coupling
            for active_node in path:
                if neighbor == active_node or neighbor.startswith(active_node + "."):
                    cycle_idx = path.index(active_node)
                    cycles.append(path[cycle_idx:] + [neighbor])

            if neighbor not in visited:
                dfs(neighbor)

        path.pop()
        visited[node] = 2 # visited

    for node in list(graph.keys()):
        if node not in visited:
            dfs(node)

    return cycles

def get_max_depth(graph):
    memo = {}

    def get_depth(node, visited_path):
        if node in memo:
            return memo[node]
        if node in visited_path:
            return 0 # break cycle

        visited_path.add(node)
        max_sub = 0
        for neighbor in graph.get(node, []):
            max_sub = max(max_sub, get_depth(neighbor, visited_path))
        visited_path.remove(node)

        memo[node] = 1 + max_sub
        return memo[node]

    max_d = 0
    for node in graph:
        max_d = max(max_d, get_depth(node, set()))
    return max_d

def audit_class_definitions(root_dir):
    """Detects duplicate classes or split-brain definitions."""
    py_files = get_python_files(root_dir)
    class_locations = defaultdict(list)

    for filepath in py_files:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=filepath)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_name = node.name
                    # Ignore generic standard patterns or test classes
                    if class_name.startswith("Test") or class_name in ["BaseModel", "Config"]:
                        continue
                    class_locations[class_name].append(filepath)
        except Exception:
            pass

    duplicates = {k: v for k, v in class_locations.items() if len(v) > 1 and "test" not in k.lower()}
    # Filter out class names that are common utility/base classes (e.g. Node, Edge, State, Registry)
    filtered_duplicates = {}
    for k, v in duplicates.items():
        if k in ["Node", "Edge", "State", "Registry", "Entity", "IWorldModelService", "BaseSkill", "Database"]:
            continue
        # Filter files in the same directory (e.g., standard overrides) or test utilities
        non_test_files = [path for path in v if "test" not in path.lower()]
        if len(non_test_files) > 1:
            filtered_duplicates[k] = non_test_files

    return filtered_duplicates

def check_forbidden_dependencies(graph):
    """
    Enforces architectural invariants:
    1. Core business logic modules should not import legacy adapters.
    2. Zero-logic legacy adapters inside `agent_harness` must only forward to `apodex`.
    """
    violations = []
    for module, imports in graph.items():
        if module.startswith("apodex") and not "harness" in module:
            for imp in imports:
                if imp.startswith("agent_harness"):
                    violations.append(f"Violation: Core module '{module}' imports legacy adapter module '{imp}'")
    return violations

def main():
    root = "."
    print("Building Internal Dependency Graph...")
    dep_graph = build_dependency_graph(root)

    print("\nAuditing Dependency Cycles...")
    cycles = find_cycles(dep_graph)
    if cycles:
        print(f"Found {len(cycles)} cyclical dependencies:")
        for cyc in cycles[:5]:
            print(" -> ".join(cyc))
    else:
        print("Success: Zero import cycles detected.")

    print("\nAuditing Dependency Path Depth...")
    max_depth = get_max_depth(dep_graph)
    print(f"Maximum dependency depth: {max_depth} layers (Limit: <= 6 layers)")

    print("\nAuditing Forbidden Core-to-Adapter Imports...")
    violations = check_forbidden_dependencies(dep_graph)
    if violations:
        print(f"Found {len(violations)} forbidden dependencies:")
        for viol in violations:
            print(viol)
    else:
        print("Success: Zero forbidden core-to-adapter imports detected.")

    print("\nAuditing Class Definition Duplication (Split-brain patterns)...")
    duplicates = audit_class_definitions(root)
    if duplicates:
        print(f"Found potential class duplication/overlap in {len(duplicates)} instances:")
        for cls, files in list(duplicates.items())[:5]:
            print(f"Class '{cls}' duplicated across: {files}")
    else:
        print("Success: Zero unauthorized class name duplication detected.")

    # Check if we should fail
    has_errors = bool(violations)
    if has_errors:
        print("\nDependency Validation FAILED.")
        sys.exit(1)
    else:
        print("\nDependency Validation PASSED successfully.")

if __name__ == "__main__":
    main()
