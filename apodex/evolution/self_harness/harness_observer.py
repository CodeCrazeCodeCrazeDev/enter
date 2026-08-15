"""
HarnessObserver conforming to the LoopObserver protocol.
"""
from __future__ import annotations
import time
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

from agent_harness.core.loop_types import LoopConfig, TurnContext, ToolResult, AgentLoopResult
from apodex.evolution.self_harness.trajectory_areal import AgentTrajectory, AReaLDataProxy


class HarnessObserver:
    def __init__(self, data_proxy: AReaLDataProxy, tenant_id: str) -> None:
        self.data_proxy = data_proxy
        self.tenant_id = tenant_id
        self.current_trajectory: Optional[AgentTrajectory] = None

    async def on_loop_start(self, config: LoopConfig) -> None:
        self.current_trajectory = AgentTrajectory(task_id=config.task_id)

    async def on_tool_result(self, ctx: TurnContext, result: ToolResult) -> None:
        if self.current_trajectory:
            self.current_trajectory.add_step({
                "step_id": result.tool_call_id or f"step_{len(self.current_trajectory.steps) + 1}",
                "node_type": "tool_execution",
                "tool_name": result.name,
                "status": "failed" if result.is_error else "success",
                "is_error": result.is_error,
                "tool_result_preview": result.result,
                "duration_ms": result.duration_ms,
                "timestamp": time.time()
            })

    async def on_turn_end(self, ctx: TurnContext) -> None:
        if self.current_trajectory:
            is_err = "error" in ctx.ai_text.lower() or "overflow" in ctx.ai_text.lower()
            self.current_trajectory.add_step({
                "step_id": f"step_end_{len(self.current_trajectory.steps) + 1}",
                "node_type": "prompt_error" if is_err else "turn_end",
                "tool_name": "",
                "status": "failed" if is_err else "success",
                "is_error": is_err,
                "tool_result_preview": ctx.ai_text,
                "duration_ms": 0,
                "timestamp": time.time()
            })

    async def on_loop_end(self, result: AgentLoopResult) -> None:
        if self.current_trajectory:
            self.data_proxy.buffer_trajectory(self.tenant_id, self.current_trajectory)
