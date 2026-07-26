from __future__ import annotations
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class BottleneckFailure(BaseModel):
    failure_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    task_name: str
    error_signature: str
    context_traces: List[str] = Field(default_factory=list)


class InstitutionalPolicyRule(BaseModel):
    rule_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    target_pattern: str
    remedy_instruction: str
    is_active: bool = True


class ResearchSelfImprovementEngine:
    """
    Compiles system bottleneck failures into procedural InstitutionalPolicy rules.
    Emulates natural language backpropagation (TextGrad) over agent prompts.
    """

    def __init__(self) -> None:
        self.active_policies: List[InstitutionalPolicyRule] = []

    def compile_failure_to_policy(self, failure: BottleneckFailure) -> InstitutionalPolicyRule:
        """
        Synthesizes a corrective policy rule based on the observed error signature.
        """
        target = failure.task_name
        remedy = f"CRITICAL: Avoid pattern '{failure.error_signature}' during task execution."

        # Simple heuristic mapping for typical bottlenecks
        if "timeout" in failure.error_signature.lower():
            remedy = "CRITICAL: Enforce batch-size reduction and enable parallel execution nodes."
        elif "compile" in failure.error_signature.lower() or "syntax" in failure.error_signature.lower():
            remedy = "CRITICAL: Always run python validation checks inside isolated sandboxes prior to deployment."

        rule = InstitutionalPolicyRule(
            target_pattern=target,
            remedy_instruction=remedy
        )
        self.active_policies.append(rule)
        return rule

    def optimize_system_prompts(self, base_prompt: str, task_name: str) -> str:
        """
        Applies compiled policies to optimize system instruction prompts dynamically.
        """
        optimized = base_prompt
        for rule in self.active_policies:
            if rule.is_active and rule.target_pattern == task_name:
                optimized += f"\n[Self-Improvement Policy]: {rule.remedy_instruction}"
        return optimized
