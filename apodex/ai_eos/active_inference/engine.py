"""Active Inference, Bayesian Belief Engine, and Epistemic Risk Queries implementation for SERO v2.1.

Implements conjugate posterior distribution updates, calibration audits, and epistemic
risk queries to prevent false certainty.
"""

from __future__ import annotations
import math
import logging
from typing import Any, Dict, List, Optional
from uuid import UUID

from ..domain.models import VentureCell, Hypothesis, Evidence
from ..interfaces.services import IExecutiveOptimizer

logger = logging.getLogger("sero.active_inference")


class ExecutiveOptimizer(IExecutiveOptimizer):
    """The multi-objective optimizer, Bayesian Belief Engine, and Epistemic Risk manager."""

    def __init__(self, w_risk: float = 1.5, w_compute: float = 0.5, w_info: float = 2.0, w_gov: float = 3.0) -> None:
        self.w_risk = w_risk
        self.w_compute = w_compute
        self.w_info = w_info
        self.w_gov = w_gov
        self.calibration_trail: List[Dict[str, Any]] = []

    # ------------------------------------------------------------------
    # Bayesian Belief conjugate updates
    # ------------------------------------------------------------------
    def update_beliefs(self, cell: VentureCell, actual_revenue: int, expected_revenue: int) -> VentureCell:
        """Execute Bayesian update of belief states based on observation prediction errors."""
        pred_error = float(actual_revenue - expected_revenue)
        cell.prediction_error = pred_error

        # Retrieve prior parameters representing conversion/success probability
        prior_alpha = float(cell.belief_state.get("alpha", 10.0))
        prior_beta = float(cell.belief_state.get("beta", 10.0))

        # Conjugate update using standard reliability weights
        reliability_weight = 1.0
        if actual_revenue >= expected_revenue:
            updated_alpha = prior_alpha + reliability_weight
            updated_beta = prior_beta
        else:
            updated_alpha = prior_alpha
            updated_beta = prior_beta + reliability_weight

        cell.belief_state["alpha"] = updated_alpha
        cell.belief_state["beta"] = updated_beta

        sum_ab = updated_alpha + updated_beta
        mean = updated_alpha / sum_ab
        entropy = - (mean * math.log(max(1e-5, mean)) + (1.0 - mean) * math.log(max(1e-5, 1.0 - mean)))

        old_entropy = cell.uncertainty
        cell.uncertainty = float(entropy)
        cell.information_gain = max(0.0, old_entropy - entropy)

        variance = (updated_alpha * updated_beta) / ((sum_ab ** 2) * (sum_ab + 1.0))
        cell.confidence = min(1.0, max(0.0, 1.0 - 4.0 * variance))

        logger.info(f"Bayesian conjugate update completed: Pred Error = {pred_error}, Uncertainty = {cell.uncertainty:.4f}")
        return cell

    def compute_composite_objective(self, cell: VentureCell, policy_expected_utility: float, policy_risk: float) -> float:
        """Calculate composite objective G score."""
        risk_penalty = float(policy_risk)
        compute_cost = 0.1 * len(cell.sub_agent_ids)
        info_gain = float(cell.information_gain)
        gov_penalty = 5.0 if cell.risk > 0.8 else 0.0

        g_score = (
            policy_expected_utility
            - self.w_risk * risk_penalty
            - self.w_compute * compute_cost
            + self.w_info * info_gain
            - self.w_gov * gov_penalty
        )
        cell.expected_free_energy = g_score
        return float(g_score)

    def optimize_allocations(self, cells: List[VentureCell], total_budget_cents: int) -> Dict[UUID, int]:
        """Solve multi-objective portfolio budget allocation subject to risk and capacity ceilings."""
        if not cells:
            return {}

        total_score = 0.0
        priorities = {}
        for cell in cells:
            score = max(0.1, cell.expected_free_energy + cell.capital_allocation_score)
            if cell.risk > 0.7:
                score *= 0.1

            priorities[cell.cell_id] = score
            total_score += score

        allocations = {}
        remaining_budget = total_budget_cents

        for cell in cells:
            priority = priorities[cell.cell_id]
            share = priority / total_score
            allocated_cents = int(total_budget_cents * share)

            if cell.risk > 0.5:
                max_cap = int(0.20 * total_budget_cents)
                if allocated_cents > max_cap:
                    allocated_cents = max_cap

            allocations[cell.cell_id] = allocated_cents
            remaining_budget -= allocated_cents

        if remaining_budget > 0 and cells:
            highest_priority_id = max(priorities, key=lambda k: priorities[k])
            allocations[highest_priority_id] += remaining_budget

        return allocations

    # ------------------------------------------------------------------
    # Epistemic Risk Query Layers (Formal Spec §5 & §7)
    # ------------------------------------------------------------------
    def flag_high_impact_low_evidence(self, hypotheses: List[Hypothesis]) -> List[Hypothesis]:
        """Query layer to identify unproven high-impact assumptions (Formal Spec §5.2)."""
        flagged = []
        for h in hypotheses:
            evidence_count = len(h.supporting_evidence) + len(h.contradicting_evidence)
            # High impact: downstream_decisions >= 3, low evidence: evidence_count <= 1
            if len(h.downstream_decisions) >= 3 and evidence_count <= 1:
                h.high_impact_low_evidence_flag = True
                flagged.append(h)
                logger.warning(f"EPISTEMIC RISK: Flagged high-impact low-evidence node: {h.hypothesis_id}")
        return flagged

    def assumption_depth(self, hyp: Hypothesis, kos_dict: Dict[str, Hypothesis]) -> int:
        """Recursively count the unproven dependency depth of a given hypothesis (Formal Spec §5.3)."""
        if not hyp.dependent_hypotheses:
            return 0

        max_depth = 0
        for dep_id in hyp.dependent_hypotheses:
            dep_hyp = kos_dict.get(dep_id)
            if dep_hyp and dep_hyp.status != "theory_promoted":
                depth = 1 + self.assumption_depth(dep_hyp, kos_dict)
                max_depth = max(max_depth, depth)

        return max_depth

    def ignorance_registry(self, hypotheses: List[Hypothesis]) -> Dict[str, Any]:
        """A view representing the system's own structural ignorance (Formal Spec §5.5)."""
        high_impact = self.flag_high_impact_low_evidence(hypotheses)
        sparse_domains = {}

        for h in hypotheses:
            evidence_count = len(h.supporting_evidence) + len(h.contradicting_evidence)
            if evidence_count < 2:
                if h.domain not in sparse_domains:
                    sparse_domains[h.domain] = []
                sparse_domains[h.domain].append(str(h.hypothesis_id))

        return {
            "high_impact_low_evidence": [str(h.hypothesis_id) for h in high_impact],
            "sparse_domains": sparse_domains
        }

    def audit_calibration(self) -> Dict[str, Any]:
        """Periodically audit calibration bounds to prevent overconfidence (Formal Spec §3.3 & §7.1)."""
        logger.info("Executing Calibration Audit over strategic decision records...")
        buckets: Dict[str, List[float]] = {"60-70": [], "70-80": [], "80-90": [], "90-100": []}

        # Aggregate decision outcomes by confidence
        for record in self.calibration_trail:
            conf = record.get("confidence", 0.5)
            realized = record.get("realized", False)
            val = 1.0 if realized else 0.0

            if 0.60 <= conf < 0.70:
                buckets["60-70"].append(val)
            elif 0.70 <= conf < 0.80:
                buckets["70-80"].append(val)
            elif 0.80 <= conf < 0.90:
                buckets["80-90"].append(val)
            elif 0.90 <= conf <= 1.00:
                buckets["90-100"].append(val)

        deviations = {}
        for b_name, vals in buckets.items():
            if vals:
                realized_rate = sum(vals) / len(vals)
                midpoint = (float(b_name.split("-")[0]) + float(b_name.split("-")[1])) / 200.0
                deviation = abs(realized_rate - midpoint)
                deviations[b_name] = {"realized_rate": realized_rate, "deviation": deviation}
                if deviation > 0.15:
                    logger.warning(f"CALIBRATION AUDIT FAULT: Bucket {b_name} miscalibration {deviation:.2%} exceeds 15% threshold!")
            else:
                deviations[b_name] = {"realized_rate": None, "deviation": 0.0}

        return deviations

    # ------------------------------------------------------------------
    # EIOS Strategic Mathematical Proof Implementations (Section 8)
    # ------------------------------------------------------------------
    def calculate_ebbinghaus_memory_decay(self, initial_confidence: float, time_elapsed_days: float, decay_constant: float = 0.05) -> float:
        """Calculate confidence retention parameter using Ebbinghaus exponential forgetting curve (Section 8.3).

        Formula: confidence_t = confidence_0 * exp(-lambda * t)
        """
        decayed = initial_confidence * math.exp(-decay_constant * time_elapsed_days)
        logger.info(f"Ebbinghaus memory decay: Initial={initial_confidence:.4f}, Days={time_elapsed_days}, Decayed={decayed:.4f}")
        return max(0.0, min(1.0, decayed))

    def detect_regime_change(self, prior_entropy: float, observed_entropy: float, threshold: float = 0.5) -> Dict[str, Any]:
        """Differentiate local parameter offset from a structural regime change using Bayesian Surprise (Section 8.4).

        Calculates simple divergence: Surprise = abs(observed_entropy - prior_entropy)
        """
        surprise = abs(observed_entropy - prior_entropy)
        is_regime_change = surprise >= threshold
        action_directive = "STRUCTURE_RE_SYNTHESIS" if is_regime_change else "PARAMETER_TUNING"

        logger.info(f"Regime detection: surprise={surprise:.4f}, threshold={threshold}, directive={action_directive}")
        return {
            "surprise": surprise,
            "is_regime_change": is_regime_change,
            "action_directive": action_directive
        }

    def vessel_depressurization_protocol(self, hazard_rate: float, threshold: float = 0.8) -> Dict[str, Any]:
        """Stochastic hazard protocol for organizational death prevention (Section 8.15).

        If hazard rate crosses safety threshold, locks down assets and scales back burn to zero.
        """
        is_critical = hazard_rate >= threshold
        state = "VESSEL_DEPRESSURIZED_ASSETS_SECURED" if is_critical else "NOMINAL_EXPLORATION"
        allocation_factor = 0.0 if is_critical else 1.0

        logger.warning(f"Vessel depressurization audit: hazard={hazard_rate:.2%}, state={state}, allocation_factor={allocation_factor:.2%}")
        return {
            "is_critical": is_critical,
            "state": state,
            "allocation_factor": allocation_factor
        }

    def score_originality(self, novelty_kl_divergence: float, expected_utility: float) -> float:
        """Score proposal originality as the product of structural novelty and expected utility (Section 8.12).

        Formula: Originality = Novelty_KL * Utility
        """
        originality = novelty_kl_divergence * max(0.0, expected_utility)
        logger.info(f"Originality score: Novelty={novelty_kl_divergence:.4f}, Utility={expected_utility:.4f}, Score={originality:.4f}")
        return max(0.0, originality)
