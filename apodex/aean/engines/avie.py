"""AVIE — Autonomous Visual Intelligence Engine.

AVIE converts narratives into campaign-ready visual assets with a predicted
click-through rate. It produces a generative prompt (via the pluggable LLM
adapter), explodes it into format variants, and scores each variant with a
lightweight performance-prediction heuristic that stands in for the TRIBEv2
perception model described in the spec. Real image generation can be wired in
behind the same interface when an image API key is supplied.
"""
from __future__ import annotations

import logging
import random
from typing import List, Optional

from ..ekg import EconomicKnowledgeGraph
from ..governance import ConstitutionalFilter
from ..llm import LLMAdapter
from ..models import EngineName, Narrative, VisualAsset

logger = logging.getLogger("aean.avie")

FORMATS = ["social_square", "story_vertical", "banner_wide", "thumbnail"]
CONCEPTS = ["bold_typographic", "product_hero", "lifestyle_scene", "data_visual", "minimal_brand"]


class AutonomousVisualIntelligenceEngine:
    """Visual intelligence and generative creative (AVIE)."""

    def __init__(
        self,
        ekg: EconomicKnowledgeGraph,
        governance: ConstitutionalFilter,
        llm: Optional[LLMAdapter] = None,
        *,
        rng: Optional[random.Random] = None,
        variants_per_narrative: int = 3,
    ) -> None:
        self.ekg = ekg
        self.governance = governance
        self.llm = llm or LLMAdapter()
        self._rng = rng or random.Random()
        self.variants_per_narrative = variants_per_narrative

    def produce_assets(self, narrative: Narrative) -> List[VisualAsset]:
        """Generate and score creative variants for a narrative."""
        base_prompt = self.llm.complete(
            f"Describe a visual concept for the marketing hook: '{narrative.hook}'.",
            system="You are AVIE, an autonomous visual creative director.",
            max_tokens=80,
        )
        assets: List[VisualAsset] = []
        for _ in range(self.variants_per_narrative):
            concept = self._rng.choice(CONCEPTS)
            fmt = self._rng.choice(FORMATS)
            prompt = f"{concept} | {fmt} | {base_prompt}"
            verdict = self.governance.review_content(prompt)
            if not verdict.approved:
                self.governance.note_decision(EngineName.AVIE, success=False)
                continue
            predicted_ctr = self._predict_ctr(narrative, concept, fmt)
            asset = VisualAsset(
                narrative_id=narrative.narrative_id,
                concept=concept,
                format=fmt,
                predicted_ctr=predicted_ctr,
                prompt=prompt,
                generated_by=self.llm.provider,
            )
            self.ekg.record_asset(asset)
            self.governance.note_decision(EngineName.AVIE, success=predicted_ctr >= 0.03)
            assets.append(asset)
        return assets

    def _predict_ctr(self, narrative: Narrative, concept: str, fmt: str) -> float:
        """Heuristic performance predictor standing in for TRIBEv2."""
        concept_bonus = {
            "bold_typographic": 0.010,
            "product_hero": 0.012,
            "lifestyle_scene": 0.008,
            "data_visual": 0.006,
            "minimal_brand": 0.009,
        }[concept]
        fmt_bonus = {"social_square": 0.006, "story_vertical": 0.009, "banner_wide": 0.003, "thumbnail": 0.005}[fmt]
        base = 0.02 + 0.04 * narrative.predicted_resonance
        ctr = base + concept_bonus + fmt_bonus + self._rng.uniform(-0.004, 0.006)
        return round(max(0.001, min(0.25, ctr)), 5)
