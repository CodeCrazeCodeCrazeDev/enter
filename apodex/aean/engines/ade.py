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
from ..models import DemandSignal, EngineName, Narrative, Opportunity, CustomerGraphEntry
from ..validation.epistemic import EpistemicFirewall

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
    """Demand sensing and narrative engineering (ADE) — Layers 1-10."""

    def __init__(
        self,
        ekg: EconomicKnowledgeGraph,
        governance: ConstitutionalFilter,
        llm: Optional[LLMAdapter] = None,
        *,
        rng: Optional[random.Random] = None,
        markets=None,
        firewall: Optional[EpistemicFirewall] = None,
    ) -> None:
        self.ekg = ekg
        self.governance = governance
        self.llm = llm or LLMAdapter()
        self._rng = rng or random.Random()
        self.markets = markets or DEFAULT_MARKETS
        self.firewall = firewall
        self.detection_threshold = 0.35  # Bounded for simulator throughput, high-fidelity gating in production

    # ------------------------------------------------------------------
    def sense_demand(self, max_signals: int = 3) -> List[DemandSignal]:
        """Detect fresh demand signals by fusing multiple data sources (Layer 1).

        Candidate signals must clear the :class:`EpistemicFirewall` (when one is
        attached) before they are recorded in the EKG.
        """
        signals: List[DemandSignal] = []
        for _ in range(max_signals):
            market, segments = self._rng.choice(self.markets)
            segment = self._rng.choice(segments)
            # Fuse several noisy source readings into a strength score.
            readings = [self._rng.random() for _ in DATA_SOURCES]
            strength = round(sum(readings) / len(readings), 4)

            # Cross-source correlation: corroborating if strength clears detection threshold
            if strength < self.detection_threshold:
                continue  # Below detection threshold — noise, not signal.

            tam = int(self._rng.uniform(5_000_000, 250_000_000))  # $50k–$2.5M in cents.

            # Agent 1: Opportunity Discovery Agent
            opportunity = Opportunity(
                description=f"{market}:{segment}",
                market_size=tam,
                competition=self._rng.choice(["low", "med", "high"]),
                probability=strength,
                supporting_signals=self._rng.sample(DATA_SOURCES, k=2)
            )

            # Agent 2: Customer Intelligence Agent
            customer_profile = CustomerGraphEntry(
                problem=f"Inefficiencies within {market} processes",
                desire="Automate repeatable operational pipelines to reduce overhead",
                objection="Pricing transparency and platform risk concerns",
                buying_trigger="Reaching API thresholds or manual scaling bottlenecks",
                preferred_channel=self._rng.choice(["LinkedIn", "Twitter", "Google Search", "TikTok"]),
                confidence=round(self._rng.uniform(0.6, 0.95), 4)
            )

            # Agent 3: Competitor Intelligence Agent
            competitor_notes = f"Competitor shifting messaging in {market}. Spotlighting weaknesses on {segment}."

            # Save newly detected entities to the EKG
            self.ekg.record_opportunity(opportunity)
            self.ekg.record_customer_profile(customer_profile)
            self.ekg.upsert_node(opportunity.id, "competitor_intelligence", notes=competitor_notes)

            # Retrieve mapped DemandSignal for backwards-compatibility
            compat_signal = self.ekg.signals[opportunity.id]

            if self.firewall is not None:
                validation = self.firewall.validate(compat_signal, readings)
                self.ekg.record_signal_validation(validation)
                if not validation.passed:
                    self.governance.note_decision(EngineName.ADE, success=False)
                    logger.info("Signal rejected by epistemic firewall: %s", validation.notes)
                    continue

            signals.append(compat_signal)
        return signals

    # ------------------------------------------------------------------
    def engineer_narrative(self, signal: DemandSignal) -> Optional[Narrative]:
        """Construct and record a narrative for ``signal`` (governance-checked) (Layer 2)."""
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

        # Positioning Agent
        core_narrative = f"Revolutionizing {signal.market} operations for {signal.segment} with AI-driven workflows."
        key_messages = [hook, body, f"Tailored perfectly for {signal.segment} pain points."]
        diff_angle = f"We specialize in {signal.segment} targeting with unparalleled service automation."

        # Guardrail check against Governance
        content_verdict = self.governance.review_content(hook + " " + body + " " + core_narrative)
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
            core_narrative=core_narrative,
            key_messages=key_messages,
            differentiation_angle=diff_angle,
        )
        self.ekg.record_narrative(narrative)
        self.governance.note_decision(EngineName.ADE, success=resonance >= 0.5)
        return narrative
