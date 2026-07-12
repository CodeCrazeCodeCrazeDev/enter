from __future__ import annotations
import logging
import uuid
from typing import Any, Dict, List
from pydantic import BaseModel, Field

logger = logging.getLogger("arcs.opportunities.scanner")


class MarketOpportunity(BaseModel):
    opportunity_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    domain: str
    description: str
    estimated_size_cents: int
    pain_point_score: float = 0.5
    status: str = "discovered"  # discovered, validated, archived, active


class OpportunityScanner:
    """Enterprise-grade market scanning engine for mining pain points and unmet demand."""

    def __init__(self, confidence_threshold: float = 0.75) -> None:
        self.confidence_threshold = confidence_threshold
        self.discovered_opportunities: List[MarketOpportunity] = []

    def scan_market(self, domain: str, raw_feed: List[Dict[str, Any]]) -> List[MarketOpportunity]:
        """Scan raw market data, review feeds, and search queries to extract viable opportunities."""
        logger.info(f"[Scanner] Beginning market intelligence scan on domain: {domain}")
        found = []

        for item in raw_feed:
            query_volume = item.get("search_volume", 0)
            sentiment_friction = item.get("friction_sentiment", 0.0)  # High friction is good opportunity
            size_est = item.get("market_size_est_cents", 1000000)

            # High volume combined with high customer sentiment friction represents a major gap
            if query_volume > 5000 and sentiment_friction > 0.60:
                opp = MarketOpportunity(
                    domain=domain,
                    description=item.get("gap_description", "Unmet demand detected"),
                    estimated_size_cents=size_est,
                    pain_point_score=sentiment_friction,
                    status="discovered"
                )
                found.append(opp)
                self.discovered_opportunities.append(opp)
                logger.info(f"[Scanner] Discovered High-ROI Opportunity: {opp.description} (Est Size: {size_est} cents)")

        return found
