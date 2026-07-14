"""Tests for the AEAN (Autonomous Economic Actor Network) implementation."""
from __future__ import annotations

import json
import random

from apodex.aean import (
    ConstitutionalFilter,
    ConstitutionalRules,
    EconomicKnowledgeGraph,
    HiveMind,
    LLMAdapter,
    Organism,
    ThompsonBandit,
)
from apodex.aean.coordination.hive_mind import TaskBid
from apodex.aean.engines.are import AutonomousRevenueEngine, BASE_UNIT_COST_CENTS
from apodex.aean.models import DemandSignal, EngineName, MicroCell, MicroCellStatus, Narrative


# ---------------------------------------------------------------------------
# EKG
# ---------------------------------------------------------------------------
def test_ekg_records_and_indexes_entities():
    ekg = EconomicKnowledgeGraph()
    sig = DemandSignal(market="devtools", segment="startups", strength=0.7, estimated_tam_cents=1_000_000)
    ekg.record_signal(sig)
    nar = Narrative(signal_id=sig.signal_id, theme="t", hook="h", body="b", predicted_resonance=0.8)
    ekg.record_narrative(nar)

    assert sig.signal_id in ekg.signals
    assert ekg.narratives_for(sig.signal_id) == [nar]
    assert ekg.open_signals() == [sig]  # No cell exploits it yet.
    assert ekg.stats()["events"] >= 2


def test_ekg_open_signals_excludes_exploited():
    ekg = EconomicKnowledgeGraph()
    sig = DemandSignal(market="fintech", segment="smb", strength=0.6, estimated_tam_cents=500_000)
    ekg.record_signal(sig)
    ekg.record_cell(MicroCell(signal_id=sig.signal_id, market="fintech", segment="smb"))
    assert ekg.open_signals() == []


def test_ekg_edges_are_deduplicated():
    ekg = EconomicKnowledgeGraph()
    ekg.add_edge("a", "b", "LINK", weight=0.5)
    ekg.add_edge("a", "b", "LINK", weight=0.9)
    links = ekg.neighbors("a", "LINK")
    assert len(links) == 1 and links[0].weight == 0.9


# ---------------------------------------------------------------------------
# Thompson Sampling bandit
# ---------------------------------------------------------------------------
def test_thompson_bandit_learns_best_arm():
    rng = random.Random(0)
    bandit = ThompsonBandit(rng=rng)
    # Arm "good" pays out 90% of the time, "bad" 10%.
    for _ in range(300):
        bandit.update("good", 1.0 if rng.random() < 0.9 else 0.0)
        bandit.update("bad", 1.0 if rng.random() < 0.1 else 0.0)
    assert bandit.expected_value("good") > bandit.expected_value("bad")
    # Over many draws the bandit should prefer the good arm.
    picks = [bandit.rank(["good", "bad"])[0] for _ in range(200)]
    assert picks.count("good") > picks.count("bad")


def test_thompson_bandit_reward_is_clamped():
    bandit = ThompsonBandit()
    bandit.update("x", 5.0)  # Out-of-range reward.
    bandit.update("x", -3.0)
    assert 0.0 <= bandit.expected_value("x") <= 1.0


# ---------------------------------------------------------------------------
# Governance
# ---------------------------------------------------------------------------
def test_governance_blocks_oversized_allocation():
    gov = ConstitutionalFilter()
    verdict = gov.review_allocation(amount_cents=90, treasury_cents=100, currently_deployed_cents=0)
    assert not verdict.approved
    assert gov.blocks == 1


def test_governance_reserve_is_enforced():
    gov = ConstitutionalFilter(ConstitutionalRules(max_single_allocation_pct=1.0, min_treasury_reserve_pct=0.5))
    verdict = gov.review_allocation(amount_cents=60, treasury_cents=100, currently_deployed_cents=0)
    assert not verdict.approved


def test_governance_blocks_banned_content():
    gov = ConstitutionalFilter()
    assert not gov.review_content("guaranteed returns with zero risk").approved
    assert gov.review_content("a clear, honest value proposition").approved


def test_autonomy_is_earned():
    gov = ConstitutionalFilter()
    assert not gov.is_autonomous(EngineName.PAEAN)
    for _ in range(30):
        gov.note_decision(EngineName.PAEAN, success=True)
    assert gov.is_autonomous(EngineName.PAEAN)


# ---------------------------------------------------------------------------
# Hive Mind
# ---------------------------------------------------------------------------
def test_hive_mind_arbitrates_within_budget():
    hm = HiveMind(token_budget=30)
    grants = hm.arbitrate([
        TaskBid("a", priority=0.9, expected_value=0.9, token_cost=20),
        TaskBid("b", priority=0.1, expected_value=0.1, token_cost=20),
    ])
    granted = hm.granted_tasks(grants)
    assert granted["a"] is True   # Higher score funded first.
    assert granted["b"] is False  # Budget exhausted.


# ---------------------------------------------------------------------------
# ARE pricing
# ---------------------------------------------------------------------------
def test_are_optimal_price_above_cost():
    are = AutonomousRevenueEngine(EconomicKnowledgeGraph(), ConstitutionalFilter())
    price = are.compute_optimal_price_cents(BASE_UNIT_COST_CENTS, elasticity=-1.5)
    assert price > BASE_UNIT_COST_CENTS
    # Elastic (-2.0) demand yields a lower optimal markup than less-elastic (-1.2).
    assert are.compute_optimal_price_cents(1000, -2.0) < are.compute_optimal_price_cents(1000, -1.2)


# ---------------------------------------------------------------------------
# LLM adapter fallback
# ---------------------------------------------------------------------------
def test_llm_adapter_falls_back_to_simulation(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("AEAN_LLM_PROVIDER", raising=False)
    llm = LLMAdapter()
    assert llm.provider == "simulation"
    assert not llm.is_live
    out = llm.complete("write a hook for devtools startups")
    assert isinstance(out, str) and out


def test_llm_simulation_is_deterministic():
    a = LLMAdapter(provider="simulation")
    b = LLMAdapter(provider="simulation")
    assert a.complete("same prompt") == b.complete("same prompt")


# ---------------------------------------------------------------------------
# Organism / flywheel
# ---------------------------------------------------------------------------
def test_organism_runs_and_is_deterministic():
    a = Organism(initial_capital_cents=100_000_00, seed=7)
    b = Organism(initial_capital_cents=100_000_00, seed=7)
    a.run(15)
    b.run(15)
    assert a.snapshot()["net_worth_cents"] == b.snapshot()["net_worth_cents"]


def test_organism_flywheel_produces_all_entities():
    o = Organism(initial_capital_cents=100_000_00, seed=7)
    o.run(20)
    stats = o.ekg.stats()
    assert stats["signals"] > 0
    assert stats["narratives"] > 0
    assert stats["assets"] > 0
    assert stats["cells"] > 0


def test_organism_capital_is_conserved_within_bounds():
    o = Organism(initial_capital_cents=100_000_00, seed=3)
    o.run(25)
    # Treasury must never go negative and portfolio cap is respected.
    assert o.treasury_cents >= 0
    assert o.active_cells_count() <= o.paean.max_active_cells


def test_organism_kills_and_scales_cells():
    o = Organism(initial_capital_cents=100_000_00, seed=1)
    o.run(30)
    statuses = {c.status for c in o.ekg.cells.values()}
    assert MicroCellStatus.KILLED in statuses or MicroCellStatus.SCALED in statuses


def test_snapshot_is_json_serialisable():
    o = Organism(initial_capital_cents=100_000_00, seed=7)
    o.run(10)
    snap = o.snapshot()
    json.dumps(snap)  # Must not raise.
    assert snap["cycle"] == 10
    assert "history" in snap and len(snap["history"]) == 10


def test_run_returns_cycle_results():
    o = Organism(initial_capital_cents=50_000_00, seed=2)
    results = o.run(5)
    assert len(results) == 5
    assert [r.cycle for r in results] == [1, 2, 3, 4, 5]
