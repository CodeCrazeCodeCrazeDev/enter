"""ADE — Autonomous Demand Engine.

ADE performs two jobs in the flywheel:

1. **Demand sensing** — it synthesises demand signals from a configurable set of
   "data sources" (search velocity, social momentum, economic indicators,
   competitor moves). In the offline simulator these are stochastic processes
   seeded per market; in production they would be real connectors.
2. **Narrative engineering** — for a detected signal it constructs a narrative
   (theme + hook + body) via the pluggable :class:`LLMAdapter`, then predicts
   resonance. Narratives pass the constitutional content filter before landing
   in the EKG.
"""
from __future__ import annotations

import logging
import random
from typing import List, Optional

from ..ekg import EconomicKnowledgeGraph
from ..governance import ConstitutionalFilter
from ..llm import LLMAdapter
from ..models import DemandSignal, EngineName, Narrative

logger = logging.getLogger("aean.ade")

DEFAULT_MARKETS = [
    ("devtools", ["startups", "enterprise", "indie"]),
    ("fintech", ["smb", "consumer", "wealth"]),
    ("healthtech", ["clinics", "payers", "patients"]),
    ("climate", ["utilities", "industrial", "prosumer"]),
    ("creator_economy", ["solo", "agency", "brand"]),
]

DATA_SOURCES = ["search_velocity", "social_momentum", "economic_indicator", "competitor_move"]


class AutonomousDemandEngine:
    """Demand sensing and narrative engineering (ADE)."""

    def __init__(
        self,
        ekg: EconomicKnowledgeGraph,
        governance: ConstitutionalFilter,
        llm: Optional[LLMAdapter] = None,
        *,
        rng: Optional[random.Random] = None,
        markets=None,
    ) -> None:
        self.ekg = ekg
        self.governance = governance
        self.llm = llm or LLMAdapter()
        self._rng = rng or random.Random()
        self.markets = markets or DEFAULT_MARKETS

    # ------------------------------------------------------------------
    def sense_demand(self, max_signals: int = 3) -> List[DemandSignal]:
        """Detect fresh demand signals by fusing multiple data sources."""
        signals: List[DemandSignal] = []
        for _ in range(max_signals):
            market, segments = self._rng.choice(self.markets)
            segment = self._rng.choice(segments)
            # Fuse several noisy source readings into a strength score.
            readings = [self._rng.random() for _ in DATA_SOURCES]
            strength = round(sum(readings) / len(readings), 4)
            if strength < 0.35:
                continue  # Below detection threshold — noise, not signal.
            tam = int(self._rng.uniform(5_000_000, 250_000_000))  # $50k–$2.5M in cents.
            signal = DemandSignal(
                market=market,
                segment=segment,
                strength=strength,
                estimated_tam_cents=tam,
                elasticity=round(self._rng.uniform(-2.2, -0.8), 3),
                keywords=self._rng.sample(DATA_SOURCES, k=2),
            )
            self.ekg.record_signal(signal)
            signals.append(signal)
        return signals

    # ------------------------------------------------------------------
    def engineer_narrative(self, signal: DemandSignal) -> Optional[Narrative]:
        """Construct and record a narrative for ``signal`` (governance-checked)."""
        system = (
            "You are ADE, an autonomous demand engine. Write a concise, honest, "
            "compelling marketing narrative. Never make deceptive or guaranteed claims."
        )
        prompt = (
            f"Market: {signal.market}; segment: {signal.segment}; "
            f"signals: {', '.join(signal.keywords)}. Craft a one-line hook."
        )
        hook = self.llm.complete(prompt, system=system, max_tokens=60)
        body = self.llm.complete(
            f"Expand the hook into two sentences of value proposition for {signal.segment} in {signal.market}.",
            system=system,
            max_tokens=120,
        )
        content_verdict = self.governance.review_content(hook + " " + body)
        if not content_verdict.approved:
            self.governance.note_decision(EngineName.ADE, success=False)
            logger.info("ADE narrative rejected by governance: %s", content_verdict.reasons)
            return None

        resonance = round(min(1.0, 0.4 + 0.5 * signal.strength + self._rng.uniform(-0.1, 0.15)), 4)
        narrative = Narrative(
            signal_id=signal.signal_id,
            theme=f"{signal.market}:{signal.segment}",
            hook=hook,
            body=body,
            predicted_resonance=max(0.0, resonance),
            generated_by=self.llm.provider,
        )
        self.ekg.record_narrative(narrative)
        self.governance.note_decision(EngineName.ADE, success=resonance >= 0.5)
        return narrative
