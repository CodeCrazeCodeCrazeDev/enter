from __future__ import annotations
from typing import Dict, List, Optional
from apodex.skills.models import BusinessSkill, KnowledgeType, CostTier


class SkillRegistry:
    """Centralized, global registry populated with all 60 grounded business skills."""

    def __init__(self) -> None:
        self._skills: Dict[str, BusinessSkill] = {}
        self._populate_registry()

    def register(self, skill: BusinessSkill) -> None:
        """Register a new business skill dynamically."""
        self._skills[skill.name] = skill

    def get_skill(self, name: str) -> Optional[BusinessSkill]:
        """Retrieve a registered skill by name."""
        return self._skills.get(name)

    def list_skills(self, domain: Optional[str] = None, knowledge_type: Optional[KnowledgeType] = None) -> List[BusinessSkill]:
        """List skills, optionally filtering by domain or knowledge type."""
        results = list(self._skills.values())
        if domain:
            results = [s for s in results if s.domain == domain]
        if knowledge_type:
            results = [s for s in results if s.knowledge_type == knowledge_type]
        return results

    def _populate_registry(self) -> None:
        skills_data = [
            # =================================================================
            # 1. Entrepreneurs & Business Books (Strategy, Risk, Value Creation)
            # =================================================================
            {
                "name": "idea_generation_patterns",
                "domain": "strategy",
                "description": "How founders systematically generate and refine ideas via pain-point mining and scratch-your-own-itch.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 20,
            },
            {
                "name": "opportunity_evaluation_frameworks",
                "domain": "strategy",
                "description": "Frameworks to evaluate ideas based on market size, urgency, competition, and timing.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 25,
            },
            {
                "name": "mvp_lean_experimentation",
                "domain": "strategy",
                "description": "Designing minimum viable products to validate core assumptions quickly and cheaply.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 20,
            },
            {
                "name": "pivot_vs_persevere_criteria",
                "domain": "strategy",
                "description": "Recognizing structural triggers and metrics to pivot vs. double down.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 15,
            },
            {
                "name": "moats_and_defensibility",
                "domain": "strategy",
                "description": "Building sustainable advantages like network effects, switching costs, and distribution.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 20,
            },
            {
                "name": "risk_management_under_uncertainty",
                "domain": "strategy",
                "description": "Betting small, learning via feedback, and scaling only when signals are strong.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 15,
            },
            {
                "name": "strategic_focus_prioritization",
                "domain": "strategy",
                "description": "Choosing the few high-impact bets and filtering out distracting noise.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 15,
            },
            {
                "name": "compounding_improvement_mindset",
                "domain": "strategy",
                "description": "Stacking marginal product, process, and brand improvements to build long-term advantages.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 10,
            },
            {
                "name": "business_model_design",
                "domain": "strategy",
                "description": "Optimizing subscription vs transactional, platforms, usage-based, or freemium structures.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 30,
            },
            {
                "name": "partnership_ecosystem_strategies",
                "domain": "strategy",
                "description": "Leveraging external distribution, data, or product integrations to compound reach.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 20,
            },

            # =================================================================
            # 2. Companies & Market Research (Customer, Competition, Demand)
            # =================================================================
            {
                "name": "customer_segmentation",
                "domain": "market_research",
                "description": "Grouping potential buyers by needs, behaviors, willingness to pay, and operational contexts.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 20,
            },
            {
                "name": "persona_creation",
                "domain": "market_research",
                "description": "Defining user/buyer archetypes complete with pain points, objections, and triggers.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 15,
            },
            {
                "name": "jobs_to_be_done_analysis",
                "domain": "market_research",
                "description": "Uncovering the structural progress or 'job' customers are trying to resolve with a product.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 20,
            },
            {
                "name": "customer_discovery_interviewing",
                "domain": "market_research",
                "description": "Eliciting unbiased demand insights via structured 'The Mom Test' interviewing methodology.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 20,
            },
            {
                "name": "competitive_landscape_mapping",
                "domain": "market_research",
                "description": "Identifying direct/indirect competitors, tracking feature/pricing matrices, and locating gaps.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 25,
            },
            {
                "name": "market_sizing_and_potential",
                "domain": "market_research",
                "description": "Estimating addressable markets (TAM, SAM, SOM) for strategic sizing.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 20,
            },
            {
                "name": "trend_detection",
                "domain": "market_research",
                "description": "Spotting high-velocity macroeconomic and user behavioral signals (DECAYING).",
                "knowledge_type": KnowledgeType.DECAYING,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 30,
            },
            {
                "name": "pain_point_prioritization",
                "domain": "market_research",
                "description": "Ranking customer friction by severity, frequency, and willingness to pay.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 15,
            },
            {
                "name": "feedback_loop_design",
                "domain": "market_research",
                "description": "Structuring NPS, in-app micro-surveys, and usage-triggered metrics to drive iteration.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 15,
            },
            {
                "name": "product_market_fit_signals",
                "domain": "market_research",
                "description": "Evaluating qualitative and quantitative traction signals (the Sean Ellis test, churn plateaus).",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 25,
            },

            # =================================================================
            # 3. Marketing Agencies & Brand Strategy (Positioning, Story, Perception)
            # =================================================================
            {
                "name": "positioning_frameworks",
                "domain": "marketing",
                "description": "Defining unique market positions (For [segment] who [need], we are [category] that [differentiator]).",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 20,
            },
            {
                "name": "category_strategy",
                "domain": "marketing",
                "description": "Establishing positioning inside an existing market vs. designing and owning a new category.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 25,
            },
            {
                "name": "brand_voice_and_tone",
                "domain": "marketing",
                "description": "Defining structural brand guidelines, personality dimensions, and copywriting rules.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 15,
            },
            {
                "name": "narrative_structures",
                "domain": "marketing",
                "description": "Drafting core brand narrative (Problem -> Tension -> Solution -> Proof -> Outcome).",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 20,
            },
            {
                "name": "differentiation_mapping",
                "domain": "marketing",
                "description": "Mapping must-haves versus value-adders versus unique value drivers.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 15,
            },
            {
                "name": "message_hierarchy",
                "domain": "marketing",
                "description": "Defining primary hook, secondary benefits, evidence, risk reversals, and FAQ mapping.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 15,
            },
            {
                "name": "objection_preemption",
                "domain": "marketing",
                "description": "Proactively addressing doubts inside landing pages, emails, and initial outreach.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 15,
            },
            {
                "name": "social_proof_tactics",
                "domain": "marketing",
                "description": "Leveraging testimonials, case studies, partner logos, and security trust badges.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 10,
            },
            {
                "name": "brand_architecture",
                "domain": "marketing",
                "description": "Structuring multiple products, sub-brands, or API wrappers under a single cohesive identity.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 25,
            },
            {
                "name": "repositioning_rebranding",
                "domain": "marketing",
                "description": "Transitioning market perception of legacy assets toward higher-value target markets.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 30,
            },

            # =================================================================
            # 4. Creative & Content Teams (Copy, Design, Media, Experiments)
            # =================================================================
            {
                "name": "landing_page_patterns",
                "domain": "creative",
                "description": "Generating standard landing page wireframes (Hero, benefits, social proof, CTAs).",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 25,
            },
            {
                "name": "ad_creative_principles",
                "domain": "creative",
                "description": "Designing high-converting ad concepts (Strong hooks, pattern breaks, and call-to-actions).",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 20,
            },
            {
                "name": "educational_content_strategy",
                "domain": "creative",
                "description": "Drafting guides, blogs, and API documentation to attract and nurture organic signups.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 15,
            },
            {
                "name": "email_marketing_playbooks",
                "domain": "creative",
                "description": "Sequencing welcome flows, trial triggers, and onboarding nurtures to increase activations.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 20,
            },
            {
                "name": "platform_specific_content_formats",
                "domain": "creative",
                "description": "Adapting messaging into platform native formats (DECAYING).",
                "knowledge_type": KnowledgeType.DECAYING,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 15,
            },
            {
                "name": "basic_visual_identity",
                "domain": "creative",
                "description": "Selecting typography, color palettes, and visual templates matching brand guidelines.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 25,
            },
            {
                "name": "funnel_stage_content_mapping",
                "domain": "creative",
                "description": "Mapping creative formats to awareness, consideration, and conversion stages.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 15,
            },
            {
                "name": "structured_ab_testing",
                "domain": "creative",
                "description": "Running hypothesis-driven split testing (variants, durations, sample bounds).",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 30,
            },
            {
                "name": "storytelling_in_video",
                "domain": "creative",
                "description": "Structuring scripts and hooks for multimedia, webinars, and dynamic video ads.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 20,
            },
            {
                "name": "content_repurposing_systems",
                "domain": "creative",
                "description": "Modular workflow to translate one comprehensive asset into multichannel micro-assets.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 15,
            },

            # =================================================================
            # 5. Growth & Performance Marketing (Traffic, Attention, Growth Loops)
            # =================================================================
            {
                "name": "seo_fundamentals",
                "domain": "growth",
                "description": "Keyword research, technical structure optimization, and authority-building link maps.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 20,
            },
            {
                "name": "paid_acquisition_strategy",
                "domain": "growth",
                "description": "Allocating paid budget across ad platforms and optimizing cost per click/lead (DECAYING).",
                "knowledge_type": KnowledgeType.DECAYING,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 30,
            },
            {
                "name": "retargeting_remarketing",
                "domain": "growth",
                "description": "Nurturing bounced visitors who demonstrated intent but didn't convert (DECAYING).",
                "knowledge_type": KnowledgeType.DECAYING,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 20,
            },
            {
                "name": "funnel_analytics",
                "domain": "growth",
                "description": "Measuring multi-touch attribution (impression -> signup -> activation -> MRR).",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 25,
            },
            {
                "name": "growth_loop_design",
                "domain": "growth",
                "description": "Designing product, referral, or content growth loops that reinforce user acquisition.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 25,
            },
            {
                "name": "referral_affiliate_partner",
                "domain": "growth",
                "description": "Designing partner referral tracking networks and incentive mechanisms.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 20,
            },
            {
                "name": "community_led_growth",
                "domain": "growth",
                "description": "Nurturing developer advocacy and customer user groups to foster organic word-of-mouth.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 20,
            },
            {
                "name": "channel_lifecycle_management",
                "domain": "growth",
                "description": "Analyzing saturation limits, CPC fatigue, and forecasting replacement channels (DECAYING).",
                "knowledge_type": KnowledgeType.DECAYING,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 25,
            },
            {
                "name": "offer_engineering",
                "domain": "growth",
                "description": "Bundling plans, trial length configurations, and discounts to optimize perceived value.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 20,
            },
            {
                "name": "attention_intent_balance",
                "domain": "growth",
                "description": "Balancing cheap reach campaigns with high-cost, high-intent lead conversion flows.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 15,
            },

            # =================================================================
            # 6. Sales Agencies & Revenue Teams (Selling, Pipelines, Metrics)
            # =================================================================
            {
                "name": "lead_sourcing_qualification",
                "domain": "sales",
                "description": "Building and filtering prospect lists based on ICP fit and intent signals (DECAYING).",
                "knowledge_type": KnowledgeType.DECAYING,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 20,
            },
            {
                "name": "cold_outreach_frameworks",
                "domain": "sales",
                "description": "Drafting personalized multi-step outbound sequences (email/DMs) to get meetings.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 20,
            },
            {
                "name": "discovery_need_analysis",
                "domain": "sales",
                "description": "Diagnosing B2B buyer problems, timeline constraints, budget, and decision hierarchy.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 15,
            },
            {
                "name": "solution_selling_demos",
                "domain": "sales",
                "description": "Structuring software demos directly addressing explicit buyer pain points.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 20,
            },
            {
                "name": "structured_objection_handling",
                "domain": "sales",
                "description": "Addressing standard price, timing, authority, or integration objections.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 15,
            },
            {
                "name": "closing_strategies",
                "domain": "sales",
                "description": "Structuring trial closures, contractual agreements, and immediate next steps.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 15,
            },
            {
                "name": "pipeline_forecast_management",
                "domain": "sales",
                "description": "Tracking stage progression, forecasting closure rates, and maintaining pipeline hygiene (DECAYING).",
                "knowledge_type": KnowledgeType.DECAYING,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 25,
            },
            {
                "name": "account_expansion",
                "domain": "sales",
                "description": "Structuring cross-sells, seat expansion, or custom enterprise usage contracts.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 20,
            },
            {
                "name": "sales_marketing_alignment",
                "domain": "sales",
                "description": "Setting SQL/MQL thresholds, routing lead alerts, and establishing revenue SLAs.",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 15,
            },
            {
                "name": "revenue_metric_literacy",
                "domain": "sales",
                "description": "Evaluating overall SaaS unit economics (CAC, LTV, churn, payback, ARR/MRR).",
                "knowledge_type": KnowledgeType.EVERGREEN,
                "cost_tier": CostTier.CHEAP,
                "base_cost_credits": 30,
            },
        ]

        for s in skills_data:
            self.register(BusinessSkill(**s))
