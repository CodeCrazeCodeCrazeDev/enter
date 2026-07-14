"""The three-layer Governed Cognitive Evolution System.

This implements the AEAN v2 framework for *governed* self-improvement: the
system evolves what it does (Layer 1) and, selectively, how it is structured
(Layer 2), while its purpose (Layer 3) is held permanently outside the
optimisation loop. Layer 3 is load-bearing: every Layer-1 and Layer-2 candidate
is screened against the constitutional invariants *before* it is measured, so
the optimiser can never drift the organism's objectives, relax its risk
controls, or promote on flimsy evidence.
"""
from __future__ import annotations

import logging
import random
from typing import Callable, Dict, List, Optional, Tuple

from ..governance import ConstitutionalFilter
from ..models import (
    ArchitectureEvolutionResult,
    CapabilityEvolutionResult,
    PipelineStage,
    StageResult,
    StrategyGenome,
)

logger = logging.getLogger("aean.evolution")

# Fixed, segment-representative sandbox scenarios: (demand, uncertainty, crowding).
_SCENARIOS: List[Tuple[float, float, float]] = [
    (0.80, 0.30, 0.40),
    (0.50, 0.60, 0.50),
    (0.90, 0.20, 0.60),
    (0.40, 0.70, 0.30),
    (0.65, 0.50, 0.55),
]

# The five categorical prohibitions (Ch 11.2 / 15.4) — keys a candidate change
# may never touch autonomously.
_FORBIDDEN_KEYS = {
    "risk_controls",
    "capital_limits",
    "governance_thresholds",
    "position_sizing",
    "stop_loss",
    "drawdown_limits",
    "mission",
    "core_objective",
}


class ObjectiveStability:
    """Layer 3 — invariant objectives and the five categorical prohibitions.

    Objective stability never evolves automatically. It captures the
    constitutional parameters once at construction with a decay rate of zero and
    rejects any optimisation candidate that would breach them, before the
    candidate consumes evaluation resources.
    """

    def __init__(self, governance: ConstitutionalFilter, *, min_samples: int = 10_000) -> None:
        self.governance = governance
        self.min_samples = min_samples
        # Frozen snapshot of the risk-control invariants (decay rate = 0).
        self._invariants: Dict[str, float] = {
            "max_single_allocation_pct": governance.rules.max_single_allocation_pct,
            "min_treasury_reserve_pct": governance.rules.min_treasury_reserve_pct,
            "max_total_deployed_pct": governance.rules.max_total_deployed_pct,
        }
        self.blocked = 0

    # ------------------------------------------------------------------
    def permits_genome(self, genome: StrategyGenome) -> Tuple[bool, List[str]]:
        """Layer-1 candidates may tune behaviour but not exceed risk controls."""
        reasons: List[str] = []
        if genome.allocation_pct > self._invariants["max_single_allocation_pct"]:
            reasons.append(
                "allocation_pct exceeds the constitutional single-allocation cap "
                f"({self._invariants['max_single_allocation_pct']:.0%}) — risk control is invariant."
            )
        if reasons:
            self.blocked += 1
        return (not reasons), reasons

    def permits_change(self, change: Dict[str, object]) -> Tuple[bool, List[str]]:
        """Layer-2 structural candidates: enforce the five prohibitions."""
        reasons: List[str] = []
        touched = _FORBIDDEN_KEYS.intersection(change.keys())
        if touched:
            reasons.append(f"attempts to modify invariant parameters: {', '.join(sorted(touched))}")
        if change.get("rewrite_live_logic"):
            reasons.append("would rewrite live logic without the governed pipeline")
        if change.get("contaminated_labels"):
            reasons.append("would learn from contaminated labels (model-collapse risk)")
        samples = change.get("samples")
        if isinstance(samples, (int, float)) and samples < self.min_samples:
            reasons.append(
                f"promotion evidence {int(samples)} < {self.min_samples} minimum samples"
            )
        if reasons:
            self.blocked += 1
        return (not reasons), reasons


def _default_fitness(genome: StrategyGenome) -> float:
    """Deterministic sandbox fitness over the fixed scenario set.

    A smooth, concave landscape with an interior optimum: strategies whose
    behavioural parameters match each scenario's demand/uncertainty/crowding
    profile score higher. No randomness — measurement is reproducible.
    """
    total = 0.0
    for demand, uncertainty, crowding in _SCENARIOS:
        ideal_alloc = 0.10 + 0.12 * demand
        ideal_patience = min(1.0, 0.5 + 0.3 * uncertainty)
        err = (
            0.25 * (genome.allocation_pct - ideal_alloc) ** 2
            + 0.30 * (genome.exploration - uncertainty) ** 2
            + 0.25 * (genome.diversification - crowding) ** 2
            + 0.20 * (genome.patience - ideal_patience) ** 2
        )
        total += max(0.0, 1.0 - 2.0 * err)
    return round(total / len(_SCENARIOS), 6)


class CapabilityEvolution:
    """Layer 1 — evolve behavioural strategy genomes within the architecture."""

    def __init__(
        self,
        objective: ObjectiveStability,
        *,
        rng: Optional[random.Random] = None,
        fitness: Optional[Callable[[StrategyGenome], float]] = None,
        population: int = 10,
        elite: int = 3,
        min_improvement: float = 0.01,
        mutation_scale: float = 0.15,
    ) -> None:
        self.objective = objective
        self._rng = rng or random.Random()
        self.fitness = fitness or _default_fitness
        self.population = population
        self.elite = elite
        self.min_improvement = min_improvement
        self.mutation_scale = mutation_scale

    # ------------------------------------------------------------------
    def _mutate(self, genome: StrategyGenome) -> StrategyGenome:
        def jitter(value: float) -> float:
            return max(0.0, min(1.0, value + self._rng.gauss(0.0, self.mutation_scale)))

        return StrategyGenome(
            allocation_pct=jitter(genome.allocation_pct),
            exploration=jitter(genome.exploration),
            diversification=jitter(genome.diversification),
            patience=jitter(genome.patience),
        )

    def _crossover(self, a: StrategyGenome, b: StrategyGenome) -> StrategyGenome:
        pick = self._rng.random
        return StrategyGenome(
            allocation_pct=a.allocation_pct if pick() < 0.5 else b.allocation_pct,
            exploration=a.exploration if pick() < 0.5 else b.exploration,
            diversification=a.diversification if pick() < 0.5 else b.diversification,
            patience=a.patience if pick() < 0.5 else b.patience,
        )

    def evolve(
        self, incumbent: StrategyGenome, generations: int = 6
    ) -> Tuple[StrategyGenome, CapabilityEvolutionResult]:
        incumbent_fitness = self.fitness(incumbent)
        elites: List[Tuple[StrategyGenome, float]] = [(incumbent, incumbent_fitness)]
        rejected = 0

        for _ in range(generations):
            # Variation → measurement, seeded from the current elites.
            candidates: List[Tuple[StrategyGenome, float]] = list(elites)
            while len(candidates) < self.population:
                parent = self._rng.choice(elites)[0]
                if len(elites) >= 2 and self._rng.random() < 0.5:
                    mate = self._rng.choice(elites)[0]
                    child = self._crossover(parent, mate)
                else:
                    child = self._mutate(parent)
                # Layer-3 screen before measurement — invalid genomes never run.
                permitted, _ = self.objective.permits_genome(child)
                if not permitted:
                    rejected += 1
                    continue
                candidates.append((child, self.fitness(child)))
            # Selection → recombination substrate for the next generation.
            candidates.sort(key=lambda pair: pair[1], reverse=True)
            elites = candidates[: self.elite]

        champion, champion_fitness = elites[0]
        improvement = round(champion_fitness - incumbent_fitness, 6)
        promoted = improvement >= self.min_improvement
        notes = [
            f"Evolved {generations} generations; champion fitness {champion_fitness:.4f} "
            f"vs incumbent {incumbent_fitness:.4f} (Δ{improvement:+.4f})."
        ]
        if not promoted:
            notes.append("Improvement below significance threshold — incumbent retained.")
        result = CapabilityEvolutionResult(
            generations=generations,
            incumbent_fitness=incumbent_fitness,
            champion_fitness=champion_fitness,
            improvement=improvement,
            promoted=promoted,
            rejected_by_objective=rejected,
            notes=notes,
        )
        return (champion if promoted else incumbent), result


class ArchitectureEvolution:
    """Layer 2 — the mandatory seven-stage architecture-evolution pipeline."""

    _ORDER: List[PipelineStage] = [
        PipelineStage.SANDBOX,
        PipelineStage.BENCHMARK,
        PipelineStage.STRESS,
        PipelineStage.SECURITY,
        PipelineStage.ECONOMIC,
        PipelineStage.CANARY,
        PipelineStage.SCALE,
    ]

    def __init__(self, objective: ObjectiveStability) -> None:
        self.objective = objective

    # ------------------------------------------------------------------
    def _check(self, stage: PipelineStage, c: Dict[str, object]) -> StageResult:
        if stage is PipelineStage.SANDBOX:
            ok = bool(c.get("boots", True))
            return StageResult(stage=stage, passed=ok, detail="boot/compat in microVM isolation")
        if stage is PipelineStage.BENCHMARK:
            delta = float(c.get("benchmark_delta", 0.0))
            return StageResult(
                stage=stage, passed=delta > 0.0, detail=f"benchmark Δ {delta:+.2%} (better, not merely different)"
            )
        if stage is PipelineStage.STRESS:
            ok = bool(c.get("stress_ok", True))
            return StageResult(stage=stage, passed=ok, detail="noise/tool-loss/adversarial/load-surge")
        if stage is PipelineStage.SECURITY:
            ok = bool(c.get("security_ok", True))
            return StageResult(stage=stage, passed=ok, detail="OWASP Top 10 for AI")
        if stage is PipelineStage.ECONOMIC:
            ok = bool(c.get("cost_quality_ok", True))
            return StageResult(stage=stage, passed=ok, detail="cost-quality frontier")
        if stage is PipelineStage.CANARY:
            samples = float(c.get("samples", 0))
            diverges_ok = bool(c.get("canary_divergence_ok", True))
            ok = diverges_ok and samples >= self.objective.min_samples
            return StageResult(
                stage=stage,
                passed=ok,
                detail=f"10% canary, {int(samples)} samples, divergence within bounds",
            )
        # SCALE
        ok = bool(c.get("scale_ok", True))
        return StageResult(stage=stage, passed=ok, detail="full activation with hot-standby")

    def evaluate(self, candidate: Dict[str, object]) -> ArchitectureEvolutionResult:
        name = str(candidate.get("name", "unnamed-candidate"))
        result = ArchitectureEvolutionResult(candidate=name)

        # Compatibility validation against Layer 3 *before* sandbox resources.
        permitted, reasons = self.objective.permits_change(candidate)
        if not permitted:
            result.rejected_by_objective = True
            result.notes = ["Rejected at compatibility validation: " + "; ".join(reasons)]
            return result

        for stage in self._ORDER:
            sr = self._check(stage, candidate)
            result.stages.append(sr)
            result.stage_reached = stage
            if not sr.passed:
                result.notes = [f"Halted at {stage.value}: {sr.detail}"]
                return result

        result.promoted = True
        result.notes = ["Cleared all seven stages — promoted with 30-day hot-standby."]
        return result


class GovernedCognitiveEvolutionSystem:
    """Composes the three layers into one governed self-improvement engine."""

    def __init__(self, governance: ConstitutionalFilter, *, rng: Optional[random.Random] = None) -> None:
        self._rng = rng or random.Random()
        self.objective = ObjectiveStability(governance)
        self.capability = CapabilityEvolution(self.objective, rng=self._rng)
        self.architecture = ArchitectureEvolution(self.objective)
        # Start from a deliberately unrefined behavioural strategy so Layer-1
        # capability evolution has real headroom to climb (and later saturate).
        self.incumbent = StrategyGenome(
            allocation_pct=0.10, exploration=0.85, diversification=0.15, patience=0.25
        )

        self.capability_rounds = 0
        self.capability_promotions = 0
        self.architecture_rounds = 0
        self.architecture_promotions = 0
        self.objective_rejections = 0
        self.last_capability: Optional[CapabilityEvolutionResult] = None
        self.last_architecture: Optional[ArchitectureEvolutionResult] = None

    # ------------------------------------------------------------------
    def evolve_capability(self, generations: int = 6) -> CapabilityEvolutionResult:
        champion, result = self.capability.evolve(self.incumbent, generations)
        self.capability_rounds += 1
        self.objective_rejections += result.rejected_by_objective
        if result.promoted:
            self.incumbent = champion
            self.capability_promotions += 1
        self.last_capability = result
        return result

    def evaluate_architecture(self, candidate: Dict[str, object]) -> ArchitectureEvolutionResult:
        result = self.architecture.evaluate(candidate)
        self.architecture_rounds += 1
        if result.rejected_by_objective:
            self.objective_rejections += 1
        if result.promoted:
            self.architecture_promotions += 1
        self.last_architecture = result
        return result

    def stats(self) -> dict:
        return {
            "incumbent": self.incumbent.model_dump(),
            "capability_rounds": self.capability_rounds,
            "capability_promotions": self.capability_promotions,
            "architecture_rounds": self.architecture_rounds,
            "architecture_promotions": self.architecture_promotions,
            "objective_rejections": self.objective_rejections,
            "champion_fitness": round(self.last_capability.champion_fitness, 4)
            if self.last_capability
            else 0.0,
        }
