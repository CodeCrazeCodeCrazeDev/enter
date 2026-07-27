from __future__ import annotations
import uuid
import logging
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from apodex.arcs.world_graph import WorldGraph, EntityNode, RelationshipEdge

logger = logging.getLogger("arcs.evolution.scientific_discovery")


class Hypothesis(BaseModel):
    id: str = Field(default_factory=lambda: f"hyp_{uuid.uuid4().hex[:8]}")
    independent_variable: str
    dependent_variable: str
    expected_effect: float
    confidence: float = 0.5
    status: str = "PROPOSED"  # PROPOSED, TESTING, VALIDATED, FALSIFIED


class ScientificTheory(BaseModel):
    theory_id: str = Field(default_factory=lambda: f"theory_{uuid.uuid4().hex[:8]}")
    name: str
    hypothesis_id: str
    empirical_support: str
    p_value: float = 0.05
    equation: str


class ScientificDiscoveryEngine:
    """Layer 1 Scientific Discovery Engine.

    Treats every business decision as a scientific hypothesis. Continuously generates,
    designs RCTs, validates theories, and updates policies/world graphs based on evidence.
    """

    def __init__(self, world_graph: Optional[WorldGraph] = None) -> None:
        self.world_graph = world_graph or WorldGraph()
        self.hypotheses: Dict[str, Hypothesis] = {}
        self.theories: Dict[str, ScientificTheory] = {}

    def generate_hypothesis(self, independent: str, dependent: str, expected_effect: float) -> Hypothesis:
        """Continuously discover new relationships and generate testable hypotheses."""
        hyp = Hypothesis(
            independent_variable=independent,
            dependent_variable=dependent,
            expected_effect=expected_effect,
            status="PROPOSED"
        )
        self.hypotheses[hyp.id] = hyp
        logger.info(f"[Scientific Discovery] Formulated hypothesis {hyp.id}: '{independent}' causally affects '{dependent}' by {expected_effect:+.2f}")
        return hyp

    def design_rct_experiment(self, hypothesis_id: str) -> Dict[str, Any]:
        """Formulate a robust Randomized Controlled Trial (RCT) experiment design."""
        hyp = self.hypotheses.get(hypothesis_id)
        if not hyp:
            raise ValueError(f"Hypothesis '{hypothesis_id}' not found.")

        hyp.status = "TESTING"
        design = {
            "hypothesis_id": hypothesis_id,
            "experimental_design": "Randomized Controlled Trial (RCT)",
            "treatment_group_allocation": "50% traffic randomized",
            "control_group_allocation": "50% traffic randomized",
            "statistical_power_target": 0.8,
            "significance_level": 0.05
        }
        logger.info(f"[Scientific Discovery] Designed RCT experiment for hypothesis {hypothesis_id}")
        return design

    def synthesize_to_theory(self, hypothesis_id: str, sample_size: int, actual_effect: float, p_value: float) -> Optional[ScientificTheory]:
        """Fuses empirical outcome data, performs significance checks, and compiles a scientific theory."""
        hyp = self.hypotheses.get(hypothesis_id)
        if not hyp:
            return None

        if p_value < 0.05 and (actual_effect * hyp.expected_effect > 0):
            hyp.status = "VALIDATED"
            theory = ScientificTheory(
                name=f"Theory of {hyp.independent_variable.replace('_', ' ').title()} Impact",
                hypothesis_id=hypothesis_id,
                empirical_support=f"Validated via RCT with sample size of {sample_size}",
                p_value=p_value,
                equation=f"d({hyp.dependent_variable}) = {actual_effect:.3f} * d({hyp.independent_variable})"
            )
            self.theories[theory.theory_id] = theory

            # Update the WorldGraph with validated causal edge
            edge = RelationshipEdge(
                source_id=hyp.independent_variable,
                target_id=hyp.dependent_variable,
                relation_type="CAUSES",
                weight=1.0 - p_value,
                properties={"coefficient": actual_effect, "p_value": p_value, "theory_id": theory.theory_id}
            )
            self.world_graph.add_relation(edge)

            logger.info(f"[Scientific Discovery] THEORY COMPILED: '{theory.name}'. Updated Causal Edge in WorldGraph.")
            return theory
        else:
            hyp.status = "FALSIFIED"
            logger.warning(f"[Scientific Discovery] Hypothesis {hypothesis_id} FALSIFIED (p_value: {p_value:.3f}, actual_effect: {actual_effect:+.2f})")
            return None
