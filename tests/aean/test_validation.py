"""Tests for the AEAN reality & validation systems (Part II).

Covers the RGAE three-layer pipeline + TRIBEv2 perception/calibration, the
Three-Critic Stack, and the epistemic firewall, plus their wiring into the EKG
and the organism flywheel.
"""
from __future__ import annotations

import random

from apodex.aean import (
    CalibrationLayer,
    ConstitutionalFilter,
    EconomicKnowledgeGraph,
    EpistemicFirewall,
    Organism,
    PerceptionPredictor,
    RealityGroundedAdaptiveEngine,
    ThreeCriticStack,
)
from apodex.aean.models import (
    CriticName,
    DemandSignal,
    MicroCell,
    Narrative,
    PerceptionScore,
    ValidationStage,
    VisualAsset,
)


def _signal(strength: float = 0.7) -> DemandSignal:
    return DemandSignal(
        market="devtools",
        segment="startups",
        strength=strength,
        estimated_tam_cents=200_000_000,
        elasticity=-1.5,
        keywords=["search_velocity", "social_momentum"],
    )


def _narrative(signal_id: str, resonance: float = 0.8) -> Narrative:
    return Narrative(
        signal_id=signal_id, theme="t", hook="honest hook", body="clear value", predicted_resonance=resonance
    )


def _assets(narrative_id: str, n: int = 4, ctr: float = 0.06) -> list[VisualAsset]:
    concepts = ["bold_typographic", "product_hero", "minimal_brand", "data_visual"]
    return [
        VisualAsset(
            narrative_id=narrative_id,
            concept=concepts[i % len(concepts)],
            format="story_vertical",
            predicted_ctr=ctr,
            prompt=f"variant {i}",
        )
        for i in range(n)
    ]


# ---------------------------------------------------------------------------
# TRIBEv2 perception + calibration
# ---------------------------------------------------------------------------
def test_perception_dimensions_are_bounded_and_deterministic():
    sig = _signal()
    nar = _narrative(sig.signal_id)
    asset = _assets(nar.narrative_id, n=1)[0]
    a = PerceptionPredictor().predict(nar, asset, rng=random.Random(1))
    b = PerceptionPredictor().predict(nar, asset, rng=random.Random(1))
    assert a == b
    for dim in ("attention", "valence", "arousal", "cognitive_load", "engagement_likelihood"):
        assert 0.0 <= getattr(a, dim) <= 1.0


def test_calibration_value_bounded_and_learns():
    cal = CalibrationLayer(learning_rate=0.2)
    p = PerceptionScore(attention=0.9, valence=0.8, arousal=0.5, cognitive_load=0.2, engagement_likelihood=0.9)
    before = cal.value(p, "seg")
    assert 0.0 <= before <= 1.0
    for _ in range(50):
        cal.update(p, "seg", observed_reward=1.0)
    after = cal.value(p, "seg")
    assert after > before  # Converges toward the observed reward.
    assert cal.updates == 50


def test_calibration_discounts_cognitive_load():
    cal = CalibrationLayer()
    clear = PerceptionScore(attention=0.7, valence=0.7, arousal=0.5, cognitive_load=0.1, engagement_likelihood=0.7)
    overloaded = clear.model_copy(update={"cognitive_load": 0.95})
    assert cal.value(clear, "s") > cal.value(overloaded, "s")


# ---------------------------------------------------------------------------
# RGAE three-layer pipeline
# ---------------------------------------------------------------------------
def test_rgae_produces_a_record_per_asset_with_stages():
    sig = _signal()
    nar = _narrative(sig.signal_id)
    assets = _assets(nar.narrative_id, n=4)
    rgae = RealityGroundedAdaptiveEngine(rng=random.Random(3))
    records = rgae.screen(nar, assets, sig)
    assert len(records) == len(assets)
    assert {r.asset_id for r in records} == {a.asset_id for a in assets}
    assert all(r.stage_reached in set(ValidationStage) for r in records)
    # A healthy batch should pass at least one creative through the revenue gate.
    assert any(r.passed for r in records)
    for r in records:
        if r.passed:
            assert r.stage_reached is ValidationStage.PASSED
            assert r.ltv_cpa_ratio >= rgae.target_ltv_cpa


def test_rgae_rejects_weak_creatives():
    sig = _signal(strength=0.4)
    nar = _narrative(sig.signal_id, resonance=0.2)
    weak = _assets(nar.narrative_id, n=4, ctr=0.002)  # Near-zero CTR.
    rgae = RealityGroundedAdaptiveEngine(rng=random.Random(0))
    records = rgae.screen(nar, weak, sig)
    assert all(not r.passed for r in records)


def test_rgae_feeds_calibration():
    sig = _signal()
    nar = _narrative(sig.signal_id)
    assets = _assets(nar.narrative_id, n=4)
    rgae = RealityGroundedAdaptiveEngine(rng=random.Random(3))
    rgae.screen(nar, assets, sig)
    assert rgae.calibration.updates >= 1


def test_rgae_screen_empty_is_safe():
    rgae = RealityGroundedAdaptiveEngine()
    assert rgae.screen(_narrative("x"), [], _signal()) == []


# ---------------------------------------------------------------------------
# Three-Critic Stack
# ---------------------------------------------------------------------------
def _cell(amount: int) -> MicroCell:
    return MicroCell(signal_id="s", market="devtools", segment="startups", allocated_cents=amount)


def test_three_critic_approves_sound_allocation():
    stack = ThreeCriticStack(ConstitutionalFilter())
    verdict = stack.review_allocation(
        _cell(10_000), treasury_cents=1_000_000, deployed_cents=0, expected_value=0.6, signal=_signal()
    )
    assert verdict.approved
    assert {r.critic for r in verdict.reviews} == {CriticName.TRUTH, CriticName.POLICY, CriticName.STRATEGY}
    assert verdict.latency_ms >= 0.0


def test_policy_critic_blocks_oversized_allocation():
    stack = ThreeCriticStack(ConstitutionalFilter())
    verdict = stack.review_allocation(
        _cell(900_000), treasury_cents=1_000_000, deployed_cents=0, expected_value=0.6, signal=_signal()
    )
    assert not verdict.approved
    policy = next(r for r in verdict.reviews if r.critic is CriticName.POLICY)
    assert not policy.passed
    assert stack.blocks == 1


def test_strategy_critic_blocks_low_expected_value():
    stack = ThreeCriticStack(ConstitutionalFilter(), min_strategy_ev=0.5)
    verdict = stack.review_allocation(
        _cell(10_000), treasury_cents=1_000_000, deployed_cents=0, expected_value=0.1, signal=_signal()
    )
    assert not verdict.approved
    strategy = next(r for r in verdict.reviews if r.critic is CriticName.STRATEGY)
    assert not strategy.passed


def test_truth_critic_flags_allocation_beyond_tam():
    stack = ThreeCriticStack(ConstitutionalFilter(), max_tam_fraction=0.5)
    small_tam_signal = _signal()
    small_tam_signal.estimated_tam_cents = 10_000
    verdict = stack.review_allocation(
        _cell(9_000), treasury_cents=10_000_000, deployed_cents=0, expected_value=0.6, signal=small_tam_signal
    )
    truth = next(r for r in verdict.reviews if r.critic is CriticName.TRUTH)
    assert not truth.passed


# ---------------------------------------------------------------------------
# Epistemic firewall
# ---------------------------------------------------------------------------
def test_firewall_passes_corroborated_signal():
    fw = EpistemicFirewall()
    v = fw.validate(_signal(strength=0.6), readings=[0.6, 0.55, 0.7, 0.5])
    assert v.passed
    assert v.oracle_ok and v.consensus_ok and v.red_team_ok
    assert v.corroborating_sources == 4


def test_firewall_rejects_without_consensus():
    fw = EpistemicFirewall(min_consensus_sources=2)
    v = fw.validate(_signal(strength=0.6), readings=[0.6, 0.1, 0.05, 0.02])
    assert not v.passed
    assert not v.consensus_ok


def test_firewall_red_team_flags_astroturf():
    fw = EpistemicFirewall()
    # Very high headline strength but only one hot source (dispersion spike).
    v = fw.validate(_signal(strength=0.9), readings=[0.95, 0.1, 0.08, 0.05])
    assert not v.passed
    assert not v.red_team_ok


def test_firewall_rejects_implausible_elasticity():
    fw = EpistemicFirewall()
    sig = _signal()
    sig.elasticity = 0.5  # Positive elasticity is physically impossible.
    v = fw.validate(sig, readings=[0.6, 0.6, 0.6])
    assert not v.oracle_ok and not v.passed


# ---------------------------------------------------------------------------
# EKG wiring
# ---------------------------------------------------------------------------
def test_ekg_tracks_validated_assets():
    ekg = EconomicKnowledgeGraph()
    sig = _signal()
    ekg.record_signal(sig)
    nar = _narrative(sig.signal_id)
    ekg.record_narrative(nar)
    assets = _assets(nar.narrative_id, n=4)
    for a in assets:
        ekg.record_asset(a)
    rgae = RealityGroundedAdaptiveEngine(rng=random.Random(3))
    for record in rgae.screen(nar, assets, sig):
        ekg.record_validation(record)
    validated = ekg.validated_assets_for(nar.narrative_id)
    assert 0 < len(validated) <= len(assets)
    assert ekg.stats()["validated_assets"] == len(validated)


# ---------------------------------------------------------------------------
# Organism integration
# ---------------------------------------------------------------------------
def test_organism_snapshot_exposes_validation_layer():
    o = Organism(initial_capital_cents=100_000_00, seed=7)
    o.run(15)
    snap = o.snapshot()
    val = snap["validation"]
    assert val["epistemic_firewall"]["signals_checked"] > 0
    assert val["rgae"]["assets_screened"] > 0
    assert val["rgae"]["assets_passed"] > 0
    assert val["three_critic_stack"]["reviews"] > 0
    assert snap["history"][0]["assets_validated"] >= 0


def test_organism_only_spends_on_validated_assets():
    o = Organism(initial_capital_cents=100_000_00, seed=7)
    o.run(20)
    # Every cell that realised revenue must have a validated creative for its
    # signal — the RGAE revenue gate is load-bearing.
    for cell in o.ekg.cells.values():
        if cell.revenue_cents > 0:
            validated = [
                a
                for n in o.ekg.narratives_for(cell.signal_id)
                for a in o.ekg.validated_assets_for(n.narrative_id)
            ]
            assert validated, f"cell {cell.cell_id} earned revenue without a validated asset"
