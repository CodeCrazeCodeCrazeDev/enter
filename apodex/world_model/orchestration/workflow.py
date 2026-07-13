from __future__ import annotations
from typing import List
from pydantic import BaseModel, Field


class WorkflowNode(BaseModel):
    """A single execution node inside an orchestration workflow."""
    node_id: str
    engine_name: str
    action_name: str
    parameters: dict = Field(default_factory=dict)
    dependencies: List[str] = Field(default_factory=list)


class WmcOrchestrationWorkflow(BaseModel):
    """DAG specification of sequential or parallel engine actions."""
    workflow_id: str
    nodes: List[WorkflowNode] = Field(default_factory=list)
