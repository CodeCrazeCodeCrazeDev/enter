from __future__ import annotations
import uuid
import pytest

from apodex.memory.models import CostMode, ScenarioPattern
from apodex.memory.services import TencentDBMemoryStore
from apodex.safety.core import ImmutableSafetyCore, RiskTier
from apodex.evolution.research.ticket import ResearchTicketManager, ResearchAgent
from apodex.evolution.research.search import SandboxExperimentRunner, ArchitectureSearchEngine
from apodex.evolution.research.promote import CapabilityDeltaLog, ResearchPromotionPipeline


@pytest.mark.asyncio
async def test_full_research_loop_integration():
    """
    Validates end-to-end slow research loop:
    1. Scan scenarios to identify weaknesses -> create Research Tickets.
    2. Propose Architecture Candidates.
    3. Run evolutionary search using isolated Cube Sandbox evaluations.
    4. Promote candidates through tiered safety approvals and record Capability Deltas.
    """
    # Initialize Memory Store
    db = TencentDBMemoryStore()
    tenant_id = "org_zeta"
    user_id = "user_omega"

    # Seed T3 Scenarios with low success rate (e.g. 75%) to trigger ticket creation
    scenario_id = uuid.uuid4()
    scen = ScenarioPattern(
        scenario_id=scenario_id,
        tenant_id=tenant_id,
        name="Adversarial Pen-Testing Workflow",
        pattern_type="adversarial_fuzzing",
        typical_workflow=["main_agent"],
        success_rate=0.75,
        average_latency_ms=1500.0,
        average_token_cost=8000
    )
    db.scenarios[scenario_id] = scen

    # 1. Research Ticket Management (Scan & Mine)
    ticket_mgr = ResearchTicketManager(tencent_db=db)
    tickets = ticket_mgr.scan_for_weaknesses(tenant_id=tenant_id)

    assert len(tickets) == 1
    assert "Adversarial Pen-Testing Workflow" in tickets[0].title
    assert tickets[0].priority == 2

    # 2. Research Agent Candidate Proposal
    safety = ImmutableSafetyCore()
    agent = ResearchAgent(safety_core=safety)

    # Propose low risk change (Tier 1)
    cand_t1 = agent.propose_candidate(tickets[0], "Prompt Wording Optimization", "Slight phrasing refinement.")
    assert cand_t1.risk_tier == RiskTier.TIER_1_LOW

    # Propose medium risk change (Tier 2)
    cand_t2 = agent.propose_candidate(tickets[0], "Topology Addition of Parallel Verifier", "Adding verifier role.")
    assert cand_t2.risk_tier == RiskTier.TIER_2_MEDIUM

    # Propose high risk change (Tier 3)
    cand_t3 = agent.propose_candidate(tickets[0], "Upgrade to Claude-3-5-Sonnet Model", "Swap core LLM family.")
    assert cand_t3.risk_tier == RiskTier.TIER_3_HIGH
    assert "model_family" in cand_t3.model_configuration

    # 3. Architecture Search & Sandbox Evaluation
    runner = SandboxExperimentRunner()
    search_engine = ArchitectureSearchEngine(sandbox_runner=runner)

    # Evaluate Tier 2 candidate
    eval_t2 = await runner.run_sandbox_eval(cand_t2, CostMode.BALANCED)
    assert eval_t2.is_stable is True
    assert eval_t2.quality_score > 0.65

    # Run evolutionary search over base candidate
    best_eval = await search_engine.search_best_architecture(
        tickets[0].ticket_id,
        cand_t2,
        CostMode.MAX_QUALITY,
        generations=2
    )
    assert best_eval is not None
    assert best_eval.quality_score >= 0.7

    # 4. Staged Promotion & Capability Delta Tracking
    delta_log = CapabilityDeltaLog(tencent_db=db)
    pipeline = ResearchPromotionPipeline(safety_core=safety, delta_log=delta_log)

    # Promote Tier 1 -> Auto Promote
    res_p1 = await pipeline.promote_candidate(tenant_id, user_id, cand_t1, best_eval, CostMode.BALANCED)
    assert res_p1["status"] == "auto_promoted"
    assert len(pipeline.approved_deltas) == 1

    # Promote Tier 2 -> Sandbox Shadow Test
    res_p2 = await pipeline.promote_candidate(tenant_id, user_id, cand_t2, best_eval, CostMode.BALANCED)
    assert res_p2["status"] == "shadow_tested"
    assert len(pipeline.approved_deltas) == 2

    # Promote Tier 3 -> Staged for human review
    res_p3 = await pipeline.promote_candidate(tenant_id, user_id, cand_t3, best_eval, CostMode.BALANCED)
    assert res_p3["status"] == "staged_for_manual_approval"
    assert cand_t3.candidate_id in pipeline.staged_candidates

    # Human-override execution (Approved)
    res_manual = pipeline.execute_manual_promotion(cand_t3.candidate_id, tenant_id, best_eval, approved=True)
    assert res_manual["status"] == "manually_promoted"
    assert len(pipeline.approved_deltas) == 3
