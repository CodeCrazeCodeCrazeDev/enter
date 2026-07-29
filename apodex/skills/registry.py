from __future__ import annotations
from typing import Dict, Any, Type, Optional, List, Union

from apodex.skills.base import BaseSkill
from apodex.skills.models import BusinessSkill, KnowledgeType, CostTier


class SkillRegistry:
    """A central registry to register, discover, and resolve executable skills."""

    def __init__(self) -> None:
        self._skills: Dict[str, BusinessSkill] = {}
        self._legacy_skills: Dict[str, BaseSkill[Any, Any]] = {}
        self._populate_default_skills()

    def _populate_default_skills(self) -> None:
        # 1. strategy domain (exactly 10 skills, all EVERGREEN)
        strategy_skills = [
            BusinessSkill(
                name="opportunity_evaluation_frameworks",
                domain="strategy",
                description="Framework to evaluate market opportunities and estimate addressable size.",
                knowledge_type=KnowledgeType.EVERGREEN,
                cost_tier=CostTier.CHEAP,
                base_cost_credits=25
            ),
            BusinessSkill(
                name="business_model_design",
                domain="strategy",
                description="Design sustainable business and monetization strategies.",
                knowledge_type=KnowledgeType.EVERGREEN,
                cost_tier=CostTier.CHEAP,
                base_cost_credits=30
            ),
            BusinessSkill(
                name="corporate_strategy_review",
                domain="strategy",
                description="Perform regular strategic alignment and review corporate direction.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="market_entry_heuristics",
                domain="strategy",
                description="Heuristics to determine optimal strategies to enter new market niches.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="competitive_moat_analysis",
                domain="strategy",
                description="Analyze defensive factors and competitive moats.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="pricing_elasticity_strategy",
                domain="strategy",
                description="Formulate pricing models based on value elasticities.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="capital_budgeting_framework",
                domain="strategy",
                description="Framework to guide and restrict strategic capital deployment.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="portfolio_risk_hedging",
                domain="strategy",
                description="Formulate hedging plans for research/venture portfolio exposures.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="acquisition_target_evaluation",
                domain="strategy",
                description="Evaluate strategic merger and acquisition opportunities.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="exit_scenario_planning",
                domain="strategy",
                description="Plan long-term exit scenarios and strategic transitions.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            )
        ]

        # 2. analytics domain (10 skills, exactly 4 DECAYING and 6 EVERGREEN)
        analytics_skills = [
            BusinessSkill(
                name="revenue_metric_literacy",
                domain="analytics",
                description="Interpret real-time MRR, CAC, and LTV performance metrics.",
                knowledge_type=KnowledgeType.DECAYING,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="realtime_competitor_price_tracking",
                domain="analytics",
                description="Track real-time dynamic competitor price modifications.",
                knowledge_type=KnowledgeType.DECAYING,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="weekly_churn_analysis",
                domain="analytics",
                description="Compute weekly customer churn velocity and patterns.",
                knowledge_type=KnowledgeType.DECAYING,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="hourly_web_traffic_anomalies",
                domain="analytics",
                description="Detect hourly spikes or drops in inbound web traffic.",
                knowledge_type=KnowledgeType.DECAYING,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="cohort_retention_modeling",
                domain="analytics",
                description="Perform advanced customer cohort retention modeling.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="customer_lifetime_value_projection",
                domain="analytics",
                description="Project customer lifetime values based on historical trends.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="attribution_funnel_analytics",
                domain="analytics",
                description="Evaluate marketing attribution across multi-touch funnels.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="data_pipeline_throughput_audit",
                domain="analytics",
                description="Audit data processing pipelines for bottleneck detection.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="anomaly_detection_telemetry",
                domain="analytics",
                description="Evaluate real-time operational telemetry for system anomalies.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="predictive_lead_scoring",
                domain="analytics",
                description="Construct predictive scoring models for sales pipeline optimization.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            )
        ]

        # 3. creative domain (5 skills, all EVERGREEN)
        creative_skills = [
            BusinessSkill(
                name="structured_ab_testing",
                domain="creative",
                description="Structure split-testing protocols for messaging and offers.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="copywriting_headline_generator",
                domain="creative",
                description="Synthesize compelling and relevant headlines for target audiences.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="ad_banner_variant_synthesis",
                domain="creative",
                description="Generate visual layout configurations for split ad variants.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="brand_identity_alignment_check",
                domain="creative",
                description="Ensure creative copy adheres strictly to institutional guidelines.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="creative_concept_brainstorming",
                domain="creative",
                description="Generate raw concepts and ideas for growth experimentation.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            )
        ]

        # 4. marketing domain (8 skills, exactly 2 DECAYING and 6 EVERGREEN)
        marketing_skills = [
            BusinessSkill(
                name="social_media_trending_signals",
                domain="marketing",
                description="Track trending keywords and viral topics across socials.",
                knowledge_type=KnowledgeType.DECAYING,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="live_ads_ctr_feed",
                domain="marketing",
                description="Analyze current hour CTR feed for live active campaigns.",
                knowledge_type=KnowledgeType.DECAYING,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="narrative_structures",
                domain="marketing",
                description="Define problem-solution narrative frameworks.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="campaign_performance_optimization",
                domain="marketing",
                description="Optimize marketing parameters based on cost-per-acquisition yields.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="email_sequences_auto_responder",
                domain="marketing",
                description="Draft automated sequence responder campaigns.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="seo_metadata_keyword_injection",
                domain="marketing",
                description="Audit metadata index terms to enhance organic search relevance.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="influence_network_outreach",
                domain="marketing",
                description="Identify relevant distribution channels and coordinate collaborations.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="content_distribution_automation",
                domain="marketing",
                description="Automate distribution patterns across publishing channels.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            )
        ]

        # 5. sales domain (5 skills, exactly 1 DECAYING and 4 EVERGREEN)
        sales_skills = [
            BusinessSkill(
                name="seasonal_demand_forecasting",
                domain="sales",
                description="Forecast demand variations based on volatile seasonal data.",
                knowledge_type=KnowledgeType.DECAYING,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="inbound_lead_qualification",
                domain="sales",
                description="Qualify prospects against enterprise readiness metrics.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="sales_pipeline_velocity_audit",
                domain="sales",
                description="Calculate lead transition rates across transaction phases.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="proposal_generation_assistant",
                domain="sales",
                description="Generate tailored service agreements based on specifications.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="discount_elasticity_evaluation",
                domain="sales",
                description="Assess customer conversion response to temporary discount incentives.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            )
        ]

        # 6. engineering domain (8 skills, all EVERGREEN)
        engineering_skills = [
            BusinessSkill(
                name="landing_page_patterns",
                domain="engineering",
                description="Implement optimal high-converting landing page layouts.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="database_schema_tuning",
                domain="engineering",
                description="Tune relational indexing paths to minimize querying latencies.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="container_orchestration_setup",
                domain="engineering",
                description="Configure cluster deployment maps for scaled environments.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="automated_unit_testing",
                domain="engineering",
                description="Execute automated testing sequences and compile logs.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="api_endpoint_latency_optimization",
                domain="engineering",
                description="Profile and optimize endpoint response paths.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="secure_credentials_management",
                domain="engineering",
                description="Audit environment credential access to prevent accidental leakage.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="ci_cd_deployment_pipeline",
                domain="engineering",
                description="Maintain reliable deployment triggers and rollback hooks.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="static_code_analysis_linter",
                domain="engineering",
                description="Execute static architectural scanners for security vulnerabilities.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            )
        ]

        # 7. operations domain (5 skills, all EVERGREEN)
        operations_skills = [
            BusinessSkill(
                name="inventory_turnover_optimization",
                domain="operations",
                description="Evaluate stocking velocities to optimize capital utilization.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="supply_chain_logistics_routing",
                domain="operations",
                description="Determine optimal transportation paths to minimize costs.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="customer_support_sla_tracker",
                domain="operations",
                description="Monitor response timelines to maintain service commitments.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="resource_utilization_scheduler",
                domain="operations",
                description="Schedule personnel allocations based on active project demands.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="vendor_pricing_negotiation_audit",
                domain="operations",
                description="Audit supplier invoices against contract agreement specifications.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            )
        ]

        # 8. legal domain (5 skills, all EVERGREEN)
        legal_skills = [
            BusinessSkill(
                name="contract_clause_risk_parser",
                domain="legal",
                description="Analyze legal documents to flag high-risk liabilities.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="intellectual_property_patent_search",
                domain="legal",
                description="Search patent databases to confirm registration freedom.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="terms_of_service_generator",
                domain="legal",
                description="Generate compliant online terms of use frameworks.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="privacy_policy_compliance_review",
                domain="legal",
                description="Verify privacy disclosures satisfy global regulatory changes.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="non_disclosure_agreement_validator",
                domain="legal",
                description="Validate parameters of non-disclosure templates.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            )
        ]

        # 9. compliance domain (4 skills, all EVERGREEN)
        compliance_skills = [
            BusinessSkill(
                name="grc_policy_conformance_scanner",
                domain="compliance",
                description="Run corporate governance compliance checklist reviews.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="financial_transaction_audit_trail",
                domain="compliance",
                description="Ensure transaction entries maintain strict immutable histories.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="know_your_customer_identity_verifier",
                domain="compliance",
                description="Process identity documents to satisfy verification thresholds.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="anti_money_laundering_flag_detector",
                domain="compliance",
                description="Monitor velocity patterns to detect suspicious trading behavior.",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            )
        ]

        # Combine all 60 authentic skills
        all_default_skills = (
            strategy_skills +
            analytics_skills +
            creative_skills +
            marketing_skills +
            sales_skills +
            engineering_skills +
            operations_skills +
            legal_skills +
            compliance_skills
        )

        # Register everything into the registry maps
        for skill in all_default_skills:
            self._skills[skill.name] = skill

    def register(self, name: str, skill: BaseSkill[Any, Any]) -> None:
        """Register a legacy BaseSkill execution unit."""
        self._legacy_skills[name] = skill

    def get(self, name: str) -> Optional[BaseSkill[Any, Any] | BusinessSkill]:
        """Fetch a skill from the registry."""
        if name in self._legacy_skills:
            return self._legacy_skills[name]
        return self._skills.get(name)

    def get_skill(self, name: str) -> Optional[BusinessSkill]:
        """Backwards compatible alias for retrieving a typed BusinessSkill."""
        return self._skills.get(name)

    def list_skills(
        self,
        domain: Optional[str] = None,
        knowledge_type: Optional[KnowledgeType] = None
    ) -> Union[List[str], List[BusinessSkill]]:
        """
        List and filter registered skills.
        To maintain strict backwards-compatibility with legacy public callers:
        - If no filtering arguments are passed, returns List[str] representing skill names.
        - If filtering arguments are provided (indicating a new capability/test caller),
          returns List[BusinessSkill] filtered objects.
        """
        if domain is None and knowledge_type is None:
            return list(self._skills.keys())

        # If filtering is provided, return filtered BusinessSkill list
        skills = list(self._skills.values())
        if domain is not None:
            skills = [s for s in skills if s.domain == domain]
        if knowledge_type is not None:
            skills = [s for s in skills if s.knowledge_type == knowledge_type]
        return skills


# Singleton instance for simple runtime lookup
skill_registry = SkillRegistry()
