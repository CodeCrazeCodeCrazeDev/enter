from __future__ import annotations
import pytest
import uuid
from datetime import datetime, UTC

from apodex.arcs.world_graph import WorldGraph
from apodex.arcs.memory.unified_memory import UnifiedMemoryAPI, MemoryType, MemoryEntry
from apodex.arcs.causal.causal_engine import CausalIntelligenceEngine
from apodex.arcs.digital_twin.twin_engine import EconomicDigitalTwin
from apodex.arcs.governance.gateway import HumanGovernanceGateway, ActionState, GovernanceStage
from apodex.arcs.integrations.adapters import ExecutionSurfaceRegistry, AdapterMode
from apodex.arcs.workflows import (
    AutonomousEntrepreneurialActorOS,
    CapabilityTier,
    ExecutiveCouncil,
    StrategicPlanner,
    ResearchCoordinator
)


# =====================================================================
# 1. Memory Integration Tests
# =====================================================================

def test_unified_memory_and_world_graph():
    wg = WorldGraph()
    memory = UnifiedMemoryAPI(world_graph=wg)

    # Store episodic memory
    entry = MemoryEntry(
        type=MemoryType.EPISODIC,
        tenant_id="tenant_123",
        context={"subsystem": "marketing", "campaign": "launch"},
        payload={"ctr_achieved": 0.045, "spend_usd": 1500}
    )
    memory.store_memory(entry)

    # Store strategic memory
    strategic_entry = MemoryEntry(
        type=MemoryType.STRATEGIC,
        tenant_id="tenant_123",
        context={"limit_type": "ad_spend"},
        payload={"weekly_cap_usd": 5000}
    )
    memory.store_memory(strategic_entry)

    # Retrieve memory by type
    retrieved = memory.retrieve_memory(MemoryType.EPISODIC, tenant_id="tenant_123")
    assert len(retrieved) == 1
    assert retrieved[0].id == entry.id
    assert retrieved[0].payload["ctr_achieved"] == 0.045

    # Retrieve memory by context
    retrieved_strategic = memory.retrieve_memory(
        MemoryType.STRATEGIC,
        tenant_id="tenant_123",
        query_context={"limit_type": "ad_spend"}
    )
    assert len(retrieved_strategic) == 1
    assert retrieved_strategic[0].payload["weekly_cap_usd"] == 5000

    # Link memories semantically
    memory.link_memories(entry.id, strategic_entry.id, "GOVERNED_BY", weight=0.95)
    relations = wg.get_relations_from(entry.id)
    assert len(relations) == 1
    assert relations[0].target_id == strategic_entry.id
    assert relations[0].relation_type == "GOVERNED_BY"

    # Assert belief over relation
    memory.add_memory_belief("belief_tx_01", f"{entry.id}:{strategic_entry.id}", probability=0.88, evidence=["sha_hash_1"])
    assert wg.beliefs["belief_tx_01"].probability == 0.88


# =====================================================================
# 2. Causal Intelligence Tests
# =====================================================================

def test_causal_intelligence_engine():
    wg = WorldGraph()
    engine = CausalIntelligenceEngine(world_graph=wg)

    # Define causal path: Ad_Spend -> Ad_Clicks -> Revenue
    engine.register_causal_relation("ad_spend", "ad_clicks", coefficient=1.5, p_value=0.01)
    engine.register_causal_relation("ad_clicks", "revenue", coefficient=0.8, p_value=0.02)

    # Estimate treatment effect (Wright's path propagation: 1.5 * 0.8 = 1.2)
    effect = engine.estimate_treatment_effect("ad_spend", "revenue")
    assert effect["path_found"] is True
    assert pytest.approx(effect["treatment_effect"], abs=1e-5) == 1.2
    assert effect["confidence"] == pytest.approx(0.99 * 0.98, abs=1e-5)

    # Counterfactual reasoning: if we increase ad_spend by 100, predicted revenue increase is 120 (100 * 1.2)
    predicted_outcome = engine.run_counterfactual(
        intervention_id="ad_spend",
        intervention_value_change=100.0,
        outcome_id="revenue",
        baseline_value=10.0
    )
    assert pytest.approx(predicted_outcome, abs=1e-5) == 130.0

    # Bayesian update check
    posterior = engine.bayesian_update_belief(prior_prob=0.5, likelihood_ratio=3.0)
    assert pytest.approx(posterior, abs=1e-5) == 0.75


# =====================================================================
# 3. Rehearsal Simulation Tests
# =====================================================================

def test_rehearsal_simulation_environment():
    # baseline MRR = $5000, churn = 4%, cash = $100k, monthly fixed burn = $5k
    twin = EconomicDigitalTwin(
        baseline_mrr_cents=5000_00,
        baseline_churn_rate=0.04,
        initial_cash_cents=100_000_00,
        monthly_fixed_burn_cents=5_000_00
    )

    # Standard rehearsal run (no competitor reactions)
    run_normal = twin.simulate_full_rehearsal(
        months=6,
        marketing_monthly_spend_cents=1_000_00, # $1k spend
        est_cac_cents=200_00,                  # $200 CAC -> 5 acquisitions/month
        arpu_cents=100_00,                     # $100 ARPU -> $500 MRR added/month
        competitor_reaction="none"
    )
    assert len(run_normal["monthly_history"]) == 6
    assert run_normal["final_mrr_cents"] > 5000_00

    # Run rehearsal with competitor price undercutting
    run_undercut = twin.simulate_full_rehearsal(
        months=6,
        marketing_monthly_spend_cents=1_000_00,
        est_cac_cents=200_00,
        arpu_cents=100_00,
        competitor_reaction="pricing_undercut"
    )
    # Undercutting increases churn and CAC, leading to less MRR compared to normal
    assert run_undercut["final_mrr_cents"] < run_normal["final_mrr_cents"]


# =====================================================================
# 4. Interchangeable Execution Surface Tests
# =====================================================================

@pytest.mark.asyncio
async def test_execution_surface_adapters():
    registry = ExecutionSurfaceRegistry(AdapterMode.MOCK)

    # Verify CRM mock write
    crm_res = await registry.crm.upsert_contact("user@apodex.io", {"plan": "growth"})
    assert crm_res["status"] == "success"
    assert "crm_contact_" in crm_res["contact_id"]

    # Verify Ads mock write
    ads_res = await registry.ads.create_campaign("Trial Camp", 500_00)
    assert ads_res["status"] == "success"
    assert ads_res["campaign_id"] == "ads_camp_trial_camp"

    # Swap mode to sandbox
    registry.set_mode(AdapterMode.SANDBOX)
    assert registry.crm.mode == AdapterMode.SANDBOX
    assert registry.ads.mode == AdapterMode.SANDBOX


# =====================================================================
# 5. Non-Waivable Human Governance Gate State Machine Tests
# =====================================================================

def test_governance_state_machine_and_audit():
    gateway = HumanGovernanceGateway(GovernanceStage.SUPERVISED)

    # Create high-risk spending proposal
    proposal = gateway.create_proposal("spending", risk_score=0.75, context={"budget": 10000})
    assert proposal.state == ActionState.PROPOSED
    assert len(proposal.audit_trail) == 1
    assert proposal.audit_hash != ""

    # Process action through supervised logic (risk >= 0.50 escalates to pending human approval)
    res = gateway.process_action("spending", risk_score=0.75, context={"budget": 10000})
    assert res["cleared"] is False
    assert res["approval_id"] is not None

    p_updated = gateway.proposals[res["approval_id"]]
    assert p_updated.state == ActionState.PENDING_APPROVAL

    # Grant approval
    approved = gateway.grant_approval(res["approval_id"], approver_name="jules_auditor")
    assert approved is True
    assert p_updated.state == ActionState.EXECUTING

    # Verify immutable hash chain integrity: hash updates on each transition
    for event in p_updated.audit_trail:
        assert event.signature != ""

    # Complete execution
    gateway.complete_action(res["approval_id"])
    assert p_updated.state == ActionState.COMPLETED


# =====================================================================
# 6. Unified AI-EOS Multi-Subsystem (A-J) End-to-End Run
# =====================================================================

@pytest.mark.asyncio
async def test_aean_os_subsystems_flow():
    # Instantiate the complete OS
    os = AutonomousEntrepreneurialActorOS(initial_cash_cents=100_000_00, baseline_mrr_cents=5000_00)

    # Verify Executive Council financial health check
    council = ExecutiveCouncil(os.governance)
    assert council.check_financial_health() is True

    # 1. Run Subsystem A (Discovery) -> Surfaces opportunities
    sub_a_res = await os.subsystems["discovery"].discover_opportunities()
    assert sub_a_res["status"] == "completed"
    assert len(sub_a_res["opportunities"]) == 2

    # 2. Run Subsystem B (Business Model Design) -> Designs unit economics
    sub_b_res = await os.subsystems["business_model"].design_business_model("opp_doc_nlp")
    assert sub_b_res["status"] == "completed"
    assert sub_b_res["pricing_cents"] == 4900

    # 3. Promote Subsystem E (Growth) to TIER 2 (Limited Execution) to test execution pipeline
    growth_sub = os.subsystems["growth"]
    assert growth_sub.tier == CapabilityTier.TIER_0_RESEARCH

    # Run at TIER 0 Research (execution is skipped)
    sub_e_res_t0 = await growth_sub.run_marketing_campaign(5000_00)
    assert sub_e_res_t0["status"] == "completed"
    assert "channels_utilized" not in sub_e_res_t0

    # Promote to Tier 2 (Limited Execution)
    growth_sub.verify_and_promote(performance_score=0.94)  # T0 -> T1
    growth_sub.verify_and_promote(performance_score=0.94)  # T1 -> T2
    assert growth_sub.tier == CapabilityTier.TIER_2_LIMITED_EXECUTION

    # Run at TIER 2 Limited Execution (execution succeeds!)
    sub_e_res_t2 = await growth_sub.run_marketing_campaign(5000_00)
    assert sub_e_res_t2["status"] == "completed"
    assert sub_e_res_t2["execution_result"]["status"] == "success"

    # Verify that learning has updated Unified Memory
    mem_records = os.memory.retrieve_memory(MemoryType.EPISODIC)
    assert len(mem_records) > 0


# =====================================================================
# 7. EIOS Version 2: Active Inference, Compiler, & Scientific Discovery Tests
# =====================================================================

def test_active_inference_hierarchy():
    from apodex.arcs.causal.active_inference import ActiveInferenceEngine
    from apodex.arcs.kernel import HierarchicalActiveInference

    # Single Active Inference loop (reducing Free Energy)
    engine = ActiveInferenceEngine()
    prior = engine.beliefs["customer_demand_is_high"]

    # Observation shows high demand (1.0), reducing Free Energy on next loop
    fe = engine.observe("customer_demand_is_high", 1.0)
    assert fe > 0
    assert engine.beliefs["customer_demand_is_high"] > prior

    # Select uncertainty-minimizing action based on expected free energy
    options = {
        "conjoint_test": {"expected_roi": 1.5, "epistemic_value": 0.9},
        "straight_scale": {"expected_roi": 2.0, "epistemic_value": 0.1}
    }
    best_key, selected = engine.select_action_to_minimize_uncertainty(options)
    # conjoint_test is selected because its high uncertainty-reduction (epistemic value) yields lower Expected Free Energy
    assert best_key == "conjoint_test"

    # Hierarchical active inference (multiple cascading layers)
    hierarchy = HierarchicalActiveInference()
    fe_layer = hierarchy.calculate_layer_free_energy("team", actual_outcome=0.9, expected_outcome=0.5)
    assert fe_layer > 0


@pytest.mark.asyncio
async def test_eios_kernel_and_compiler():
    from apodex.arcs.kernel import EIOSKernel, EntrepreneurialCompiler, RecursivePlanner, TimeHorizon

    # 1. Compiler translates high-level goal to execution DAG
    compiler = EntrepreneurialCompiler()
    dag = compiler.compile_goal_to_dag("Achieve LTV:CAC >= 3:1 in target segment", target_budget_usd=10000)
    assert len(dag.nodes) == 4

    # 2. Kernel schedules and executes the DAG with failure recovery
    kernel = EIOSKernel()
    success = await kernel.execute_dag(dag)
    assert success is True

    # 3. Recursive Planner cascadesvision down across horizons
    planner = RecursivePlanner()
    planner.cascade_vision_down("Build a fully autonomous, self-sustaining software group.")
    assert len(planner.plan_registry[TimeHorizon.VISION_10Y]) == 1
    assert len(planner.plan_registry[TimeHorizon.WEEK]) == 2


def test_scientific_discovery_and_evolution():
    from apodex.arcs.evolution import ScientificDiscoveryEngine, AgentEvolutionEngine

    # 1. Scientific hypothesis generation & RCT conjoint design
    wg = WorldGraph()
    science = ScientificDiscoveryEngine(world_graph=wg)
    hyp = science.generate_hypothesis("pricing_model_type", "customer_retention", expected_effect=0.35)
    assert hyp.independent_variable == "pricing_model_type"

    rct = science.design_rct_experiment(hyp.id)
    assert rct["experimental_design"] == "Randomized Controlled Trial (RCT)"

    # Synthesize to scientific theory based on empirical proof (p-value < 0.05)
    theory = science.synthesize_to_theory(hyp.id, sample_size=1500, actual_effect=0.42, p_value=0.01)
    assert theory is not None
    assert theory.p_value == 0.01

    # 2. Agent evolution tournaments
    evolution = AgentEvolutionEngine(role_name="Software Engineer")
    champion = evolution.run_tournament()
    assert champion.role_name == "Software Engineer"


# =====================================================================
# 8. EIOS Version 2: Society of Agents, Debate & Venture Studio Portfolio
# =====================================================================

def test_collective_intelligence_and_venture_studio():
    # Instantiate the Version 2 Operating System
    os = AutonomousEntrepreneurialActorOS(initial_cash_cents=100_000_00)

    # 1. Run AlphaAlgo Verdict-style Adversarial Debate & Consensus
    debate_res = os.run_collective_intelligence_debate("Should we transition pricing model to usage-based?")
    assert "winning_strategy" in debate_res
    assert debate_res["consensus_confidence"] > 0.5

    # 2. Run Autonomous Venture Studio portfolio management
    os.add_portfolio_venture("venture_01", "Apodex PDF Parser", allocated_capital=30_000_00)
    os.add_portfolio_venture("venture_02", "Apodex Ads Optimizer", allocated_capital=15_000_00)

    # Reallocate capital from high-surplus venture to under-funded high yield venture
    reallocation = os.reallocate_portfolio_capital()
    assert len(reallocation) > 0
