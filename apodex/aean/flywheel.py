"""The compounding flywheel — the AEAN organism orchestrator.

This module wires the six engines around the Economic Knowledge Graph and runs
the six-stage compounding loop described in the spec:

    demand detection -> narrative creation -> visual production ->
    attention capture -> revenue conversion -> capital reallocation

Each turn of the loop enriches the EKG, updates PAEAN's Thompson-Sampling
posteriors, and (when cells are profitable) compounds the treasury. The
:class:`Organism` exposes ``step`` (one cycle) and ``run`` (N cycles) plus a
JSON-serialisable :meth:`snapshot` for the dashboard.
"""
from __future__ import annotations

import logging
import random
from typing import List, Optional

from .coordination.hive_mind import HiveMind, TaskBid
from .coordination.research import ResearchEngine, ResearchInsight
from .ekg import EconomicKnowledgeGraph
from .engines.ade import AutonomousDemandEngine
from .engines.are import AutonomousRevenueEngine
from .engines.avie import AutonomousVisualIntelligenceEngine
from .engines.paean import PAEAN
from .evolution.three_layer import GovernedCognitiveEvolutionSystem
from .governance import ConstitutionalFilter
from .llm import LLMAdapter
from .models import CycleResult, OrganismState
from .validation.critics import ThreeCriticStack
from .validation.epistemic import EpistemicFirewall
from .validation.pretrade import PreTradeValidationEngine
from .validation.rgae import RealityGroundedAdaptiveEngine

# AI-EOS Core Imports
from .core import (
    SystemEconomics,
    PaymentsFinancialOps,
    LegalComplianceLayer,
    PlatformRiskManager,
    IdentityResolver,
    SecurityRobustness,
    UnifiedHITLFramework,
    SelfImprovementEngine,
    SelfEvolutionEngine,
    CapitalAllocationLayer,
)

logger = logging.getLogger("aean.flywheel")


class Organism:
    """The unified AEAN economic organism."""

    def __init__(
        self,
        initial_capital_cents: int = 100_000_00,  # $100,000.00
        *,
        seed: Optional[int] = None,
        llm: Optional[LLMAdapter] = None,
        token_budget: int = 120,
    ) -> None:
        self._rng = random.Random(seed)
        # Validation subsystems get an independent RNG so the reality layer's
        # stochastic draws never perturb the core engines' deterministic order.
        self._val_rng = random.Random(None if seed is None else seed + 90210)
        self.ekg = EconomicKnowledgeGraph()
        self.governance = ConstitutionalFilter()
        self.llm = llm or LLMAdapter()

        # AI-EOS Core Services (Sections 7.1–7.12)
        self.economics = SystemEconomics()
        self.payments = PaymentsFinancialOps(self.economics)
        self.legal = LegalComplianceLayer()
        self.platform_risk = PlatformRiskManager()
        self.identity_resolver = IdentityResolver()
        self.security = SecurityRobustness()
        self.hitl = UnifiedHITLFramework()
        self.self_improvement = SelfImprovementEngine()
        self.self_evolution = SelfEvolutionEngine()
        self.capital_allocation = CapitalAllocationLayer()

        # Reality & validation systems (Part II of the architecture).
        self.firewall = EpistemicFirewall(governance=self.governance)
        self.rgae = RealityGroundedAdaptiveEngine(rng=self._val_rng)
        self.critics = ThreeCriticStack(self.governance)
        self.pretrade = PreTradeValidationEngine(rng=self._val_rng)

        # Governed Cognitive Evolution System (Ch 11 + 15). Uses its own RNG so
        # the self-improvement loop never perturbs the core engines' order.
        self._evo_rng = random.Random(None if seed is None else seed + 70707)
        self.evolution = GovernedCognitiveEvolutionSystem(self.governance, rng=self._evo_rng)

        self.ade = AutonomousDemandEngine(
            self.ekg, self.governance, self.llm, rng=self._rng, firewall=self.firewall
        )
        self.avie = AutonomousVisualIntelligenceEngine(self.ekg, self.governance, self.llm, rng=self._rng)
        self.paean = PAEAN(
            self.ekg, self.governance, rng=self._rng, critics=self.critics, pretrade=self.pretrade
        )
        self.are = AutonomousRevenueEngine(self.ekg, self.governance, rng=self._rng)
        self.hive_mind = HiveMind(token_budget=token_budget)
        self.research = ResearchEngine(self.ekg)

        self.initial_capital_cents = initial_capital_cents
        self.treasury_cents = initial_capital_cents
        self.cycle = 0
        self.history: List[CycleResult] = []
        self.latest_insights: List[ResearchInsight] = []

    # ------------------------------------------------------------------
    def _bids(self) -> List[TaskBid]:
        open_signals = len(self.ekg.open_signals())
        active = len(self.ekg.active_cells())
        return [
            TaskBid("sense_demand", priority=0.8, expected_value=0.6, token_cost=15),
            TaskBid("engineer_narratives", priority=0.7, expected_value=0.5 + 0.05 * open_signals, token_cost=20),
            TaskBid("produce_visuals", priority=0.65, expected_value=0.5, token_cost=20),
            TaskBid("allocate_capital", priority=0.9, expected_value=0.7, token_cost=20),
            TaskBid("run_revenue", priority=0.95, expected_value=0.5 + 0.05 * active, token_cost=20),
            TaskBid("rebalance", priority=0.85, expected_value=0.6, token_cost=10),
            TaskBid("evolve", priority=0.5, expected_value=0.55, token_cost=10),
        ]

    def step(self) -> CycleResult:
        """Run a single turn of the compounding flywheel."""
        self.cycle += 1
        grants = self.hive_mind.granted_tasks(self.hive_mind.arbitrate(self._bids()))
        result = CycleResult(cycle=self.cycle)
        blocks_before = self.governance.blocks

        # Stage 0: governed cognitive evolution. Layer 1 evolves the behavioural
        # allocation strategy within the fixed architecture; when it promotes a
        # champion, the improved (governance-bounded) strategy is redeployed. On
        # a slower cadence a structural proposal is routed through the Layer-2
        # seven-stage pipeline. Objective stability (Layer 3) guards both.
        if grants.get("evolve") and self.cycle % 5 == 0:
            cap = self.evolution.evolve_capability()
            self.ekg.record_capability_evolution(cap)
            if cap.promoted:
                self.paean.base_allocation_pct = max(
                    0.08, min(0.22, self.evolution.incumbent.allocation_pct)
                )
            if self.cycle % 15 == 0:
                arch = self.evolution.evaluate_architecture(self._architecture_candidate())
                self.ekg.record_architecture_evolution(arch)
                # Self Evolution proposals proposal integration
                self.self_evolution.propose_architectural_shift(recent_performance=self.cumulative_roi())

        # Stage 1: demand detection.
        if grants.get("sense_demand"):
            signals = self.ade.sense_demand()
            result.signals_detected = len(signals)
            for s in signals:
                self.identity_resolver.resolve_identity([s.segment, s.market])
                self.economics.attribute_cost("ADE", "Layer1_Sensing", 150, opportunity_id=s.signal_id)

        # Stage 2: narrative creation.
        if grants.get("engineer_narratives"):
            for signal in self.ekg.open_signals():
                if not self.ekg.narratives_for(signal.signal_id):
                    # Scan for prompt injection
                    if self.security.scan_for_injection(signal.market):
                        self.hitl.raise_escalation("ADE", f"Blocked suspicious market string injection: {signal.market}", "high")
                        continue
                    if self.ade.engineer_narrative(signal):
                        result.narratives_created += 1
                        self.economics.attribute_cost("ADE", "Layer2_Narrative", 300, opportunity_id=signal.signal_id)

        # Stage 3: visual production + RGAE reality validation. Newly produced
        # assets are screened through the three-layer pipeline; only creatives
        # that clear the revenue gate become eligible for media spend.
        if grants.get("produce_visuals"):
            for narrative in list(self.ekg.narratives.values()):
                if not self.ekg.assets_for(narrative.narrative_id):
                    assets = self.avie.produce_assets(narrative)
                    result.assets_produced += len(assets)
                    for asset in assets:
                        self.economics.attribute_cost("AVIE", "Layer3_Generative", 250, opportunity_id=narrative.signal_id)
                    signal = self.ekg.signals.get(narrative.signal_id)
                    if signal is not None and assets:
                        for record in self.rgae.screen(narrative, assets, signal):
                            self.ekg.record_validation(record)
                            if record.passed:
                                result.assets_validated += 1

        # Stage 4: capital allocation. Committed capital is carved out of the
        # live treasury; ARE spends from within each cell's committed budget.
        cycle_spend = 0
        cycle_revenue = 0
        if grants.get("allocate_capital"):
            spawned = self.paean.spawn_cells(self.treasury_cents)
            self.treasury_cents -= sum(c.allocated_cents for c in spawned)

        # Stage 5: revenue conversion. Spend is drawn from already-committed
        # capital, so only realised revenue flows back into the treasury.
        if grants.get("run_revenue"):
            for cell in self.ekg.active_cells():
                before = cell.deployed_cents
                revenue = self.are.run_funnel(cell)
                cycle_spend += cell.deployed_cents - before
                cycle_revenue += revenue

                # Payment operations & cost attribution
                if revenue > 0:
                    tx = self.payments.process_payment(cell.cell_id, revenue)
                    self.payments.reconcile_payments()
                    self.economics.attribute_cost("ARE", "Layer4_Sales", 400, opportunity_id=cell.signal_id)
            self.treasury_cents += cycle_revenue

        # Stage 6: capital reallocation (learn + kill/scale). Killed cells
        # refund unspent capital; scaled winners draw fresh capital.
        self.paean.learn_from_outcomes()
        if grants.get("rebalance"):
            counts = self.paean.rebalance(self.treasury_cents)
            self.treasury_cents += counts["refund_cents"] - counts["extra_commit_cents"]
            result.cells_killed = counts["killed"]
            result.cells_scaled = counts["scaled"]

        # Self-Improvement diagnostics over losing/poor performing cells
        for cell in self.ekg.cells.values():
            if cell.roi < 0:
                self.self_improvement.diagnose_and_suggest(
                    f"low_roi_{cell.cell_id[:8]}",
                    f"Cell underperforming with negative ROI: {cell.roi}"
                )

        # Research + bookkeeping.
        total_decisions = sum(r.decisions for r in self.governance.records.values())
        total_success = sum(r.successes for r in self.governance.records.values())
        accuracy = total_success / total_decisions if total_decisions else 0.0
        self.latest_insights = self.research.discover(total_decisions, accuracy)

        result.active_cells = len(self.ekg.active_cells())
        result.capital_deployed_cents = cycle_spend
        result.revenue_cents = cycle_revenue
        result.treasury_cents = self.treasury_cents
        result.portfolio_roi = self.portfolio_roi()
        result.governance_blocks = self.governance.blocks - blocks_before
        self.history.append(result)
        return result

    def run(self, cycles: int) -> List[CycleResult]:
        return [self.step() for _ in range(cycles)]

    # ------------------------------------------------------------------
    def portfolio_roi(self) -> float:
        deployed = sum(c.deployed_cents for c in self.ekg.cells.values())
        revenue = sum(c.revenue_cents for c in self.ekg.cells.values())
        if deployed <= 0:
            return 0.0
        return (revenue - deployed) / deployed

    def active_cells_count(self) -> int:
        return len(self.ekg.active_cells())

    def net_worth_cents(self) -> int:
        """Treasury plus unspent capital still committed to active cells."""
        uncommitted = sum(
            max(0, c.allocated_cents - c.deployed_cents) for c in self.ekg.active_cells()
        )
        return self.treasury_cents + uncommitted

    def cumulative_roi(self) -> float:
        if self.initial_capital_cents <= 0:
            return 0.0
        return (self.net_worth_cents() - self.initial_capital_cents) / self.initial_capital_cents

    def state(self) -> OrganismState:
        cells = list(self.ekg.cells.values())
        return OrganismState(
            cycle=self.cycle,
            treasury_cents=self.treasury_cents,
            initial_capital_cents=self.initial_capital_cents,
            total_revenue_cents=sum(c.revenue_cents for c in cells),
            total_deployed_cents=sum(c.deployed_cents for c in cells),
            active_cells=len(self.ekg.active_cells()),
            killed_cells=sum(1 for c in cells if c.status.value == "killed"),
            scaled_cells=sum(1 for c in cells if c.status.value == "scaled"),
            cumulative_roi=self.cumulative_roi(),
            history=self.history,
        )

    def _architecture_candidate(self) -> dict:
        """The Ch 15.3.4 worked example: Research→Critic→Simulation→Execution.

        A well-formed structural proposal that respects the Layer-3 invariants
        and carries production-grade promotion evidence (>=10k canary samples).
        """
        return {
            "name": "research-critic-simulation-execution",
            "boots": True,
            "benchmark_delta": 0.28,  # 28% revision-rate reduction (better, not merely different).
            "stress_ok": True,
            "security_ok": True,
            "cost_quality_ok": True,
            "canary_divergence_ok": True,
            "samples": 12_000,
            "scale_ok": True,
        }

    def _evolution_stats(self) -> dict:
        """Aggregate governed-evolution metrics for the dashboard/CLI."""
        return self.evolution.stats()

    def _pretrade_stats(self) -> dict:
        stats = self.pretrade.stats()
        stats["avg_fragility"] = (
            round(
                sum(a.fragility_index for a in self.ekg.pretrade.values() if a.passed)
                / max(1, stats["approved"]),
                4,
            )
            if stats["approved"]
            else 0.0
        )
        return stats

    def _validation_stats(self) -> dict:
        """Aggregate reality/validation-layer metrics for the dashboard."""
        vals = list(self.ekg.validations.values())
        sig_vals = list(self.ekg.signal_validations.values())
        stage_counts: dict = {}
        for v in vals:
            stage_counts[v.stage_reached.value] = stage_counts.get(v.stage_reached.value, 0) + 1
        return {
            "epistemic_firewall": {
                "signals_checked": len(sig_vals),
                "signals_rejected": self.firewall.rejected,
                "avg_credibility": round(
                    sum(s.credibility for s in sig_vals) / len(sig_vals), 4
                ) if sig_vals else 0.0,
            },
            "rgae": {
                "assets_screened": len(vals),
                "assets_passed": sum(1 for v in vals if v.passed),
                "stage_reached": stage_counts,
                "calibration_updates": self.rgae.calibration.updates,
            },
            "three_critic_stack": self.critics.stats(),
            "pretrade": self._pretrade_stats(),
        }

    def snapshot(self) -> dict:
        """JSON-serialisable view for the dashboard/API."""
        st = self.state()
        return {
            "cycle": st.cycle,
            "treasury_cents": st.treasury_cents,
            "net_worth_cents": self.net_worth_cents(),
            "initial_capital_cents": st.initial_capital_cents,
            "cumulative_roi": round(st.cumulative_roi, 4),
            "portfolio_roi": round(self.portfolio_roi(), 4),
            "active_cells": st.active_cells,
            "killed_cells": st.killed_cells,
            "scaled_cells": st.scaled_cells,
            "total_revenue_cents": st.total_revenue_cents,
            "total_deployed_cents": st.total_deployed_cents,
            "governance_blocks": self.governance.blocks,
            "llm_provider": self.llm.provider,
            "llm_live": self.llm.is_live,
            "ekg": self.ekg.stats(),
            "validation": self._validation_stats(),
            "evolution": self._evolution_stats(),
            "autonomy": {
                engine.value: {
                    "decisions": rec.decisions,
                    "accuracy": round(rec.accuracy, 3),
                    "autonomous": self.governance.is_autonomous(engine),
                }
                for engine, rec in self.governance.records.items()
            },
            "insights": [
                {"kind": i.kind, "subject": i.subject, "detail": i.detail, "confidence": round(i.confidence, 3)}
                for i in self.latest_insights
            ],
            "history": [
                {
                    "cycle": h.cycle,
                    "treasury_cents": h.treasury_cents,
                    "revenue_cents": h.revenue_cents,
                    "capital_deployed_cents": h.capital_deployed_cents,
                    "active_cells": h.active_cells,
                    "cells_killed": h.cells_killed,
                    "cells_scaled": h.cells_scaled,
                    "portfolio_roi": round(h.portfolio_roi, 4),
                    "signals_detected": h.signals_detected,
                    "narratives_created": h.narratives_created,
                    "assets_produced": h.assets_produced,
                    "assets_validated": h.assets_validated,
                    "governance_blocks": h.governance_blocks,
                }
                for h in st.history
            ],
            "cells": [
                {
                    "cell_id": c.cell_id[:8],
                    "market": c.market,
                    "segment": c.segment,
                    "status": c.status.value,
                    "allocated_cents": c.allocated_cents,
                    "deployed_cents": c.deployed_cents,
                    "revenue_cents": c.revenue_cents,
                    "roi": round(c.roi, 4),
                }
                for c in sorted(self.ekg.cells.values(), key=lambda c: c.roi, reverse=True)
            ],
            "system_economics": {
                "total_tokens_cost": sum(log.token_cost for log in self.economics.logs),
                "total_dollars_cost": sum(log.dollars_cost for log in self.economics.logs),
                "escalations_pending": sum(1 for i in self.hitl.queue.values() if i.status == "PENDING"),
                "total_payments_reconciled": sum(1 for tx in self.payments.transactions.values() if tx.status == "RECONCILED"),
            }
        }
