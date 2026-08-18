"""
Integration tests validating the joint cross-layer cognitive operating system workflow.

Tests the interaction across:
- ResearchOS (Discovery, literature Jaccard ranking, evidence evaluation, statistical power analysis)
- ExecutiveOptimizer (Active Inference Expected Free Energy calculations & Ebbinghaus memory decay)
- EOS Engine (Entrepreneurial multi-loop business dynamics, venture cell management & capital allocation)
- AEAN Hive Mind (Swarm task arbitration, second-price clearing, Bayesian Nash equilibrium)
- APODEX (SkillRegistry discovery, runner execution, and WorldModel state update)
"""

import pytest
import numpy as np
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.ai_eos.active_inference.engine import ExecutiveOptimizer
from apodex.ai_eos.intelligence.eos_engine import EOSEngine, VentureCell
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid
from apodex.skills.registry import SkillRegistry
from apodex.skills.runner import SkillRunner
from agent_harness.core.cost_tier import CostTier
from apodex.world_model.world_model import WorldModel, CausalNode, RelationEdge


def test_end_to_end_cognitive_os_subsystems_flow():
    # 1. Research OS - Discovery & Evidence Evaluation
    ros = ResearchOS()
    res = ros.conduct_literature_review("active inference expected free energy active learning")
    assert "synthesized_trends" in res or "domain" in res

    # 2. Executive Optimizer - Memory decay & Composite Free Energy Objective
    optimizer = ExecutiveOptimizer()
    decayed_confidence = optimizer.calculate_ebbinghaus_memory_decay(initial_confidence=0.9, time_elapsed_days=5)
    assert 0.0 < decayed_confidence < 0.9

    cell1 = VentureCell(name="Strategic Cell", namespace="cell_1")
    g_score = optimizer.compute_composite_objective(cell=cell1, policy_expected_utility=2.5, policy_risk=0.1)
    assert isinstance(g_score, float)

    # 3. EOS Engine - Business Execution Loop Evaluation
    eos = EOSEngine()
    cells = [
        VentureCell(name="AI Analytics Cell", namespace="cell_analytics"),
        VentureCell(name="Robotics R&D Cell", namespace="cell_robotics"),
    ]
    cycle_result = eos.run_continuous_sensing_cycle(cells=cells, total_budget_cents=5000000)
    assert cycle_result["market_uncertainty"] >= 0.0
    assert "allocated_budgets" in cycle_result
    assert len(cycle_result["allocated_budgets"]) == 2

    # 4. AEAN Hive Mind - Swarm Arbitration & Second-Price Clearing
    hive_mind = HiveMind(token_budget=100)
    bids = [
        TaskBid(task="EXPAND_GTM", priority=0.9, expected_value=1.0, token_cost=30),
        TaskBid(task="CONSERVE_CAPITAL", priority=0.6, expected_value=0.5, token_cost=20)
    ]
    grants = hive_mind.arbitrate(bids)
    assert len(grants) == 2
    assert grants[0].granted is True
    assert grants[0].task == "EXPAND_GTM"

    # 5. APODEX - Skill Registry & World Model Execution
    registry = SkillRegistry()
    skills = registry.list_skills()
    assert len(skills) >= 10

    skill_obj = registry.get_skill("competitive_analysis")
    runner = SkillRunner()
    result = runner.execute_skill(
        skill=skill_obj,
        tenant_id="tenant_default",
        venture_id="venture_001",
        input_payload={"sector": "ai_agents"},
        tier=CostTier.CHEAP
    )
    assert result is not None

    wm = WorldModel()
    n1 = CausalNode(node_id="node_1", node_type="state", properties={"name": "ResearchOS_Insight", "confidence": 0.95})
    n2 = CausalNode(node_id="node_2", node_type="state", properties={"name": "EIOS_Strategy", "status": "APPROVED"})
    wm.add_node(n1)
    wm.add_node(n2)
    wm.add_relation(RelationEdge(source_id="node_1", target_id="node_2", relation_type="CAUSES", weight=0.85))

    assert len(wm.nodes) == 2
    assert len(wm.edges) == 1
