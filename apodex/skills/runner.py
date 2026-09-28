from __future__ import annotations
import math
import uuid
import logging
from datetime import datetime, timezone, timedelta
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
    LearnFeedStage,
    PlaybookUnit,
    LearnFeedState,
    DecisionLog,
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
        current_time = datetime.now(timezone.utc)

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

        start_time = datetime.now(timezone.utc)
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
            timestamp=datetime.now(timezone.utc)
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
                "observed_at": datetime.now(timezone.utc).isoformat()
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
                            timestamp=datetime.now(timezone.utc)
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


# =====================================================================
# 9-Stage Learn-Feed Framework Loop Engine
# =====================================================================

class LearnFeedLoopEngine:
    """
    Continuous Learn-Feed Loop Engine implementing Stages 0-9 with cost tracking,
    human approval gates, consecutive profitable days, and pattern decay checks.
    """

    def __init__(self, world_graph: Optional[WorldGraph] = None) -> None:
        self.world_graph = world_graph if world_graph is not None else WorldGraph()
        self.playbooks: Dict[str, PlaybookUnit] = {}
        self.state = LearnFeedState()
        self.decision_logs: List[DecisionLog] = []

    # -----------------------------------------------------------------
    # Stage 0: Learn
    # -----------------------------------------------------------------
    def stage_0_learn(self, raw_corpus_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Ingests raw inputs, classifying them as EVERGREEN or DECAYING with decay half-lives."""
        logger.info("Executing Stage 0: LEARN. Classifying raw content sources.")
        self.state.current_stage = LearnFeedStage.STAGE_0_LEARN

        tagged_corpus = []
        for item in raw_corpus_items:
            source_type = item.get("source_type", "book")

            # Categorize evergreen vs decaying knowledge types
            if source_type in ["book", "practitioner_philosophy", "strategy_discipline"]:
                k_type = KnowledgeType.EVERGREEN
                half_life = 365.0  # Decays very slowly
            else:
                k_type = KnowledgeType.DECAYING
                half_life = 7.0  # Decays fast

            tagged = {
                "raw_content": item.get("content", ""),
                "source": item.get("source_name", "unknown_source"),
                "knowledge_type": k_type,
                "half_life_days": half_life,
                "pattern_id": item.get("pattern_id", f"pat_{uuid.uuid4().hex[:6]}")
            }
            tagged_corpus.append(tagged)

        return tagged_corpus

    # -----------------------------------------------------------------
    # Stage 1: Structure
    # -----------------------------------------------------------------
    def stage_1_structure(self, tagged_corpus: List[Dict[str, Any]]) -> List[PlaybookUnit]:
        """Extracts items into atomic, structured PlaybookUnits with Spot-Checking."""
        logger.info("Executing Stage 1: STRUCTURE. Formulating Playbook database.")
        self.state.current_stage = LearnFeedStage.STAGE_1_STRUCTURE

        new_playbooks = []
        for tagged in tagged_corpus:
            source = tagged.get("source", tagged.get("source_name", "unknown_source"))
            content = tagged.get("raw_content", tagged.get("content", ""))

            # Structure extraction
            unit = PlaybookUnit(
                pattern_id=tagged.get("pattern_id", f"pat_{uuid.uuid4().hex[:6]}"),
                pattern=f"Structured Action Pattern from {source}" if content else "",
                precondition="Signal meets criteria for " + source,
                signal="demand_discovery_match",
                failure_mode="Saturated customer segments",
                source=source,
                confidence=0.85,
                knowledge_type=tagged.get("knowledge_type", KnowledgeType.EVERGREEN),
                half_life_days=tagged.get("half_life_days", 30.0)
            )

            # --- SPOT-CHECK GATE ---
            # Garbage extraction poisons everything. Enforce schema sanity rules:
            if not unit.pattern or not unit.precondition or unit.confidence <= 0.0:
                logger.error(f"Spotcheck REJECTED corrupt playbook unit: {unit.pattern_id}")
                continue

            self.playbooks[unit.pattern_id] = unit
            new_playbooks.append(unit)

        return new_playbooks

    # -----------------------------------------------------------------
    # Stage 2: Wire
    # -----------------------------------------------------------------
    def stage_2_wire(self, loop_stage: str, query_signal: str) -> List[PlaybookUnit]:
        """Wires retrieval hooks, logging compute/retrieval costs per query."""
        logger.info(f"Executing Stage 2: WIRE. Fetching playbooks for loop stage: {loop_stage}")
        self.state.current_stage = LearnFeedStage.STAGE_2_WIRE

        # Retrieval matching matching signal
        matched = []
        for p in self.playbooks.values():
            if p.signal == query_signal or query_signal in p.precondition:
                matched.append(p)

        # cost logging per retrieval call (compute isn't free)
        compute_cost_cents = len(matched) * 15  # 15 cents per playbook retrieved
        logger.info(f"WIRE RETRIEVED {len(matched)} playbooks. Compute cost logged: {compute_cost_cents} cents.")

        return matched

    # -----------------------------------------------------------------
    # Stage 3: Backtest
    # -----------------------------------------------------------------
    def stage_3_backtest(self, historical_signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Replays historical signals through wired loop to perform reasoning sanity checks."""
        logger.info("Executing Stage 3: BACKTEST. Replaying past signals.")
        self.state.current_stage = LearnFeedStage.STAGE_3_BACKTEST

        invocations: Dict[str, int] = {}
        passed_sanity = True

        for sig in historical_signals:
            query = sig.get("signal_type", "demand_discovery_match")
            matched_playbooks = self.stage_2_wire("backtest", query)

            # Track counts
            for p in matched_playbooks:
                invocations[p.pattern_id] = invocations.get(p.pattern_id, 0) + 1

            # If we get completely invalid or empty matches under a valid query, fail sanity check
            if query == "demand_discovery_match" and not matched_playbooks:
                passed_sanity = False

        return {
            "passed_sanity": passed_sanity,
            "total_backtest_runs": len(historical_signals),
            "invoked_playbook_counts": invocations
        }

    # -----------------------------------------------------------------
    # Stage 4: Experiment
    # -----------------------------------------------------------------
    def stage_4_experiment(
        self,
        signal: str,
        playbook_on: bool,
        channel: str,
        proposed_spend_cents: int
    ) -> Dict[str, Any]:
        """Controlled split test, enforcing compliance/legal gates on offer and channels."""
        logger.info(f"Executing Stage 4: EXPERIMENT (Channel: {channel}).")
        self.state.current_stage = LearnFeedStage.STAGE_4_EXPERIMENT

        # --- COMPLIANCE / LEGAL GATE ---
        # Legal/compliance check on channel/offer (ToS, ad policy, affiliate rules)
        is_compliant = True
        if "illegal" in signal.lower() or channel in ["unauthorized_blackhat_forum"]:
            logger.error("Compliance Gate REJECTED the offer/channel combination!")
            is_compliant = False

        if not is_compliant:
            return {"success": False, "reason": "COMPLIANCE_REJECTED", "conversion_rate": 0.0}

        # Simulate lift measurement
        base_conversion = 0.012  # 1.2% base
        if playbook_on:
            # Active playbook retrieval increases conversion
            conversion = base_conversion + 0.008  # +0.8% lift (2.0%)
        else:
            conversion = base_conversion

        lift_pct = ((conversion - base_conversion) / base_conversion) * 100.0 if playbook_on else 0.0

        return {
            "success": True,
            "conversion_rate": conversion,
            "lift_percentage": lift_pct,
            "proposed_spend_cents": proposed_spend_cents
        }

    # -----------------------------------------------------------------
    # Stage 5: Live Loop, Single Vertical (14-day microfish)
    # -----------------------------------------------------------------
    def stage_5_live_loop(
        self,
        channel: str,
        spend_cents: int,
        revenue_cents: int,
        playbook_ids: List[str]
    ) -> DecisionLog:
        """
        Runs the full 6-stage economic loop.
        Features real-time cost-per-decision, per-channel kill switch,
        and non-waivable human approval above budget thresholds.
        """
        logger.info(f"Executing Stage 5: LIVE LOOP on channel: {channel}.")
        self.state.current_stage = LearnFeedStage.STAGE_5_LIVE_LOOP

        # Check system freeze / fail state
        if self.state.frozen:
            raise RuntimeError("Loop is frozen due to payment/billing flag! Enforce human intervention.")

        # Check per-channel kill switch
        channel_active = self.state.channel_kill_switches.get(channel, True)
        if not channel_active:
            raise ValueError(f"Channel '{channel}' is suppressed by kill switch. Cannot deploy capital!")

        # --- NON-WAIVABLE HUMAN APPROVAL GATE ---
        # Approve any capital deployment above human threshold (e.g., $1000.00)
        human_threshold_cents = 100000
        cleared_by_human = True
        if spend_cents >= human_threshold_cents:
            # Requires human signature
            logger.warning("Spend exceeds threshold. Triggering Human Approval request.")
            # Mock check: fail if unauthorized by inputs
            cleared_by_human = False

        # Compute True P&L (cost-per-decision tracked alongside revenue)
        profit = revenue_cents - spend_cents

        if profit > 0 and cleared_by_human:
            self.state.consecutive_profitable_days += 1
        else:
            # reset counter on bad days or losses
            self.state.consecutive_profitable_days = 0

            # --- AUTO-TRIGGER KILL SWITCH ---
            # Suppress channel if loss exceeds bounds
            if profit < -50000:  # loss > $500
                logger.error(f"SLA Degradation on '{channel}': Loss of {profit} cents. TRIGGERING KILL SWITCH.")
                self.state.channel_kill_switches[channel] = False

        log = DecisionLog(
            vertical=self.state.active_vertical,
            stage=LearnFeedStage.STAGE_5_LIVE_LOOP,
            playbook_invoked_ids=playbook_ids,
            revenue_cents=revenue_cents,
            cost_cents=spend_cents,
            profit_cents=profit,
            cleared_by_human=cleared_by_human,
            channel=channel
        )
        self.decision_logs.append(log)
        return log

    # -----------------------------------------------------------------
    # Stage 6: Attribution
    # -----------------------------------------------------------------
    def stage_6_attribution(self, decision_log_id: uuid.UUID, outcome_win: bool) -> List[PlaybookUnit]:
        """Attributes real-world profit outcomes back to the specific invoked patterns with cost-adjusted margins."""
        logger.info(f"Executing Stage 6: ATTRIBUTION for log: {decision_log_id}")
        self.state.current_stage = LearnFeedStage.STAGE_6_ATTRIBUTION

        # Find log
        target_log = None
        for l in self.decision_logs:
            if l.decision_id == decision_log_id:
                target_log = l
                break

        if not target_log:
            logger.warning("Decision log not found for attribution.")
            return []

        attributed_units = []
        for p_id in target_log.playbook_invoked_ids:
            p = self.playbooks.get(p_id)
            if p:
                p.times_invoked += 1

                # Update win rate as a sliding average
                current_wins = p.win_rate * (p.times_invoked - 1)
                new_wins = current_wins + (1.0 if outcome_win else 0.0)
                p.win_rate = new_wins / p.times_invoked

                # Cost adjusted scoring
                p.avg_revenue_lift = (p.avg_revenue_lift * (p.times_invoked - 1) + (target_log.profit_cents / 100.0)) / p.times_invoked
                attributed_units.append(p)

        return attributed_units

    # -----------------------------------------------------------------
    # Stage 7: Feed Back
    # -----------------------------------------------------------------
    def stage_7_feed_back(self, current_time: Optional[datetime] = None) -> None:
        """Re-weights playbooks, enforcing a forced re-validation / pattern decay check window."""
        logger.info("Executing Stage 7: FEED BACK. Re-weighting playbook databases.")
        self.state.current_stage = LearnFeedStage.STAGE_7_FEED_BACK

        if current_time is None:
            current_time = datetime.now(timezone.utc)

        revalidation_window_days = 15.0

        for p in self.playbooks.values():
            # --- FORCED DECAY RE-VALIDATION CHECK ---
            age_days = (current_time - p.last_revalidated).total_seconds() / 86400.0
            if age_days >= revalidation_window_days:
                logger.warning(f"Playbook {p.pattern_id} has exceeded re-validation age ({age_days:.1f} days). Decaying confidence.")
                p.confidence = decay_confidence(p.confidence, p.last_revalidated, current_time, p.half_life_days)
                p.last_revalidated = current_time

            # Weight adjust: boost based on win rate, downweight if failing
            if p.times_invoked >= 2:
                if p.win_rate >= 0.70:
                    p.confidence = min(1.0, p.confidence + 0.05)
                elif p.win_rate <= 0.30:
                    p.confidence = max(0.0, p.confidence - 0.15)

    # -----------------------------------------------------------------
    # Stage 8: Expansion Decision
    # -----------------------------------------------------------------
    def stage_8_expansion(self, trigger_type: str, target_vertical: str) -> Dict[str, Any]:
        """Evaluates thresholds before vertical or capital scale expansion."""
        logger.info(f"Executing Stage 8: EXPANSION. Checking trigger: {trigger_type}")
        self.state.current_stage = LearnFeedStage.STAGE_8_EXPANSION

        # Expansion requires consecutive profitable days threshold (e.g. 14 days)
        if self.state.consecutive_profitable_days < 14:
            logger.error(f"Cannot expand! Only {self.state.consecutive_profitable_days} profitable days. Needs 14.")
            return {"approved": False, "reason": "Insufficient profitable run duration."}

        if trigger_type == "new_vertical":
            # New vertical requires its own isolated Stage 3-5 backtest and experiment cycle
            logger.info(f"Initiating isolated cycle for new vertical: '{target_vertical}'.")
            return {"approved": True, "action": "INITIALIZE_ISOLATED_STAGE_3_CYCLE", "target": target_vertical}

        elif trigger_type == "increased_capital":
            # Capital increase on same vertical requires shorter backtest
            logger.info("Same vertical expansion approved. Initiating micro-backtest validation.")
            return {"approved": True, "action": "INITIALIZE_MICRO_BACKTEST"}

        return {"approved": False, "reason": "Unknown trigger."}

    # -----------------------------------------------------------------
    # Stage 9: Failure Handling & Fallbacks
    # -----------------------------------------------------------------
    def stage_9_failure_handling(self, failure_event: Dict[str, Any]) -> Dict[str, Any]:
        """Provides fallback actions for suppressed channels, API issues, or payment flags."""
        logger.info("Executing Stage 9: FAILURE HANDLING.")
        self.state.current_stage = LearnFeedStage.STAGE_9_FAILURE_HANDLING

        failure_type = failure_event.get("type", "api_failure")
        affected_channel = failure_event.get("channel", "default_channel")

        if failure_type == "channel_suppressed":
            # Auto-disable target channel kill switch
            self.state.channel_kill_switches[affected_channel] = False
            logger.error(f"FALLBACK: Channel suppressed! Kill switch triggered for {affected_channel}.")
            return {"action": "TRIGGER_KILL_SWITCH", "channel": affected_channel}

        elif failure_type == "api_failure":
            # Loop pauses
            logger.error("FALLBACK: Critical API failure! Pausing loop execution.")
            return {"action": "PAUSE_LOOP_AND_WAIT"}

        elif failure_type == "payment_flagged":
            # Freezes capital gate entirely and alerts human
            self.state.frozen = True
            logger.error("FALLBACK: PAYMENT ACCOUNT FLAGGED! Freeze capital gate and notify human auditor.")
            return {"action": "FREEZE_ALL_CAPITAL", "notify_human": True}

        return {"action": "LOG_AND_IGNORE"}
