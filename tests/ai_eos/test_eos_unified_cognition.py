"""Unit tests for the integrated, native Entrepreneurial Operating System (EOS) cognitive capabilities of EIOSKernel."""

import pytest
from apodex.arcs.kernel.kernel import EIOSKernel


def test_sense_opportunity_anomalies():
    """Verify that EIOSKernel correctly senses structural anomalies and ignores noise."""
    kernel = EIOSKernel()

    # Test minor deviation (Noise)
    noise_report = kernel.sense_opportunity_anomalies("conversion_rate", 0.052, 0.050)
    assert noise_report["is_anomaly"] is False
    assert noise_report["classification"] == "NOISE"

    # Test major deviation (Anomaly)
    anomaly_report = kernel.sense_opportunity_anomalies("conversion_rate", 0.015, 0.050)
    assert anomaly_report["is_anomaly"] is True
    assert anomaly_report["classification"] == "STRUCTURAL_SHIFT"
    assert anomaly_report["surprise_ratio"] > 0.25


def test_generate_falsifiable_hypothesis():
    """Verify hypothesis formulation from an anomaly report with kill criteria."""
    kernel = EIOSKernel()

    anomaly_report = {
        "signal": "pricing",
        "actual": 19.99,
        "expected": 49.99,
        "is_anomaly": True
    }

    hypothesis = kernel.generate_falsifiable_hypothesis(anomaly_report, "conversion_rate")
    assert "hyp_" in hypothesis["id"]
    assert "pricing" in hypothesis["statement"]
    assert "conversion_rate" in hypothesis["statement"]
    assert hypothesis["risk_type"] == "TYPE_II"
    assert hypothesis["kill_criteria"]["max_test_cost_usd"] == 150.0


def test_validate_opportunity_economics():
    """Verify that opportunity viability is correctly assessed from unit economics."""
    kernel = EIOSKernel()

    # Test highly viable case
    viable_res = kernel.validate_opportunity_economics(
        smoke_test_conversions=10,
        total_visits=200,
        ltv_cents=150_00,       # $150
        test_spend_cents=10_00  # $10
    )
    assert viable_res["is_viable"] is True
    assert viable_res["conversion_rate"] == 0.05
    assert viable_res["projected_cac_cents"] == 1_00
    assert viable_res["ltv_to_cac_ratio"] == 150.0
    assert viable_res["decision"] == "VALIDATED"

    # Test unviable case due to low LTV/CAC
    unviable_res = kernel.validate_opportunity_economics(
        smoke_test_conversions=5,
        total_visits=500,
        ltv_cents=20_00,        # $20
        test_spend_cents=50_00  # $50
    )
    assert unviable_res["is_viable"] is False
    assert unviable_res["decision"] == "KILL_SIGNAL"


def test_allocate_capital_opportunity():
    """Verify that capital allocation applies risk-adjusted opportunity cost filters."""
    kernel = EIOSKernel()

    # Allocates capital if viable
    validated_viable = {
        "ltv_to_cac_ratio": 5.0,
        "is_viable": True
    }
    capital_viable = kernel.allocate_capital_opportunity(validated_viable, available_budget_cents=10000_00)
    assert capital_viable["opportunity_cost_met"] is True
    assert capital_viable["allocated_cents"] == 5000_00  # 50% allocation (5.0 / 10.0)
    assert capital_viable["reinvestment_capacity_cents"] == 5000_00

    # Rejects allocation if unviable
    validated_unviable = {
        "ltv_to_cac_ratio": 1.5,
        "is_viable": False
    }
    capital_unviable = kernel.allocate_capital_opportunity(validated_unviable, available_budget_cents=10000_00)
    assert capital_unviable["opportunity_cost_met"] is False
    assert capital_unviable["allocated_cents"] == 0


def test_reason_gtm_channel():
    """Verify GTM channel-fit selection based on complexity and contract value."""
    kernel = EIOSKernel()

    # Enterprise segment -> Sales-Led Growth
    assert kernel.reason_gtm_channel(product_complexity_score=0.85, acv_usd=6000) == "SALES_LED_GROWTH"

    # SMB self-serve -> Product-Led Growth
    assert kernel.reason_gtm_channel(product_complexity_score=0.25, acv_usd=500) == "PRODUCT_LED_GROWTH"

    # Mid-market -> Hybrid Growth
    assert kernel.reason_gtm_channel(product_complexity_score=0.60, acv_usd=2500) == "HYBRID_GROWTH"


def test_analyze_moat_durability():
    """Verify competitive moat scoring and durability classification."""
    kernel = EIOSKernel()

    # Defensible Moat
    moat_defensible = kernel.analyze_moat_durability(network_coefficient=0.6, user_switching_cost_usd=150.0)
    assert moat_defensible["durability"] == "DEFENSIBLE"
    assert moat_defensible["moat_score"] == 45.0

    # Unassailable Moat
    moat_unassailable = kernel.analyze_moat_durability(network_coefficient=0.9, user_switching_cost_usd=400.0)
    assert moat_unassailable["durability"] == "UNASSAILABLE"


def test_evaluate_lifecycle_stage():
    """Verify organizational lifecycle stage classification."""
    kernel = EIOSKernel()

    # Early Idea
    assert kernel.evaluate_lifecycle_stage(active_months=0, monthly_active_users=0, monthly_revenue_usd=0) == "IDEA"

    # Validation
    assert kernel.evaluate_lifecycle_stage(active_months=2, monthly_active_users=50, monthly_revenue_usd=0) == "VALIDATION"

    # PMF
    assert kernel.evaluate_lifecycle_stage(active_months=12, monthly_active_users=1200, monthly_revenue_usd=3000) == "PRODUCT_MARKET_FIT"

    # Market Leadership
    assert kernel.evaluate_lifecycle_stage(active_months=48, monthly_active_users=120000, monthly_revenue_usd=1500000) == "MARKET_LEADERSHIP"


def test_trigger_reinvention_review():
    """Verify trigger of strategic self-disruption under leading risk indicator breaches."""
    kernel = EIOSKernel()

    # Indicators healthy -> No trigger
    assert kernel.trigger_reinvention_review(market_share_delta=-0.01, customer_satisfaction_index=0.85) is False

    # Market share plummet -> Triggered
    assert kernel.trigger_reinvention_review(market_share_delta=-0.12, customer_satisfaction_index=0.85) is True

    # Satisfaction score plummet -> Triggered
    assert kernel.trigger_reinvention_review(market_share_delta=-0.01, customer_satisfaction_index=0.62) is True
