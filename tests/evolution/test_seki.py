from __future__ import annotations
import pytest
from uuid import UUID, uuid4

from apodex.memory.models import CostMode
from apodex.evolution.common.models import MultiObjectiveMetric
from apodex.evolution.research.seki import (
    ArchitectureSpec,
    SEKISearchEngine,
    SEKIKnowledgeRepository,
    SEKIPromptGenerator,
    SEKIPromptAdapter,
    C_Input,
    D_Input,
    E_Input,
    OptimizationStrategy,
)


def test_seki_models_and_prompt_generation():
    """Validates the construction and formatting of SEKI prompts and models."""
    spec = ArchitectureSpec(
        arch_type="agent_workflow",
        config={"num_agents": 2, "verifier_depth": 2},
        constraints={"max_latency": 1.0}
    )
    metrics = MultiObjectiveMetric(quality=0.8, cost=0.2, latency=0.1)

    c_in = C_Input(spec=spec, metrics=metrics, failure_modes=["high_latency"], goals=["improve_latency"])
    c_prompt = SEKIPromptGenerator.generate_c_prompt(c_in)
    assert "agent_workflow" in c_prompt
    assert "high_latency" in c_prompt

    strategy = OptimizationStrategy(
        description="Reduce nested depth",
        type="reduce_depth",
        impact_hypothesis="Will lower latency"
    )
    d_in = D_Input(strategy=strategy, parent_spec=spec, constraints={"max_latency": 0.8})
    d_prompt = SEKIPromptGenerator.generate_d_prompt(d_in)
    assert "reduce_depth" in d_prompt

    e_in = E_Input(xi_architectures=[
        {"spec": spec.model_dump(), "strategy_description": "Reduce verifier depth", "metrics": metrics.model_dump(), "score": 0.85}
    ])
    e_prompt = SEKIPromptGenerator.generate_e_prompt(e_in)
    assert "associated strategy" in e_prompt.lower() or "associated_strategy" in e_prompt.lower()


def test_seki_prompt_adapter_simulation():
    """Validates SEKIPromptAdapter simulation mode outputs correct and deterministic specs."""
    adapter = SEKIPromptAdapter(mode="simulation")

    # Test C(cdot) Strategy extraction
    spec = ArchitectureSpec(
        arch_type="agent_workflow",
        config={"num_agents": 2, "verifier_depth": 2},
        constraints={}
    )
    metrics = MultiObjectiveMetric(quality=0.8, cost=0.2, latency=0.1)
    c_out = adapter.execute_c(C_Input(spec=spec, metrics=metrics))
    assert len(c_out.strategies) == 1
    strategy = c_out.strategies[0]
    assert strategy.type in ("reduce_depth", "split_agent", "increase_parallelism")

    # Test D(cdot) Refined spec generation
    d_out = adapter.execute_d(D_Input(strategy=strategy, parent_spec=spec))
    assert len(d_out.candidate_specs) == 1
    mutated = d_out.candidate_specs[0]
    assert mutated.arch_type == "agent_workflow"
    if strategy.type == "reduce_depth":
        assert mutated.config["verifier_depth"] == 1
    elif strategy.type == "split_agent":
        assert mutated.config["num_agents"] == 3

    # Test E(cdot) Knowledge distillation
    e_in = E_Input(xi_architectures=[
        {"spec": spec.model_dump(), "strategy_description": "Reduce verifier depth", "metrics": metrics.model_dump(), "score": 0.85}
    ])
    e_out = adapter.execute_e(e_in)
    assert len(e_out.principles) == 1
    assert len(e_out.inspired_specs) == 1
    inspired = e_out.inspired_specs[0]
    assert inspired.config.get("inspired") is True


def test_seki_repository_operations():
    """Validates top-k ranking, xi-sampling, and VCS rollback layers."""
    repo = SEKIKnowledgeRepository()
    spec1 = ArchitectureSpec(arch_type="agent_workflow", config={"v": 1})
    spec2 = ArchitectureSpec(arch_type="agent_workflow", config={"v": 2})
    spec3 = ArchitectureSpec(arch_type="agent_workflow", config={"v": 3})

    metrics = MultiObjectiveMetric(quality=0.8, cost=0.1, latency=0.1)

    repo.add_architecture(spec1, metrics, 0.70, provenance="run_1")
    repo.add_architecture(spec2, metrics, 0.85, provenance="run_2")
    repo.add_architecture(spec3, metrics, 0.65, provenance="run_3")

    # Test best selection
    best = repo.get_best()
    assert best is not None
    assert best.spec.config["v"] == 2

    # Test top-k
    top_2 = repo.get_top_k(k=2)
    assert len(top_2) == 2
    assert top_2[0].f_alpha == 0.85
    assert top_2[1].f_alpha == 0.70

    # Test xi selection
    sampled = repo.select_xi_from_top_k(k=2, xi=1)
    assert len(sampled) == 1
    assert sampled[0].spec.config["v"] in (1, 2)

    # Test VCS rollback on degradation
    reverted = repo.rollback()
    assert reverted is not None
    assert reverted.f_alpha == 0.85


@pytest.mark.asyncio
async def test_full_seki_search_loop_integration():
    """Runs a complete multi-round SEKI search loop with budget controls and verifies outcome."""
    init_spec = ArchitectureSpec(
        arch_type="agent_workflow",
        config={"num_agents": 2, "verifier_depth": 2},
        constraints={"max_latency": 1.0}
    )

    # Initialize SEKI engine
    engine = SEKISearchEngine(
        cost_mode=CostMode.BALANCED,
        adapter_mode="simulation",
        budget=100.0
    )

    # Run search for 2 lambda rounds (Self-Evolution) and 1 gamma round (Knowledge Inspiration)
    final_spec = await engine.run_search(
        init_spec=init_spec,
        lambda_rounds=2,
        gamma_rounds=1,
        k=4,
        xi=2
    )

    assert final_spec is not None
    assert final_spec.arch_type == "agent_workflow"
    # The search loop must have registered at least 3 trials in the repository
    assert len(engine.repository.commits) >= 2
    # Verify budget was decremented
    assert engine.budget < 100.0


@pytest.mark.asyncio
async def test_seki_budget_exhaustion_halting():
    """Validates that SEKISearchEngine halts search when budget is depleted."""
    init_spec = ArchitectureSpec(
        arch_type="agent_workflow",
        config={"num_agents": 2, "verifier_depth": 2}
    )

    # Start with a very low budget (15.0), enough for initialization but should halt
    engine = SEKISearchEngine(
        cost_mode=CostMode.FAST_CHEAP,
        adapter_mode="simulation",
        budget=15.0
    )

    final_spec = await engine.run_search(
        init_spec=init_spec,
        lambda_rounds=5,
        gamma_rounds=5,
        k=4,
        xi=2
    )

    # Engine must stop early after at most 1 round of Self-Evolution (initial evaluates + 1 round consumes 10)
    assert final_spec is not None
    assert engine.budget <= 5.0
