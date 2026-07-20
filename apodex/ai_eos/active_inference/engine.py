"""Active Inference & Executive Optimization Layer implementation for AI-EOS.

Solves constrained multi-objective optimizations and executes Bayesian belief updating
to balance exploitation utility and epistemic exploration.
"""

from __future__ import annotations
import math
import logging
from typing import Any, Dict, List, Optional
from uuid import UUID

from ..domain.models import VentureCell
from ..interfaces.services import IExecutiveOptimizer

logger = logging.getLogger("ai_eos.executive")


class ExecutiveOptimizer(IExecutiveOptimizer):
    """The multi-objective optimizer and active inference engine of AI-EOS."""

    def __init__(self, w_risk: float = 1.5, w_compute: float = 0.5, w_info: float = 2.0, w_gov: float = 3.0) -> None:
        self.w_risk = w_risk
        self.w_compute = w_compute
        self.w_info = w_info
        self.w_gov = w_gov

    def update_beliefs(self, cell: VentureCell, actual_revenue: int, expected_revenue: int) -> VentureCell:
        """Execute Bayesian update of belief states based on observation prediction errors."""
        # Calculate prediction error
        pred_error = float(actual_revenue - expected_revenue)
        cell.prediction_error = pred_error

        # Retrieve or initialize beta-prior parameters representing conversion/success probability
        prior_alpha = float(cell.belief_state.get("alpha", 10.0))
        prior_beta = float(cell.belief_state.get("beta", 10.0))

        # Conjugate update: If actual >= expected, increment alpha (successes), else beta (failures)
        if actual_revenue >= expected_revenue:
            updated_alpha = prior_alpha + 1.0
            updated_beta = prior_beta
        else:
            updated_alpha = prior_alpha
            updated_beta = prior_beta + 1.0

        # Update belief state
        cell.belief_state["alpha"] = updated_alpha
        cell.belief_state["beta"] = updated_beta

        # Compute new uncertainty as Shannon Entropy of the updated Beta distribution (approximation)
        sum_ab = updated_alpha + updated_beta
        mean = updated_alpha / sum_ab
        entropy = - (mean * math.log(max(1e-5, mean)) + (1.0 - mean) * math.log(max(1e-5, 1.0 - mean)))

        # Predicted reduction in belief entropy (Information Gain)
        old_entropy = cell.uncertainty
        cell.uncertainty = float(entropy)
        cell.information_gain = max(0.0, old_entropy - entropy)

        # Update confidence based on inverse variance
        variance = (updated_alpha * updated_beta) / ((sum_ab ** 2) * (sum_ab + 1.0))
        cell.confidence = min(1.0, max(0.0, 1.0 - 4.0 * variance)) # normalized confidence

        logger.info(f"Bayesian update completed for cell {cell.name}: Prediction Error = {pred_error}, Uncertainty = {cell.uncertainty:.4f}, Confidence = {cell.confidence:.4f}")
        return cell

    def compute_composite_objective(self, cell: VentureCell, policy_expected_utility: float, policy_risk: float) -> float:
        """Calculate composite objective G.

        G = EconomicUtility - w_risk * RiskPenalty - w_compute * ComputeCost + w_info * InformationGain - w_gov * GovernancePenalty
        """
        risk_penalty = float(policy_risk)
        compute_cost = 0.1 * len(cell.sub_agent_ids)  # linear scaling of cost with agent size
        info_gain = float(cell.information_gain)
        gov_penalty = 5.0 if cell.risk > 0.8 else 0.0  # high risk triggers governance penalties

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

        # 1. Compute priority score for each cell
        total_score = 0.0
        priorities = {}
        for cell in cells:
            # Active priority combines expected free energy and capital allocation score
            score = max(0.1, cell.expected_free_energy + cell.capital_allocation_score)

            # Risk Gate: If risk exceeds the threshold, severely penalize and cap allocation
            if cell.risk > 0.7:
                score *= 0.1

            priorities[cell.cell_id] = score
            total_score += score

        # 2. Proportional allocation
        allocations = {}
        remaining_budget = total_budget_cents

        for cell in cells:
            priority = priorities[cell.cell_id]
            share = priority / total_score
            allocated_cents = int(total_budget_cents * share)

            # Risk Cap: Cells with high risk (risk > 0.5) cannot receive more than 20% of total budget
            if cell.risk > 0.5:
                max_cap = int(0.20 * total_budget_cents)
                if allocated_cents > max_cap:
                    allocated_cents = max_cap

            allocations[cell.cell_id] = allocated_cents
            remaining_budget -= allocated_cents

        # Distribute any rounding dust to the highest priority cell
        if remaining_budget > 0 and cells:
            highest_priority_id = max(priorities, key=lambda k: priorities[k])
            allocations[highest_priority_id] += remaining_budget

        # Log allocation results
        for cell_id, cents in allocations.items():
            cell_obj = next(c for c in cells if c.cell_id == cell_id)
            logger.info(f"Optimized capital allocated to cell {cell_obj.name}: ${cents/100:.2f}")

        return allocations
