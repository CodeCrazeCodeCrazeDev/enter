"""Unit tests for Phase 4 Entrepreneurial Intelligence System (EIS) strategic decisions."""

import pytest
from apodex.ai_eos.domain.models import Theory
from apodex.ai_eos.intelligence.decision_engine import EntrepreneurialIntelligenceSystem


def test_meta_economic_decision_framework():
    """Verify that the optimal commercialization form is selected based on capital/confidence."""
    eis = EntrepreneurialIntelligenceSystem()

    theory_strong = Theory(
        theory_id="theory_strong",
        statement="Theory of Top Banner Conversion",
        constituent_hypotheses=["hyp1"],
        predictive_scope=["untested1"],
        confidence=0.85
    )

    # High capital and confidence -> BUILD_VENTURE
    form_build = eis.evaluate_opportunity_form(theory_strong, available_capital_cents=50000_00)
    assert form_build == "BUILD_VENTURE"

    # Low capital and confidence -> LICENSE_IP
    form_license = eis.evaluate_opportunity_form(theory_strong, available_capital_cents=5000_00)
    assert form_license == "LICENSE_IP"

    theory_mod = Theory(
        theory_id="theory_mod",
        statement="Theory of Social Media Engagement",
        constituent_hypotheses=["hyp2"],
        predictive_scope=["untested2"],
        confidence=0.65
    )
    # Moderate confidence with predictive scope -> OPEN_SOURCE
    form_os = eis.evaluate_opportunity_form(theory_mod, available_capital_cents=5000_00)
    assert form_os == "OPEN_SOURCE"


def test_recursive_scientific_organization():
    """Verify that high forecasting errors trigger proposals for specialized agent spawning."""
    eis = EntrepreneurialIntelligenceSystem()

    # Small error -> no proposals
    proposals_clean = eis.recommend_capability_refinements(forecasting_errors_ratio=0.04)
    assert len(proposals_clean) == 0

    # Elevated error -> spawn pricing specialist
    proposals_elevated = eis.recommend_capability_refinements(forecasting_errors_ratio=0.18)
    assert "SPAWN_PRICING_SPECIALIST_AGENT" in proposals_elevated

    # Extreme error -> split generalist
    proposals_extreme = eis.recommend_capability_refinements(forecasting_errors_ratio=0.35)
    assert "SPAWN_PRICING_SPECIALIST_AGENT" in proposals_extreme
    assert "SPLIT_GENERALIST_INTO_PEER_REVIEW_TRIAD" in proposals_extreme


def test_eios_executive_optimizer_mathematical_proofs():
    """Verify that EIOS strategic proofs function according to theoretical specifications."""
    from apodex.ai_eos.active_inference.engine import ExecutiveOptimizer

    opt = ExecutiveOptimizer()

    # 1. Ebbinghaus exponential forgetting decay (Section 8.3)
    # y = 1.0 * exp(-0.05 * 10) = exp(-0.5) ≈ 0.6065
    decayed = opt.calculate_ebbinghaus_memory_decay(initial_confidence=1.0, time_elapsed_days=10, decay_constant=0.05)
    assert 0.60 <= decayed <= 0.61

    # 2. Bayesian surprise regime detection (Section 8.4)
    # Low surprise -> parameter tuning
    regime_low = opt.detect_regime_change(prior_entropy=1.2, observed_entropy=1.4, threshold=0.5)
    assert regime_low["is_regime_change"] is False
    assert regime_low["action_directive"] == "PARAMETER_TUNING"

    # High surprise -> structure re-synthesis
    regime_high = opt.detect_regime_change(prior_entropy=1.2, observed_entropy=1.8, threshold=0.5)
    assert regime_high["is_regime_change"] is True
    assert regime_high["action_directive"] == "STRUCTURE_RE_SYNTHESIS"

    # 3. Originality score (Section 8.12)
    # Score = novelty_kl * expected_utility = 1.5 * 2.0 = 3.0
    orig_score = opt.score_originality(novelty_kl_divergence=1.5, expected_utility=2.0)
    assert orig_score == 3.0

    # Negative expected utility shouldn't result in negative originality
    orig_neg = opt.score_originality(novelty_kl_divergence=1.5, expected_utility=-1.0)
    assert orig_neg == 0.0

    # 4. Stochastic hazard vessel depressurization (Section 8.15)
    # Nominal rate -> no depressurization
    vessel_nominal = opt.vessel_depressurization_protocol(hazard_rate=0.2, threshold=0.8)
    assert vessel_nominal["is_critical"] is False
    assert vessel_nominal["allocation_factor"] == 1.0
    assert vessel_nominal["state"] == "NOMINAL_EXPLORATION"

    # Critical hazard rate -> lockdown and zero allocation
    vessel_critical = opt.vessel_depressurization_protocol(hazard_rate=0.85, threshold=0.8)
    assert vessel_critical["is_critical"] is True
    assert vessel_critical["allocation_factor"] == 0.0
    assert vessel_critical["state"] == "VESSEL_DEPRESSURIZED_ASSETS_SECURED"


def test_eios_structural_causal_interventions_and_bottlenecks():
    """Verify Pearl SCM evaluation and shadow price rate-limiting bottlenecks."""
    eis = EntrepreneurialIntelligenceSystem()

    # 1. Pearl SCM backdoor criteria (Section 8.5)
    # Low confounding -> PROCEED
    scm_clear = eis.evaluate_scm_do_calculus(intervention="pricing_restructuring", confounding_metrics=[0.1, 0.2, 0.3])
    assert scm_clear["is_confounded"] is False
    assert scm_clear["decision"] == "PROCEED_WITH_INTERVENTION"
    assert scm_clear["expected_utility_delta"] == 0.45

    # High confounding -> BLOCK
    scm_blocked = eis.evaluate_scm_do_calculus(intervention="pricing_restructuring", confounding_metrics=[0.7, 0.8, 0.9])
    assert scm_blocked["is_confounded"] is True
    assert scm_blocked["decision"] == "BLOCK_INTERVENTION"
    assert scm_blocked["expected_utility_delta"] == 0.0

    # 2. Dual shadow price bottleneck detection (Section 8.9)
    prices = {
        "Capital": 1.25,
        "Compute": -3.50,
        "Talent": 0.85
    }
    # Largest absolute shadow price determines the rate-limiting bottleneck
    bottleneck = eis.detect_rate_limiting_bottlenecks(prices)
    assert bottleneck == "Compute"
