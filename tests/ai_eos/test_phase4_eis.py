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


def test_eis_pearl_do_calculus():
    """Verify Pearl causal backdoor do-calculus estimation matches SCM requirements."""
    eis = EntrepreneurialIntelligenceSystem()
    observational_data = {"n": 500, "correlation": 0.8}

    # 2 confounders => adjusted_effect = 0.8 - 2 * 0.05 = 0.70
    result = eis.evaluate_scm_do_calculus(
        treatment="price_decrease",
        outcome="unit_sales",
        confounders=["seasonal_index", "competitor_discount"],
        observational_data=observational_data
    )

    assert result["treatment"] == "price_decrease"
    assert result["outcome"] == "unit_sales"
    assert result["adjusted_effect"] == pytest.approx(0.70)
    assert len(result["confounders_adjusted"]) == 2


def test_eis_lagrange_shadow_prices():
    """Verify Lagrange multipliers find limiting operational capacity bottlenecks."""
    eis = EntrepreneurialIntelligenceSystem()
    constraints = {"engineering_hours": 100.0, "marketing_tokens": 50.0}
    demands = {"engineering_hours": 150.0, "marketing_tokens": 40.0}

    shadow_prices = eis.detect_rate_limiting_bottlenecks(constraints, demands)

    # Engineering is constrained (150 > 100) => shadow price is (150 - 100)/100 = 0.50
    # Marketing is stable (40 <= 50) => shadow price is 0.0
    assert shadow_prices["engineering_hours"] == pytest.approx(0.50)
    assert shadow_prices["marketing_tokens"] == pytest.approx(0.0)


def test_active_inference_ebbinghaus_forgetting():
    """Verify Ebbinghaus memory consolidation retention curve decay matches exponential patterns."""
    from apodex.ai_eos.active_inference.engine import ExecutiveOptimizer
    opt = ExecutiveOptimizer()

    # R_0 = 1.0, elapsed = 10 steps, decay = 0.06 => 1.0 * exp(-0.6) = 0.5488
    retention = opt.calculate_ebbinghaus_memory_decay(initial_retention=1.0, elapsed_time_steps=10.0)
    assert retention == pytest.approx(0.5488, abs=0.01)


def test_active_inference_surprise_regime_change():
    """Verify Bayesian surprise correctly flags sudden operational regime shifts."""
    from apodex.ai_eos.active_inference.engine import ExecutiveOptimizer
    opt = ExecutiveOptimizer()

    historical_variance = [10.0, 11.0, 9.0, 10.0, 10.0]  # mean = 10.0, var = 0.4

    # Observation = 15.0 => surprise is extremely high, flags regime change
    assert opt.detect_regime_change(historical_variance, current_observation=15.0, surprise_threshold=2.0) is True
    # Observation = 10.2 => surprise is minor, stable regime
    assert opt.detect_regime_change(historical_variance, current_observation=10.2, surprise_threshold=2.0) is False


def test_active_inference_vessel_depressurization():
    """Verify system-level hazard-rate vessel shutdown and depressurization limits."""
    from apodex.ai_eos.active_inference.engine import ExecutiveOptimizer
    opt = ExecutiveOptimizer()

    bounds = {"min_runway_months": 3.0, "max_token_utilization_rate": 5000.0}

    # Runway breach => emergency shutdown
    res_runway = opt.vessel_depressurization_protocol(current_runway_months=2.5, token_utilization_rate=1000.0, critical_safety_bounds=bounds)
    assert res_runway == "DEPRESSURIZE_EMERGENCY_SHUTDOWN"

    # Token surge => throttle compute
    res_tokens = opt.vessel_depressurization_protocol(current_runway_months=12.0, token_utilization_rate=6000.0, critical_safety_bounds=bounds)
    assert res_tokens == "DEPRESSURIZE_THROTTLE_COMPUTE"

    # Perfect status => stable
    res_stable = opt.vessel_depressurization_protocol(current_runway_months=12.0, token_utilization_rate=1000.0, critical_safety_bounds=bounds)
    assert res_stable == "VESSEL_PRESSURE_STABLE"


def test_active_inference_originality_scoring():
    """Verify Jaccard distance Novelty and Originality scores are calculated accurately."""
    from apodex.ai_eos.active_inference.engine import ExecutiveOptimizer
    opt = ExecutiveOptimizer()

    proposal = ["zero", "fee", "payment"]
    corpus = [
        ["zero", "fee", "merchant"],
        ["micro", "lending", "credit"]
    ]

    # Intersection with 1st is {"zero", "fee"} => size 2
    # Union is {"zero", "fee", "payment", "merchant"} => size 4
    # Jaccard Similarity = 2/4 = 0.5 => Jaccard Distance = 0.5
    # Similarity with 2nd is 0/5 = 0.0 => Distance = 1.0
    # Expected originality (minimum distance) is 0.50
    score = opt.score_originality(proposal, corpus)
    assert score == pytest.approx(0.50)
