from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, List
from pydantic import BaseModel

from apodex.skills.models import KnowledgeType, CostTier
from apodex.skills.runner import SkillRunner
from apodex.arcs.world_graph import EntityNode, RelationshipEdge, BeliefNode


# =====================================================================
# Specialized Custom Executors for the Core Growth Loop
# =====================================================================

def execute_opportunity_evaluation(
    inputs: Dict[str, Any],
    tier: CostTier,
    runner: SkillRunner
) -> Dict[str, Any]:
    """
    Custom Executor for 'opportunity_evaluation_frameworks'.
    Inputs: 'niche_name', 'estimated_tam_cents'
    Mutations: Creates a Market node, a Competitor node, a COMPETES_WITH relation, and a Belief.
    """
    niche = inputs.get("niche_name", "AI PDF Processor")
    tam = inputs.get("estimated_tam_cents", 100000000)  # $1M baseline

    market_id = f"market_{uuid.uuid4().hex[:6]}"
    competitor_id = f"competitor_{uuid.uuid4().hex[:6]}"

    # 1. Add Market node
    market_node = EntityNode(
        node_id=market_id,
        node_type="market",
        properties={
            "name": niche,
            "estimated_tam_cents": tam,
            "knowledge_type": KnowledgeType.EVERGREEN.value,
            "observed_at": datetime.utcnow().isoformat()
        }
    )
    runner.world_graph.add_node(market_node)

    # 2. Add Competitor node
    competitor_node = EntityNode(
        node_id=competitor_id,
        node_type="competitor",
        properties={
            "name": f"Legacy competitor for {niche}",
            "knowledge_type": KnowledgeType.EVERGREEN.value,
            "observed_at": datetime.utcnow().isoformat()
        }
    )
    runner.world_graph.add_node(competitor_node)

    # 3. Add Relationship: Competitor COMPETES_WITH Venture Market
    competes_edge = RelationshipEdge(
        source_id=competitor_id,
        target_id=market_id,
        relation_type="COMPETES_WITH",
        weight=0.85 if tier == CostTier.EXPENSIVE else 0.5,
        properties={
            "knowledge_type": KnowledgeType.EVERGREEN.value,
            "observed_at": datetime.utcnow().isoformat()
        }
    )
    runner.world_graph.add_relation(competes_edge)

    # 4. Add Bayesian Belief Node over the edge
    belief = BeliefNode(
        belief_id=f"belief_opp_{uuid.uuid4().hex[:6]}",
        target_edge_id=f"{competitor_id}:{market_id}",
        probability=0.90 if tier == CostTier.EXPENSIVE else 0.70,
        evidence=["industry_report_2026_q3"]
    )
    runner.world_graph.add_belief(belief)

    return {
        "status": "opportunity_validated",
        "market_id": market_id,
        "competitor_id": competitor_id,
        "anchors_hit": ["anchor_opportunity_evaluation_success"],
        "metrics_lift": {"market_validation_confidence": 0.15 if tier == CostTier.EXPENSIVE else 0.05}
    }


def execute_narrative_structures(
    inputs: Dict[str, Any],
    tier: CostTier,
    runner: SkillRunner
) -> Dict[str, Any]:
    """
    Custom Executor for 'narrative_structures'.
    Inputs: 'market_id', 'core_pain_point'
    Mutations: Creates a Narrative node, and a TARGETS_PERSONA relationship.
    """
    market_id = inputs.get("market_id", "market_default")
    pain = inputs.get("core_pain_point", "High pricing friction")

    narrative_id = f"narrative_{uuid.uuid4().hex[:6]}"

    # 1. Create Narrative Node
    narrative_node = EntityNode(
        node_id=narrative_id,
        node_type="resource",
        properties={
            "name": f"Solution to {pain} Narrative",
            "narrative_framework": "Problem-Tension-Solution-Proof",
            "knowledge_type": KnowledgeType.EVERGREEN.value,
            "observed_at": datetime.utcnow().isoformat()
        }
    )
    runner.world_graph.add_node(narrative_node)

    # 2. Assert relationship: Narrative targets the market niche
    targets_edge = RelationshipEdge(
        source_id=narrative_id,
        target_id=market_id,
        relation_type="TARGETS_PERSONA",
        weight=0.95 if tier == CostTier.EXPENSIVE else 0.8,
        properties={
            "knowledge_type": KnowledgeType.EVERGREEN.value,
            "observed_at": datetime.utcnow().isoformat()
        }
    )
    runner.world_graph.add_relation(targets_edge)

    return {
        "status": "narrative_designed",
        "narrative_id": narrative_id,
        "anchors_hit": ["anchor_narrative_structures_success"],
        "metrics_lift": {"messaging_relevance_score": 0.20 if tier == CostTier.EXPENSIVE else 0.04}
    }


def execute_landing_page_patterns(
    inputs: Dict[str, Any],
    tier: CostTier,
    runner: SkillRunner
) -> Dict[str, Any]:
    """
    Custom Executor for 'landing_page_patterns'.
    Inputs: 'narrative_id', 'product_name'
    Mutations: Creates a Product node, an Offer node, and an OFFERS relationship.
    """
    narrative_id = inputs.get("narrative_id", "narrative_default")
    prod_name = inputs.get("product_name", "Apodex PDF Parser")

    product_id = f"product_{uuid.uuid4().hex[:6]}"
    offer_id = f"offer_{uuid.uuid4().hex[:6]}"

    # 1. Create Product Node
    product_node = EntityNode(
        node_id=product_id,
        node_type="product",
        properties={
            "name": prod_name,
            "knowledge_type": KnowledgeType.EVERGREEN.value,
            "observed_at": datetime.utcnow().isoformat()
        }
    )
    runner.world_graph.add_node(product_node)

    # 2. Create Offer Node
    offer_node = EntityNode(
        node_id=offer_id,
        node_type="resource",
        properties={
            "price_cents": 1900,  # $19/mo
            "knowledge_type": KnowledgeType.EVERGREEN.value,
            "observed_at": datetime.utcnow().isoformat()
        }
    )
    runner.world_graph.add_node(offer_node)

    # 3. Assert relationship: Product OFFERS Offer
    offers_edge = RelationshipEdge(
        source_id=product_id,
        target_id=offer_id,
        relation_type="OFFERS",
        weight=1.0,
        properties={
            "knowledge_type": KnowledgeType.EVERGREEN.value,
            "observed_at": datetime.utcnow().isoformat()
        }
    )
    runner.world_graph.add_relation(offers_edge)

    return {
        "status": "landing_page_live",
        "product_id": product_id,
        "offer_id": offer_id,
        "anchors_hit": ["anchor_landing_page_patterns_success"],
        "metrics_lift": {"landing_page_ctr": 0.12 if tier == CostTier.EXPENSIVE else 0.03}
    }


def execute_structured_ab_testing(
    inputs: Dict[str, Any],
    tier: CostTier,
    runner: SkillRunner
) -> Dict[str, Any]:
    """
    Custom Executor for 'structured_ab_testing'.
    Inputs: 'offer_id', 'variant_count'
    Mutations: Creates a Campaign node and a RUNS_CAMPAIGN relationship.
    Note: Both campaign and relationships are marked as DECAYING signals to verify confidence decay.
    """
    offer_id = inputs.get("offer_id", "offer_default")
    variant_count = inputs.get("variant_count", 2)

    campaign_id = f"campaign_{uuid.uuid4().hex[:6]}"

    # 1. Create Campaign Node (DECAYING signal)
    campaign_node = EntityNode(
        node_id=campaign_id,
        node_type="resource",
        properties={
            "name": f"A/B Split Test with {variant_count} variants",
            "traffic_size": 5000 if tier == CostTier.EXPENSIVE else 1000,
            "knowledge_type": KnowledgeType.DECAYING.value,
            "observed_at": datetime.utcnow().isoformat()
        }
    )
    runner.world_graph.add_node(campaign_node)

    # 2. Assert relationship: Campaign RUNS_CAMPAIGN for Offer (DECAYING relationship)
    runs_edge = RelationshipEdge(
        source_id=campaign_id,
        target_id=offer_id,
        relation_type="RUNS_CAMPAIGN",
        weight=0.90 if tier == CostTier.EXPENSIVE else 0.60,
        properties={
            "knowledge_type": KnowledgeType.DECAYING.value,
            "observed_at": datetime.utcnow().isoformat(),
            "click_through_rate": 0.045 if tier == CostTier.EXPENSIVE else 0.02
        }
    )
    runner.world_graph.add_relation(runs_edge)

    return {
        "status": "ab_test_completed",
        "campaign_id": campaign_id,
        "click_through_rate": 0.045 if tier == CostTier.EXPENSIVE else 0.02,
        "anchors_hit": ["anchor_ab_testing_success"],
        "metrics_lift": {"conversion_rate_lift": 0.08 if tier == CostTier.EXPENSIVE else 0.01}
    }


def execute_revenue_metric_literacy(
    inputs: Dict[str, Any],
    tier: CostTier,
    runner: SkillRunner
) -> Dict[str, Any]:
    """
    Custom Executor for 'revenue_metric_literacy'.
    Inputs: 'campaign_id', 'cac_cents'
    Mutations: Performs calculations and asserts DECAYING SaaS metrics into WorldGraph.
    """
    campaign_id = inputs.get("campaign_id", "campaign_default")
    cac = inputs.get("cac_cents", 1500)  # $15.00 CAC

    # Derive economics
    ltv = 5500 if tier == CostTier.EXPENSIVE else 3500  # $55 LTV vs $35 LTV
    mrr_cents = 1500000 if tier == CostTier.EXPENSIVE else 300000  # $15k vs $3k MRR

    metric_node_id = f"metric_literacy_{uuid.uuid4().hex[:6]}"

    # 1. Create Economic Metrics node (DECAYING)
    metric_node = EntityNode(
        node_id=metric_node_id,
        node_type="resource",
        properties={
            "name": f"Economic Metrics for {campaign_id}",
            "cac_cents": cac,
            "ltv_cents": ltv,
            "ltv_to_cac": float(ltv) / max(1.0, float(cac)),
            "mrr_cents": mrr_cents,
            "knowledge_type": KnowledgeType.DECAYING.value,
            "observed_at": datetime.utcnow().isoformat()
        }
    )
    runner.world_graph.add_node(metric_node)

    # 2. Assert relation: Metrics linked to Campaign (DECAYING)
    metrics_edge = RelationshipEdge(
        source_id=metric_node_id,
        target_id=campaign_id,
        relation_type="CAUSES",
        weight=0.98 if tier == CostTier.EXPENSIVE else 0.70,
        properties={
            "knowledge_type": KnowledgeType.DECAYING.value,
            "observed_at": datetime.utcnow().isoformat()
        }
    )
    runner.world_graph.add_relation(metrics_edge)

    return {
        "status": "metrics_calculated",
        "metric_node_id": metric_node_id,
        "cac_cents": cac,
        "ltv_cents": ltv,
        "mrr_cents": mrr_cents,
        "anchors_hit": ["anchor_revenue_metric_literacy_success"],
        "metrics_lift": {"measurement_accuracy": 0.25 if tier == CostTier.EXPENSIVE else 0.05}
    }


def execute_business_model_design(
    inputs: Dict[str, Any],
    tier: CostTier,
    runner: SkillRunner
) -> Dict[str, Any]:
    """
    Custom Executor for 'business_model_design' / capital reallocation.
    Inputs: 'metric_node_id', 'available_surplus_cents'
    Mutations: Reallocates budget resources based on LTV/CAC yields and logs investment allocations.
    """
    metric_node_id = inputs.get("metric_node_id", "metric_default")
    surplus = inputs.get("available_surplus_cents", 500000)  # $5k

    # In a real environment we would load the metric node from the WorldGraph
    # Let's mock a standard capital optimization
    marketing_budget = int(surplus * 0.60)
    product_budget = int(surplus * 0.40)

    allocation_id = f"allocation_{uuid.uuid4().hex[:6]}"

    # 1. Create Capital Allocation Node (EVERGREEN)
    allocation_node = EntityNode(
        node_id=allocation_id,
        node_type="resource",
        properties={
            "name": f"Optimal surplus allocation: {surplus} cents",
            "marketing_allocation_cents": marketing_budget,
            "product_allocation_cents": product_budget,
            "knowledge_type": KnowledgeType.EVERGREEN.value,
            "observed_at": datetime.utcnow().isoformat()
        }
    )
    runner.world_graph.add_node(allocation_node)

    return {
        "status": "capital_reallocated",
        "allocation_id": allocation_id,
        "marketing_allocation_cents": marketing_budget,
        "product_allocation_cents": product_budget,
        "anchors_hit": ["anchor_business_model_design_success"],
        "metrics_lift": {"capital_efficiency_multiplier": 0.30 if tier == CostTier.EXPENSIVE else 0.10}
    }


# =====================================================================
# Registration Helper
# =====================================================================

def register_all_custom_executors(runner: SkillRunner) -> None:
    """Convenience function to wire all custom executors to a SkillRunner instance."""
    runner.register_custom_executor("opportunity_evaluation_frameworks", execute_opportunity_evaluation)
    runner.register_custom_executor("narrative_structures", execute_narrative_structures)
    runner.register_custom_executor("landing_page_patterns", execute_landing_page_patterns)
    runner.register_custom_executor("structured_ab_testing", execute_structured_ab_testing)
    runner.register_custom_executor("revenue_metric_literacy", execute_revenue_metric_literacy)
    runner.register_custom_executor("business_model_design", execute_business_model_design)
