from __future__ import annotations
import logging
from typing import Any, Dict, List
from pydantic import BaseModel, Field

logger = logging.getLogger("arcs.product.manager")


class SubscriptionTier(BaseModel):
    name: str  # Free, Growth, Enterprise
    arpu_cents: int
    allowed_api_calls: int
    features: List[str] = Field(default_factory=list)


class ProductPackagingManager:
    """Packaging Engine organizing modular SaaS tiers, pricing models, and grandfathered quotas."""

    def __init__(self) -> None:
        self.tiers: Dict[str, SubscriptionTier] = {
            "free": SubscriptionTier(name="Free", arpu_cents=0, allowed_api_calls=1000, features=["basic_search"]),
            "growth": SubscriptionTier(name="Growth", arpu_cents=4900, allowed_api_calls=50000, features=["basic_search", "code_compiler"]),
            "enterprise": SubscriptionTier(name="Enterprise", arpu_cents=49900, allowed_api_calls=1000000, features=["basic_search", "code_compiler", "sandbox_run", "dedicated_treasury"])
        }

    def configure_tier(self, name: str, arpu_cents: int, api_limit: int, features: List[str]) -> SubscriptionTier:
        tier = SubscriptionTier(name=name, arpu_cents=arpu_cents, allowed_api_calls=api_limit, features=features)
        self.tiers[name.lower()] = tier
        logger.info(f"[Product] Configured subscription packaging tier '{name}'")
        return tier

    def fetch_tier(self, tier_name: str) -> SubscriptionTier:
        key = tier_name.lower()
        if key not in self.tiers:
            raise KeyError(f"Subscription tier '{tier_name}' is not registered.")
        return self.tiers[key]
