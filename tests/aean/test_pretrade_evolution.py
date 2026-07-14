"""Tests for the Pre-Trade Validation Engine and the Governed Cognitive
Evolution System (three-layer framework)."""
from __future__ import annotations

import random

from apodex.aean import (
    ArchitectureEvolution,
    CapabilityEvolution,
    ConstitutionalFilter,
    ConstitutionalRules,
    GovernedCognitiveEvolutionSystem,
    ObjectiveStability,
    Organism,
    PreTradeValidationEngine,
)
from apodex.aean.evolution.three_layer import _default_fitness
from apodex.aean.models import DemandSignal, PipelineStage, StrategyGenome


def _signal(strength: float, tam: int, keywords=None) -> DemandSignal:
    return DemandSignal(
        market="devtools",
        segment="startups",
        strength=strength,
        estimated_tam_cents=tam,
        elasticity=-1.5,
        keywords=keywords or ["search_velocity", "social_momentum"],
    )


# ---------------------------------------------------------------------------
# Pre-Trade Validation Engine
# ---------------------------------------------------------------------------
def test_pretrade_passes_strong_cheap_uncontested_signal():
    engine = PreTradeValidationEngine(rng=random.Random(0))
    result = engine.assess(_signal(0.8, 150_000_000))
    assert result.gate_passed
    assert result.sim_passed
    assert result.counterfactual_passed
    assert result.passed
    assert len(result.pillars) == 4


def test_pretrade_gate_rejects_tiny_market_without_simulation():
    engine = PreTradeValidationEngine(rng=random.Random(0))
    result = engine.assess(_signal(0.5, 6_000_000))  # TAM below floor.
    assert not result.gate_passed
    assert not result.passed
    # Rejected without simulation: no Monte-Carlo stats were computed.
    assert result.sim_mean == 0.0
    assert any(p.name == "demand_size" and not p.passed for p in result.pillars)
    assert engine.stats()["gate_rejections"] == 1


def test_pretrade_gate_rejects_crowded_low_conviction_signal():
    engine = PreTradeValidationEngine(rng=random.Random(0))
    result = engine.assess(_signal(0.4, 100_000_000, keywords=["competitor_move", "social_momentum"]))
    assert not result.gate_passed
    assert not result.passed


def test_pretrade_counterfactual_can_reject_non_discriminatory_thesis():
    # An impossible divergence bar forces the opposite-narrative probe to fail
    # even for a signal that clears the gate and the synthetic test.
    engine = PreTradeValidationEngine(rng=random.Random(0), min_divergence=5.0)
    result = engine.assess(_signal(0.8, 150_000_000))
    assert result.gate_passed and result.sim_passed
    assert not result.discriminatory
    assert not result.counterfactual_passed
    assert not result.passed
    assert engine.stats()["counterfactual_rejections"] == 1


def test_pretrade_is_deterministic():
    a = PreTradeValidationEngine(rng=random.Random(42)).assess(_signal(0.7, 120_000_000))
    b = PreTradeValidationEngine(rng=random.Random(42)).assess(_signal(0.7, 120_000_000))
    assert a.sim_p05 == b.sim_p05
    assert a.sim_mean == b.sim_mean


# ---------------------------------------------------------------------------
# Layer 3 — Objective Stability
# ---------------------------------------------------------------------------
def test_objective_blocks_genome_exceeding_risk_control():
    obj = ObjectiveStability(ConstitutionalFilter())
    ok, reasons = obj.permits_genome(StrategyGenome(allocation_pct=0.90))
    assert not ok and reasons
    assert obj.permits_genome(StrategyGenome(allocation_pct=0.20))[0]


def test_objective_enforces_five_prohibitions():
    obj = ObjectiveStability(ConstitutionalFilter())
    assert not obj.permits_change({"risk_controls": "loosen"})[0]
    assert not obj.permits_change({"rewrite_live_logic": True})[0]
    assert not obj.permits_change({"contaminated_labels": True})[0]
    assert not obj.permits_change({"benchmark_delta": 0.2, "samples": 100})[0]
    assert obj.permits_change({"benchmark_delta": 0.2, "samples": 20_000})[0]


# ---------------------------------------------------------------------------
# Layer 1 — Capability Evolution
# ---------------------------------------------------------------------------
def test_capability_evolution_improves_suboptimal_incumbent():
    obj = ObjectiveStability(ConstitutionalFilter())
    evo = CapabilityEvolution(obj, rng=random.Random(0))
    incumbent = StrategyGenome(allocation_pct=0.10, exploration=0.90, diversification=0.10, patience=0.20)
    champion, result = evo.evolve(incumbent, generations=6)
    assert result.champion_fitness >= result.incumbent_fitness
    assert result.promoted
    assert result.champion_fitness == _default_fitness(champion)
    # Genes stay within bounds.
    for value in champion.model_dump().values():
        assert 0.0 <= value <= 1.0


def test_capability_evolution_respects_objective_bound():
    # A tight allocation cap forces Layer 3 to reject many mutated genomes.
    gov = ConstitutionalFilter(ConstitutionalRules(max_single_allocation_pct=0.12))
    obj = ObjectiveStability(gov)
    evo = CapabilityEvolution(obj, rng=random.Random(0))
    _, result = evo.evolve(StrategyGenome(allocation_pct=0.10), generations=6)
    assert result.rejected_by_objective > 0


# ---------------------------------------------------------------------------
# Layer 2 — Architecture Evolution (seven-stage pipeline)
# ---------------------------------------------------------------------------
def _valid_candidate() -> dict:
    return {
        "name": "research-critic-simulation-execution",
        "boots": True,
        "benchmark_delta": 0.28,
        "stress_ok": True,
        "security_ok": True,
        "cost_quality_ok": True,
        "canary_divergence_ok": True,
        "samples": 12_000,
        "scale_ok": True,
    }


def test_architecture_pipeline_promotes_valid_candidate():
    arch = ArchitectureEvolution(ObjectiveStability(ConstitutionalFilter()))
    result = arch.evaluate(_valid_candidate())
    assert result.promoted
    assert result.stage_reached == PipelineStage.SCALE
    assert [s.stage for s in result.stages] == list(ArchitectureEvolution._ORDER)


def test_architecture_pipeline_halts_on_no_improvement():
    arch = ArchitectureEvolution(ObjectiveStability(ConstitutionalFilter()))
    candidate = _valid_candidate()
    candidate["benchmark_delta"] = 0.0  # Different, not better.
    result = arch.evaluate(candidate)
    assert not result.promoted
    assert result.stage_reached == PipelineStage.BENCHMARK


def test_architecture_tiny_sample_rejected_at_compatibility_validation():
    # "Never promote on tiny sample wins" is a Layer-3 prohibition, so a
    # candidate with < 10k samples is rejected before it enters the sandbox.
    arch = ArchitectureEvolution(ObjectiveStability(ConstitutionalFilter()))
    candidate = _valid_candidate()
    candidate["samples"] = 100
    result = arch.evaluate(candidate)
    assert not result.promoted
    assert result.rejected_by_objective
    assert result.stages == []


def test_architecture_pipeline_halts_on_canary_divergence():
    arch = ArchitectureEvolution(ObjectiveStability(ConstitutionalFilter()))
    candidate = _valid_candidate()
    candidate["canary_divergence_ok"] = False  # Live-output drift out of bounds.
    result = arch.evaluate(candidate)
    assert not result.promoted
    assert result.stage_reached == PipelineStage.CANARY


def test_architecture_rejected_by_objective_before_sandbox():
    arch = ArchitectureEvolution(ObjectiveStability(ConstitutionalFilter()))
    candidate = _valid_candidate()
    candidate["capital_limits"] = "raise"
    result = arch.evaluate(candidate)
    assert result.rejected_by_objective
    assert not result.promoted
    assert result.stages == []  # Never consumed sandbox resources.


# ---------------------------------------------------------------------------
# Composed system + organism wiring
# ---------------------------------------------------------------------------
def test_gces_promotes_and_updates_incumbent():
    gces = GovernedCognitiveEvolutionSystem(ConstitutionalFilter(), rng=random.Random(0))
    before = gces.incumbent.model_copy()
    result = gces.evolve_capability()
    if result.promoted:
        assert gces.incumbent != before
        assert gces.capability_promotions == 1
    arch = gces.evaluate_architecture(_valid_candidate())
    assert arch.promoted
    stats = gces.stats()
    assert {"capability_rounds", "architecture_promotions", "objective_rejections"} <= stats.keys()


def test_organism_snapshot_exposes_pretrade_and_evolution():
    o = Organism(initial_capital_cents=100_000_00, seed=7)
    o.run(20)
    snap = o.snapshot()
    assert "pretrade" in snap["validation"]
    assert "evolution" in snap
    ekg = snap["ekg"]
    # The pre-trade gate is load-bearing: it assesses signals and rejects some
    # while still letting viable ones through to become cells.
    assert ekg["pretrade_assessments"] > 0
    assert 0 < ekg["pretrade_passed"] < ekg["pretrade_assessments"]
    assert ekg["cells"] > 0
    assert ekg["capability_evolutions"] > 0


def test_organism_still_deterministic_with_new_subsystems():
    a = Organism(initial_capital_cents=100_000_00, seed=7)
    b = Organism(initial_capital_cents=100_000_00, seed=7)
    a.run(15)
    b.run(15)
    assert a.snapshot()["net_worth_cents"] == b.snapshot()["net_worth_cents"]
    assert a.snapshot()["evolution"]["incumbent"] == b.snapshot()["evolution"]["incumbent"]
