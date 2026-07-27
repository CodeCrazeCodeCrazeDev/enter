"""Operating System Kernel & Compiler Layer for EIOS.

Provides process scheduling, goal-to-DAG compilation, recursive long-horizon
planning, and hierarchical active inference.
"""

from __future__ import annotations

from .kernel import (
    EIOSKernel,
    EntrepreneurialCompiler,
    ExecutionDAG,
    ExecutionNode,
    HierarchicalActiveInference,
    RecursivePlanner,
    TimeHorizon
)

__all__ = [
    "EIOSKernel",
    "EntrepreneurialCompiler",
    "ExecutionDAG",
    "ExecutionNode",
    "HierarchicalActiveInference",
    "RecursivePlanner",
    "TimeHorizon"
]
