from __future__ import annotations
import math
from typing import Any, Dict, List
from pydantic import BaseModel, Field

class CognitiveMetrics(BaseModel):
    plan_success: float = 1.0          # range [0.0, 1.0]
    research_quality: float = 1.0      # range [0.0, 1.0]
    reasoning_accuracy: float = 1.0    # range [0.0, 1.0]
    prediction_accuracy: float = 1.0   # range [0.0, 1.0]
    execution_completion: float = 1.0 # range [0.0, 1.0]
    knowledge_growth: float = 1.0      # range [0.0, 1.0]
    memory_accuracy: float = 1.0       # range [0.0, 1.0]
    latency_ms: float = 100.0          # penalty
    compute_tokens: int = 500          # penalty
    architecture_complexity: int = 1   # penalty

class CognitiveBenchmarkSuite:
    """
    Standardized suite of continuous capability evaluation benchmarks.
    Computes expected long-term utility score J(θ) for the Cognitive Kernel.
    """

    def __init__(self) -> None:
        self.weights = {
            "w_plan": 15.0,
            "w_research": 15.0,
            "w_reasoning": 10.0,
            "w_prediction": 10.0,
            "w_execution": 20.0,
            "w_knowledge": 10.0,
            "w_memory": 10.0,
            "p_latency": 0.005,
            "p_tokens": 0.001,
            "p_complexity": 5.0
        }

    def compute_objective_utility(self, metrics: CognitiveMetrics) -> float:
        """
        Calculates J(θ) = sum(w * dimension) - sum(p * penalty).
        Ensures cognitive optimization is empirically measurable.
        """
        positive_utility = (
            self.weights["w_plan"] * metrics.plan_success +
            self.weights["w_research"] * metrics.research_quality +
            self.weights["w_reasoning"] * metrics.reasoning_accuracy +
            self.weights["w_prediction"] * metrics.prediction_accuracy +
            self.weights["w_execution"] * metrics.execution_completion +
            self.weights["w_knowledge"] * metrics.knowledge_growth +
            self.weights["w_memory"] * metrics.memory_accuracy
        )
        negative_utility = (
            self.weights["p_latency"] * metrics.latency_ms +
            self.weights["p_tokens"] * metrics.compute_tokens +
            self.weights["p_complexity"] * metrics.architecture_complexity
        )
        return positive_utility - negative_utility
