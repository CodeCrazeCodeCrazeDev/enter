from __future__ import annotations
import uuid
import pytest
from datetime import timezone, datetime, timedelta

from pydantic import ValidationError

from apodex.skills.models import (
    BusinessSkill,
    BusinessProtocol,
    ProtocolStep,
    KnowledgeType,
    CostTier,
    SkillExecutionLog,
    LearnFeedStage,
    PlaybookUnit,
    LearnFeedState,
    DecisionLog,
)
from apodex.skills.registry import SkillRegistry
from apodex.skills.runner import SkillRunner, ProtocolEngine, decay_confidence, LearnFeedLoopEngine
from apodex.skills.implementation import register_all_custom_executors


# =====================================================================
# 1. Registry & Filtration Verification Tests
# =====================================================================

def test_registry_loading_and_filtering():
    registry = SkillRegistry()

    # Assert total count of 60 skills
    all_skills = registry.list_skills()
    assert len(all_skills) == 60, f"Expected 60 registered skills, found {len(all_skills)}."

    # Test filtering by domain
    strategy_skills = registry.list_skills(domain="strategy")
    assert len(strategy_skills) == 10
    for s in strategy_skills:
        assert s.domain == "strategy"
        assert s.knowledge_type == KnowledgeType.EVERGREEN

    # Test filtering by knowledge type
    decaying_skills = registry.list_skills(knowledge_type=KnowledgeType.DECAYING)
    assert len(decaying_skills) == 7
    for s in decaying_skills:
        assert s.knowledge_type == KnowledgeType.DECAYING

    # Test retrieving single skill
    ab_test_skill = registry.get_skill("structured_ab_testing")
    assert ab_test_skill is not None
    assert ab_test_skill.name == "structured_ab_testing"
    assert ab_test_skill.domain == "creative"
    assert ab_test_skill.knowledge_type == KnowledgeType.EVERGREEN


# =====================================================================
# 2. Confidence Weight Decay Verification Tests
# =====================================================================

def test_exponential_confidence_decay():
    now = datetime.now(timezone.utc)

    # No decay if queried at observation time
    conf_0 = decay_confidence(base_confidence=0.8, observed_time=now, current_time=now, half_life_days=7.0)
    assert pytest.approx(conf_0) == 0.8

    # 7 days decay (1 half-life) -> should be exactly 50% of 0.8 -> 0.4
    observed_time = now - timedelta(days=7)
    conf_1 = decay_confidence(base_confidence=0.8, observed_time=observed_time, current_time=now, half_life_days=7.0)
    assert pytest.approx(conf_1) == 0.4

    # 14 days decay (2 half-lives) -> should be 25% of 0.8 -> 0.2
    observed_time_2 = now - timedelta(days=14)
    conf_2 = decay_confidence(base_confidence=0.8, observed_time=observed_time_2, current_time=now, half_life_days=7.0)
    assert pytest.approx(conf_2) == 0.2

    # Verify that faster half-life decays faster
    conf_fast = decay_confidence(base_confidence=0.8, observed_time=observed_time, current_time=now, half_life_days=3.5)
    # 7 days under 3.5 half-life is 2 half-lives -> 0.2
    assert pytest.approx(conf_fast) == 0.2


# =====================================================================
# 3. Dynamic Protocol Parameter Wiring and Core-Loop Run Tests
# =====================================================================

@pytest.mark.asyncio
async def test_end_to_end_core_loop_protocol_success():
    """
    Verifies that a full protocol execution chains outputs to inputs,
    performs WorldGraph mutations, and updates performance tables under a full budget.
    """
    runner = SkillRunner()
    register_all_custom_executors(runner)

    engine = ProtocolEngine(skill_runner=runner)
    registry = SkillRegistry()

    # Build Core Economic Playbook/Protocol
    protocol = BusinessProtocol(
        name="core_growth_pipeline",
        description="Core Loop: Opportunity -> Narrative -> LP -> A/B Test -> Metrics -> Reallocation",
        steps=[
            ProtocolStep(
                skill_name="opportunity_evaluation_frameworks",
                parameter_mappings={"niche_name": "step_-1.niche_name", "estimated_tam_cents": "step_-1.estimated_tam_cents"}
            ),
            ProtocolStep(
                skill_name="narrative_structures",
                parameter_mappings={"market_id": "step_0.market_id", "core_pain_point": "step_-1.core_pain_point"}
            ),
            ProtocolStep(
                skill_name="landing_page_patterns",
                parameter_mappings={"narrative_id": "step_1.narrative_id", "product_name": "step_-1.product_name"}
            ),
            ProtocolStep(
                skill_name="structured_ab_testing",
                parameter_mappings={"offer_id": "step_2.offer_id", "variant_count": "step_-1.variant_count"}
            ),
            ProtocolStep(
                skill_name="revenue_metric_literacy",
                parameter_mappings={"campaign_id": "step_3.campaign_id", "cac_cents": "step_-1.cac_cents"}
            ),
            ProtocolStep(
                skill_name="business_model_design",
                parameter_mappings={"metric_node_id": "step_4.metric_node_id", "available_surplus_cents": "step_-1.available_surplus_cents"}
            )
        ],
        budget_cap_credits=1000,
        downshift_enabled=True,
        halt_on_failure=True
    )

    # Set plentiful budget credits for this venture
    tenant_id = "tenant_test"
    venture_id = "venture_test"
    engine.set_budget(tenant_id, venture_id, 500)

    initial_inputs = {
        "niche_name": "Enterprise Document Search SaaS",
        "estimated_tam_cents": 250000000,  # $2.5M
        "core_pain_point": "Manual indexing wastes hours",
        "product_name": "Apodex Search",
        "variant_count": 3,
        "cac_cents": 1200,  # $12.00
        "available_surplus_cents": 800000  # $8k
    }

    # Execute
    res = engine.run_protocol(
        protocol=protocol,
        tenant_id=tenant_id,
        venture_id=venture_id,
        registry=registry,
        initial_inputs=initial_inputs
    )

    assert res["success"] is True, f"Protocol failed: {res.get('halted_reason')}"
    assert res["remaining_budget"] < 500

    # Check that outputs of previous steps mapped correctly
    step_outputs = res["step_outputs"]
    assert "market_id" in step_outputs[0]
    assert "narrative_id" in step_outputs[1]
    assert "product_id" in step_outputs[2]
    assert "campaign_id" in step_outputs[3]
    assert "metric_node_id" in step_outputs[4]
    assert "allocation_id" in step_outputs[5]

    # Verify WorldGraph contains all written nodes and edges
    assert len(runner.world_graph.nodes) >= 8  # Market, Competitor, Narrative, Product, Offer, Campaign, Metric, Allocation
    assert len(runner.world_graph.edges) >= 5

    # Verify scorecards updated correctly
    op_scorecard = runner.get_scorecard("opportunity_evaluation_frameworks")
    assert op_scorecard.success_count == 1
    assert op_scorecard.average_cost_actual == 25  # Opportunity framework is 25 credits base

    proto_scorecard = engine.get_protocol_scorecard("core_growth_pipeline")
    assert proto_scorecard.success_count == 1


# =====================================================================
# 4. Budget Constraints: Downshifting & Halting Tests
# =====================================================================

@pytest.mark.asyncio
async def test_protocol_budget_downshifting():
    """
    Checks that when budget is moderate, expensive steps downshift to CHEAP
    instead of halting execution.
    """
    runner = SkillRunner()
    register_all_custom_executors(runner)
    engine = ProtocolEngine(skill_runner=runner)
    registry = SkillRegistry()

    protocol = BusinessProtocol(
        name="downshift_pipeline",
        description="Pipeline to test budget downshifting",
        steps=[
            ProtocolStep(skill_name="business_model_design", parameter_mappings={})
        ],
        budget_cap_credits=100,
        downshift_enabled=True,
        halt_on_failure=True
    )

    tenant_id = "tenant_downshift"
    venture_id = "venture_downshift"

    # business_model_design needs 30 credits base.
    # If budget is 10, expensive (30) fails. Since downshift_enabled=True,
    # it downshifts to CHEAP which costs base // 5 = 6 credits.
    engine.set_budget(tenant_id, venture_id, 10)

    res = engine.run_protocol(
        protocol=protocol,
        tenant_id=tenant_id,
        venture_id=venture_id,
        registry=registry,
        initial_inputs={"available_surplus_cents": 5000}
    )

    assert res["success"] is True
    assert res["remaining_budget"] == 4  # 10 - 6 = 4 credits remaining
    assert len(runner.execution_logs) == 1
    assert runner.execution_logs[0].tier_used == CostTier.CHEAP
    assert runner.execution_logs[0].cost_actual == 6


@pytest.mark.asyncio
async def test_protocol_budget_halting():
    """
    Checks that when budget is below even the cheapest option,
    the protocol engine immediately Halts with BUDGET_HALTED and leaves the step unexecuted.
    """
    runner = SkillRunner()
    register_all_custom_executors(runner)
    engine = ProtocolEngine(skill_runner=runner)
    registry = SkillRegistry()

    protocol = BusinessProtocol(
        name="halt_pipeline",
        description="Pipeline to test budget halting",
        steps=[
            ProtocolStep(skill_name="business_model_design", parameter_mappings={})
        ],
        budget_cap_credits=100,
        downshift_enabled=True,
        halt_on_failure=True
    )

    tenant_id = "tenant_halt"
    venture_id = "venture_halt"

    # Needs at least 6 credits for CHEAP tier. We give it only 3 credits.
    engine.set_budget(tenant_id, venture_id, 3)

    res = engine.run_protocol(
        protocol=protocol,
        tenant_id=tenant_id,
        venture_id=venture_id,
        registry=registry,
        initial_inputs={"available_surplus_cents": 5000}
    )

    assert res["success"] is False
    assert res["halted_reason"] == "BUDGET_HALTED"
    assert res["remaining_budget"] == 3  # unchanged

    # The step execution log records the BUDGET_HALTED state
    assert len(runner.execution_logs) == 1
    assert runner.execution_logs[0].status == "BUDGET_HALTED"
    assert runner.execution_logs[0].cost_actual == 0


# =====================================================================
# 5. Decay Signal Filtering and WorldGraph Isolation Tests
# =====================================================================

def test_decayed_signals_filtering_in_graph():
    """
    Verifies that we can write both EVERGREEN and DECAYING nodes,
    and query/filter decayed DECAYING signals distinctly using time-decay functions.
    """
    runner = SkillRunner()
    register_all_custom_executors(runner)

    # Assert clean graph
    assert len(runner.world_graph.nodes) == 0

    # 1. Run 'opportunity_evaluation_frameworks' which produces EVERGREEN nodes
    skill_opp = SkillRegistry().get_skill("opportunity_evaluation_frameworks")
    runner.execute_skill(
        skill=skill_opp,
        tenant_id="test",
        venture_id="test",
        input_payload={"niche_name": "SaaS PDF"},
        tier=CostTier.CHEAP
    )

    # 2. Run 'structured_ab_testing' which produces DECAYING nodes
    skill_ab = SkillRegistry().get_skill("structured_ab_testing")
    runner.execute_skill(
        skill=skill_ab,
        tenant_id="test",
        venture_id="test",
        input_payload={"offer_id": "offer_123"},
        tier=CostTier.CHEAP
    )

    # Let's manually backdate the DECAYING edge's timestamp to 7 days ago to test decay filtering
    decayed_edges = [e for e in runner.world_graph.edges if e.properties.get("knowledge_type") == KnowledgeType.DECAYING.value]
    assert len(decayed_edges) == 1
    edge = decayed_edges[0]

    # Backdate to 7 days ago
    seven_days_ago = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
    edge.properties["observed_at"] = seven_days_ago
    edge.weight = 0.8

    # Query decayed signals
    decayed_signals = runner.query_decayed_signals(half_life_days=7.0)
    assert len(decayed_signals) == 1
    assert decayed_signals[0]["base_weight"] == 0.8
    # 1 half-life -> should be exactly 0.4
    assert pytest.approx(decayed_signals[0]["decayed_weight"]) == 0.4


# =====================================================================
# 6. 9-Stage Learn-Feed Framework Tests
# =====================================================================

def test_stage_0_to_4_learn_feed_stages():
    """
    Verifies Stage 0, Stage 1, Stage 2, Stage 3, and Stage 4 execution.
    Classifying, structuring, retrieval-cost wiring, backtesting, and compliance checks.
    """
    engine = LearnFeedLoopEngine()

    # Sample raw items (Stage 0)
    raw = [
        {"content": "Zero to One Strategy", "source_name": "Peter Thiel", "source_type": "book", "pattern_id": "pat_thiel"},
        {"content": "Ad Campaign CTR spike", "source_name": "Facebook Ad API", "source_type": "ad_velocity", "pattern_id": "pat_fb"}
    ]

    # Stage 0: Learn class classification
    tagged = engine.stage_0_learn(raw)
    assert len(tagged) == 2
    assert tagged[0]["knowledge_type"] == KnowledgeType.EVERGREEN
    assert tagged[1]["knowledge_type"] == KnowledgeType.DECAYING
    assert tagged[1]["half_life_days"] == 7.0

    # Stage 1: Structure with Spot-Checking
    playbooks = engine.stage_1_structure(tagged)
    assert len(playbooks) == 2
    assert "pat_thiel" in engine.playbooks

    # Corrupt item test should be filtered out
    corrupt_tagged = [{"content": "", "source_name": "corrupt", "knowledge_type": KnowledgeType.EVERGREEN, "half_life_days": 10.0, "pattern_id": "pat_corrupt"}]
    structured_corrupt = engine.stage_1_structure(corrupt_tagged)
    assert len(structured_corrupt) == 0  # rejected

    # Stage 2: Wire with compute cost logging
    matched = engine.stage_2_wire("narrative_synthesis", "demand_discovery_match")
    assert len(matched) == 2  # both signal maps are demand_discovery_match by default

    # Stage 3: Backtest
    backtest_res = engine.stage_3_backtest([{"signal_type": "demand_discovery_match"}])
    assert backtest_res["passed_sanity"] is True
    assert backtest_res["invoked_playbook_counts"]["pat_thiel"] == 1

    # Stage 4: Experiment with compliance/legal checks
    experiment_ok = engine.stage_4_experiment("Valid niche product", playbook_on=True, channel="google_ads", proposed_spend_cents=5000)
    assert experiment_ok["success"] is True
    assert experiment_ok["lift_percentage"] > 0

    # Compliance rejection
    experiment_bad = engine.stage_4_experiment("Illegal shadow market", playbook_on=True, channel="unauthorized_blackhat_forum", proposed_spend_cents=1000)
    assert experiment_bad["success"] is False
    assert experiment_bad["reason"] == "COMPLIANCE_REJECTED"


def test_stage_5_live_loop_and_kill_switches():
    """
    Verifies Stage 5 consecutive profitable days counter, reset on loss,
    and automatic SLA kill-switch trigger on a suppressed channel.
    """
    engine = LearnFeedLoopEngine()
    engine.playbooks["pat_1"] = PlaybookUnit(
        pattern_id="pat_1", pattern="pat", precondition="pre", signal="sig",
        failure_mode="fail", source="src", confidence=0.8, knowledge_type=KnowledgeType.EVERGREEN, half_life_days=30.0
    )

    # 1. Day 1: Profitable run ($50 spend, $150 revenue) -> profit = $100
    log1 = engine.stage_5_live_loop(channel="facebook_ads", spend_cents=5000, revenue_cents=15000, playbook_ids=["pat_1"])
    assert log1.profit_cents == 10000
    assert engine.state.consecutive_profitable_days == 1

    # Day 2: Profitable run -> increments to 2
    engine.stage_5_live_loop(channel="facebook_ads", spend_cents=5000, revenue_cents=15000, playbook_ids=["pat_1"])
    assert engine.state.consecutive_profitable_days == 2

    # 2. Reset on Loss or failure
    # Day 3: Net loss ($100 spend, $40 revenue) -> profit = -$60
    log3 = engine.stage_5_live_loop(channel="facebook_ads", spend_cents=10000, revenue_cents=4000, playbook_ids=["pat_1"])
    assert log3.profit_cents == -6000
    assert engine.state.consecutive_profitable_days == 0  # reset!

    # 3. SLA Auto kill-switch trigger
    # Huge loss ($800 spend, $100 revenue) -> profit = -$700 -> below -$500 threshold
    log4 = engine.stage_5_live_loop(channel="facebook_ads", spend_cents=80000, revenue_cents=10000, playbook_ids=["pat_1"])
    assert log4.profit_cents == -70000
    assert engine.state.channel_kill_switches["facebook_ads"] is False  # Suppressed!

    # Executing on suppressed channel raises error
    with pytest.raises(ValueError, match="is suppressed by kill switch"):
        engine.stage_5_live_loop(channel="facebook_ads", spend_cents=5000, revenue_cents=15000, playbook_ids=["pat_1"])


def test_stage_6_7_attribution_and_feedback():
    """
    Verifies Stage 6 cost-adjusted attribution and Stage 7 pattern re-weighting with forced decay.
    """
    engine = LearnFeedLoopEngine()
    p1 = PlaybookUnit(
        pattern_id="pat_1", pattern="pat", precondition="pre", signal="sig",
        failure_mode="fail", source="src", confidence=0.8, knowledge_type=KnowledgeType.EVERGREEN, half_life_days=30.0
    )
    engine.playbooks["pat_1"] = p1

    # Run log
    log = engine.stage_5_live_loop(channel="google", spend_cents=1000, revenue_cents=4000, playbook_ids=["pat_1"])

    # Stage 6: Attribution
    attributed = engine.stage_6_attribution(log.decision_id, outcome_win=True)
    assert len(attributed) == 1
    assert p1.times_invoked == 1
    assert p1.win_rate == 1.0
    assert p1.avg_revenue_lift == 30.0  # profit ($30.00) / times_invoked

    # Stage 7: Feed Back with forced re-validation decay
    # Backdate playbook last revalidation to 15 days ago
    p1.last_revalidated = datetime.now(timezone.utc) - timedelta(days=15)
    p1.confidence = 0.8

    engine.stage_7_feed_back()
    # Conf should decay because of 15 days gap
    assert p1.confidence < 0.8


def test_stage_8_expansion_triggers():
    """
    Verifies Stage 8 expansion decision rules based on profitable durations.
    """
    engine = LearnFeedLoopEngine()

    # Under-threshold
    engine.state.consecutive_profitable_days = 5
    exp_fail = engine.stage_8_expansion("new_vertical", "fintech")
    assert exp_fail["approved"] is False

    # At-threshold (14 consecutive profitable days)
    engine.state.consecutive_profitable_days = 14
    exp_ok = engine.stage_8_expansion("new_vertical", "fintech")
    assert exp_ok["approved"] is True
    assert exp_ok["action"] == "INITIALIZE_ISOLATED_STAGE_3_CYCLE"
    assert exp_ok["target"] == "fintech"


def test_stage_9_failure_handling_modes():
    """
    Verifies Stage 9 fallbacks for suppressed channels, API failures, and payment locks.
    """
    engine = LearnFeedLoopEngine()

    # 1. Channel suppressed
    res1 = engine.stage_9_failure_handling({"type": "channel_suppressed", "channel": "tiktok"})
    assert res1["action"] == "TRIGGER_KILL_SWITCH"
    assert engine.state.channel_kill_switches["tiktok"] is False

    # 2. API failure
    res2 = engine.stage_9_failure_handling({"type": "api_failure"})
    assert res2["action"] == "PAUSE_LOOP_AND_WAIT"

    # 3. Payment flagged -> freezes capital gates
    assert engine.state.frozen is False
    res3 = engine.stage_9_failure_handling({"type": "payment_flagged"})
    assert res3["action"] == "FREEZE_ALL_CAPITAL"
    assert engine.state.frozen is True
