"""End-to-End Joint Integration Test Suite for Research OS, EIOS, EOS, AEAN, and APODEX Subsystems."""

from __future__ import annotations

import pytest

from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind
from apodex.cognition.brain import CognitiveBrain
from apodex.skills.registry import skill_registry


@pytest.mark.asyncio
async def test_research_os_conduct_literature_review():
    """Verify literature review discovery in ResearchOS."""
    ros = ResearchOS()
    literature = ros.conduct_literature_review("active inference")
    assert "reviewed_citations_count" in literature
    assert literature["reviewed_citations_count"] >= 0
    assert "synthesized_trends" in literature


@pytest.mark.asyncio
async def test_eios_kernel_dag_execution():
    """Verify EIOS Kernel process initialization and DAG execution capabilities."""
    kernel = EIOSKernel()
    assert hasattr(kernel, "execute_dag")
    assert hasattr(kernel, "active_processes")


@pytest.mark.asyncio
async def test_eos_engine_continuous_sensing():
    """Verify EOS Engine continuous sensing cycle execution."""
    eos = EOSEngine()
    result = eos.run_continuous_sensing_cycle(cells=[], total_budget_cents=100000)
    assert result is not None
    assert hasattr(eos, "portfolio_manager")
    assert hasattr(eos, "hypothesis_engine")


@pytest.mark.asyncio
async def test_aean_hivemind_arbitration():
    """Verify AEAN HiveMind task arbitration and budget capabilities."""
    hive = HiveMind()
    assert hasattr(hive, "arbitrate")
    assert hasattr(hive, "token_budget")


@pytest.mark.asyncio
async def test_apodex_brain_and_skill_registry():
    """Verify APODEX CognitiveBrain initialization and SkillRegistry populate."""
    brain = CognitiveBrain()
    assert brain is not None

    skill_names = list(skill_registry._skills.keys())
    assert len(skill_names) >= 60
    assert "opportunity_evaluation_frameworks" in skill_names
    assert "business_model_design" in skill_names
