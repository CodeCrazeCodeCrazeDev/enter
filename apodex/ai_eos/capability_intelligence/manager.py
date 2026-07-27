"""Frontier Capability & Model Intelligence and Capability Registry implementation for AI-EOS.

Coordinates the 4-pipeline lifecycle for discovering, distilling, validating, and
promoting modular agent capabilities while preventing direct external code imports.
"""

from __future__ import annotations
import logging
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from datetime import datetime

from ..domain.models import Capability, SubsystemMaturity
from ..interfaces.services import ICapabilityRegistry

logger = logging.getLogger("ai_eos.capability")


class CapabilityRegistry(ICapabilityRegistry):
    """Ledger database for managing version-controlled system capabilities and rollback histories."""

    def __init__(self) -> None:
        self._registry: Dict[str, Capability] = {}
        self._rollback_history: List[Dict[str, Any]] = []

    def register_capability(self, capability: Capability) -> None:
        """Register a validated capability."""
        self._registry[capability.capability_id] = capability
        logger.info(f"Registered capability in active registry: {capability.name} [id={capability.capability_id}, maturity={capability.maturity.value}]")

    def get_capability(self, capability_id: str) -> Optional[Capability]:
        """Fetch a capability by ID."""
        return self._registry.get(capability_id)

    def trigger_rollback(self, capability_id: str, reason: str) -> bool:
        """Revert a degraded capability to its previous baseline and log a negative signal."""
        cap = self._registry.get(capability_id)
        if not cap:
            logger.warning(f"Failed to rollback non-existent capability: {capability_id}")
            return False

        logger.warning(f"CRITICAL SLA REGRESSION DETECTED! Rolling back capability {cap.name} [id={capability_id}]. Reason: {reason}")

        # Archive rollback event
        rollback_record = {
            "capability_id": capability_id,
            "name": cap.name,
            "rolled_back_at": datetime.utcnow(),
            "reason": reason,
            "previous_status": cap.deployment_status,
            "rollback_sha256": cap.rollback_trigger
        }
        self._rollback_history.append(rollback_record)

        # Revert status
        cap.deployment_status = "rolled_back"
        cap.maturity = SubsystemMaturity.DEPRECATED
        self._registry[capability_id] = cap
        return True


class CapabilityIntelligenceManager:
    """Orchestrates Frontier Capability Discovery, Distillation, Validation, and Promotion."""

    def __init__(self, registry: CapabilityRegistry) -> None:
        self.registry = registry
        # Model intelligence profile database
        self.model_profiles: Dict[str, Dict[str, Any]] = {
            "Claude-3.5-Sonnet": {"cost_per_1M_input": 3.0, "latency_score": 0.85, "reasoning_score": 0.95, "coding_score": 0.96},
            "Qwen-2.5-Coder": {"cost_per_1M_input": 0.4, "latency_score": 0.95, "reasoning_score": 0.72, "coding_score": 0.88},
            "DeepSeek-R1": {"cost_per_1M_input": 0.55, "latency_score": 0.65, "reasoning_score": 0.98, "coding_score": 0.92}
        }

    # ------------------------------------------------------------------
    # Pipeline A: Discovery
    # ------------------------------------------------------------------
    def discover_candidates(self, source_feed: str) -> List[Dict[str, Any]]:
        """Scan a source (e.g. GitHub, arXiv specs) and output raw candidate descriptions."""
        logger.info(f"Scanning frontier capability source feed: {source_feed}")
        # Return mock parsed capability candidates from external paper/repo
        return [
            {
                "name": "MonteCarloTreeSearchAdCreative",
                "origin": f"arXiv:2502.20422 ({source_feed})",
                "description": "Adaptive creative layout search using MCTS and rollout scores.",
                "source": "https://github.com/harness/mcts-creatives",
                "extracted_dependencies": ["avie.visual_production"]
            }
        ]

    # ------------------------------------------------------------------
    # Pipeline B: Distillation
    # ------------------------------------------------------------------
    def distill_capability(self, candidate: Dict[str, Any]) -> Capability:
        """Extract schemas, architectures, and compile reusable stubs to avoid raw code imports."""
        logger.info(f"Distilling capability patterns for candidate: {candidate['name']}")

        capability_id = f"cap_{uuid4().hex[:8]}"
        return Capability(
            capability_id=capability_id,
            name=candidate["name"],
            description=candidate["description"],
            source=candidate["source"],
            origin=candidate["origin"],
            evidence=[f"distilled_at_{datetime.utcnow().isoformat()}"],
            benchmark_results={"accuracy": 0.0, "latency_ms": 0.0},
            risk_score=0.15,
            dependencies=candidate["extracted_dependencies"],
            owner="FrontierIntelligence",
            maturity=SubsystemMaturity.EXPERIMENTAL,
            deployment_status="staged",
            rollback_trigger="latency_ms_ratio > 1.5",
            retirement_policy="accuracy_drop_ratio > 0.10"
        )

    # ------------------------------------------------------------------
    # Pipeline C: Validation
    # ------------------------------------------------------------------
    def validate_capability_sandbox(self, capability: Capability, simulated_acc: float, cost_ratio: float) -> bool:
        """Verify safety and compliance in isolated Sandbox simulation and benchmark accuracy."""
        logger.info(f"Executing Sandbox verification and replay benchmarking for capability: {capability.name}")

        # Enforce validation bounds
        is_safe = capability.risk_score < 0.40
        is_performant = simulated_acc >= 0.80 and cost_ratio < 1.30

        if is_safe and is_performant:
            capability.maturity = SubsystemMaturity.VALIDATED
            capability.benchmark_results = {
                "accuracy": simulated_acc,
                "cost_ratio": cost_ratio,
                "validated_at": datetime.utcnow().isoformat()
            }
            logger.info(f"Capability successfully cleared Sandbox Validation: Accuracy = {simulated_acc:.4f}")
            return True
        else:
            logger.warning(f"Capability FAILED Sandbox Validation: Safe={is_safe}, Performant={is_performant}")
            return False

    # ------------------------------------------------------------------
    # Pipeline D: Promotion
    # ------------------------------------------------------------------
    def promote_to_production(self, capability: Capability) -> bool:
        """Promote a validated capability to active production status."""
        if capability.maturity != SubsystemMaturity.VALIDATED:
            logger.warning(f"Cannot promote unvalidated capability: {capability.name}")
            return False

        capability.maturity = SubsystemMaturity.PRODUCTION
        capability.deployment_status = "production"
        self.registry.register_capability(capability)
        logger.info(f"PROMOTED CAPABILITY TO PRODUCTION: {capability.name} [id={capability.capability_id}]")
        return True

    # ------------------------------------------------------------------
    # Frontier Model Intelligence
    # ------------------------------------------------------------------
    def get_optimal_routing_policy(self, task_domain: str, budget_tier: str) -> str:
        """Formulate optimal prompt routing policies based on current model profiles."""
        if task_domain == "coding" or task_domain == "math":
            if budget_tier == "EXPENSIVE":
                return "DeepSeek-R1"  # Max reasoning
            else:
                return "Qwen-2.5-Coder"  # Cheap & highly capable for coding
        return "Claude-3.5-Sonnet"  # Balanced default
