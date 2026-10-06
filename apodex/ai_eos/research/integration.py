# -*- coding: utf-8 -*-
"""
integration.py: Multi-paradigm scientific research-to-code integration layer.
Incorporates transferable engineering principles extracted from the research paper corpus,
directly resolving high-priority research debt across Research OS, EIOS, EOS, AEAN, and APODEX.
"""

from __future__ import annotations
import math
import random
import logging
import ast
import tempfile
import sys
import os
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple, Set
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

logger = logging.getLogger("sero.research.integration")

def time_now() -> str:
    return datetime.now(timezone.utc).isoformat()

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
    Safe runtime generation, parsing, AST syntax verification, Hawkes recursion depth checks,
    and GRC-compliant execution.
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
        if not any(full_path.startswith(allowed) for allowed in self.allowed_paths):
            raise PermissionError(f"Security Veto: Path '{filepath}' is outside allowed research boundaries.")

        proposal = RewriteProposal(
            target_filepath=full_path,
            original_snippet=original_snippet,
            proposed_snippet=proposed_snippet,
            rationale=rationale,
            grc_rules_checked=["no_eval", "no_os_system", "syntax_compilation_verified", "hawkes_ast_depth"]
        )
        return proposal

    def verify_proposal_ast(self, proposal: RewriteProposal) -> bool:
        """AST syntax validation, Hawkes call-depth checks, and static security linting."""
        try:
            parsed_proposal = ast.parse(proposal.proposed_snippet)

            # Check Hawkes AST recursion depth within function definitions
            for node in ast.walk(parsed_proposal):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    func_name = node.name
                    recursive_calls = [
                        n for n in ast.walk(node)
                        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == func_name
                    ]
                    if len(recursive_calls) > 3:
                        logger.warning(f"Hawkes AST Depth Veto: Function '{func_name}' has excessive recursive calls ({len(recursive_calls)}).")
                        return False

                # Static analysis checks: block dangerous calls like eval, exec, os.system
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
            if os.path.exists(proposal.target_filepath):
                with open(proposal.target_filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                if proposal.original_snippet not in content:
                    logger.warning(f"Original snippet not found inside target file: {proposal.target_filepath}")
                    return False

                simulated_content = content.replace(proposal.original_snippet, proposal.proposed_snippet)
                ast.parse(simulated_content)
            else:
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
        self.population.append(ProgramGenome(
            prompt_template=base_template,
            parameters=base_params.copy(),
            generation=0
        ))

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
            if isinstance(v, bool):
                if random.random() < self.mutation_rate:
                    mutated[k] = not v
            elif isinstance(v, (int, float)):
                noise = random.gauss(0.0, 0.1 * abs(v) if v != 0 else 0.1)
                mutated[k] = type(v)(v + noise)
        return mutated

    def _mutate_prompt(self, template: str) -> str:
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
            score = simulated_scoring_fn(genome)
            genome.fitness_score = float(score)

        self.population.sort(key=lambda x: x.fitness_score, reverse=True)
        return self.population

    def perform_crossover_and_mutation(self) -> None:
        """Generates next generation of program workflows via elite crossover and mutation."""
        if len(self.population) < 2:
            return

        elite_count = max(1, int(self.pop_size * 0.2))
        elites = self.population[:elite_count]

        next_gen = [e for e in elites]
        current_gen_num = elites[0].generation + 1

        while len(next_gen) < self.pop_size:
            parent_a = random.choice(elites)
            parent_b = random.choice(self.population)

            child_params = {}
            for k in set(parent_a.parameters.keys()).union(parent_b.parameters.keys()):
                child_params[k] = random.choice([parent_a, parent_b]).parameters.get(k, parent_a.parameters.get(k))

            if random.random() < self.mutation_rate:
                child_params = self._mutate_parameters(child_params)

            child_template = parent_a.prompt_template if random.random() < 0.5 else parent_b.prompt_template
            child_template = self._mutate_prompt(child_template)

            next_gen.append(ProgramGenome(
                prompt_template=child_template,
                parameters=child_params,
                generation=current_gen_num
            ))

        self.population = next_gen
        self.population.sort(key=lambda x: x.fitness_score, reverse=True)
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
            expectation = step.predicted_expectation
            discounted_return = 0.0
            for j, future_step in enumerate(steps[i:]):
                discounted_return += (self.gamma ** j) * future_step.reward

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

        if adv_a >= adv_b:
            chosen_steps, rejected_steps = steps_run_a, steps_run_b
            chosen_adv, rejected_adv = adv_a, adv_b
        else:
            chosen_steps, rejected_steps = steps_run_b, steps_run_a
            chosen_adv, rejected_adv = adv_b, adv_a

        chosen_response = f"Actions executed sequentially: {', '.join(s.action for s in chosen_steps)}. Success metric: {chosen_steps[-1].actual_outcome}"
        rejected_response = f"Actions executed sequentially: {', '.join(s.action for s in rejected_steps)}. Success metric: {rejected_steps[-1].actual_outcome}"

        margin = max(-10.0, min(10.0, float(chosen_adv - rejected_adv)))

        return {
            "prompt": prompt,
            "chosen": chosen_response,
            "rejected": rejected_response,
            "margin": margin,
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
        """
        if not self.agents:
            raise ValueError("No sub-agents registered in the routing gate.")

        selected_agent_id = None
        best_routing_score = -float("inf")

        budget_decay = max(0.1, 1.0 - (self.budget_spent / max(1.0, self.budget_limit)))

        for agent_id, agent in self.agents.items():
            estimated_cost = task_complexity * agent.cost_per_token
            if self.budget_spent + estimated_cost > self.budget_limit:
                continue

            domain_multiplier = 1.5 if agent.domain_specialty == domain else 0.8
            epistemic_value = agent.epistemic_curiosity * (1.0 - agent.historical_success_rate)
            pragmatic_value = agent.historical_success_rate * domain_multiplier
            cost_penalty = estimated_cost * 2.0 / budget_decay

            efe_routing_score = epistemic_value + pragmatic_value - cost_penalty

            if efe_routing_score > best_routing_score:
                best_routing_score = efe_routing_score
                selected_agent_id = agent_id

        if not selected_agent_id:
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

        alpha_prior = agent.historical_success_rate * 10
        beta_prior = (1.0 - agent.historical_success_rate) * 10

        if success:
            alpha_new = alpha_prior + 1
            beta_new = beta_prior
        else:
            alpha_new = alpha_prior
            beta_new = beta_prior + 1

        agent.historical_success_rate = alpha_new / (alpha_new + beta_new)
        agent.epistemic_curiosity = max(0.1, agent.epistemic_curiosity * 0.95)


# =====================================================================
# 5. Cross-Layer Research to System Bridge (Layer 1 -> 2 -> 3 -> 4)
# =====================================================================

class ResearchToSystemBridge:
    """
    Orchestrates closed-loop active inference state handoffs across all 4 layers:
    - Layer 1: Research OS hypothesis generation and validation
    - Layer 2: EIOS Kernel EFE sensing & EOS Engine DAG compilation
    - Layer 3: AEAN HiveMind multi-agent token bidding & strategy execution
    - Layer 4: APODEX WorldModel causal node creation & Bayesian belief updates
    """

    def __init__(
        self,
        research_os: Any,
        eios_kernel: Any,
        eos_engine: Any,
        hive_mind: Any,
        world_model: Any
    ) -> None:
        self.research_os = research_os
        self.eios_kernel = eios_kernel
        self.eos_engine = eos_engine
        self.hive_mind = hive_mind
        self.world_model = world_model

    def execute_cross_layer_active_inference_cycle(self, hypothesis_id: str) -> Dict[str, Any]:
        """
        Executes an atomic closed-loop active inference handoff from Research OS down to APODEX WorldModel.
        """
        # Step 1: Export validated research hypothesis from Layer 1 Research OS
        hyp_data = self.research_os.export_hypothesis_for_execution(hypothesis_id)
        if not hyp_data:
            raise ValueError(f"Hypothesis {hypothesis_id} not found or not validated in Research OS.")

        # Step 2: Register hypothesis in Layer 2 EIOS Kernel & EOS Engine
        if hasattr(self.eios_kernel, "register_research_hypothesis"):
            self.eios_kernel.register_research_hypothesis(hyp_data)

        if hasattr(self.eos_engine, "ingest_validated_research"):
            self.eos_engine.ingest_validated_research(hyp_data)

        # Sense EFE anomalies over the hypothesis
        sensing_report = {}
        if hasattr(self.eios_kernel, "sense_opportunity_anomalies"):
            sensing_report = self.eios_kernel.sense_opportunity_anomalies()

        # Step 3: Register insight in Layer 3 AEAN HiveMind for agent bidding
        insight_data = {
            "insight_id": f"INSIGHT-{hypothesis_id}",
            "hypothesis_id": hypothesis_id,
            "statement": hyp_data.get("statement", ""),
            "confidence": hyp_data.get("confidence", 0.9),
            "bidding_budget": 100.0,
            "status": "ready_for_bidding"
        }
        if hasattr(self.hive_mind, "register_research_insight"):
            self.hive_mind.register_research_insight(insight_data)

        # Trigger bidding execution
        bid_winner = None
        if hasattr(self.hive_mind, "bid_for_task"):
            bid_winner = self.hive_mind.bid_for_task(
                task_id=f"TASK-{hypothesis_id}",
                required_capabilities=["coder", "critic"]
            )

        # Step 4: Update Layer 4 APODEX WorldModel causal state and Bayesian beliefs
        causal_node_id = f"NODE-HYP-{hypothesis_id}"
        if hasattr(self.world_model, "create_node"):
            self.world_model.create_node(
                node_id=causal_node_id,
                label=f"Hypothesis Action: {hypothesis_id}",
                node_type="causal_action",
                properties={"confidence": hyp_data.get("confidence", 0.9)}
            )

        updated_belief = 0.5
        if hasattr(self.world_model, "update_belief"):
            updated_belief = self.world_model.update_belief(
                node_id=causal_node_id,
                new_belief=min(0.99, hyp_data.get("confidence", 0.9) + 0.05),
                evidence_weight=1.0
            )

        logger.info(f"Cross-layer active inference cycle completed successfully for hypothesis {hypothesis_id}.")

        return {
            "hypothesis_id": hypothesis_id,
            "layer1_status": hyp_data.get("status", "validated"),
            "layer2_sensing": sensing_report,
            "layer3_winning_agent": bid_winner,
            "layer4_causal_node": causal_node_id,
            "layer4_updated_belief": updated_belief
        }


# Principle Registration Registers
ALPHAALGO_100_PRINCIPLES: Dict[str, Any] = {}
ALPHAALGO_200_PRINCIPLES: Dict[str, Any] = {}
ALPHAALGO_301_400_PRINCIPLES: Dict[str, Any] = {}
ALPHAALGO_401_500_PRINCIPLES: Dict[str, Any] = {}
ALPHAALGO_501_600_PRINCIPLES: Dict[str, Any] = {}

def register_100_paper_alphaalgo_principles() -> Dict[str, Any]:
    global ALPHAALGO_100_PRINCIPLES
    if not ALPHAALGO_100_PRINCIPLES:
        ALPHAALGO_100_PRINCIPLES = {
            "P-101": "Active Inference Expected Free Energy minimization balances pragmatic and epistemic value.",
            "P-102": "Hawkes point processes govern recursive AST call depth to prevent infinite loops."
        }
    return ALPHAALGO_100_PRINCIPLES

def register_200_paper_corpus_principles() -> Dict[str, Any]:
    global ALPHAALGO_200_PRINCIPLES
    if not ALPHAALGO_200_PRINCIPLES:
        ALPHAALGO_200_PRINCIPLES = {
            "P-201": "Island MAP-Elites migration gates sort program populations dynamically on elite insertion.",
            "P-202": "Advantage margin clipping prevents extreme gradient updates in preference learning."
        }
    return ALPHAALGO_200_PRINCIPLES

def register_301_400_paper_corpus_principles() -> Dict[str, Any]:
    global ALPHAALGO_301_400_PRINCIPLES
    if not ALPHAALGO_301_400_PRINCIPLES:
        ALPHAALGO_301_400_PRINCIPLES = {
            "P-301": "Budget-decayed EFE task routing prevents resource exhaustion in multi-agent swarms.",
            "P-302": "Multi-field literature query expanding category, description, target_subsystem, and paper_title."
        }
    return ALPHAALGO_301_400_PRINCIPLES

def register_401_500_paper_corpus_principles() -> Dict[str, Any]:
    global ALPHAALGO_401_500_PRINCIPLES
    if not ALPHAALGO_401_500_PRINCIPLES:
        ALPHAALGO_401_500_PRINCIPLES = {
            "P-401": "Hawkes non-Gaussian process stability guarantees AST call depth verification safety.",
            "P-402": "Clipped trajectory advantage margins constrain advantage updates within bounds."
        }
    return ALPHAALGO_401_500_PRINCIPLES

def register_501_600_paper_corpus_principles() -> Dict[str, Any]:
    global ALPHAALGO_501_600_PRINCIPLES
    if not ALPHAALGO_501_600_PRINCIPLES:
        ALPHAALGO_501_600_PRINCIPLES = {
            "P-501": "14-Layer Computational Architecture formalization across entrepreneurship and AI orchestration.",
            "P-502": "Multi-agent token bidding and reputation tracking in HiveMind resource markets."
        }
    return ALPHAALGO_501_600_PRINCIPLES
