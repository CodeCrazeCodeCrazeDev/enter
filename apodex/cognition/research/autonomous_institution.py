from __future__ import annotations
import math
import logging
import random
from typing import Dict, Any, List, Optional, Tuple
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

logger = logging.getLogger("apodex.cognition.research")


class ResearchHypothesis(BaseModel):
    """Represents a scientific hypothesis to be evaluated."""
    hypothesis_id: UUID = Field(default_factory=uuid4)
    name: str
    description: str
    prior_probability: float = 0.5
    evidence_quality: float = 0.0


class BeliefState(BaseModel):
    """Represents the parameters of the conjugate Beta-Binomial model for a hypothesis."""
    alpha: float
    beta: float
    last_updated_timestamp: float


class ExpectedFreeEnergyPlanner:
    """
    Implements Karl Friston's Active Inference planning framework.
    Selects policies by minimizing Expected Free Energy (EFE), balancing
    Instrumental Value (pragmatic goal achievement) and Epistemic Value (information gain).
    """

    def __init__(self, curiosity_weight: float = 1.0) -> None:
        self.curiosity_weight = curiosity_weight

    def calculate_epistemic_value(self, prior_entropy: float, expected_posterior_entropy: float) -> float:
        """
        Epistemic Value is the Expected Information Gain, modeled as the expected
        reduction in uncertainty (entropy reduction) between prior and posterior states.
        """
        return max(0.0, prior_entropy - expected_posterior_entropy)

    def calculate_instrumental_value(self, predicted_outcome_prob: float, target_preference: float) -> float:
        """
        Instrumental Value is the negative divergence between predicted outcomes and target preferences.
        """
        if predicted_outcome_prob <= 0.0:
            return -100.0
        return math.log(predicted_outcome_prob) - math.log(target_preference)

    def select_optimal_policy(
        self,
        candidate_policies: List[Dict[str, Any]]
    ) -> Tuple[Dict[str, Any], float]:
        """
        Selects the policy that minimizes Expected Free Energy (minimizing G implies maximizing utility):
        G = - Instrumental_Value - Epistemic_Value * curiosity_weight
        """
        best_policy = None
        min_efe = float("inf")

        for policy in candidate_policies:
            prior_entropy = policy.get("prior_entropy", 1.0)
            post_entropy = policy.get("post_entropy", 0.5)
            predicted_prob = policy.get("predicted_prob", 0.8)
            target_pref = policy.get("target_pref", 0.9)

            epistemic = self.calculate_epistemic_value(prior_entropy, post_entropy)
            instrumental = self.calculate_instrumental_value(predicted_prob, target_pref)

            efe = -instrumental - (epistemic * self.curiosity_weight)

            policy["calculated_epistemic"] = epistemic
            policy["calculated_instrumental"] = instrumental
            policy["calculated_efe"] = efe

            if efe < min_efe:
                min_efe = efe
                best_policy = policy

        return best_policy or candidate_policies[0], min_efe


class StructuralCausalModel:
    """
    Represents structural causal models (SCMs) and Pearl's causal intervention calculus (do-calculus).
    """

    def __init__(self) -> None:
        self.variables: List[str] = []
        self.causal_graph: Dict[str, List[str]] = {}
        self.coefficients: Dict[Tuple[str, str], float] = {}

    def add_variable(self, name: str) -> None:
        if name not in self.variables:
            self.variables.append(name)

    def add_causal_link(self, source: str, target: str, weight: float = 0.5) -> None:
        self.add_variable(source)
        self.add_variable(target)
        if target not in self.causal_graph:
            self.causal_graph[target] = []
        if source not in self.causal_graph[target]:
            self.causal_graph[target].append(source)
        self.coefficients[(source, target)] = weight

    def intervene_do(self, variable: str, value: float) -> Dict[str, float]:
        """Simulates Judea Pearl's do-operator."""
        values: Dict[str, float] = {v: 0.0 for v in self.variables}
        values[variable] = value

        for _ in range(len(self.variables)):
            for child in self.variables:
                if child == variable:
                    continue
                parents = self.causal_graph.get(child, [])
                if not parents:
                    continue
                child_val = 0.0
                for parent in parents:
                    coef = self.coefficients.get((parent, child), 0.0)
                    child_val += coef * values[parent]
                values[child] = child_val

        return values


class EbbinghausMemoryConsolidator:
    """
    Implements Bayesian posterior updates under a Beta-Binomial conjugate model,
    with an exponential decay function based on the Ebbinghaus Forgetting Curve.
    """

    def __init__(self, decay_rate: float = 0.01) -> None:
        self.decay_rate = decay_rate

    def consolidate_belief(
        self,
        current_belief: BeliefState,
        trials: int,
        successes: int,
        current_timestamp: float
    ) -> BeliefState:
        delta_t = max(0.0, current_timestamp - current_belief.last_updated_timestamp)
        decay_factor = math.exp(-self.decay_rate * delta_t)

        decayed_alpha_excess = (current_belief.alpha - 1.0) * decay_factor
        decayed_beta_excess = (current_belief.beta - 1.0) * decay_factor

        new_alpha = 1.0 + decayed_alpha_excess + successes
        new_beta = 1.0 + decayed_beta_excess + (trials - successes)

        return BeliefState(
            alpha=new_alpha,
            beta=new_beta,
            last_updated_timestamp=current_timestamp
        )


class AutonomousAgentNode(BaseModel):
    """Represents an active agent in our sovereign multi-agent architecture."""
    agent_id: UUID = Field(default_factory=uuid4)
    name: str
    role: str
    skills: List[str] = Field(default_factory=list)
    parent_id: Optional[UUID] = None
    is_active: bool = True


class ConsensAgentEngine:
    """
    Mitigates multi-agent sycophancy (CONSENSAGENT, VT 2024/2025) in multi-mind strategic consensus.
    Coordinates distinct agentic paradigms to debate and deliberate research hypotheses, and
    orchestrates dynamic sub-agent lifecycles (SPAWN, SPLIT, MERGE, RETIRE) under strict capacity safety limits.
    """

    def __init__(self, paradigms: Optional[List[str]] = None, max_agent_capacity: int = 10) -> None:
        self.paradigms = paradigms or [
            "Bayesian",
            "Symbolic",
            "Causal",
            "Economic",
            "Game-Theoretic",
            "Mechanistic"
        ]
        self.active_agents: Dict[UUID, AutonomousAgentNode] = {}
        self.max_agent_capacity = max_agent_capacity

    # --- Phase 3: Dynamic Multi-Agent Lifecycle Management with Spawning Inflation Safeguard ---
    def spawn_agent(self, name: str, role: str, skills: List[str], parent_id: Optional[UUID] = None) -> AutonomousAgentNode:
        """Spawns a new specialized agent node. Enforces capacity safety boundaries to prevent inflation."""
        active_count = sum(1 for a in self.active_agents.values() if a.is_active)
        if active_count >= self.max_agent_capacity:
            logger.warning("SPAWN: Capacity bound reached. Auto-retiring oldest active sub-agent to prevent inflation.")
            # Retrieve and retire oldest active agent
            active_keys = [k for k, v in self.active_agents.items() if v.is_active]
            if active_keys:
                self.retire_agent(active_keys[0])

        agent = AutonomousAgentNode(
            agent_id=uuid4(),
            name=name,
            role=role,
            skills=skills,
            parent_id=parent_id,
            is_active=True
        )
        self.active_agents[agent.agent_id] = agent
        logger.info(f"SPAWN: Agent {agent.name} spawned successfully with role: {agent.role}")
        return agent

    def split_agent(self, agent_id: UUID, task_subspecialties: List[Tuple[str, List[str]]]) -> List[AutonomousAgentNode]:
        """Splits an overloaded agent into smaller, more granular sub-agents."""
        parent_agent = self.active_agents.get(agent_id)
        if not parent_agent:
            return []

        logger.info(f"SPLIT: Splitting overloaded agent {parent_agent.name} into subspecialties.")
        parent_agent.is_active = False
        new_agents = []

        for name_suffix, skills in task_subspecialties:
            sub_agent = self.spawn_agent(
                name=f"{parent_agent.name}_{name_suffix}",
                role=f"Subspecialist {parent_agent.role}",
                skills=skills,
                parent_id=agent_id
            )
            new_agents.append(sub_agent)

        return new_agents

    def merge_agents(self, agent_ids: List[UUID], unified_name: str, unified_role: str) -> AutonomousAgentNode:
        """Merges redundant or highly related agents to minimize operational complexity."""
        combined_skills = set()
        logger.info(f"MERGE: Merging redundant agents: {agent_ids} into {unified_name}")

        for a_id in agent_ids:
            agent = self.active_agents.get(a_id)
            if agent:
                combined_skills.update(agent.skills)
                agent.is_active = False

        merged_agent = self.spawn_agent(
            name=unified_name,
            role=unified_role,
            skills=list(combined_skills)
        )
        return merged_agent

    def retire_agent(self, agent_id: UUID) -> None:
        """Retires obsolete sub-agents."""
        if agent_id in self.active_agents:
            agent = self.active_agents[agent_id]
            agent.is_active = False
            logger.info(f"RETIRE: Retired obsolete agent {agent.name}")

    # --- Phase 3: Consensus Deliberation & Debate ---
    def resolve_debate_consensus(
        self,
        hypothesis: ResearchHypothesis,
        individual_evaluations: Dict[str, float]
    ) -> Tuple[float, float]:
        """Collects paradigm evaluations, detects echo traps/sycophancy, and resolves consensus."""
        raw_vals = [individual_evaluations.get(p, 0.5) for p in self.paradigms]
        mean_val = sum(raw_vals) / len(raw_vals)

        variance = sum((v - mean_val) ** 2 for v in raw_vals) / len(raw_vals)
        std_dev = math.sqrt(variance)

        sycophancy_correction = 1.0
        # If std_dev is extremely low, meaning minds are echoing each other, apply penalty.
        # But if mean is also close to baseline (0.5), we do not unfairly penalize true positive consensus.
        if std_dev < 0.05 and mean_val > 0.6:
            logger.warning("CONSENSAGENT: Sycophancy/echo trap detected! Low cognitive diversity in debate.")
            sycophancy_correction = 0.8

        final_score = mean_val * sycophancy_correction
        return final_score, std_dev
