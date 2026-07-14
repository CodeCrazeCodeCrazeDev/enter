"""AEAN Research — the autonomous discovery engine.

The Research engine mines the EKG's append-only event log and realised
micro-cell outcomes to surface validated insights: which market/segment arms
are compounding, which are decaying, and where capital is being wasted. It also
tracks the organism's *autonomy level* (1-6) as a function of how many
decisions have been made and how accurate they have proven — the "10-level
discovery engine / autonomy ladder" from the spec, capped at the levels a
simulation can legitimately claim.
"""
from __future__ import annotations

import logging
from collections import defaultdict
from dataclasses import dataclass
from typing import List

from ..ekg import EconomicKnowledgeGraph

logger = logging.getLogger("aean.research")


@dataclass
class ResearchInsight:
    kind: str  # "compounding_arm" | "decaying_arm" | "capital_waste" | "autonomy"
    subject: str
    detail: str
    confidence: float


class ResearchEngine:
    """Autonomous market discovery and self-monitoring over the EKG."""

    def __init__(self, ekg: EconomicKnowledgeGraph) -> None:
        self.ekg = ekg

    def autonomy_level(self, decisions: int, accuracy: float) -> int:
        """Map track record onto the 1-6 autonomy ladder.

        Level 4 (autonomous analysis w/ human review) is the honest starting
        point; Levels 5-6 are earned with volume and accuracy.
        """
        if decisions < 25:
            return 3
        if accuracy >= 0.9 and decisions >= 200:
            return 6
        if accuracy >= 0.8 and decisions >= 75:
            return 5
        return 4

    def discover(self, decisions: int = 0, accuracy: float = 0.0) -> List[ResearchInsight]:
        insights: List[ResearchInsight] = []

        # Aggregate realised ROI by market:segment arm.
        by_arm_roi: dict[str, List[float]] = defaultdict(list)
        for cell in self.ekg.cells.values():
            if cell.deployed_cents > 0:
                by_arm_roi[f"{cell.market}:{cell.segment}"].append(cell.roi)

        for arm, rois in by_arm_roi.items():
            avg = sum(rois) / len(rois)
            conf = min(1.0, 0.4 + 0.1 * len(rois))
            if avg >= 0.3:
                insights.append(ResearchInsight("compounding_arm", arm, f"avg ROI {avg:.2f} over {len(rois)} cells", conf))
            elif avg <= -0.15:
                insights.append(ResearchInsight("decaying_arm", arm, f"avg ROI {avg:.2f}; consider retiring", conf))

        # Capital waste: killed cells that never returned revenue.
        wasted = [c for c in self.ekg.cells.values() if c.status.value == "killed" and c.revenue_cents == 0]
        if wasted:
            total = sum(c.deployed_cents for c in wasted)
            insights.append(
                ResearchInsight("capital_waste", "portfolio", f"{len(wasted)} dead cells burned {total} cents", 0.7)
            )

        level = self.autonomy_level(decisions, accuracy)
        insights.append(
            ResearchInsight("autonomy", "organism", f"operating at autonomy level {level}", accuracy or 0.5)
        )
        return insights
