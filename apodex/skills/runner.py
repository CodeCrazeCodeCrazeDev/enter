from __future__ import annotations
import math
import uuid
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Callable

from pydantic import BaseModel, Field
from apodex.skills.models import (
    BusinessSkill,
    BusinessProtocol,
    ProtocolStep,
    SkillExecutionLog,
    SkillScorecard,
    ProtocolScorecard,
    KnowledgeType,
    CostTier,
)
from apodex.common.graph import DirectedGraph
from apodex.arcs.world_graph import WorldGraph, EntityNode, RelationshipEdge, BeliefNode

logger = logging.getLogger("apodex.skills.runner")


def decay_confidence(
    base_confidence: float,
    observed_time: datetime,
    current_time: Optional[datetime] = None,
    half_life_days: float = 7.0
) -> float:
    """
    Applies exponential decay to a base confidence score of a DECAYING signal.
    Formula: C(t) = C_0 * 0.5 ** (delta_t / half_life)
    """
    if current_time is None:
        current_time = datetime.utcnow()

    # Ensure timezone naive for comparison
    observed = observed_time.replace(tzinfo=None)
    now = current_time.replace(tzinfo=None)

    delta_seconds = max(0.0, (now - observed).total_seconds())
    delta_days = delta_seconds / 86400.0

    decay_factor = 0.5 ** (delta_days / half_life_days)
    return max(0.0, base_confidence * decay_factor)


class SkillRunner:
    """Executes business skills and updates the global WorldGraph and scorecards."""

    def __init__(self, world_graph: Optional[WorldGraph] = None) -> None:
        self.world_graph = world_graph if world_graph is not None else WorldGraph()
        self.custom_executors: Dict[str, Callable[[Dict[str, Any], CostTier, SkillRunner], Dict[str, Any]]] = {}
        self.execution_logs: List[SkillExecutionLog] = []
        self.skill_scorecards: Dict[str, SkillScorecard] = {}

    def register_custom_executor(
        self,
        skill_name: str,
        executor: Callable[[Dict[str, Any], CostTier, SkillRunner], Dict[str, Any]]
    ) -> None:
        """Register a specialized custom python function for a skill."""
        self.custom_executors[skill_name] = executor

    def get_scorecard(self, skill_name: str) -> SkillScorecard:
        """Retrieve or initialize a scorecard for a specific skill."""
        if skill_name not in self.skill_scorecards:
            self.skill_scorecards[skill_name] = SkillScorecard(skill_name=skill_name)
        return self.skill_scorecards[skill_name]

    def execute_skill(
        self,
        skill: BusinessSkill,
        tenant_id: str,
        venture_id: str,
        input_payload: Dict[str, Any],
        tier: CostTier,
        protocol_name: Optional[str] = None,
        step_index: Optional[int] = None
    ) -> Dict[str, Any]:
        """Runs a business skill, invoking custom or generic simulated paths."""
        logger.info(f"Executing skill '{skill.name}' under {tier} tier (Tenant: {tenant_id}, Venture: {venture_id}).")

        # Verify inputs against schema (simulated validation)
        for key in skill.input_schema:
            if key not in input_payload:
                logger.warning(f"Input payload missing parameter '{key}' for skill '{skill.name}'.")

        cost_est = skill.base_cost_credits
        if tier == CostTier.CHEAP:
            cost_est = max(1, cost_est // 5)  # CHEAP is 5x cheaper than standard

        start_time = datetime.utcnow()
        output_payload: Dict[str, Any] = {}
        status = "SUCCESS"
        anchors_hit: List[str] = []
        metrics_lift: Dict[str, float] = {}

        try:
            if skill.name in self.custom_executors:
                # Run custom specialized handler
                output_payload = self.custom_executors[skill.name](input_payload, tier, self)
            else:
                # Fallback to metadata-driven generic simulation run
                output_payload = self._generic_simulation_run(skill, input_payload, tier)

            anchors_hit = output_payload.get("anchors_hit", [f"anchor_{skill.name}_success"])
            metrics_lift = output_payload.get("metrics_lift", {"conversion_uplift": 0.01})
        except Exception as e:
            logger.exception(f"Failure during execution of skill '{skill.name}': {e}")
            status = "INFRA_ERROR"
            output_payload = {"error": str(e)}

        cost_act = cost_est if status == "SUCCESS" else int(cost_est * 0.2)  # Partial charge for failure

        # Create immutable execution log
        log = SkillExecutionLog(
            tenant_id=tenant_id,
            venture_id=venture_id,
            skill_name=skill.name,
            protocol_name=protocol_name,
            step_index=step_index,
            cost_estimated=cost_est,
            cost_actual=cost_act,
            tier_used=tier,
            status=status,
            output_payload=output_payload,
            anchors_hit=anchors_hit,
            metrics_lift=metrics_lift,
            timestamp=datetime.utcnow()
        )
        self.execution_logs.append(log)

        # Update aggregated scorecard
        scorecard = self.get_scorecard(skill.name)
        if status == "SUCCESS":
            scorecard.success_count += 1
            # Rolling average for cost
            scorecard.average_cost_actual = (
                (scorecard.average_cost_actual * (scorecard.success_count - 1) + cost_act) / scorecard.success_count
            )
            # Update average metrics lift
            for metric, lift in metrics_lift.items():
                curr_lift = scorecard.average_lift.get(metric, 0.0)
                scorecard.average_lift[metric] = (
                    (curr_lift * (scorecard.success_count - 1) + lift) / scorecard.success_count
                )
        else:
            scorecard.failure_count += 1

        return output_payload

    def query_decayed_signals(self, half_life_days: float = 7.0) -> List[Dict[str, Any]]:
        """Queries the WorldGraph and applies time decay to DECAYING nodes/edges."""
        decayed_results = []
        for edge in self.world_graph.edges:
            is_decaying = edge.properties.get("knowledge_type") == KnowledgeType.DECAYING.value
            if is_decaying:
                observed_str = edge.properties.get("observed_at")
                if observed_str:
                    observed_time = datetime.fromisoformat(observed_str)
                    decayed_weight = decay_confidence(
                        base_confidence=edge.weight,
                        observed_time=observed_time,
                        half_life_days=half_life_days
                    )
                    decayed_results.append({
                        "edge": edge,
                        "base_weight": edge.weight,
                        "decayed_weight": decayed_weight,
                        "observed_at": observed_time
                    })
        return decayed_results

    def _generic_simulation_run(self, skill: BusinessSkill, input_payload: Dict[str, Any], tier: CostTier) -> Dict[str, Any]:
        """Default generic simulation if no custom logic is defined."""
        logger.info(f"Running generic simulation for '{skill.name}'")

        # Mutate WorldGraph dynamically with simulated nodes
        entity_id = f"sim_{skill.name}_{uuid.uuid4().hex[:6]}"
        node_type = "resource"
        if skill.domain == "market_research":
            node_type = "market"
        elif skill.domain == "marketing":
            node_type = "campaign"
        elif skill.domain == "sales":
            node_type = "customer"

        node = EntityNode(
            node_id=entity_id,
            node_type=node_type,
            properties={
                "name": f"Generic Simulated {skill.name}",
                "generated_by": skill.name,
                "knowledge_type": skill.knowledge_type.value,
                "tier": tier.value,
                "observed_at": datetime.utcnow().isoformat()
            }
        )
        self.world_graph.add_node(node)

        # Standard output payload
        return {
            "status": "simulated",
            "entity_id": entity_id,
            "anchors_hit": [f"anchor_{skill.name}_sim_success"],
            "metrics_lift": {"generic_efficiency": 0.02 if tier == CostTier.EXPENSIVE else 0.005}
        }


class ProtocolEngine:
    """Manages execution of multi-step declarative BusinessProtocols with budget tracking."""

    def __init__(self, skill_runner: SkillRunner) -> None:
        self.runner = skill_runner
        # Map of tenant_id/venture_id to remaining budget credits
        self.budgets: Dict[str, int] = {}
        self.protocol_scorecards: Dict[str, ProtocolScorecard] = {}

    def get_budget(self, tenant_id: str, venture_id: str) -> int:
        key = f"{tenant_id}:{venture_id}"
        return self.budgets.get(key, 0)

    def set_budget(self, tenant_id: str, venture_id: str, amount_credits: int) -> None:
        key = f"{tenant_id}:{venture_id}"
        self.budgets[key] = amount_credits

    def get_protocol_scorecard(self, protocol_name: str) -> ProtocolScorecard:
        if protocol_name not in self.protocol_scorecards:
            self.protocol_scorecards[protocol_name] = ProtocolScorecard(protocol_name=protocol_name)
        return self.protocol_scorecards[protocol_name]

    def _resolve_input(self, step_inputs: Dict[str, Any], previous_step_outputs: Dict[int, Dict[str, Any]]) -> Dict[str, Any]:
        """Resolves inputs using parameter mappings like 'step_0.product_id'."""
        resolved: Dict[str, Any] = {}
        for key, mapping in step_inputs.items():
            if isinstance(mapping, str) and mapping.startswith("step_"):
                # Parse "step_0.param_name"
                try:
                    parts = mapping.split(".", 1)
                    step_num = int(parts[0].split("_")[1])
                    param_name = parts[1]
                    resolved[key] = previous_step_outputs[step_num].get(param_name)
                except Exception as e:
                    logger.warning(f"Failed to resolve mapping '{mapping}': {e}")
                    resolved[key] = None
            else:
                resolved[key] = mapping
        return resolved

    def run_protocol(
        self,
        protocol: BusinessProtocol,
        tenant_id: str,
        venture_id: str,
        registry: Any,
        initial_inputs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Executes a full pipeline, routing parameter state, and managing budget downshifting/halting."""
        logger.info(f"Initiating protocol '{protocol.name}' (Venture: {venture_id}).")

        key = f"{tenant_id}:{venture_id}"
        budget = self.get_budget(tenant_id, venture_id)

        # Ensure budget stays within protocol cap
        if budget > protocol.budget_cap_credits:
            budget = protocol.budget_cap_credits
            self.set_budget(tenant_id, venture_id, budget)

        previous_step_outputs: Dict[int, Dict[str, Any]] = {-1: initial_inputs}
        step_outputs: Dict[int, Dict[str, Any]] = {}

        success = True
        halted_reason: Optional[str] = None

        for idx, step in enumerate(protocol.steps):
            skill = registry.get_skill(step.skill_name)
            if not skill:
                logger.error(f"Skill '{step.skill_name}' not registered in registry. Halting protocol.")
                success = False
                halted_reason = f"Skill '{step.skill_name}' missing from registry."
                break

            # 1. Resolve inputs from prior step outputs
            resolved_inputs = self._resolve_input(step.parameter_mappings, previous_step_outputs)
            # Merge with initial inputs if not mapped
            for k, v in initial_inputs.items():
                if k not in resolved_inputs:
                    resolved_inputs[k] = v

            # 2. Budget and Cost Tier Determination
            expensive_cost = skill.base_cost_credits
            cheap_cost = max(1, expensive_cost // 5)

            selected_tier = CostTier.EXPENSIVE
            current_budget = self.get_budget(tenant_id, venture_id)

            if current_budget < expensive_cost:
                if protocol.downshift_enabled and current_budget >= cheap_cost:
                    logger.warning(f"Budget low ({current_budget} credits). Downshifting '{skill.name}' to CHEAP tier.")
                    selected_tier = CostTier.CHEAP
                else:
                    logger.error(f"Budget exhausted ({current_budget} credits, needs at least {cheap_cost}). BUDGET_HALTED.")
                    success = False
                    halted_reason = "BUDGET_HALTED"

                    # Record a budget-halted log entry
                    self.runner.execution_logs.append(
                        SkillExecutionLog(
                            tenant_id=tenant_id,
                            venture_id=venture_id,
                            skill_name=skill.name,
                            protocol_name=protocol.name,
                            step_index=idx,
                            cost_estimated=cheap_cost,
                            cost_actual=0,
                            tier_used=CostTier.CHEAP,
                            status="BUDGET_HALTED",
                            output_payload={"reason": "Insufficient budget for step execution."},
                            timestamp=datetime.utcnow()
                        )
                    )
                    break

            # 3. Execute Skill
            output = self.runner.execute_skill(
                skill=skill,
                tenant_id=tenant_id,
                venture_id=venture_id,
                input_payload=resolved_inputs,
                tier=selected_tier,
                protocol_name=protocol.name,
                step_index=idx
            )

            # Deduct budget credits
            act_cost = self.runner.execution_logs[-1].cost_actual
            self.set_budget(tenant_id, venture_id, max(0, current_budget - act_cost))

            # Store outputs
            previous_step_outputs[idx] = output
            step_outputs[idx] = output

            # Validate success and halt policies
            if self.runner.execution_logs[-1].status != "SUCCESS":
                if protocol.halt_on_failure:
                    logger.error(f"Step {idx} ({skill.name}) failed. Halting protocol as halt_on_failure is enabled.")
                    success = False
                    halted_reason = f"Step {idx} ({skill.name}) failed."
                    break

        # Update protocol scorecard
        scorecard = self.get_protocol_scorecard(protocol.name)
        if success:
            scorecard.success_count += 1
        else:
            scorecard.failure_count += 1

        return {
            "protocol_name": protocol.name,
            "success": success,
            "halted_reason": halted_reason,
            "step_outputs": step_outputs,
            "remaining_budget": self.get_budget(tenant_id, venture_id)
        }
