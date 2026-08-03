from __future__ import annotations
import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger("apodex.cognition.observers")


class LoopConfig(BaseModel):
    task_id: str
    role_id: str = "agent"
    max_turns: int = 10


class TurnContext(BaseModel):
    turn: int
    max_turns: int
    task_id: str
    role_id: str
    ai_text: str
    thinking: str = ""
    tool_calls: List[Dict[str, Any]] = Field(default_factory=list)
    messages: List[Dict[str, Any]] = Field(default_factory=list)
    usage: Optional[Dict[str, Any]] = Field(default_factory=dict)
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class InterventionResponse(BaseModel):
    pop_last_message: bool = False
    continue_to_next_turn: bool = False
    inject_messages: List[str] = Field(default_factory=list)


class MetaReasonerObserver:
    """Meta-reasoner observer tracking live loops, detecting echo traps, and monitoring goal drift."""

    def __init__(self, max_repeated_calls: int = 2, drift_threshold: float = 0.2) -> None:
        self.max_repeated_calls = max_repeated_calls
        self.drift_threshold = drift_threshold
        self.goal: Optional[str] = None
        self.tool_call_history: List[Dict[str, Any]] = []
        self.unrelated_turns = 0

    async def on_loop_start(self, config: Any) -> None:
        self.tool_call_history = []
        self.unrelated_turns = 0
        logger.info(f"MetaReasonerObserver: Initialized loop for task {getattr(config, 'task_id', 'unknown')}")

    def _extract_goal(self, messages: List[Dict[str, Any]]) -> Optional[str]:
        for msg in messages:
            if msg.get("role") == "system" and "goal" in msg.get("content", "").lower():
                return msg.get("content")
        return None

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        # Simple Jaccard similarity between words
        w1 = set(text1.lower().split())
        w2 = set(text2.lower().split())
        if not w1 or not w2:
            return 0.0
        return len(w1.intersection(w2)) / len(w1.union(w2))

    async def on_llm_response(self, context: TurnContext) -> Optional[InterventionResponse]:
        """Examines the LLM response on-the-fly and triggers corrections for repeating tool calls or goal drift."""
        # 1. Update the goal from system prompt if not yet set
        if not self.goal and context.messages:
            self.goal = self._extract_goal(context.messages)

        # 2. Check for E1 Echo Trap: duplicate identical tool calls
        if context.tool_calls:
            first_call = context.tool_calls[0]
            call_repr = {"name": first_call.get("name"), "args": first_call.get("args")}

            # Count occurrences in history
            matching_count = 1
            for past_call in self.tool_call_history:
                if past_call["name"] == call_repr["name"] and past_call["args"] == call_repr["args"]:
                    matching_count += 1

            self.tool_call_history.append(call_repr)

            if matching_count >= self.max_repeated_calls:
                logger.warning(f"Echo Trap Detected! Too many repeated calls: {call_repr}")
                # Clear history to prevent infinite triggers
                self.tool_call_history = []
                return InterventionResponse(
                    pop_last_message=True,
                    continue_to_next_turn=True,
                    inject_messages=["WARNING: Echo Trap Detected. You are repeating the same tool call with identical arguments. Choose a different parameter or approach."]
                )

        # 3. Check for E5 Goal Drift Monitor
        if self.goal and context.ai_text:
            similarity = self._calculate_similarity(context.ai_text, self.goal)
            # If similarity is lower than threshold, mark as potentially unrelated
            if similarity < self.drift_threshold:
                self.unrelated_turns += 1
            else:
                self.unrelated_turns = 0  # reset on healthy turn

            # If consecutive unrelated turns reaches 3, trigger intervention
            if self.unrelated_turns >= 3:
                logger.warning(f"Goal Drift Detected! {self.unrelated_turns} turns unrelated to: {self.goal}")
                self.unrelated_turns = 0  # reset
                return InterventionResponse(
                    pop_last_message=True,
                    continue_to_next_turn=True,
                    inject_messages=[f"WARNING: Goal Drift Detected. Your latest responses are drifting away from the core goal: '{self.goal}'. Recalibrate your next action."]
                )

        return None
