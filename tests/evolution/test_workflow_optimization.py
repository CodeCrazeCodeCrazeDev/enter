from __future__ import annotations
import pytest
from apodex.evolution.common.models import CostMode
from apodex.evolution.harness_loop.optimizers import WorkflowConfig, WorkflowEvolutionSearch


def test_workflow_evolution_search():
    """
    Verifies that WorkflowEvolutionSearch runs its generational population and selects
    a config with high fitness.
    """
    searcher = WorkflowEvolutionSearch()
    initial_config = WorkflowConfig(
        workflow_id="wf_01",
        nodes=["agent_react"],
        has_verification_step=False,
        max_samples=1,
        tool_threshold=0.5
    )

    available_agents = ["agent_react", "agent_critic", "agent_verifier"]

    # Run evolution search under max_quality -> should favor adding verification and samples
    fittest_max_quality = searcher.run_evolution_search(
        initial_config,
        available_agents,
        CostMode.MAX_QUALITY,
        generations=3,
        population_size=4
    )

    assert fittest_max_quality is not None
    # Let's assert that the quality is high, which usually means it evolved toward better features
    fitness_mq = searcher.calculate_fitness(fittest_max_quality, CostMode.MAX_QUALITY)
    fitness_initial = searcher.calculate_fitness(initial_config, CostMode.MAX_QUALITY)
    assert fitness_mq >= fitness_initial


def test_workflow_cost_gating_behavior():
    """
    Confirms that in FAST_CHEAP mode, an expensive workflow configuration has a lower fitness
    than a cheap, simple workflow config.
    """
    searcher = WorkflowEvolutionSearch()

    cheap_config = WorkflowConfig(
        workflow_id="wf_cheap",
        nodes=["agent_react"],
        has_verification_step=False,
        max_samples=1,
        tool_threshold=0.5
    )

    expensive_config = WorkflowConfig(
        workflow_id="wf_expensive",
        nodes=["agent_react", "agent_critic", "agent_verifier"],
        has_verification_step=True,
        max_samples=3,
        tool_threshold=0.5
    )

    # 1. Under FAST_CHEAP, simple/cheap configuration must have higher fitness
    fitness_cheap_fc = searcher.calculate_fitness(cheap_config, CostMode.FAST_CHEAP)
    fitness_expensive_fc = searcher.calculate_fitness(expensive_config, CostMode.FAST_CHEAP)
    assert fitness_cheap_fc > fitness_expensive_fc

    # 2. Under MAX_QUALITY, expensive (but higher quality) configuration has higher fitness
    fitness_cheap_mq = searcher.calculate_fitness(cheap_config, CostMode.MAX_QUALITY)
    fitness_expensive_mq = searcher.calculate_fitness(expensive_config, CostMode.MAX_QUALITY)
    assert fitness_expensive_mq > fitness_cheap_mq
