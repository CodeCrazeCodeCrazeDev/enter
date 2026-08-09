from __future__ import annotations
import pytest
from apodex.arcs.kernel.kernel import EIOSKernel


def test_sense_opportunity_anomalies():
    kernel = EIOSKernel()
    signals = [
        {"id": "sig_01", "value": 1.0, "description": "Baseline trend"},
        {"id": "sig_02", "value": 1.6, "description": "High internet traffic shift"},
        {"id": "sig_03", "value": 2.2, "description": "Massive compute surge"},
        {"id": "sig_04", "value": 0.9, "description": "Slight variation"}
    ]
    anomalies = kernel.sense_opportunity_anomalies(signals, baseline=1.0, threshold=0.5)

    # sig_02 (deviation=0.6) and sig_03 (deviation=1.2) should be flagged as anomalies
    assert len(anomalies) == 2
    assert anomalies[0]["signal_id"] == "sig_02"
    assert anomalies[0]["type"] == "significant_anomaly"
    assert anomalies[1]["signal_id"] == "sig_03"
    assert anomalies[1]["type"] == "structural_shift"  # deviation 1.2 > threshold*2 (1.0)


def test_generate_falsifiable_hypothesis():
    kernel = EIOSKernel()
    anomaly = {"signal_id": "sig_02", "description": "High internet traffic shift"}

    # Type II (reversible/low-stakes)
    hyp_ii = kernel.generate_falsifiable_hypothesis(anomaly, risk_type="Type_II")
    assert hyp_ii["risk_type"] == "Type_II"
    assert hyp_ii["deliberation_speed"] == "fast_cheap"
    assert "CTR" in hyp_ii["kill_criteria"]

    # Type I (irreversible/high-stakes)
    hyp_i = kernel.generate_falsifiable_hypothesis(anomaly, risk_type="Type_I")
    assert hyp_i["risk_type"] == "Type_I"
    assert hyp_i["deliberation_speed"] == "slow_high_scrutiny"
    assert "unit economics" in hyp_i["kill_criteria"]


def test_validate_opportunity_economics():
    kernel = EIOSKernel()

    # Viable economics
    viable = kernel.validate_opportunity_economics(cac=100.0, ltv=400.0, payback_months=6.0, gross_margin=0.8)
    assert viable["is_viable"] is True
    assert viable["cac_ltv_ratio"] == 4.0
    assert len(viable["reasons"]) == 0

    # Non-viable ratio
    bad_ratio = kernel.validate_opportunity_economics(cac=100.0, ltv=250.0, payback_months=6.0, gross_margin=0.8)
    assert bad_ratio["is_viable"] is False
    assert len(bad_ratio["reasons"]) == 1
    assert "CAC:LTV" in bad_ratio["reasons"][0]

    # Non-viable payback and gross margin
    bad_all = kernel.validate_opportunity_economics(cac=100.0, ltv=400.0, payback_months=15.0, gross_margin=0.4)
    assert bad_all["is_viable"] is False
    assert len(bad_all["reasons"]) == 2


def test_allocate_capital_opportunity():
    kernel = EIOSKernel()

    # Fully approved
    res = kernel.allocate_capital_opportunity(treasury_total=10000.0, request_amount=2000.0, active_allocations=[1000.0, 500.0])
    assert res["status"] == "APPROVED"
    assert res["approved_amount"] == 2000.0

    # Partially approved due to single cap rules (max 35% single cap, so max approved is 3500)
    res_capped = kernel.allocate_capital_opportunity(treasury_total=10000.0, request_amount=4000.0, active_allocations=[1000.0, 500.0])
    assert res_capped["status"] == "PARTIALLY_APPROVED_CAPPED"
    assert res_capped["approved_amount"] == 3500.0

    # Partially approved due to 10% reserve limits (reserve must be at least 1000)
    res_reserve = kernel.allocate_capital_opportunity(treasury_total=10000.0, request_amount=3000.0, active_allocations=[6000.0])
    # available: 4000. available - request = 1000. This is exactly 10%, so it should be APPROVED
    assert res_reserve["status"] == "APPROVED"
    assert res_reserve["approved_amount"] == 3000.0

    # Exceeds reserve
    res_exceed = kernel.allocate_capital_opportunity(treasury_total=10000.0, request_amount=3500.0, active_allocations=[6000.0])
    assert res_exceed["status"] == "PARTIALLY_APPROVED_RESERVE_LIMIT"
    assert res_exceed["approved_amount"] == 3000.0


def test_reason_gtm_channel():
    kernel = EIOSKernel()

    # CLG (low price, network effects)
    clg = kernel.reason_gtm_channel(product_price=50.0, complexity="low", network_effects=True)
    assert clg["recommended_motion"] == "CLG"
    assert "community" in clg["channels"]

    # PLG (low-mid price, low-mid complexity, no network effects)
    plg = kernel.reason_gtm_channel(product_price=150.0, complexity="medium", network_effects=False)
    assert plg["recommended_motion"] == "PLG"
    assert "content" in plg["channels"]

    # SLG (high price or high complexity)
    slg_price = kernel.reason_gtm_channel(product_price=500.0, complexity="medium", network_effects=False)
    assert slg_price["recommended_motion"] == "SLG"
    assert "enterprise_sales" in slg_price["channels"]


def test_analyze_moat_durability():
    kernel = EIOSKernel()

    # Strong durability with no failure modes
    strong_moat = kernel.analyze_moat_durability(
        active_moats=["network_effects", "switching_costs"],
        metrics={"retention_rate": 0.90, "competitor_undercut": False}
    )
    assert strong_moat["durability_level"] == "strong"
    assert strong_moat["durability_score"] == 0.55
    assert len(strong_moat["failure_modes_detected"]) == 0

    # Weak durability with weak positioning failure mode
    weak_moat = kernel.analyze_moat_durability(
        active_moats=["brand"],
        metrics={"retention_rate": 0.75, "competitor_undercut": True}
    )
    assert weak_moat["durability_level"] == "weak"
    assert len(weak_moat["failure_modes_detected"]) == 2
    assert weak_moat["failure_modes_detected"][0]["type"] == "weak_positioning"


def test_evaluate_lifecycle_stage():
    kernel = EIOSKernel()

    # Startup Stage
    startup = kernel.evaluate_lifecycle_stage({"validated_learnings": 5, "paying_customers": 10})
    assert startup["current_stage"] == "Startup"
    assert len(startup["detected_risks"]) == 0

    # PMF Stage
    pmf = kernel.evaluate_lifecycle_stage({
        "validated_learnings": 5,
        "paying_customers": 20,
        "repeatable_acquisition": True,
        "retention_curve_flattened": True
    })
    assert pmf["current_stage"] == "PMF"

    # Premature Scaling risk
    premature = kernel.evaluate_lifecycle_stage({
        "validated_learnings": 2,
        "paying_customers": 1,
        "marketing_scale_spend": True
    })
    assert premature["current_stage"] == "Validation"
    assert len(premature["detected_risks"]) == 1
    assert premature["detected_risks"][0]["type"] == "premature_scaling"


def test_trigger_reinvention_review():
    kernel = EIOSKernel()

    # No trigger
    no_trigger = kernel.trigger_reinvention_review({
        "nps_trend": "stable",
        "cac_trend": "stable",
        "market_share_trend": "stable",
        "decision_latency_days": 1.5
    })
    assert no_trigger["trigger_reinvention"] is False

    # Trigger activated (2 leading indicators met)
    trigger = kernel.trigger_reinvention_review({
        "nps_trend": "declining",
        "cac_trend": "rising_rapidly",
        "market_share_trend": "stable",
        "decision_latency_days": 2.0
    })
    assert trigger["trigger_reinvention"] is True
    assert len(trigger["reasons"]) == 2
