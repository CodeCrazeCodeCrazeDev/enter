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


def test_evaluate_scm_do_calculus():
    """Verify Pearl's do-calculus causal flow propagation across downstream dependencies."""
    eis = EntrepreneurialIntelligenceSystem()

    # Define DAG: learning_rate -> model_accuracy -> business_revenue
    causal_links = {
        "learning_rate": {"model_accuracy": 0.8},
        "model_accuracy": {"business_revenue": 1.5}
    }

    # Intervene: do(learning_rate = 0.5)
    result = eis.evaluate_scm_do_calculus("learning_rate", 0.5, causal_links)

    assert result["learning_rate"] == 0.5
    # model_accuracy = 0.5 * 0.8 = 0.4
    assert pytest.approx(result["model_accuracy"]) == 0.4
    # business_revenue = 0.4 * 1.5 = 0.6
    assert pytest.approx(result["business_revenue"]) == 0.6


def test_detect_rate_limiting_bottlenecks():
    """Verify dual shadow price calculation identifies the rate-limiting bottleneck resource."""
    eis = EntrepreneurialIntelligenceSystem()

    # Resource constraints
    resource_capacities = {
        "compute_tokens": 1000.0,
        "developer_hours": 100.0,
        "ad_budget": 500.0
    }

    # Demands from 2 active projects
    demand_vectors = {
        "compute_tokens": [600.0, 300.0],  # Total demand = 900 <= 1000 (No bottleneck)
        "developer_hours": [80.0, 50.0],    # Total demand = 130 > 100 (Bottleneck!)
        "ad_budget": [200.0, 100.0]        # Total demand = 300 <= 500 (No bottleneck)
    }

    # Priority weights for activities: Project A (1.2), Project B (0.8)
    weights = [1.2, 0.8]

    shadow_prices = eis.detect_rate_limiting_bottlenecks(resource_capacities, demand_vectors, weights)

    # compute_tokens: demand = 600*1.2 + 300*0.8 = 720 + 240 = 960 <= 1000. Shadow price = 0
    assert shadow_prices["compute_tokens"] == 0.0

    # developer_hours: demand = 80*1.2 + 50*0.8 = 96 + 40 = 136 > 100.
    # excess = 136 - 100 = 36. Capacity = 100.
    # shadow price = (36 / 100) * avg_weight = 0.36 * 1.0 = 0.36
    assert pytest.approx(shadow_prices["developer_hours"]) == 0.36

    # ad_budget: demand = 200*1.2 + 100*0.8 = 240 + 80 = 320 <= 500. Shadow price = 0
    assert shadow_prices["ad_budget"] == 0.0
