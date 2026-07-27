"""Execution Surface Adapters for ARCS / AEAN OS.

Defines the interchangeable Mock, Sandbox, and Production adapter pattern
for 10 external interfaces.
"""

from __future__ import annotations

from .adapters import AdapterMode, ExecutionSurfaceRegistry, BaseAdapter

__all__ = ["AdapterMode", "ExecutionSurfaceRegistry", "BaseAdapter"]
