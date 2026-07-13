from __future__ import annotations
import random
import time
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from apodex.evolution.common.models import (
    CostMode,
    ConfigDelta,
    ChangelogEntry,
    MultiObjectiveMetric,
    calculate_multiobjective_score,
    EvolutionChangelog,
)
from apodex.evolution.verifier.judge import EvolutionVerifier, EvaluationReport


# -------------------------------------------------------------
# 1. Self-Critique + Revise Cycle (RISE-inspired)
# -------------------------------------------------------------
class SelfCritiqueOptimizer:
    """
    Implements a self-critique + revise cycle (RISE style) in the harness loop.
    Generates and scores initial answers, critiques them, and revises them.
    Revision is accepted only if the verifier's multi-objective score improves under the cost mode.
    """

    def __init__(self, verifier: Optional[EvolutionVerifier] = None):
        self.verifier = verifier or EvolutionVerifier()

    async def run_revision_cycle(
        self,
        prompt: str,
        initial_completion: str,
        cost_mode: CostMode,
        expected_keywords: Optional[List[str]] = None,
        mock_revised_completion: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Runs the critique and revision loop.
        - Evaluates initial_completion.
        - Formulates a mock or real critique.
        - Generates/revises completion.
        - Evaluates revised completion.
        - Compares multi-objective scores under cost_mode.
        """
        # 1. Evaluate initial completion
        initial_report = await self.verifier.evaluate_output(
            prompt, initial_completion, expected_keywords=expected_keywords
        )
        initial_score = calculate_multiobjective_score(initial_report.metrics, cost_mode)

        # 2. Formulate critique
        critique = "Formatting could be stronger, try surrounding with braces '{}' and increasing density."

        # 3. Revise completion
        # If mock_revised_completion is provided, use it; otherwise auto-improve initial_completion
        if mock_revised_completion:
            revised_completion = mock_revised_completion
        else:
            revised_completion = f"{{\n  \"original\": \"{initial_completion}\",\n  \"status\": \"revised\"\n}}"

        # 4. Evaluate revised completion
        revised_report = await self.verifier.evaluate_output(
            prompt, revised_completion, expected_keywords=expected_keywords
        )
        revised_score = calculate_multiobjective_score(revised_report.metrics, cost_mode)

        # 5. Decide whether to keep the revision
        accepted = revised_score > initial_score

        final_completion = revised_completion if accepted else initial_completion
        final_score = revised_score if accepted else initial_score
        final_report = revised_report if accepted else initial_report

        return {
            "initial_completion": initial_completion,
            "initial_score": initial_score,
            "critique": critique,
            "revised_completion": revised_completion,
            "revised_score": revised_score,
            "accepted": accepted,
            "final_completion": final_completion,
            "final_score": final_score,
            "report": final_report,
        }


# -------------------------------------------------------------
# 2. Declarative Prompt / Workflow Parameters (DSPy-inspired)
# -------------------------------------------------------------
class PromptParameter(BaseModel):
    """Holds a declarative prompt parameter that can be optimized."""
    parameter_id: str
    current_value: str
    candidates: List[str] = Field(default_factory=list)


class DeclarativeOptimizer:
    """
    DSPy-like programmatic prompt & routing parameter optimizer.
    Selects optimal prompt templates/parameters from candidates by evaluating them
    on an evaluation test set under multi-objective cost profiles.
    """

    def __init__(self, verifier: Optional[EvolutionVerifier] = None, changelog: Optional[EvolutionChangelog] = None):
        self.verifier = verifier or EvolutionVerifier()
        self.changelog = changelog or EvolutionChangelog()

    async def optimize_parameter(
        self,
        param: PromptParameter,
        test_inputs: List[str],
        cost_mode: CostMode,
        expected_keywords: Optional[List[str]] = None,
        mock_completions: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Iterates over parameter candidates, runs evaluations, and applies the highest-scoring
        parameter settings as configuration deltas. Creates rollback-safe changelog entries.
        """
        best_candidate = param.current_value
        best_score = -1.0
        best_metrics: Optional[MultiObjectiveMetric] = None

        # Helper mock completion getter
        def get_completion(candidate: str, test_input: str) -> str:
            if mock_completions and candidate in mock_completions:
                return mock_completions[candidate]
            # Simple fallback completion
            return f"Processed using prompt candidate: {candidate}. Input: {test_input}"

        # Evaluate the baseline (current value)
        baseline_scores = []
        for inp in test_inputs:
            comp = get_completion(param.current_value, inp)
            rep = await self.verifier.evaluate_output(inp, comp, expected_keywords=expected_keywords)
            mo_score = calculate_multiobjective_score(rep.metrics, cost_mode)
            baseline_scores.append(mo_score)
        baseline_avg_score = sum(baseline_scores) / len(baseline_scores) if baseline_scores else 0.0

        best_score = baseline_avg_score

        # Check candidate parameters
        candidate_evals = {}
        for candidate in param.candidates:
            if candidate == param.current_value:
                continue

            candidate_scores = []
            metrics_list = []
            for inp in test_inputs:
                comp = get_completion(candidate, inp)
                rep = await self.verifier.evaluate_output(inp, comp, expected_keywords=expected_keywords)
                mo_score = calculate_multiobjective_score(rep.metrics, cost_mode)
                candidate_scores.append(mo_score)
                metrics_list.append(rep.metrics)

            avg_score = sum(candidate_scores) / len(candidate_scores) if candidate_scores else 0.0
            candidate_evals[candidate] = avg_score

            if avg_score > best_score:
                best_score = avg_score
                best_candidate = candidate
                # Simple average of metrics
                best_metrics = MultiObjectiveMetric(
                    quality=sum(m.quality for m in metrics_list) / len(metrics_list),
                    cost=sum(m.cost for m in metrics_list) / len(metrics_list),
                    latency=sum(m.latency for m in metrics_list) / len(metrics_list),
                )

        # Apply changes if we found an improvement
        improved = best_candidate != param.current_value
        deltas = []
        if improved:
            delta = ConfigDelta(
                target_id=param.parameter_id,
                delta_type="prompt",
                old_value=param.current_value,
                new_value=best_candidate,
                metadata={"improvement": best_score - baseline_avg_score}
            )
            deltas.append(delta)

            entry = ChangelogEntry(
                entry_id=f"entry_{int(time.time())}_{random.randint(1000, 9999)}",
                timestamp=time.time(),
                cost_mode=cost_mode,
                applied_deltas=deltas,
                verifier_score_before=baseline_avg_score,
                verifier_score_after=best_score,
                description=f"Optimized parameter {param.parameter_id} under cost mode {cost_mode.value}."
            )
            self.changelog.apply_change(entry)

        return {
            "parameter_id": param.parameter_id,
            "original_value": param.current_value,
            "best_value": best_candidate,
            "baseline_score": baseline_avg_score,
            "best_score": best_score,
            "improved": improved,
            "candidate_evals": candidate_evals,
        }


# -------------------------------------------------------------
# 3. Simple Evolutionary Search for Workflows (GPTSwarm-inspired)
# -------------------------------------------------------------
class WorkflowConfig(BaseModel):
    """Represents a candidate workflow configuration graph."""
    workflow_id: str
    nodes: List[str] = Field(default_factory=list)  # list of sub-agent IDs or tool calls
    has_verification_step: bool = False
    max_samples: int = 1
    tool_threshold: float = 0.5


class WorkflowEvolutionSearch:
    """
    Implements a simple genetic/evolutionary search algorithm over workflow graphs.
    Mutates topological nodes, thresholds, and samples, measuring fitness across cost profiles.
    """

    def __init__(self, verifier: Optional[EvolutionVerifier] = None):
        self.verifier = verifier or EvolutionVerifier()

    def calculate_fitness(self, config: WorkflowConfig, cost_mode: CostMode) -> float:
        """
        Calculates fitness score [0.0, 1.0] for a WorkflowConfig based on CostMode.
        - Quality: higher if verification step is enabled or sample count is balanced.
        - Cost: increases with number of nodes, sample count, and verification step.
        - Latency: increases with nodes and sample count.
        """
        # Determine base quality
        quality = 0.5
        if config.has_verification_step:
            quality += 0.2
        if config.max_samples > 1:
            quality += min(0.2, (config.max_samples - 1) * 0.1)
        if len(config.nodes) >= 2:
            quality += 0.1

        quality = min(1.0, quality)

        # Calculate simulated cost [0.0, 1.0]
        base_cost = len(config.nodes) * 0.1 + (0.15 if config.has_verification_step else 0.0)
        cost = min(1.0, base_cost * config.max_samples)

        # Calculate simulated latency [0.0, 1.0]
        base_latency = len(config.nodes) * 0.08 + (0.1 if config.has_verification_step else 0.0)
        latency = min(1.0, base_latency * (1.2 if config.max_samples > 1 else 1.0))

        metrics = MultiObjectiveMetric(quality=quality, cost=cost, latency=latency)
        return calculate_multiobjective_score(metrics, cost_mode)

    def mutate(self, config: WorkflowConfig, available_agents: List[str]) -> WorkflowConfig:
        """Performs a mutation operation on the workflow configuration."""
        mutated_nodes = list(config.nodes)
        mutation_type = random.choice(["add_node", "remove_node", "toggle_verify", "change_samples", "change_threshold"])

        if mutation_type == "add_node" and available_agents:
            new_node = random.choice(available_agents)
            if new_node not in mutated_nodes:
                mutated_nodes.append(new_node)
        elif mutation_type == "remove_node" and len(mutated_nodes) > 1:
            mutated_nodes.pop(random.randint(0, len(mutated_nodes) - 1))
        elif mutation_type == "toggle_verify":
            has_verification = not config.has_verification_step
            return WorkflowConfig(
                workflow_id=config.workflow_id,
                nodes=mutated_nodes,
                has_verification_step=has_verification,
                max_samples=config.max_samples,
                tool_threshold=config.tool_threshold,
            )
        elif mutation_type == "change_samples":
            max_samples = max(1, config.max_samples + random.choice([-1, 1]))
            return WorkflowConfig(
                workflow_id=config.workflow_id,
                nodes=mutated_nodes,
                has_verification_step=config.has_verification_step,
                max_samples=max_samples,
                tool_threshold=config.tool_threshold,
            )
        elif mutation_type == "change_threshold":
            tool_threshold = min(1.0, max(0.0, config.tool_threshold + random.choice([-0.1, 0.1])))
            return WorkflowConfig(
                workflow_id=config.workflow_id,
                nodes=mutated_nodes,
                has_verification_step=config.has_verification_step,
                max_samples=config.max_samples,
                tool_threshold=tool_threshold,
            )

        return WorkflowConfig(
            workflow_id=config.workflow_id,
            nodes=mutated_nodes,
            has_verification_step=config.has_verification_step,
            max_samples=config.max_samples,
            tool_threshold=config.tool_threshold,
        )

    def run_evolution_search(
        self,
        initial_config: WorkflowConfig,
        available_agents: List[str],
        cost_mode: CostMode,
        generations: int = 5,
        population_size: int = 4
    ) -> WorkflowConfig:
        """Runs the genetic algorithm over workflow graphs to find the fittest graph config."""
        population = [initial_config]
        # Seed population with mutations
        for _ in range(population_size - 1):
            population.append(self.mutate(initial_config, available_agents))

        for _ in range(generations):
            # Calculate fitness
            scored_pop = [(self.calculate_fitness(c, cost_mode), c) for c in population]
            scored_pop.sort(key=lambda x: x[0], reverse=True)

            # Selection: keep top 50%
            survivors = [c for _, c in scored_pop[:max(1, population_size // 2)]]

            # Reproduction & Mutation
            next_generation = list(survivors)
            while len(next_generation) < population_size:
                parent = random.choice(survivors)
                child = self.mutate(parent, available_agents)
                next_generation.append(child)

            population = next_generation

        # Return fittest config of final generation
        scored_pop = [(self.calculate_fitness(c, cost_mode), c) for c in population]
        scored_pop.sort(key=lambda x: x[0], reverse=True)
        return scored_pop[0][1]
