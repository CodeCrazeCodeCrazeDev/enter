from __future__ import annotations

from apodex.applications.engines import (
    AutonomousCapitalEngine,
    AutonomousDemandEngine,
    AutonomousOperationsEngine,
    AutonomousProductEngine,
    AutonomousRevenueEngine,
    AutonomousTradingEngine,
    CapitalAsset,
    DemandCampaign,
    ProductOpportunity,
)


async def test_product_engine_discovers_opportunities():
    ape = AutonomousProductEngine({})
    opps = await ape.discover_opportunities(["devs"])
    assert len(opps) == 1
    assert isinstance(opps[0], ProductOpportunity)
    assert opps[0].confidence_score == 0.88


async def test_product_engine_blueprint_links_opportunity():
    ape = AutonomousProductEngine({})
    opp = (await ape.discover_opportunities(["devs"]))[0]
    blueprint = await ape.design_product_blueprint(opp)
    assert blueprint["opportunity_id"] == opp.opportunity_id
    assert len(blueprint["factory_task_ids"]) == 3


async def test_demand_engine_compile_graph():
    ade = AutonomousDemandEngine({})
    graph = await ade.compile_demand_graph("market-1")
    assert graph["market_id"] == "market-1"
    assert 0 <= graph["trust_index"] <= 1


async def test_demand_engine_launch_campaign_projects_leads():
    ade = AutonomousDemandEngine({})
    campaign = DemandCampaign(
        target_icp="startups", channels=["email"], budget_cents=50000, narrative_theme="growth"
    )
    result = await ade.launch_campaign(campaign)
    assert result["status"] == "launched"
    assert result["projected_leads_count"] == 50  # 50000 / 1000


async def test_revenue_engine_price_with_elastic_demand():
    are = AutonomousRevenueEngine(service_registry=None)
    price = await are.compute_optimal_price_cents(1000, demand_elasticity=-2.0)
    # markup = 1/2 = 0.5 -> 1000 * 1.5 = 1500
    assert price == 1500


async def test_revenue_engine_price_inelastic_defaults_markup():
    are = AutonomousRevenueEngine(service_registry=None)
    price = await are.compute_optimal_price_cents(1000, demand_elasticity=1.0)
    # positive elasticity -> markup 0.5 -> 1500
    assert price == 1500


async def test_revenue_engine_never_below_cost():
    are = AutonomousRevenueEngine(service_registry=None)
    price = await are.compute_optimal_price_cents(1000, demand_elasticity=-0.0001)
    assert price >= 1000


async def test_capital_engine_optimize_portfolio_conserves_total():
    ace = AutonomousCapitalEngine({})
    assets = [
        CapitalAsset(asset_id="a", asset_type="cash", amount_cents=6000, yield_pct=0.05),
        CapitalAsset(asset_id="b", asset_type="stablecoin", amount_cents=4000, yield_pct=0.10),
    ]
    result = await ace.optimize_portfolio(assets, target_risk_score=0.5)
    assert result["portfolio_valuation_cents"] == 10000
    assert set(result["optimized_allocations"].keys()) == {"a", "b"}
    assert sum(result["optimized_allocations"].values()) <= 10000


async def test_operations_engine_routes_billing_to_are():
    aoe = AutonomousOperationsEngine({})
    result = await aoe.automate_support_routing("I have a billing issue")
    assert result["assigned_department"] == "ARE"


async def test_operations_engine_routes_bug_to_ape():
    aoe = AutonomousOperationsEngine({})
    result = await aoe.automate_support_routing("found a bug")
    assert result["assigned_department"] == "APE"


async def test_operations_engine_default_route_and_auto_reply():
    aoe = AutonomousOperationsEngine({})
    result = await aoe.automate_support_routing("How to reset password")
    assert result["assigned_department"] == "default_agent"
    assert result["resolution_action"] == "auto_reply"


async def test_trading_engine_scan_arbitrage():
    ate = AutonomousTradingEngine({})
    opps = await ate.scan_arbitrage_opportunities(["USDC/EUR"])
    assert len(opps) == 1
    assert opps[0]["price_spread_pct"] > 0
