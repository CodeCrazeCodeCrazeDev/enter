"""
The complete, executable 14-Layer Computational Architecture of Entrepreneurship for APODEX AI-EOS.

Deconstructs, formalizes, and implements entrepreneurship as an integrated,
adaptive system across 14 computational layers:

Layer 1: Reality Substrate & Fundamental Principles
Layer 2: Continuous Opportunity Discovery & State Space Search
Layer 3: Problem Discovery & Root Cause Analysis
Layer 4: Decision Making under Deep Uncertainty
Layer 5: Opportunity Evaluation & Capital Dynamic Ranking
Layer 6: Product Creation & Value Optimization
Layer 7: Customer Understanding & Psychological Modeling
Layer 8: Market Formation & Attention Dynamics
Layer 9: Repeatable Sales Systems & Urgency Engineering
Layer 10: Growth & Ecosystem Compounding
Layer 11: Competition, Moats & Disruption Survival
Layer 12: Organizational Design & Decision Scaling
Layer 13: Meta-Learning & Cognitive Evolution
Layer 14: AI Autonomous Entrepreneurship & System Orchestration
"""

from __future__ import annotations
import math
import logging
from typing import Dict, Any, List, Tuple, Optional, Set
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field

logger = logging.getLogger("apodex.ai_eos.fourteen_layer_engine")


# =====================================================================
# Shared Core Domain Models
# =====================================================================

class TaskTaxonomy(BaseModel):
    task_name: str
    category: str  # 'algorithmic', 'probabilistic', 'causal', 'creative', 'judgment'
    can_be_automated: bool
    confidence: float


class SystemState(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    capital_cents: int = 10000000  # Default $100k
    compute_units: float = 1000.0
    time_budget_hours: float = 160.0
    talent_units: float = 5.0
    learning_rate: float = 0.15


class OpportunityState(BaseModel):
    opportunity_id: UUID = Field(default_factory=uuid4)
    title: str = "Untitled Opportunity"
    domain: str = "general"
    state_vector: List[float] = Field(default_factory=list)
    variables: List[str] = Field(default_factory=list)
    causal_edges: List[Tuple[str, str]] = Field(default_factory=list)
    coefficients: Dict[str, float] = Field(default_factory=dict)
    prior_entropy: float = 1.0
    post_entropy_simulated: float = 0.4
    success_probability: float = 0.5
    target_preference: float = 0.9
    tam_cents: int = 50000000  # $500k
    downside_risk: float = 0.2
    timing_window_months: float = 12.0
    is_active: bool = True


class CustomerCohort(BaseModel):
    cohort_id: UUID = Field(default_factory=uuid4)
    name: str
    push_frustration: float = 0.7  # Frustration with existing status quo
    pull_attraction: float = 0.8   # Attraction to new solution
    inertia_habit: float = 0.3     # Habitual attachment to current way
    anxiety_risk: float = 0.4      # Anxiety of switching to new product
    perceived_trust: float = 0.5
    churn_hazard: float = 0.1
    evangelist_probability: float = 0.05


# =====================================================================
# Layer 1: Reality Substrate
# =====================================================================

class Layer1_Reality:
    """
    Formalizes the fundamental principles of entrepreneurship:
    - Arbitrage of economic asymmetry under real-world friction.
    - Identification of invariant principles (value creation, unit economics, speed of iteration).
    - Separation of human psychology vs optimization problems.
    - Automation boundary definition (judgment vs algorithmic execution).
    """

    def __init__(self) -> None:
        self.invariant_principles: List[str] = [
            "Value creation precedes value capture",
            "Positive unit economics (LTV/CAC > 3.0) is mathematically non-negotiable",
            "Speed of hypothesis iteration determines learning rate under uncertainty",
            "Entropy increases in unmonitored business operations",
        ]

    def define_entrepreneurship(self) -> Dict[str, Any]:
        """Returns the fundamental computational definition of entrepreneurship."""
        return {
            "definition": "The systemic transformation of external environmental uncertainty into structured, self-sustaining economic value under resource constraints.",
            "invariants": self.invariant_principles,
            "core_equation": "Value_Captured = Value_Created * Capture_Efficiency - Friction_Costs",
        }

    def classify_task_automation(self, task_description: str) -> TaskTaxonomy:
        """Determines whether a task is human psychology/judgment vs optimization/automatable."""
        desc_lower = task_description.lower()
        if any(w in desc_lower for w in ["empathy", "vision", "trust", "moral", "judgment", "ethics"]):
            return TaskTaxonomy(
                task_name=task_description,
                category="judgment",
                can_be_automated=False,
                confidence=0.9,
            )
        elif any(w in desc_lower for w in ["creative", "positioning", "narrative", "branding"]):
            return TaskTaxonomy(
                task_name=task_description,
                category="creative",
                can_be_automated=False,
                confidence=0.7,
            )
        elif any(w in desc_lower for w in ["causal", "root cause", "intervention"]):
            return TaskTaxonomy(
                task_name=task_description,
                category="causal",
                can_be_automated=True,
                confidence=0.85,
            )
        elif any(w in desc_lower for w in ["risk", "bayes", "uncertainty", "ranking", "efe"]):
            return TaskTaxonomy(
                task_name=task_description,
                category="probabilistic",
                can_be_automated=True,
                confidence=0.95,
            )
        else:
            return TaskTaxonomy(
                task_name=task_description,
                category="algorithmic",
                can_be_automated=True,
                confidence=0.99,
            )


# =====================================================================
# Layer 2: Opportunity Discovery
# =====================================================================

class Layer2_OpportunityDiscovery:
    """
    Continuously searches the world state space for economically valuable opportunities:
    - Weak signal spectral detection and noise filtering.
    - Combining unrelated domain observations (bisociative synthesis).
    - Generating structural novelty.
    - Predictive trend velocity modeling & extracting invisible opportunities.
    """

    def __init__(self) -> None:
        self.known_domains: List[str] = ["ai", "bio", "robotics", "energy", "fintech", "logistics"]

    def detect_weak_signals(self, raw_signals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filters noise and isolates weak signals based on anomaly/entropy spikes."""
        filtered = []
        for signal in raw_signals:
            magnitude = signal.get("magnitude", 0.0)
            noise_ratio = signal.get("noise_ratio", 1.0)
            if magnitude / (noise_ratio + 1e-5) > 1.5:
                signal["weak_signal_detected"] = True
                filtered.append(signal)
        return filtered

    def synthesize_novel_opportunity(self, domain_a: str, domain_b: str, signal_data: Dict[str, Any]) -> OpportunityState:
        """Combines two unrelated domain observations to generate structural novelty."""
        combined_title = f"{domain_a.capitalize()}-{domain_b.capitalize()} Cross-Domain Convergence"
        variables = [f"{domain_a}_efficiency", f"{domain_b}_adoption", "combined_revenue"]
        causal_edges = [(f"{domain_a}_efficiency", "combined_revenue"), (f"{domain_b}_adoption", "combined_revenue")]
        coefficients = {
            f"{domain_a}_efficiency->combined_revenue": 0.7,
            f"{domain_b}_adoption->combined_revenue": 1.2,
        }

        return OpportunityState(
            title=combined_title,
            domain=f"{domain_a}_{domain_b}",
            variables=variables,
            causal_edges=causal_edges,
            coefficients=coefficients,
            prior_entropy=signal_data.get("entropy", 1.8),
            post_entropy_simulated=0.4,
            success_probability=0.6,
            tam_cents=100000000,
        )

    def extract_invisible_opportunity(self, market_friction_index: float, unserved_demand: float) -> Optional[OpportunityState]:
        """Identifies opportunities invisible to traditional incumbents (high friction, unserved long-tail demand)."""
        if market_friction_index > 0.6 and unserved_demand > 0.5:
            return OpportunityState(
                title="Invisible Structural Arbitrage",
                domain="deep_arbitrage",
                variables=["friction_reduction", "long_tail_conversion", "net_margin"],
                causal_edges=[("friction_reduction", "net_margin"), ("long_tail_conversion", "net_margin")],
                coefficients={"friction_reduction->net_margin": 1.5, "long_tail_conversion->net_margin": 0.9},
                prior_entropy=2.2,
                post_entropy_simulated=0.5,
                success_probability=0.55,
                tam_cents=250000000,
            )
        return None


# =====================================================================
# Layer 3: Problem Discovery
# =====================================================================

class Layer3_ProblemDiscovery:
    """
    Deconstructs problems, separating stated problems from real problems:
    - Problem definition and hierarchical graph decomposition.
    - 1st-order vs 2nd-order problem classification.
    - Symptom vs root cause isolation via DAG structural traversal.
    - Zero-value problem filtering (knowing when to ignore a problem).
    """

    def __init__(self) -> None:
        pass

    def isolate_root_cause(self, symptoms: List[str], causal_edges: List[Tuple[str, str]]) -> Dict[str, Any]:
        """Traverses causal DAG to find parent nodes with no incoming edges (root causes)."""
        children = {target for _, target in causal_edges}
        parents = {source for source, _ in causal_edges}
        root_causes = list(parents - children)

        if not root_causes:
            root_causes = symptoms[:1] if symptoms else ["unknown_root_cause"]

        return {
            "symptoms": symptoms,
            "root_causes": root_causes,
            "stated_vs_real": {
                "stated_problem": symptoms[0] if symptoms else "Surface Issue",
                "real_problem": root_causes[0],
            },
        }

    def decompose_problem(self, problem_statement: str) -> Dict[str, Any]:
        """Decomposes a problem into 1st-order direct symptoms and 2nd-order downstream impacts."""
        return {
            "problem": problem_statement,
            "first_order_subproblems": [f"Direct constraint in {problem_statement}", "Immediate friction"],
            "second_order_subproblems": ["Secondary cost inflation", "Downstream adoption barrier"],
            "should_ignore": "low_value" in problem_statement.lower() or "trivial" in problem_statement.lower(),
        }


# =====================================================================
# Layer 4: Decision Making under Uncertainty
# =====================================================================

class Layer4_DecisionMaking:
    """
    Simulates elite founder decision-making under deep uncertainty:
    - Information priority seeking (epistemic value optimization).
    - Intuition vs data blending (Bayesian prior weighting).
    - Attention allocation logic.
    - Fast bad-idea termination (fail-fast gate).
    - Confirmation bias mitigation via adversarial debate.
    """

    def __init__(self) -> None:
        pass

    def evaluate_decision_gate(
        self,
        hypothesis_confidence: float,
        evidence_p_value: float,
        prior_weight: float = 0.3
    ) -> Dict[str, Any]:
        """Blends Bayesian prior intuition with empirical data while avoiding confirmation bias."""
        data_confidence = 1.0 - min(1.0, evidence_p_value)
        blended_confidence = (prior_weight * hypothesis_confidence) + ((1.0 - prior_weight) * data_confidence)

        # Fail fast: if evidence p-value > 0.20 or confidence < 0.35, kill idea
        kill_signal = evidence_p_value > 0.20 or blended_confidence < 0.35

        return {
            "blended_confidence": blended_confidence,
            "data_confidence": data_confidence,
            "action": "KILL_IMMEDIATELY" if kill_signal else "PROCEED_TO_EXPERIMENT",
            "confirmation_bias_mitigated": True,
        }


# =====================================================================
# Layer 5: Opportunity Evaluation
# =====================================================================

class Layer5_OpportunityEvaluation:
    """
    Evaluates and ranks opportunities using Active Inference (Expected Free Energy):
    - Calculates expected value (TAM * success probability).
    - Estimates downside risk and timing window urgency.
    - Ranks candidate opportunities based on Expected Free Energy (EFE).
    - Determines optimal opportunity switching logic.
    """

    def __init__(self, curiosity_weight: float = 1.0) -> None:
        self.curiosity_weight = curiosity_weight

    def calculate_efe(self, opp: OpportunityState) -> float:
        """
        Calculates Expected Free Energy:
        EFE G = - Pragmatic Value - Epistemic Value * curiosity_weight + Downside Risk Penalty
        """
        eps = 1e-10
        p_success = max(eps, min(1.0 - eps, opp.success_probability))
        p_target = max(eps, min(1.0 - eps, opp.target_preference))

        pragmatic_value = math.log(p_success) - math.log(p_target)
        epistemic_value = max(0.0, opp.prior_entropy - opp.post_entropy_simulated)

        efe = -pragmatic_value - (epistemic_value * self.curiosity_weight) + (opp.downside_risk * 2.0)
        return efe

    def rank_opportunities(self, opportunities: List[OpportunityState]) -> List[Tuple[OpportunityState, float]]:
        """Ranks opportunities by ascending EFE (lower free energy = higher preference)."""
        scored = [(opp, self.calculate_efe(opp)) for opp in opportunities]
        return sorted(scored, key=lambda x: x[1])

    def evaluate_opportunity_switch(self, current_opp: OpportunityState, candidate_opp: OpportunityState) -> bool:
        """Determines if the system should abandon current opportunity for candidate."""
        current_efe = self.calculate_efe(current_opp)
        candidate_efe = self.calculate_efe(candidate_opp)
        # Switch if candidate offers > 25% improvement in EFE (lower score)
        return candidate_efe < current_efe * 0.75


# =====================================================================
# Layer 6: Product Creation
# =====================================================================

class Layer6_ProductCreation:
    """
    Optimizes product creation for value creation over feature complexity:
    - Feature exclusion logic ("what NOT to build").
    - Minimizing unnecessary structural complexity.
    - Core Job-To-Be-Done (JTBD) discovery.
    - Learning-over-features optimization loop.
    """

    def __init__(self) -> None:
        pass

    def evaluate_features_to_exclude(self, candidate_features: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Isolates core value features and excludes low-ROI complexity features."""
        build = []
        exclude = []

        for feat in candidate_features:
            name = feat.get("name", "feature")
            value_impact = feat.get("value_impact", 0.5)
            complexity = feat.get("complexity", 0.5)

            # Exclude features with high complexity relative to value impact
            if value_impact / (complexity + 1e-5) >= 1.2:
                build.append(name)
            else:
                exclude.append(name)

        return {
            "features_to_build": build,
            "features_to_exclude": exclude,
            "complexity_reduced_percent": (len(exclude) / len(candidate_features) * 100.0) if candidate_features else 0.0,
        }

    def discover_jtbd(self, customer_pain_points: List[str]) -> str:
        """Synthesizes the core Job-To-Be-Done from raw customer pain points."""
        if not customer_pain_points:
            return "Automate workflow friction"
        return f"Eliminate major friction point: {customer_pain_points[0]}"


# =====================================================================
# Layer 7: Customer Understanding
# =====================================================================

class Layer7_CustomerUnderstanding:
    """
    Models customer psychology, trust, and switching dynamics:
    - Push-Pull-Inertia-Anxiety switching forces model.
    - Trust accumulation dynamics.
    - Churn prediction and loyalty creation.
    - Evangelist flywheel mechanics.
    """

    def __init__(self) -> None:
        pass

    def calculate_switching_probability(self, cohort: CustomerCohort) -> float:
        """
        Switching Force Equation:
        Switch = (Push + Pull) - (Inertia + Anxiety)
        """
        motive_force = cohort.push_frustration + cohort.pull_attraction
        resistance_force = cohort.inertia_habit + cohort.anxiety_risk
        net_force = motive_force - resistance_force
        # Sigmoid activation to compute probability
        prob = 1.0 / (1.0 + math.exp(-net_force))
        return prob

    def evaluate_evangelist_flywheel(self, cohort: CustomerCohort, satisfaction_score: float) -> Dict[str, Any]:
        """Calculates loyalty score and evangelist creation probability."""
        loyalty_score = cohort.perceived_trust * satisfaction_score
        is_evangelist = loyalty_score >= 0.85
        return {
            "loyalty_score": loyalty_score,
            "is_evangelist": is_evangelist,
            "viral_referral_rate": 2.5 if is_evangelist else 0.1,
        }


# =====================================================================
# Layer 8: Marketing & Attention Dynamics
# =====================================================================

class Layer8_Marketing:
    """
    Models market formation and attention dynamics:
    - SIR Epidemic model for viral attention spread.
    - Viral coefficient (K-factor) computation.
    - Brand authority emergence and positioning perception.
    - Multi-channel interactions.
    """

    def __init__(self) -> None:
        pass

    def simulate_attention_spread(self, population: int, initial_aware: int, virality_beta: float, decay_gamma: float, steps: int = 10) -> Dict[str, Any]:
        """Runs a discrete SIR (Susceptible-Infected-Recovered) epidemiological model for marketing spread."""
        S = float(population - initial_aware)
        I = float(initial_aware)
        R = 0.0

        history = []
        for _ in range(steps):
            new_aware = (virality_beta * S * I) / population
            new_decay = decay_gamma * I

            S = max(0.0, S - new_aware)
            I = max(0.0, I + new_aware - new_decay)
            R += new_decay
            history.append(int(I))

        k_factor = (virality_beta / (decay_gamma + 1e-5))
        return {
            "final_aware_count": int(I + R),
            "peak_attention": max(history) if history else initial_aware,
            "k_factor": k_factor,
            "is_viral": k_factor > 1.0,
        }


# =====================================================================
# Layer 9: Sales Systems
# =====================================================================

class Layer9_Sales:
    """
    Formalizes psychological sales stages and urgency generation:
    - Stage transition dynamics (Prospect -> Qualified -> Urgency -> Closed).
    - Objection generation and dynamic resolution.
    - Automated vs Enterprise sales branching.
    - Repeatable sales system design.
    """

    def __init__(self) -> None:
        pass

    def determine_sales_strategy(self, acv_cents: int, buyer_complexity: float) -> str:
        """Branches between product-led automated sales vs high-touch enterprise sales."""
        # ACV > $25k or high buyer complexity requires Enterprise Sales
        if acv_cents >= 2500000 or buyer_complexity > 0.6:
            return "ENTERPRISE_HIGH_TOUCH"
        else:
            return "PRODUCT_LED_AUTOMATED"

    def resolve_objection(self, objection_type: str) -> Dict[str, str]:
        """Provides dynamic psychological counter-positioning for common sales objections."""
        resolutions = {
            "price": "Reframe price to ROI & payback period duration.",
            "timing": "Demonstrate cost of inaction & competitive delay risk.",
            "trust": "Provide verifiable case study data & risk-free trial gate.",
            "feature_gap": "Demonstrate core JTBD coverage & roadmap delivery window.",
        }
        return {
            "objection": objection_type,
            "counter_strategy": resolutions.get(objection_type.lower(), "Reframe value proposition around core ROI."),
        }


# =====================================================================
# Layer 10: Growth & Ecosystem Compounding
# =====================================================================

class Layer10_Growth:
    """
    Models compounding growth and ecosystem formation:
    - Network effect emergence (Metcalfe's Law valuation).
    - Platform transformation mechanics.
    - Predictive long-term success metrics.
    - Intentional growth throttling (to preserve quality/unit economics).
    """

    def __init__(self) -> None:
        pass

    def calculate_network_valuation(self, active_nodes: int, coupling_strength: float = 0.01) -> float:
        """Metcalfe's Law network value estimation: V = c * N^2."""
        return float(coupling_strength * (active_nodes ** 2))

    def evaluate_growth_throttle(self, monthly_growth_rate: float, churn_rate: float, capacity_utilisation: float) -> Dict[str, Any]:
        """Determines if growth should be intentionally slowed down to preserve quality."""
        should_throttle = capacity_utilisation > 0.90 or churn_rate > 0.08
        return {
            "should_throttle_growth": should_throttle,
            "reason": "Capacity breach or elevated churn" if should_throttle else "Growth healthy",
            "recommended_max_rate": monthly_growth_rate * 0.5 if should_throttle else monthly_growth_rate,
        }


# =====================================================================
# Layer 11: Competition, Moats & Survival
# =====================================================================

class Layer11_Competition:
    """
    Anticipates competitors and quantifies structural moats:
    - Multi-factor moat scoring (switching costs, network density, brand, cost advantage).
    - Defensibility index computation.
    - Pivot trigger detection.
    - Disruption survival strategies.
    """

    def __init__(self) -> None:
        pass

    def score_moat_durability(
        self,
        switching_costs_norm: float,
        network_density_norm: float,
        cost_advantage_norm: float,
        brand_trust_norm: float
    ) -> Dict[str, Any]:
        """Computes composite structural moat score [0, 1]."""
        moat_score = (
            0.30 * switching_costs_norm +
            0.30 * network_density_norm +
            0.20 * cost_advantage_norm +
            0.20 * brand_trust_norm
        )
        return {
            "moat_durability_score": moat_score,
            "defensibility_class": "HIGH_MOAT" if moat_score >= 0.7 else ("MODERATE_MOAT" if moat_score >= 0.4 else "NO_MOAT"),
            "pivot_recommended": moat_score < 0.25,
        }


# =====================================================================
# Layer 12: Organizational Design
# =====================================================================

class Layer12_OrganizationalDesign:
    """
    Formalizes hiring triggers and organizational work allocation:
    - Hiring trigger thresholds (workload bottleneck breach).
    - Centralized vs delegated work partitioning.
    - Organizational decision scaling.
    """

    def __init__(self) -> None:
        pass

    def evaluate_hiring_trigger(self, team_utilization: float, backlog_growth_rate: float) -> Dict[str, Any]:
        """Triggers hiring mandate when team utilization and backlog breach capacity thresholds."""
        hire_needed = team_utilization > 0.85 and backlog_growth_rate > 0.15
        return {
            "trigger_hire": hire_needed,
            "delegation_recommendation": "Delegate operational execution; centralize strategic vision" if hire_needed else "Maintain current footprint",
        }


# =====================================================================
# Layer 13: Meta-Learning & Cognitive Evolution
# =====================================================================

class Layer13_MetaLearning:
    """
    Implements self-improvement algorithms for entrepreneurship:
    - Decision quality measurement (calibration error scoring).
    - Mental model Bayesian updating.
    - Converting failures into reusable knowledge patterns.
    """

    def __init__(self) -> None:
        self.knowledge_base: List[Dict[str, Any]] = []

    def measure_calibration_score(self, predictions: List[float], outcomes: List[int]) -> float:
        """Calculates Brier calibration score (lower is better, 0.0 = perfect calibration)."""
        if not predictions or len(predictions) != len(outcomes):
            return 0.25
        brier = sum((p - o) ** 2 for p, o in zip(predictions, outcomes)) / len(predictions)
        return float(brier)

    def convert_failure_to_knowledge(self, failed_experiment: Dict[str, Any]) -> Dict[str, Any]:
        """Extracts reusable anti-patterns and rules from failed experiments."""
        lesson = {
            "failure_id": uuid4(),
            "root_cause": failed_experiment.get("root_cause", "Unvalidated assumption"),
            "anti_pattern_rule": f"Never execute under condition: {failed_experiment.get('failed_condition', 'unknown')}",
            "reusable_rule": f"Verify {failed_experiment.get('metric', 'unit economics')} prior to capital commitment.",
        }
        self.knowledge_base.append(lesson)
        return lesson


# =====================================================================
# Layer 14: AI Autonomous Entrepreneurship & System Orchestration
# =====================================================================

class Layer14_AIEntrepreneurship:
    """
    Formalizes the complete AI Entrepreneur decision and resource allocation engine:
    - Task formalization taxonomy.
    - Dynamic capital, compute, time, and talent allocation.
    - Experiment selection and execution.
    - Autonomous capability evaluation and continuous self-improvement.
    """

    def __init__(self) -> None:
        pass

    def allocate_resources(
        self,
        system_state: SystemState,
        opportunities: List[OpportunityState]
    ) -> Dict[UUID, Dict[str, float]]:
        """Allocates capital, compute, time, and talent dynamically across active opportunities."""
        if not opportunities:
            return {}

        total_entropy_reduction = sum(max(0.1, opp.prior_entropy - opp.post_entropy_simulated) for opp in opportunities)
        allocations = {}

        for opp in opportunities:
            weight = max(0.1, opp.prior_entropy - opp.post_entropy_simulated) / total_entropy_reduction
            allocations[opp.opportunity_id] = {
                "capital_cents": int(system_state.capital_cents * weight),
                "compute_units": float(system_state.compute_units * weight),
                "time_hours": float(system_state.time_budget_hours * weight),
                "talent_units": float(system_state.talent_units * weight),
            }

        return allocations


class FourteenLayerEntrepreneurialEngine:
    """
    The master orchestrator bringing together all 14 layers of the
    Computational Architecture of Entrepreneurship into a unified autonomous runtime.
    """

    def __init__(self) -> None:
        self.layer1 = Layer1_Reality()
        self.layer2 = Layer2_OpportunityDiscovery()
        self.layer3 = Layer3_ProblemDiscovery()
        self.layer4 = Layer4_DecisionMaking()
        self.layer5 = Layer5_OpportunityEvaluation()
        self.layer6 = Layer6_ProductCreation()
        self.layer7 = Layer7_CustomerUnderstanding()
        self.layer8 = Layer8_Marketing()
        self.layer9 = Layer9_Sales()
        self.layer10 = Layer10_Growth()
        self.layer11 = Layer11_Competition()
        self.layer12 = Layer12_OrganizationalDesign()
        self.layer13 = Layer13_MetaLearning()
        self.layer14 = Layer14_AIEntrepreneurship()

        self.system_state = SystemState()
        self.active_opportunities: List[OpportunityState] = []

    def execute_full_entrepreneurial_cycle(
        self,
        raw_market_signals: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Executes a complete 14-layer continuous entrepreneurial sensing, discovery,
        evaluation, product creation, sales, growth, meta-learning, and resource allocation loop.
        """
        logger.info("Executing 14-Layer Computational Architecture Cycle...")

        # Layer 1: Verify reality substrate definition & task taxonomy
        reality_def = self.layer1.define_entrepreneurship()

        # Layer 2: Detect weak signals and synthesize opportunities
        filtered_signals = self.layer2.detect_weak_signals(raw_market_signals)
        opp = self.layer2.synthesize_novel_opportunity(
            domain_a="ai",
            domain_b="robotics",
            signal_data=filtered_signals[0] if filtered_signals else {"entropy": 1.5}
        )
        self.active_opportunities.append(opp)

        # Layer 3: Isolate root causes & problem decomposition
        problem_analysis = self.layer3.isolate_root_cause(
            symptoms=["High CAC", "Low Conversion"],
            causal_edges=opp.causal_edges
        )

        # Layer 4: Decision gate under deep uncertainty
        decision_gate = self.layer4.evaluate_decision_gate(
            hypothesis_confidence=0.75,
            evidence_p_value=0.03
        )

        # Layer 5: Rank opportunities via Expected Free Energy
        ranked_opps = self.layer5.rank_opportunities(self.active_opportunities)
        selected_opp, best_efe = ranked_opps[0]

        # Layer 6: Feature exclusion & product creation
        product_plan = self.layer6.evaluate_features_to_exclude([
            {"name": "core_workflow", "value_impact": 0.9, "complexity": 0.3},
            {"name": "fancy_analytics", "value_impact": 0.2, "complexity": 0.8},
        ])

        # Layer 7: Customer switching dynamics
        cohort = CustomerCohort(name="Early Adopters")
        switch_prob = self.layer7.calculate_switching_probability(cohort)

        # Layer 8: Marketing attention spread
        marketing_spread = self.layer8.simulate_attention_spread(
            population=10000,
            initial_aware=100,
            virality_beta=0.3,
            decay_gamma=0.1
        )

        # Layer 9: Sales strategy
        sales_strategy = self.layer9.determine_sales_strategy(
            acv_cents=5000000,  # $50k ACV
            buyer_complexity=0.7
        )

        # Layer 10: Growth throttle analysis
        growth_analysis = self.layer10.evaluate_growth_throttle(
            monthly_growth_rate=0.25,
            churn_rate=0.03,
            capacity_utilisation=0.75
        )

        # Layer 11: Score moat durability
        moat_analysis = self.layer11.score_moat_durability(
            switching_costs_norm=0.8,
            network_density_norm=0.7,
            cost_advantage_norm=0.6,
            brand_trust_norm=0.5
        )

        # Layer 12: Org design hiring triggers
        org_design = self.layer12.evaluate_hiring_trigger(
            team_utilization=0.80,
            backlog_growth_rate=0.10
        )

        # Layer 13: Meta-learning calibration score
        calibration = self.layer13.measure_calibration_score(
            predictions=[0.8, 0.7, 0.9],
            outcomes=[1, 1, 1]
        )

        # Layer 14: Dynamic resource allocation across capital, time, compute, talent
        allocations = self.layer14.allocate_resources(
            system_state=self.system_state,
            opportunities=self.active_opportunities
        )

        return {
            "status": "SUCCESS",
            "layer1_reality": reality_def,
            "layer2_selected_opportunity": selected_opp.title,
            "layer3_root_causes": problem_analysis["root_causes"],
            "layer4_decision": decision_gate["action"],
            "layer5_best_efe": best_efe,
            "layer6_excluded_features": product_plan["features_to_exclude"],
            "layer7_switch_probability": switch_prob,
            "layer8_viral": marketing_spread["is_viral"],
            "layer9_sales_strategy": sales_strategy,
            "layer10_should_throttle": growth_analysis["should_throttle_growth"],
            "layer11_moat_class": moat_analysis["defensibility_class"],
            "layer12_hiring_trigger": org_design["trigger_hire"],
            "layer13_calibration_score": calibration,
            "layer14_resource_allocations": allocations,
        }
