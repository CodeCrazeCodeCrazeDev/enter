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
from ..models import EngineName, Narrative, VisualAsset, GenerationBrief, Visual

logger = logging.getLogger("aean.avie")

FORMATS = ["social_square", "story_vertical", "banner_wide", "thumbnail"]
CONCEPTS = ["bold_typographic", "product_hero", "lifestyle_scene", "data_visual", "minimal_brand"]
EMOTIONS = ["curiosity", "trust", "excitement", "calmness", "urgency"]


class AutonomousVisualIntelligenceEngine:
    """Visual intelligence and generative creative (AVIE) — Layers 1-8."""

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
        """Generate and score creative variants for a narrative (Layer 3 & 4)."""
        # Layer 1 & 2: Visual Demand Intelligence & Visual Psychology Engine
        required_features = ["high contrast", "clear typography"]
        avoid_features = ["low resolution", "cluttered backgrounds"]
        if "startups" in narrative.theme or "indie" in narrative.theme:
            required_features.append("human element")
            target_emotion = "excitement"
        else:
            required_features.append("data visualization")
            target_emotion = "trust"

        brief = GenerationBrief(
            required_features=required_features,
            avoid_features=avoid_features,
            target_emotion=target_emotion,
            target_segment=narrative.theme.split(":")[-1] if ":" in narrative.theme else "general",
            confidence=round(self._rng.uniform(0.7, 0.95), 4)
        )

        # Layer 3: Generative Engine (steered by psychology brief, compiling model-specific prompts)
        base_prompt = self.llm.complete(
            f"Describe a visual concept for the marketing hook: '{narrative.hook}'. Required: {', '.join(brief.required_features)}. Avoid: {', '.join(brief.avoid_features)}.",
            system="You are AVIE, an autonomous visual creative director guided by visual psychology.",
            max_tokens=80,
        )

        assets: List[VisualAsset] = []
        # Layer 4: Variant Explosion Engine (generating a structured grid of variants)
        for _ in range(self.variants_per_narrative):
            concept = self._rng.choice(CONCEPTS)
            fmt = self._rng.choice(FORMATS)
            prompt = f"{concept} | {fmt} | {base_prompt}"

            verdict = self.governance.review_content(prompt)
            if not verdict.approved:
                self.governance.note_decision(EngineName.AVIE, success=False)
                continue

            predicted_ctr = self._predict_ctr(narrative, concept, fmt)

            # Record a Visual contract object in EKG
            visual_contract = Visual(
                narrative_id=narrative.narrative_id,
                features={
                    "concept": concept,
                    "format": fmt,
                    "prompt": prompt,
                    "predicted_ctr": predicted_ctr,
                    "target_emotion": brief.target_emotion,
                    "generated_by": self.llm.provider
                },
                channel_variants=[f"ad_{fmt}", f"funnel_{fmt}"]
            )

            # Compatibility asset mapping
            asset = VisualAsset(
                asset_id=visual_contract.visual_id,
                narrative_id=narrative.narrative_id,
                concept=concept,
                format=fmt,
                predicted_ctr=predicted_ctr,
                prompt=prompt,
                generated_by=self.llm.provider,
            )

            # Record both contract and compatibility assets in EKG
            self.ekg.record_asset(asset)
            self.ekg.upsert_node(
                visual_contract.visual_id,
                "visual_contract",
                channel_variants=visual_contract.channel_variants,
                emotion=brief.target_emotion
            )

            self.governance.note_decision(EngineName.AVIE, success=predicted_ctr >= 0.03)
            assets.append(asset)

        return assets

    def _predict_ctr(self, narrative: Narrative, concept: str, fmt: str) -> float:
        """Heuristic performance predictor standing in for TRIBEv2 (Layer 1)."""
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
