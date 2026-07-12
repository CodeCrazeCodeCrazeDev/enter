from __future__ import annotations
import logging
from typing import Any, Dict

logger = logging.getLogger("apodex.cognition.model_router")


class ModelRouter:
    """Enterprise-grade model routing engine designed to optimize API costs.

    Routes queries dynamically across three cognitive tiers (CHEAP, MEDIUM, EXPENSIVE)
    based on task type, token load, and cognitive complexity.
    """

    def __init__(self, cheap_model: str = "gpt-4o-mini", medium_model: str = "claude-3-5-haiku", expensive_model: str = "gpt-4o") -> None:
        self.cheap_model = cheap_model
        self.medium_model = medium_model
        self.expensive_model = expensive_model

    def classify_and_route(self, prompt: str, task_context: Dict[str, Any]) -> Dict[str, str]:
        """Determine the optimal model and cost tier for a given task prompt."""
        task_type = task_context.get("task_type", "general")
        complexity_score = task_context.get("complexity", 0.5)

        logger.info(f"[ModelRouter] Classifying task type '{task_type}' (Complexity: {complexity_score})")

        # 1. Classification & routing decision tree
        if task_type in ["classification", "intent_detection", "sentiment"] or complexity_score < 0.3:
            selected_model = self.cheap_model
            tier = "CHEAP"
        elif task_type in ["code_generation", "refactoring", "syntax_check", "parsing"] or (0.3 <= complexity_score < 0.7):
            selected_model = self.medium_model
            tier = "MEDIUM"
        else:
            # High complexity strategic reasoning / math verification / budget constraints
            selected_model = self.expensive_model
            tier = "EXPENSIVE"

        logger.info(f"[ModelRouter] Selected Tier: {tier} -> Model: {selected_model}")

        return {
            "model": selected_model,
            "tier": tier,
            "prompt": prompt
        }
