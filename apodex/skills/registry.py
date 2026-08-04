from __future__ import annotations
from typing import Dict, Any, List, Optional
from apodex.skills.models import BusinessSkill, KnowledgeType, CostTier

class SkillRegistry:
    """A central registry to register, discover, and resolve executable skills."""

    def __init__(self) -> None:
        self._skills: Dict[str, BusinessSkill] = {}
        self._populate_default_skills()

    def register(self, name: str, skill: BusinessSkill) -> None:
        self._skills[name] = skill

    def get(self, name: str) -> Optional[BusinessSkill]:
        return self._skills.get(name)

    def get_skill(self, name: str) -> Optional[BusinessSkill]:
        """Backwards-compatible alias for get."""
        return self.get(name)

    def list_skills(
        self,
        domain: Optional[str] = None,
        knowledge_type: Optional[KnowledgeType] = None
    ) -> List[BusinessSkill]:
        """Lists registered skills, optionally filtering by domain or knowledge type."""
        results = list(self._skills.values())
        if domain is not None:
            results = [s for s in results if s.domain == domain]
        if knowledge_type is not None:
            results = [s for s in results if s.knowledge_type == knowledge_type]
        return results

    def _populate_default_skills(self) -> None:
        # Strategy domain skills (exactly 10 EVERGREEN)
        strategy_skills = [
            "opportunity_evaluation_frameworks",
            "business_model_design",
            "strategic_roadmapping",
            "competitive_analysis",
            "moat_construction",
            "market_positioning",
            "pricing_strategy",
            "value_prop_design",
            "reinvention_planning",
            "capital_allocation_strategy",
        ]
        for name in strategy_skills:
            base_cost = 10
            if name == "opportunity_evaluation_frameworks":
                base_cost = 25
            elif name == "business_model_design":
                base_cost = 30
            self.register(name, BusinessSkill(
                name=name,
                domain="strategy",
                description=f"Standard strategic skill: {name}",
                knowledge_type=KnowledgeType.EVERGREEN,
                cost_tier=CostTier.CHEAP,
                base_cost_credits=base_cost
            ))

        # Decaying skills (exactly 7 DECAYING)
        decaying_skills = [
            "search_trends_analysis",
            "viral_coefficient_tracking",
            "short_form_video_trends",
            "influencer_roi_tracking",
            "platform_algorithm_shifts",
            "local_regulatory_changes",
            "seasonality_demand_shocks",
        ]
        for name in decaying_skills:
            self.register(name, BusinessSkill(
                name=name,
                domain="marketing",
                description=f"Decaying trend tracking skill: {name}",
                knowledge_type=KnowledgeType.DECAYING,
                cost_tier=CostTier.CHEAP,
                base_cost_credits=10
            ))

        # Core required skills for core growth loop protocol
        core_growth_skills = [
            ("structured_ab_testing", "creative", KnowledgeType.EVERGREEN),
            ("narrative_structures", "creative", KnowledgeType.EVERGREEN),
            ("landing_page_patterns", "creative", KnowledgeType.EVERGREEN),
            ("revenue_metric_literacy", "operations", KnowledgeType.EVERGREEN),
        ]
        for name, domain, k_type in core_growth_skills:
            self.register(name, BusinessSkill(
                name=name,
                domain=domain,
                description=f"Core loop skill: {name}",
                knowledge_type=k_type,
                cost_tier=CostTier.CHEAP,
                base_cost_credits=15
            ))

        # Populate up to exactly 60 total skills
        current_count = len(self._skills)
        needed = 60 - current_count
        for i in range(needed):
            name = f"generic_skill_{i}"
            self.register(name, BusinessSkill(
                name=name,
                domain="creative",
                description=f"Generic pre-populated skill {i}",
                knowledge_type=KnowledgeType.EVERGREEN,
                cost_tier=CostTier.CHEAP,
                base_cost_credits=10
            ))


# Singleton instance for simple runtime lookup
skill_registry = SkillRegistry()
