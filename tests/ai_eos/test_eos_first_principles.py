"""Unit and integration test suite for EOS First-Principles Executable Engine."""

import pytest
from apodex.ai_eos.intelligence.eos_first_principles import (
    EOSState,
    EOSStateMachine,
    OpportunityDecisionTree,
    CoupledBusinessLoopsEngine,
    CustomerLifecycleEngine,
    CompanyGrowthStage,
    GrowthStageClassifier,
    MoatAnalyzer,
    FailureModeMonitor,
    FirstPrinciplesEOSEngine,
)


class TestEOSStateMachine:
    def test_initial_state_is_sensing(self):
        sm = EOSStateMachine()
        assert sm.current_state == EOSState.SENSING

    def test_valid_transitions(self):
        sm = EOSStateMachine()
        sm.transition_to(EOSState.HYPOTHESIS)
        assert sm.current_state == EOSState.HYPOTHESIS

        sm.transition_to(EOSState.CHEAP_TEST)
        assert sm.current_state == EOSState.CHEAP_TEST

        sm.transition_to(EOSState.VALIDATION)
        assert sm.current_state == EOSState.VALIDATION

        sm.transition_to(EOSState.BUILD_GATE)
        assert sm.current_state == EOSState.BUILD_GATE

    def test_invalid_transition_raises_error(self):
        sm = EOSStateMachine()
        with pytest.raises(ValueError, match="Invalid state transition"):
            sm.transition_to(EOSState.SCALE)


class TestOpportunityDecisionTree:
    def test_discard_noise(self):
        pursue, code, audit = OpportunityDecisionTree.evaluate_opportunity(
            is_structural_anomaly=False,
            is_reversible=True,
        )
        assert not pursue
        assert code == "DISCARD_NOISE"

    def test_discard_type_i_without_multi_source_signal(self):
        pursue, code, audit = OpportunityDecisionTree.evaluate_opportunity(
            is_structural_anomaly=True,
            is_reversible=False,
            has_multi_source_signal=False,
        )
        assert not pursue
        assert code == "DISCARD_UNCONFIRMED_TYPE_I"

    def test_run_cheap_test_path(self):
        pursue, code, audit = OpportunityDecisionTree.evaluate_opportunity(
            is_structural_anomaly=True,
            is_reversible=True,
            cheap_test_available=True,
            has_structural_advantage=True,
        )
        assert pursue
        assert code == "RUN_CHEAP_TEST"

    def test_commit_resources_path(self):
        pursue, code, audit = OpportunityDecisionTree.evaluate_opportunity(
            is_structural_anomaly=True,
            is_reversible=True,
            cheap_test_available=True,
            test_result_exceeds_kill_threshold=True,
            has_structural_advantage=True,
        )
        assert pursue
        assert code == "COMMIT_RESOURCES"


class TestCoupledBusinessLoopsEngine:
    def test_simulate_coupling_cycle(self):
        engine = CoupledBusinessLoopsEngine()
        res = engine.simulate_coupling_cycle({
            "arpu_cents": 150_00,
            "cac_cents": 300_00,
            "acquired_users": 200,
            "retention_rate": 0.95,
            "hiring_budget_cents": 500_000_00,
        })
        assert res["gross_revenue_cents"] == 30_000_00
        assert res["ltv_to_cac"] > 3.0
        assert "updated_stocks" in res


class TestCustomerLifecycleEngine:
    def test_evaluate_cohort_progression_bottlenecks(self):
        res = CustomerLifecycleEngine.evaluate_cohort_progression({
            "activation_rate": 0.3,
            "retention_rate": 0.6,
            "net_revenue_retention": 0.9,
        })
        assert not res["healthy_funnel"]
        assert len(res["identified_bottlenecks"]) == 3


class TestGrowthStageClassifier:
    def test_classify_startup_stage(self):
        res = GrowthStageClassifier.classify_stage({"paying_customers": 15})
        assert res["stage"] == CompanyGrowthStage.STARTUP.value
        assert res["binding_constraint"] == "Cash runway"

    def test_classify_market_leadership(self):
        res = GrowthStageClassifier.classify_stage({
            "category_share": 0.50,
            "moat_durability": 0.85,
        })
        assert res["stage"] == CompanyGrowthStage.MARKET_LEADERSHIP.value


class TestMoatAnalyzer:
    def test_score_moat_durability(self):
        res = MoatAnalyzer.score_moat_durability(
            network_density=0.8,
            avg_switching_cost_cents=8000_00,
            brand_trust_score=0.9,
        )
        assert res["composite_moat_durability_score"] > 0.4
        assert res["primary_moat_type"] in ["Network Effects", "Switching Costs", "Brand Trust"]


class TestFailureModeMonitor:
    def test_diagnose_solving_wrong_problem(self):
        alerts = FailureModeMonitor.diagnose_failure_modes({
            "survey_satisfaction": 0.9,
            "daily_active_usage": 0.05,
        })
        assert len(alerts) >= 1
        assert alerts[0]["failure_mode"] == "Solving the wrong problem"

    def test_diagnose_organizational_bottlenecks(self):
        alerts = FailureModeMonitor.diagnose_failure_modes({
            "decision_latency_days": 10.0,
            "team_size": 25,
        })
        assert any(a["failure_mode"] == "Organizational bottlenecks" for a in alerts)


class TestFirstPrinciplesEOSEngine:
    def test_run_master_sensing_cycle(self):
        engine = FirstPrinciplesEOSEngine()
        venture_state = {
            "arpu_cents": 100_00,
            "cac_cents": 250_00,
            "acquired_users": 100,
            "paying_customers": 20,
            "network_density": 0.6,
            "activation_rate": 0.8,
            "retention_rate": 0.85,
            "net_revenue_retention": 1.15,
        }
        signal = {
            "is_structural_anomaly": True,
            "is_reversible": True,
            "cheap_test_available": True,
            "has_structural_advantage": True,
        }

        res = engine.run_master_sensing_cycle(venture_state, opportunity_signal=signal)
        assert res["current_state"] == EOSState.CHEAP_TEST.value
        assert res["decision_result"]["pursue"]
        assert res["growth_stage"]["stage"] == CompanyGrowthStage.STARTUP.value
        assert res["memory_cycle_count"] == 1
