from __future__ import annotations
import uuid
import random
import logging
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger("arcs.evolution.agent_evolution")


class EvolvingAgent(BaseModel):
    id: str = Field(default_factory=lambda: f"agent_{uuid.uuid4().hex[:8]}")
    role_name: str
    prompt_parameters: Dict[str, Any] = Field(default_factory=dict)
    fitness_score: float = Field(default=0.5, ge=0.0, le=1.0)


class AgentEvolutionEngine:
    """Layer 16 Evolution Engine.

    Models continuous optimization of agents via populations, mutation, crossover,
    and performance-gated tournament selections. Only the best agent structures survive.
    """

    def __init__(self, role_name: str) -> None:
        self.role_name = role_name
        self.population: List[EvolvingAgent] = []
        self._initialize_population()

    def _initialize_population(self, size: int = 10) -> None:
        """Spawn initial diverse population of evolving agents."""
        for _ in range(size):
            agent = EvolvingAgent(
                role_name=self.role_name,
                prompt_parameters={
                    "creativity_weight": random.uniform(0.1, 0.9),
                    "rigor_coefficient": random.uniform(0.1, 0.9),
                    "temperature": random.uniform(0.0, 1.0)
                }
            )
            self.population.append(agent)
        logger.info(f"[Evolution Engine] Initialized population of {size} agents for '{self.role_name}' role.")

    def mutate(self, agent: EvolvingAgent) -> EvolvingAgent:
        """Slightly mutate the agent parameters."""
        new_params = agent.prompt_parameters.copy()
        # Mutate float weights
        for key in ["creativity_weight", "rigor_coefficient", "temperature"]:
            if key in new_params:
                mutation_delta = random.uniform(-0.15, 0.15)
                new_params[key] = max(0.01, min(0.99, new_params[key] + mutation_delta))

        child = EvolvingAgent(
            role_name=self.role_name,
            prompt_parameters=new_params,
            fitness_score=0.5
        )
        logger.info(f"[Evolution Engine] Mutated parent {agent.id} -> child {child.id}")
        return child

    def crossover(self, parent_a: EvolvingAgent, parent_b: EvolvingAgent) -> EvolvingAgent:
        """Combine strategies of two parent agents."""
        child_params = {}
        # Simple genetic uniform crossover
        for key in parent_a.prompt_parameters.keys():
            child_params[key] = random.choice([
                parent_a.prompt_parameters[key],
                parent_b.prompt_parameters[key]
            ])

        child = EvolvingAgent(
            role_name=self.role_name,
            prompt_parameters=child_params,
            fitness_score=0.5
        )
        logger.info(f"[Evolution Engine] Crossover parents {parent_a.id} & {parent_b.id} -> child {child.id}")
        return child

    def run_tournament(self) -> EvolvingAgent:
        """Perform tournament selection.

        Sorts population by fitness, discards the bottom 30%, mutates/crossovers
        the top survivors, and returns the absolute champion.
        """
        # Sort by fitness descending
        self.population.sort(key=lambda a: a.fitness_score, reverse=True)
        champion = self.population[0]

        logger.info(f"[Evolution Engine] Running tournament. Champion: {champion.id} (Fitness: {champion.fitness_score:.2%})")

        # Discard the bottom 3 agents (out of 10)
        survivors = self.population[:7]

        # Reproduce to fill back population
        new_population = list(survivors)
        while len(new_population) < 10:
            if random.random() < 0.5:
                # Mutation
                parent = random.choice(survivors)
                new_population.append(self.mutate(parent))
            else:
                # Crossover
                p1, p2 = random.sample(survivors, 2)
                new_population.append(self.crossover(p1, p2))

        self.population = new_population
        return champion
