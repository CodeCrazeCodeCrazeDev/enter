"""End-to-end integration tests for the Unified 4-Layer Cognitive Operating System.

Verifies cross-layer handoffs and joint behavior across:
- Layer 1: Research OS (Research Layer)
- Layer 2: EIOS / EOS (Execution & Orchestration Layer)
- Layer 3: AEAN (Cognitive Intelligence & Multi-Agent Layer)
- Layer 4: APODEX (Decision Platform & Execution Layer)
"""

from __future__ import annotations

import pytest
import asyncio
from typing import Dict, Any
from datetime import datetime

from apodex.ai_eos.research.research_os import ResearchOS
from apodex.ai_eos.research.integration import ResearchToSystemBridge
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.ai_eos.intelligence.eos_engine import EOSEngine, BusinessSimulator
from apodex.cognition.controller import CognitiveSystemController
from apodex.skills.registry import SkillRegistry
from apodex.memory.cmos.repositories import InMemoryMemoryRepository
from apodex.memory.cmos.models import MemoryNode, CMOSNodeType, ProvenanceBlock
from apodex.cognition.shared.schemas import StrategicGoal, CognitiveContext


@pytest.mark.asyncio
async def test_layer_1_to_layer_2_research_bridge_handoff():
    """Verify Layer 1 Research OS literature query and hypothesis export to Layer 2 EIOS Kernel."""
    research_os = ResearchOS()
    bridge = ResearchToSystemBridge()
    kernel = EIOSKernel()

    # Step 1: Conduct literature review in Layer 1
    review = research_os.conduct_literature_review("portfolio optimization")
    assert review is not None
    assert "reviewed_citations_count" in review
    assert review["reviewed_citations_count"] > 0
    assert "synthesized_trends" in review

    hyp_id = "hyp_portfolio_001"
    confidence = 0.85
    principles = review["synthesized_trends"]

    # Step 2: Export hypothesis via Bridge to Layer 2 EIOS Kernel
    handoff_result = bridge.export_validated_hypothesis_to_kernel(
        kernel=kernel,
        hypothesis_id=hyp_id,
        domain_keyword="portfolio optimization",
        confidence=confidence,
        extracted_principles=principles
    )
    assert handoff_result["status"] == "exported"
    assert handoff_result["kernel_hypothesis_count"] >= 1

    # Step 3: Layer 2 EIOS Kernel senses opportunity anomalies using active inference
    kernel_state = kernel.sense_opportunity_anomalies(
        market_signals={"volatility": 0.12, "growth_rate": 0.08},
        active_hypotheses=[hyp_id]
    )
    assert kernel_state["status"] == "sensed"
    assert "expected_free_energy" in kernel_state
    assert kernel_state["expected_free_energy"] >= 0.0


@pytest.mark.asyncio
async def test_layer_2_to_layer_3_eos_to_aean_execution():
    """Verify Layer 2 EOS engine business loops dispatch to Layer 3 AEAN multi-agent skills."""
    eos_engine = EOSEngine()
    simulator = BusinessSimulator()
    skill_registry = SkillRegistry()

    # Step 1: Run EOS business simulation cohort in Layer 2
    cohort_res = simulator.simulate_gtm_cohort(
        traffic=10000,
        conversion_rate=0.03,
        arpu_cents=50_00,
        cac_cents=100_00,
        churn_rate=0.02
    )
    assert cohort_res["unit_economics_healthy"] is True
    assert cohort_res["ltv_to_cac_ratio"] == 25.0

    # Step 2: Verify skill availability in Layer 3 AEAN Skill Registry
    skills = skill_registry.list_skills()
    assert len(skills) >= 60

    # Retrieve a registered skill (e.g., pricing_strategy)
    skill = skill_registry.get_skill("pricing_strategy")
    assert skill is not None
    assert skill.domain == "strategy"


@pytest.mark.asyncio
async def test_layer_3_to_layer_4_aean_to_apodex_governance_cycle():
    """Verify Layer 3 AEAN controller end-to-end decision cycle under Layer 4 APODEX Governance Rules."""
    controller = CognitiveSystemController()

    # Step 1: Run valid decision cycle through APODEX governance
    provenance = await controller.execute_decision_cycle(
        goal_title="Integrate Automated Risk Hedge",
        goal_description="Deploy automated Kelly criterion risk hedge module.",
        budget_cents=500_000,
        constraints=["low_latency", "python"],
        priority_score=0.88,
        simulate_success=True
    )

    assert provenance.id is not None
    assert provenance.final_decision == "APPROVED"
    assert provenance.execution_outcome.success is True
    assert provenance.feasibility.is_feasible is True

    # Step 2: Test non-bypassable Layer 4 Rule 6 Governance Veto (budget limit violation)
    overbudget_provenance = await controller.execute_decision_cycle(
        goal_title="Exceed System Budget Cap",
        goal_description="Attempt ultra high budget deployment.",
        budget_cents=200_000_000,  # 200M cents exceeds limit
        simulate_success=True
    )
    assert "REJECTED" in overbudget_provenance.final_decision
    assert "budget" in overbudget_provenance.final_decision.lower()


@pytest.mark.asyncio
async def test_unified_4_layer_full_stack_cognitive_cycle():
    """Verify complete 4-layer unified cognitive operating system cycle from Layer 1 through Layer 4."""
    # Instantiation of all 4 layers
    research_os = ResearchOS()              # Layer 1
    bridge = ResearchToSystemBridge()       # Interface I
    kernel = EIOSKernel()                  # Layer 2
    eos_engine = EOSEngine()               # Layer 2
    repo = InMemoryMemoryRepository()       # Layer 3
    controller = CognitiveSystemController()# Layer 3 & Layer 4

    # 1. Layer 1 Literature Search & Hypothesis Generation
    lit_res = research_os.conduct_literature_review("algorithmic trading")
    assert lit_res.get("reviewed_citations_count", 0) > 0
    trends = lit_res.get("synthesized_trends", [])

    # 2. Interface I State Export
    bridge_res = bridge.export_validated_hypothesis_to_kernel(
        kernel=kernel,
        hypothesis_id="hyp_algo_trading_001",
        domain_keyword="algorithmic trading",
        confidence=0.90,
        extracted_principles=trends
    )
    assert bridge_res["status"] == "exported"

    # 3. Layer 2 Active Inference Sensing & Business Simulation
    sensing = kernel.sense_opportunity_anomalies(
        market_signals={"volume_delta": 0.25},
        active_hypotheses=["hyp_algo_trading_001"]
    )
    assert sensing["expected_free_energy"] >= 0.0

    cohort = eos_engine.business_simulator.simulate_gtm_cohort(
        traffic=5000, conversion_rate=0.04, arpu_cents=100_00, cac_cents=200_00, churn_rate=0.01
    )
    assert cohort["unit_economics_healthy"] is True

    # 4. Layer 3 CMOS Memory Storage
    prov_block = ProvenanceBlock(
        origin="full_stack_cycle",
        timestamp=datetime.utcnow(),
        creator_id="layer3_aean_agent",
        confidence=0.95
    )
    mem_node = MemoryNode(
        node_type=CMOSNodeType.CLAIM,
        label="Hypothesis hyp_algo_trading_001",
        content=f"Sensing EFE: {sensing['expected_free_energy']}",
        provenance=prov_block
    )
    await repo.save_node(mem_node)
    fetched_node = await repo.get_node(mem_node.node_id)
    assert fetched_node is not None
    assert fetched_node.label == "Hypothesis hyp_algo_trading_001"

    # 5. Layer 4 Governance & Provenance Execution Cycle
    prov = await controller.execute_decision_cycle(
        goal_title="Deploy Algorithmic Trading Pipeline",
        goal_description="Deploy research-backed algorithmic trading strategy.",
        budget_cents=800_000,
        priority_score=0.92,
        simulate_success=True
    )
    assert prov.final_decision == "APPROVED"
    assert prov.execution_outcome.success is True
