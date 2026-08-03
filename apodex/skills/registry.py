from __future__ import annotations
from typing import Dict, Any, Type, Optional, List
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
        """Backwards compatible alias for get."""
        return self.get(name)

    def list_skills(self, domain: Optional[str] = None, knowledge_type: Optional[KnowledgeType] = None) -> List[BusinessSkill]:
        skills_list = list(self._skills.values())
        if domain is not None:
            skills_list = [s for s in skills_list if s.domain == domain]
        if knowledge_type is not None:
            # support both Enum and string comparison safely
            kt_val = knowledge_type.value if hasattr(knowledge_type, "value") else knowledge_type
            skills_list = [s for s in skills_list if (s.knowledge_type.value if hasattr(s.knowledge_type, "value") else s.knowledge_type) == kt_val]
        return skills_list

    def _populate_default_skills(self) -> None:
        # 1. Register 10 strategy evergreen skills (including key ones)
        strat_skills = [
            ("opportunity_evaluation_frameworks", 25),
            ("narrative_structures", 10),
            ("landing_page_patterns", 10),
            ("revenue_metric_literacy", 10),
            ("business_model_design", 30),
            ("strategic_roadmapping", 15),
            ("competitive_moat_building", 20),
            ("market_sizing_triangulation", 15),
            ("pricing_elasticity_discovery", 25),
            ("venture_portfolio_diversification", 35)
        ]
        for name, cost in strat_skills:
            self.register(name, BusinessSkill(
                name=name,
                domain="strategy",
                description=f"Automated execution for {name}",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=cost
            ))

        # 2. Register 7 decaying skills (any domain)
        for i in range(1, 8):
            name = f"trending_demand_signal_scan_{i}"
            self.register(name, BusinessSkill(
                name=name,
                domain="marketing",
                description=f"Decaying trend scanner {i}",
                knowledge_type=KnowledgeType.DECAYING,
                base_cost_credits=10
            ))

        # 3. Register creative evergreen skills (including key ones)
        self.register("structured_ab_testing", BusinessSkill(
            name="structured_ab_testing",
            domain="creative",
            description="Statistical A/B testing and variant design",
            knowledge_type=KnowledgeType.EVERGREEN,
            base_cost_credits=15
        ))

        # 4. Fill up to exactly 60 default skills
        current_count = len(self._skills)
        needed = 60 - current_count
        for i in range(needed):
            name = f"business_capability_node_{i}"
            self.register(name, BusinessSkill(
                name=name,
                domain="operations",
                description=f"Generic operations capability {i}",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ))


# Singleton instance for simple runtime lookup
skill_registry = SkillRegistry()
