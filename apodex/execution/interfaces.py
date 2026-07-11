from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class IExecutionController(ABC):
    """Interface for orchestrating multi-agent tasks, workflows, and low-level tools."""

    @abstractmethod
    async def dispatch_workflow(self, workflow_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatch a predefined or dynamically constructed sequence of agent actions."""
        pass

    @abstractmethod
    async def execute_task(self, agent_id: str, task_description: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Direct a single specialized agent to perform an isolated task."""
        pass
