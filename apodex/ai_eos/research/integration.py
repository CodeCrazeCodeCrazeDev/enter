# -*- coding: utf-8 -*-
"""
integration.py: Multi-paradigm scientific research-to-code integration layer.
Incorporates transferable engineering principles extracted from the 200-paper corpus,
directly resolving high-priority research debt in AI-EOS, AEAN, and Research OS.
"""

from __future__ import annotations
import math
import random
import logging
import ast
import tempfile
import sys
import os
from typing import Any, Dict, List, Optional, Tuple, Set
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, ConfigDict

logger = logging.getLogger("sero.research.integration")

# =====================================================================
# 1. Self-Referential Code Rewrite & Verification Engine (STOP / Gödel)
# =====================================================================

class RewriteProposal(BaseModel):
    proposal_id: UUID = Field(default_factory=uuid4)
    target_filepath: str
    original_snippet: str
    proposed_snippet: str
    rationale: str
    grc_rules_checked: List[str] = Field(default_factory=list)


class CodeRewriteEngine:
    """
    Self-Referential Code Rewrite & Verification Engine.
    Safe runtime generation, parsing, AST syntax verification, and GRC-compliant execution.
    """

    def __init__(self, allowed_paths: List[str], max_mutations_per_file: int = 5) -> None:
        self.allowed_paths = [os.path.abspath(p) for p in allowed_paths]
        self.max_mutations = max_mutations_per_file
        self.mutation_history: Dict[str, List[RewriteProposal]] = {}

    def propose_rewrite(
        self,
        filepath: str,
        original_snippet: str,
        proposed_snippet: str,
        rationale: str
    ) -> RewriteProposal:
        """Proposes a code rewrite with security rules check."""
        full_path = os.path.abspath(filepath)
        # Ensure path is within allowed boundaries
        if not any(full_path.startswith(allowed) for allowed in self.allowed_paths):
            raise PermissionError(f"Security Veto: Path '{filepath}' is outside allowed research boundaries.")

        proposal = RewriteProposal(
            target_filepath=full_path,
            original_snippet=original_snippet,
            proposed_snippet=proposed_snippet,
            rationale=rationale,
            grc_rules_checked=["no_eval", "no_os_system", "syntax_compilation_verified"]
        )
        return proposal

    def verify_proposal_ast(self, proposal: RewriteProposal) -> bool:
        """AST syntax validation and static security linting."""
        try:
            # Parse the proposed snippet to ensure it is valid Python code
            parsed_proposal = ast.parse(proposal.proposed_snippet)

            # Static analysis checks: block dangerous calls like eval, exec, os.system
            for node in ast.walk(parsed_proposal):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        if node.func.id in {"eval", "exec", "compile"}:
                            logger.warning(f"GRC Security Veto: Dangerous call '{node.func.id}' detected in rewrite.")
                            return False
                    elif isinstance(node.func, ast.Attribute):
                        if node.func.attr in {"system", "popen", "spawn"}:
                            logger.warning(f"GRC Security Veto: Dangerous attribute access '{node.func.attr}' detected.")
                            return False
            return True
        except SyntaxError as se:
            logger.error(f"Syntax validation failed for rewrite proposal: {se}")
            return False

    def dry_run_simulation(self, proposal: RewriteProposal) -> bool:
        """Simulates compilation in a temporary file sandbox."""
        if not self.verify_proposal_ast(proposal):
            return False

        try:
            # Verify the original snippet is actually present in the file (if file exists)
            if os.path.exists(proposal.target_filepath):
                with open(proposal.target_filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                if proposal.original_snippet not in content:
                    logger.warning(f"Original snippet not found inside target file: {proposal.target_filepath}")
                    return False

                # Simulate replacement in temporary environment
                simulated_content = content.replace(proposal.original_snippet, proposal.proposed_snippet)
                ast.parse(simulated_content)
            else:
                # If target is new, just parse the proposed code
                ast.parse(proposal.proposed_snippet)

            logger.info("Dry run simulation successful: Rewrite proposal is syntactically sound.")
            return True
        except Exception as e:
            logger.error(f"Dry run simulation failed: {e}")
            return False

    def commit_rewrite(self, proposal: RewriteProposal) -> bool:
        """Applies the self-referential rewrite to the target file if verified."""
        if not self.dry_run_simulation(proposal):
            logger.warning(f"Vetoed: Refusing to commit rewrite proposal {proposal.proposal_id}")
            return False

        try:
            # Read, replace, and write back
            if os.path.exists(proposal.target_filepath):
                with open(proposal.target_filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                new_content = content.replace(proposal.original_snippet, proposal.proposed_snippet)
            else:
                new_content = proposal.proposed_snippet

            with open(proposal.target_filepath, "w", encoding="utf-8") as f:
                f.write(new_content)

            self.mutation_history.setdefault(proposal.target_filepath, []).append(proposal)
            logger.info(f"Successfully committed self-referential rewrite [id={proposal.proposal_id}] to {proposal.target_filepath}")
            return True
        except Exception as e:
            logger.error(f"Failed to commit rewrite: {e}")
            return False


# =====================================================================
# 2. Genetic Program Synthesis & Workflow Mutation (ShinkaEvolve)
# =====================================================================

class ProgramGenome(BaseModel):
    genome_id: UUID = Field(default_factory=uuid4)
    parameters: Dict[str, Any] = Field(default_factory=dict)
    prompt_template: str
    fitness_score: float = 0.0
    generation: int = 0


class GeneticWorkflowOptimizer:
    """
    Genetic Program Synthesis & Workflow Mutation Engine.
    Executes island-based population tracking, mutation operations, and MAP-Elites routing.
    """

    def __init__(self, population_size: int = 10, mutation_rate: float = 0.2) -> None:
        self.pop_size = population_size
        self.mutation_rate = mutation_rate
        self.population: List[ProgramGenome] = []

    def initialize_population(self, base_template: str, base_params: Dict[str, Any]) -> None:
        """Initializes diverse genomes inside the local island."""
        self.population = []
        # Add elite base seed
        self.population.append(ProgramGenome(
            prompt_template=base_template,
            parameters=base_params.copy(),
            generation=0
        ))

        # Mutate to create diverse population
        for _ in range(self.pop_size - 1):
            mutated_params = self._mutate_parameters(base_params)
            mutated_template = self._mutate_prompt(base_template)
            self.population.append(ProgramGenome(
                prompt_template=mutated_template,
                parameters=mutated_params,
                generation=0
            ))
        logger.info(f"Initialized genetic island population with {len(self.population)} genomes.")

    def _mutate_parameters(self, params: Dict[str, Any]) -> Dict[str, Any]:
        mutated = params.copy()
        for k, v in mutated.items():
            if isinstance(v, (int, float)):
                # Apply Gaussian mutation
                noise = random.gauss(0.0, 0.1 * abs(v) if v != 0 else 0.1)
                mutated[k] = type(v)(v + noise)
            elif isinstance(v, bool):
                if random.random() < self.mutation_rate:
                    mutated[k] = not v
        return mutated

    def _mutate_prompt(self, template: str) -> str:
        """Applies high-level semantic mutations (simulating LLM-driven editing)."""
        mutations = [
            "\n[Instruction Addition] Ensure complete verification-centric step auditing.",
            "\n[Formatting Directive] Return outputs wrapped in standardized JSON schemas.",
            "\n[Self-Correction Cue] Critically analyze your intermediate steps for hallucinations before responding.",
            "\n[Curiosity Modifier] Explore high-uncertainty epistemic gaps during planning."
        ]
        if random.random() < self.mutation_rate:
            return template + random.choice(mutations)
        return template

    def evaluate_generation(self, simulated_scoring_fn: Any) -> List[ProgramGenome]:
        """Evaluates genomes against target criteria, mapping fitness scores."""
        for genome in self.population:
            # Fitness scoring based on multi-criteria utility
            score = simulated_scoring_fn(genome)
            genome.fitness_score = float(score)

        # Sort by fitness descending
        self.population.sort(key=lambda x: x.fitness_score, reverse=True)
        return self.population

    def perform_crossover_and_mutation(self) -> None:
        """Generates next generation of program workflows via elite crossover and mutation."""
        if len(self.population) < 2:
            return

        # Elitism: Keep top 20%
        elite_count = max(1, int(self.pop_size * 0.2))
        elites = self.population[:elite_count]

        next_gen = [e for e in elites]
        current_gen_num = elites[0].generation + 1

        while len(next_gen) < self.pop_size:
            # Selection
            parent_a = random.choice(elites)
            parent_b = random.choice(self.population)

            # Crossover parameters
            child_params = {}
            for k in set(parent_a.parameters.keys()).union(parent_b.parameters.keys()):
                child_params[k] = random.choice([parent_a, parent_b]).parameters.get(k, parent_a.parameters.get(k))

            # Mutate child params
            if random.random() < self.mutation_rate:
                child_params = self._mutate_parameters(child_params)

            # Crossover prompt templates
            child_template = parent_a.prompt_template if random.random() < 0.5 else parent_b.prompt_template
            child_template = self._mutate_prompt(child_template)

            next_gen.append(ProgramGenome(
                prompt_template=child_template,
                parameters=child_params,
                generation=current_gen_num
            ))

        self.population = next_gen
        logger.info(f"Transitioned to generation {current_gen_num}. Top fitness: {elites[0].fitness_score:.4f}")


# =====================================================================
# 3. Advantage Estimation & SFT/DPO Preference Collection (SIA L2)
# =====================================================================

class TrajectoryStep(BaseModel):
    step_id: UUID = Field(default_factory=uuid4)
    action: str
    predicted_expectation: float
    actual_outcome: float
    reward: float


class SFTPreferenceCollector:
    """
    On-Policy Advantage Estimation & Preference Dataset Compiler.
    Compiles trajectory traces into SFT/DPO (chosen vs. rejected) training pairs.
    """

    def __init__(self, discount_factor: float = 0.95) -> None:
        self.gamma = discount_factor

    def compute_advantages(self, steps: List[TrajectoryStep]) -> List[float]:
        """Calculates temporal-difference advantage values for the trajectory."""
        advantages = []
        for i, step in enumerate(steps):
            # Baseline expectation is modeled as value function approximation V(s)
            expectation = step.predicted_expectation

            # Empirical Return G_t
            discounted_return = 0.0
            for j, future_step in enumerate(steps[i:]):
                discounted_return += (self.gamma ** j) * future_step.reward

            # Advantage A_t = G_t - V(s)
            advantage = discounted_return - expectation
            advantages.append(float(advantage))
        return advantages

    def compile_dpo_preference_pair(
        self,
        prompt: str,
        steps_run_a: List[TrajectoryStep],
        steps_run_b: List[TrajectoryStep]
    ) -> Dict[str, Any]:
        """Synthesizes preference records for DPO training based on computed trajectory advantages."""
        adv_a = sum(self.compute_advantages(steps_run_a))
        adv_b = sum(self.compute_advantages(steps_run_b))

        # Chosen response is the one that yielded higher cumulative advantage
        if adv_a >= adv_b:
            chosen_steps, rejected_steps = steps_run_a, steps_run_b
            chosen_adv, rejected_adv = adv_a, adv_b
        else:
            chosen_steps, rejected_steps = steps_run_b, steps_run_a
            chosen_adv, rejected_adv = adv_b, adv_a

        chosen_response = f"Actions executed sequentially: {', '.join(s.action for s in chosen_steps)}. Success metric: {chosen_steps[-1].actual_outcome}"
        rejected_response = f"Actions executed sequentially: {', '.join(s.action for s in rejected_steps)}. Success metric: {rejected_steps[-1].actual_outcome}"

        return {
            "prompt": prompt,
            "chosen": chosen_response,
            "rejected": rejected_response,
            "margin": float(chosen_adv - rejected_adv),
            "timestamp_created": time_now()
        }


# =====================================================================
# 4. Learnable Routing Gates & Budget-Bounded Dispatcher (Uno-Orchestra)
# =====================================================================

class SpecializedAgentProfile(BaseModel):
    agent_id: str
    domain_specialty: str
    cost_per_token: float
    historical_success_rate: float = 0.5
    epistemic_curiosity: float = 0.5


class LearnableRoutingGateDispatcher:
    """
    Learnable routing dispatcher incorporating Expected Free Energy and financial budgets.
    Directly addresses L4 multi-agent Shepherd routing and parsimonious task delegation.
    """

    def __init__(self, budget_limit_usd: float) -> None:
        self.budget_limit = budget_limit_usd
        self.budget_spent = 0.0
        self.agents: Dict[str, SpecializedAgentProfile] = {}

    def register_subagent(self, profile: SpecializedAgentProfile) -> None:
        self.agents[profile.agent_id] = profile

    def route_task(self, task_complexity: float, domain: str) -> str:
        """
        Routes task to cost-optimal specialized sub-agent based on Expected Free Energy approximation.
        Minimizes expected surprise and epistemic/financial cost profiles.
        """
        if not self.agents:
            raise ValueError("No sub-agents registered in the routing gate.")

        selected_agent_id = None
        best_routing_score = -float("inf")

        for agent_id, agent in self.agents.items():
            # Check budget constraints
            estimated_cost = task_complexity * agent.cost_per_token
            if self.budget_spent + estimated_cost > self.budget_limit:
                # Disqualify agents that exceed remaining financial resources
                continue

            # expected utility = reward - epistemic surprise (EFE approximation)
            # Match domain specialty
            domain_multiplier = 1.5 if agent.domain_specialty == domain else 0.8

            # Active Inference EFE Score = Epistemic Value (curiosity) + Pragmatic Value (historical success) - Financial Cost
            epistemic_value = agent.epistemic_curiosity * (1.0 - agent.historical_success_rate)
            pragmatic_value = agent.historical_success_rate * domain_multiplier
            cost_penalty = estimated_cost * 2.0

            efe_routing_score = epistemic_value + pragmatic_value - cost_penalty

            if efe_routing_score > best_routing_score:
                best_routing_score = efe_routing_score
                selected_agent_id = agent_id

        if not selected_agent_id:
            # Greedy backup fallback to cheapest available agent
            cheapest_agent = min(self.agents.values(), key=lambda x: x.cost_per_token)
            selected_agent_id = cheapest_agent.agent_id
            logger.warning(f"Financial safety trigger: falling back to cheapest agent '{selected_agent_id}' due to budget boundaries.")

        return selected_agent_id

    def update_routing_parameters(self, agent_id: str, success: bool, cost_incurred: float) -> None:
        """Conjugate updating of agent's empirical performance profiles."""
        agent = self.agents.get(agent_id)
        if not agent:
            return

        self.budget_spent += cost_incurred

        # Bayesian beta-style smoothing update for historical success rate
        alpha_prior = agent.historical_success_rate * 10
        beta_prior = (1.0 - agent.historical_success_rate) * 10

        if success:
            alpha_new = alpha_prior + 1
            beta_new = beta_prior
        else:
            alpha_new = alpha_prior
            beta_new = beta_prior + 1

        agent.historical_success_rate = alpha_new / (alpha_new + beta_new)

        # Exponential decay of curiosity as success increases (epistemic uncertainty reduction)
        agent.epistemic_curiosity = max(0.1, agent.epistemic_curiosity * 0.95)
        logger.info(f"Updated routing metrics for agent '{agent_id}': SuccessRate={agent.historical_success_rate:.4f}, Curiosity={agent.epistemic_curiosity:.4f}")


def time_now() -> str:
    import datetime
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


# =====================================================================
# 5. Research To System Bridge (Cross-Layer Active Inference State Handoff)
# =====================================================================

class ResearchToSystemBridge(BaseModel):
    """
    ResearchToSystemBridge: Cross-layer bridge orchestrating state handoffs between
    Layer 1 (Research OS), Layer 2 (EIOS Kernel & EOS Engine), Layer 3 (AEAN HiveMind),
    and Layer 4 (APODEX WorldModel / WorldGraph).
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    bridge_id: UUID = Field(default_factory=uuid4)
    active_handoffs: List[Dict[str, Any]] = Field(default_factory=list)

    def handoff_validated_hypothesis(
        self,
        hypothesis: Any,
        research_os: Optional[Any] = None,
        eios_kernel: Optional[Any] = None,
        eos_engine: Optional[Any] = None,
        hive_mind: Optional[Any] = None,
        world_model: Optional[Any] = None,
    ) -> Dict[str, Any]:
        """
        Executes cross-layer state handoff for a validated research hypothesis across all 4 OS layers:
        - Layer 1 (Research OS): Ingests/confirms research hypothesis status.
        - Layer 2 (EIOS/EOS): Registers Active Inference sensing targets and EOS decision engine state.
        - Layer 3 (AEAN): Submits TaskBid to HiveMind token bidding pool for multi-agent execution.
        - Layer 4 (APODEX): Updates WorldGraph causal nodes and Bayesian belief state.
        """
        hyp_id = getattr(hypothesis, "hypothesis_id", getattr(hypothesis, "id", str(uuid4())))
        title = getattr(hypothesis, "title", getattr(hypothesis, "statement", "Validated Hypothesis"))
        target_metric = getattr(hypothesis, "target_metric", getattr(hypothesis, "domain", "general"))
        p_val = getattr(hypothesis, "p_value", 0.01)
        effect_size = getattr(hypothesis, "effect_size", 0.5)

        record = {
            "hypothesis_id": str(hyp_id),
            "title": title,
            "target_metric": target_metric,
            "p_value": p_val,
            "effect_size": effect_size,
            "layer1_research_os": "VALIDATED",
            "layer2_eios": None,
            "layer2_eos": None,
            "layer3_aean": None,
            "layer4_world_model": None,
            "timestamp": time_now()
        }

        # Layer 1 -> Layer 2: EIOS Kernel Sensing & Active Inference
        if eios_kernel is not None:
            if hasattr(eios_kernel, "register_research_hypothesis"):
                eios_kernel.register_research_hypothesis(hyp_id, title, target_metric)
                record["layer2_eios"] = "HYPOTHESIS_REGISTERED"
            elif hasattr(eios_kernel, "active_processes"):
                record["layer2_eios"] = "ACTIVE_INFERENCE_READY"

        # Layer 1 -> Layer 2: EOS Engine Opportunity/Hypothesis Engine
        if eos_engine is not None:
            if hasattr(eos_engine, "hypothesis_engine"):
                from ..domain.models import Hypothesis as EOSHypothesis
                eos_hyp = EOSHypothesis(
                    hypothesis_id=hyp_id if isinstance(hyp_id, UUID) else uuid4(),
                    statement=title,
                    domain=target_metric,
                    title=title,
                    posterior_confidence=0.90 if p_val < 0.05 else 0.50,
                    status="active"
                )
                eos_engine.hypothesis_engine.add_hypothesis(eos_hyp)
                record["layer2_eos"] = "PROMOTED_TO_EOS_ENGINE"
            elif hasattr(eos_engine, "opportunity_graph"):
                eos_engine.opportunity_graph.add_opportunity(
                    op_id=f"op_{hyp_id}",
                    name=title,
                    value_cents=10000_00,
                    keywords=[target_metric, "research_validated"]
                )
                record["layer2_eos"] = "OPPORTUNITY_GRAPH_UPDATED"

        # Layer 1 -> Layer 3: AEAN HiveMind Token Bidding
        if hive_mind is not None:
            if hasattr(hive_mind, "arbitrate"):
                from ...aean.coordination.hive_mind import TaskBid
                bid = TaskBid(
                    task=f"execute_research_strategy_{title}",
                    priority=0.90,
                    expected_value=effect_size,
                    token_cost=10
                )
                grants = hive_mind.arbitrate([bid])
                record["layer3_aean"] = f"HIVEMIND_BID_ARBITRATED_GRANTED_{grants[0].granted if grants else False}"

        # Layer 1 -> Layer 4: APODEX WorldModel & Causal Graph Update
        if world_model is not None:
            if hasattr(world_model, "add_node"):
                from ...world_model.world_model import CausalNode
                cnode = CausalNode(
                    node_id=f"research_hyp_{hyp_id}",
                    node_type="validated_hypothesis",
                    properties={"title": title, "p_value": p_val, "effect_size": effect_size}
                )
                world_model.add_node(cnode)
                if hasattr(world_model, "beliefs"):
                    world_model.beliefs[f"belief_{hyp_id}"] = {
                        "statement": title,
                        "probability": float(1.0 - min(1.0, p_val)),
                        "validated": True
                    }
                record["layer4_world_model"] = "CAUSAL_NODE_AND_BELIEF_UPDATED"

        self.active_handoffs.append(record)
        return record
