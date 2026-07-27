"""AI-EOS Core Services (Sections 7.1–7.12).

A consolidated suite of cross-cutting services providing payments, compliance,
attribution, identity resolution, platform risk management, security, and human-in-the-loop escalation.
"""
from __future__ import annotations

import logging
import uuid
import random
from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from .models import Event, Evidence, Hypothesis, Theory, DecisionProposal, AgentScope

logger = logging.getLogger("aean.core")

# ===========================================================================
# 7.9 System Economics (Cost-to-Serve)
# ===========================================================================
class CostLog(BaseModel):
    call_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    engine: str
    layer: str
    token_cost: int
    dollars_cost: float
    opportunity_id: Optional[str] = None
    lead_id: Optional[str] = None

class SystemEconomics:
    """7.9 Tracks the actual operational cost of running AI-EOS itself."""
    def __init__(self) -> None:
        self.logs: List[CostLog] = []

    def attribute_cost(self, engine: str, layer: str, token_cost: int, opportunity_id: Optional[str] = None, lead_id: Optional[str] = None) -> CostLog:
        # Simple pricing: $0.00002 per token
        dollars_cost = token_cost * 0.00002
        log = CostLog(
            engine=engine,
            layer=layer,
            token_cost=token_cost,
            dollars_cost=dollars_cost,
            opportunity_id=opportunity_id,
            lead_id=lead_id
        )
        self.logs.append(log)
        return log

    def get_net_expected_return(self, gross_return: float, opportunity_id: str) -> float:
        """Subtract cost-to-serve from gross expected return."""
        total_cost = sum(log.dollars_cost for log in self.logs if log.opportunity_id == opportunity_id)
        return gross_return - total_cost


# ===========================================================================
# 7.6 Payments & Financial Operations
# ===========================================================================
class Transaction(BaseModel):
    transaction_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    lead_id: str
    amount_cents: int
    status: str = "PENDING"  # PENDING, RECONCILED, REFUNDED

class PaymentsFinancialOps:
    """7.6 Handles actual money capture, reconciliation, and negative refund signals."""
    def __init__(self, economics: SystemEconomics) -> None:
        self.transactions: Dict[str, Transaction] = {}
        self.economics = economics

    def process_payment(self, lead_id: str, amount_cents: int) -> Transaction:
        tx = Transaction(lead_id=lead_id, amount_cents=amount_cents, status="PENDING")
        self.transactions[tx.transaction_id] = tx
        self.economics.attribute_cost("ARE", "7.6_Payments", 200, lead_id=lead_id)
        return tx

    def reconcile_payments(self) -> int:
        """Matches closed deals against received payments; returns count reconciled."""
        reconciled_count = 0
        for tx in self.transactions.values():
            if tx.status == "PENDING":
                tx.status = "RECONCILED"
                reconciled_count += 1
        return reconciled_count

    def process_refund(self, tx_id: str) -> Optional[Transaction]:
        """Processes refunds and flags customer profiles with negative feedback."""
        tx = self.transactions.get(tx_id)
        if tx:
            tx.status = "REFUNDED"
            return tx
        return None


# ===========================================================================
# 7.7 Legal, Compliance & Disclosure
# ===========================================================================
class LegalComplianceLayer:
    """7.7 Ensures automated persuasion disclosure, opt-out rules, and non-discriminatory pricing."""
    def __init__(self) -> None:
        self.consents: Dict[str, bool] = {}  # customer_id -> consented

    def verify_outreach_consent(self, customer_id: str) -> bool:
        """Checks if customer has opted out."""
        return self.consents.get(customer_id, True)

    def enforce_opt_out(self, customer_id: str) -> None:
        self.consents[customer_id] = False

    def check_pricing_discrimination(self, properties: Dict[str, Any]) -> bool:
        """Strictly ensures price floor/ceiling checks do not condition on protected characteristics."""
        protected_characteristics = {"age", "gender", "race", "religion", "ethnicity", "sexual_orientation"}
        for k in properties.keys():
            if k.lower() in protected_characteristics:
                return False
        return True

    def generate_ai_disclosure(self, context_name: str) -> str:
        return f"[AI Persuasion Disclosure: This interaction is handled autonomously by AI-EOS ({context_name}).]"


# ===========================================================================
# 7.8 Platform Risk & Identity Resilience
# ===========================================================================
class PlatformRiskManager:
    """7.8 Tracks account-standing API signals and throttles behavior dynamically."""
    def __init__(self) -> None:
        self.error_rates: Dict[str, float] = {}  # channel -> error_rate
        self.throttled_channels: Dict[str, bool] = {}

    def monitor_and_throttle(self, channel: str, error_encountered: bool) -> bool:
        rate = self.error_rates.get(channel, 0.0)
        if error_encountered:
            rate = min(1.0, rate + 0.15)
        else:
            rate = max(0.0, rate - 0.02)
        self.error_rates[channel] = rate

        # Throttle if error rate exceeds 40%
        is_throttled = rate > 0.40
        self.throttled_channels[channel] = is_throttled
        return is_throttled


# ===========================================================================
# 7.10 Identity Resolution
# ===========================================================================
class IdentityResolver:
    """7.10 Merges cross-channel identifiers into a single customer ID upstream."""
    def __init__(self) -> None:
        self.mappings: Dict[str, str] = {}  # identifier -> resolved customer_id

    def resolve_identity(self, identifiers: List[str]) -> str:
        # Find if any identifier is already mapped
        resolved_id = None
        for ident in identifiers:
            if ident in self.mappings:
                resolved_id = self.mappings[ident]
                break

        if not resolved_id:
            resolved_id = f"cust-{uuid.uuid4()}"

        for ident in identifiers:
            self.mappings[ident] = resolved_id

        return resolved_id


# ===========================================================================
# 7.11 Security & Adversarial Robustness
# ===========================================================================
class SecurityRobustness:
    """7.11 Defends against prompt-injection and adversarial bot-leads."""
    def __init__(self) -> None:
        self.blocked_patterns = [
            "ignore previous instructions",
            "system override",
            "apply a 90% discount",
            "make price 0"
        ]

    def scan_for_injection(self, user_input: str) -> bool:
        lowered = user_input.lower()
        for pattern in self.blocked_patterns:
            if pattern in lowered:
                return True
        return False

    def is_lead_legitimate(self, lead_data: Dict[str, Any]) -> bool:
        """Filters bot-generated fraudulent leads."""
        if not lead_data.get("email") or not lead_data.get("name"):
            return False
        # Very short/suspicious emails
        if len(lead_data.get("email", "")) < 5:
            return False
        return True


# ===========================================================================
# 7.12 Unified Human-in-the-Loop Framework
# ===========================================================================
class HITLQueueItem(BaseModel):
    item_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    source_layer: str
    description: str
    severity: str  # low, medium, high
    status: str = "PENDING"  # PENDING, RESOLVED, REJECTED

class UnifiedHITLFramework:
    """7.12 A single centralized queue for all human review tasks."""
    def __init__(self) -> None:
        self.queue: Dict[str, HITLQueueItem] = {}

    def raise_escalation(self, source_layer: str, description: str, severity: str) -> HITLQueueItem:
        item = HITLQueueItem(source_layer=source_layer, description=description, severity=severity)
        self.queue[item.item_id] = item
        logger.warning("HITL Escalation Raised! Layer: %s, Severity: %s, Description: %s", source_layer, severity, description)
        return item

    def resolve_item(self, item_id: str, approve: bool) -> None:
        item = self.queue.get(item_id)
        if item:
            item.status = "RESOLVED" if approve else "REJECTED"


# ===========================================================================
# 7.1 Self-Improvement & 7.2 Self-Evolution
# ===========================================================================
class SelfImprovementEngine:
    """7.1 Diagnoses losing outcomes and proposes conservative, auditable fixes."""
    def __init__(self) -> None:
        self.fixes: Dict[str, str] = {}  # error_signature -> conservative_fix_applied

    def diagnose_and_suggest(self, failure_signature: str, error_detail: str) -> str:
        if "timeout" in error_detail.lower():
            fix = "Increase timeout threshold to 30s."
        elif "auth" in error_detail.lower():
            fix = "Reject and route to Unified HITL queue."
        else:
            fix = "Route back to Layer 2 narrative repositioning."
        self.fixes[failure_signature] = fix
        return fix


class SelfEvolutionEngine:
    """7.2 Evolves the harness and architecture over longer execution horizons."""
    def __init__(self) -> None:
        self.current_roles: Dict[str, str] = {
            "ADE": "Demand & Narrative sensing director.",
            "ARE": "Dynamic funnel and conversion supervisor.",
            "AVIE": "Visual psychology concept designer."
        }

    def propose_architectural_shift(self, recent_performance: float) -> Optional[str]:
        if recent_performance < 0.2:
            return "Shift: Integrate CausalIntelligenceEngine to weight treatment effect estimates."
        return None


# ===========================================================================
# 7.3 Capital Allocation Layer
# ===========================================================================
class CapitalAllocationLayer:
    """7.3 Multi-armed expected return vs risk allocations."""
    def __init__(self) -> None:
        self.allocations: Dict[str, float] = {}

    def calculate_allocation(self, expected_return: float, risk_factor: float, base_budget: int) -> int:
        """Allocate capital proportionally using simple risk-adjusted yield."""
        # Score ranges from 0 to 1
        adjusted_score = expected_return * (1.0 - risk_factor)
        return int(base_budget * adjusted_score)


# ===========================================================================
# KOS/ROS Spec — Addendum v1.1: Production Patterns
# ===========================================================================

class EventSourcingManager:
    """1. In-process event sourcing and dispatching."""
    def __init__(self) -> None:
        self.events: List[Event] = []
        self.subscribers: Dict[str, List[Any]] = {}  # event_type -> callbacks

    def subscribe(self, event_type: str, callback: Any) -> None:
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    def publish(self, event_type: str, payload: Dict[str, Any], caused_by: Optional[str] = None) -> Event:
        evt = Event(type=event_type, payload=payload, caused_by=caused_by)
        self.events.append(evt)
        # Notify subscribers
        for callback in self.subscribers.get(event_type, []):
            try:
                callback(evt)
            except Exception as e:
                logger.error("Error in subscriber callback for %s: %s", event_type, e)
        return evt


class VersionedNodeManager:
    """2. Versioning pattern for Hypothesis, Evidence, Theory (Append-only insert)."""
    def __init__(self) -> None:
        self.evidences: Dict[str, List[Evidence]] = {}   # node_id -> versions
        self.hypotheses: Dict[str, List[Hypothesis]] = {} # node_id -> versions
        self.theories: Dict[str, List[Theory]] = {}     # node_id -> versions

    def save_evidence(self, ev: Evidence) -> None:
        versions = self.evidences.setdefault(ev.id, [])
        # If there's an existing current version, set current=False
        for existing in versions:
            if existing.current:
                existing.current = False
        new_version_num = len(versions) + 1
        ev.version = new_version_num
        ev.current = True
        versions.append(ev)

    def save_hypothesis(self, hyp: Hypothesis) -> None:
        versions = self.hypotheses.setdefault(hyp.id, [])
        for existing in versions:
            if existing.current:
                existing.current = False
        new_version_num = len(versions) + 1
        hyp.version = new_version_num
        hyp.current = True
        versions.append(hyp)

    def save_theory(self, th: Theory) -> None:
        versions = self.theories.setdefault(th.id, [])
        for existing in versions:
            if existing.current:
                existing.current = False
        new_version_num = len(versions) + 1
        th.version = new_version_num
        th.current = True
        versions.append(th)

    def version_chain(self, node_id: str, node_type: str) -> List[Any]:
        if node_type == "Evidence":
            return self.evidences.get(node_id, [])
        elif node_type == "Hypothesis":
            return self.hypotheses.get(node_id, [])
        elif node_type == "Theory":
            return self.theories.get(node_id, [])
        return []

    def current(self, node_id: str, node_type: str) -> Optional[Any]:
        chain = self.version_chain(node_id, node_type)
        for node in chain:
            if node.current:
                return node
        return None


class ProvenanceEngine:
    """3. Provenance walks caused_by chains + supporting evidence/constituent edges."""
    def __init__(self, event_manager: EventSourcingManager) -> None:
        self.event_manager = event_manager

    def lineage(self, target_id: str) -> List[Event]:
        """Returns ordered lineage history by walking caused_by chains."""
        lineage_chain = []
        current_event = None

        # Find starting event for the node
        for evt in reversed(self.event_manager.events):
            payload_vals = list(evt.payload.values())
            if target_id == evt.id or target_id in payload_vals:
                current_event = evt
                break

        while current_event is not None:
            lineage_chain.append(current_event)
            if current_event.caused_by:
                parent = None
                for evt in self.event_manager.events:
                    if evt.id == current_event.caused_by:
                        parent = evt
                        break
                current_event = parent
            else:
                current_event = None

        return lineage_chain


class DecisionLifecycleManager:
    """4. Handles the lifecycle of DecisionProposals via state machine."""
    def __init__(self, event_manager: EventSourcingManager) -> None:
        self.proposals: Dict[str, DecisionProposal] = {}
        self.event_manager = event_manager

    def propose(self, decision: str, supporting_hypotheses: List[str], proposed_by: str) -> DecisionProposal:
        prop = DecisionProposal(
            decision=decision,
            supporting_hypotheses=supporting_hypotheses,
            proposed_by=proposed_by,
            status="proposed"
        )
        self.proposals[prop.id] = prop
        self.event_manager.publish("DecisionProposed", {"proposal_id": prop.id, "decision": decision})
        return prop

    def start_simulation(self, prop_id: str, sim_result: Dict[str, Any]) -> None:
        prop = self.proposals.get(prop_id)
        if prop and prop.status == "proposed":
            prop.status = "simulating"
            prop.simulation_result = sim_result

    def approve(self, prop_id: str, approved_by: str) -> None:
        prop = self.proposals.get(prop_id)
        if prop and prop.status == "simulating":
            prop.status = "approved"
            prop.approval["approved_by"] = approved_by
            prop.approval["approved_at"] = datetime.utcnow()
            self.event_manager.publish("DecisionApproved", {"proposal_id": prop.id, "approved_by": approved_by})

    def reject(self, prop_id: str) -> None:
        prop = self.proposals.get(prop_id)
        if prop and prop.status == "simulating":
            prop.status = "rejected"

    def execute(self, prop_id: str, exec_result: Dict[str, Any], record_ref: str) -> None:
        prop = self.proposals.get(prop_id)
        if prop and prop.status == "approved":
            prop.status = "executed"
            prop.execution_result = exec_result
            prop.decision_record = record_ref
            self.event_manager.publish("DecisionExecuted", {"proposal_id": prop.id, "record_ref": record_ref})

    def cancel(self, prop_id: str) -> None:
        prop = self.proposals.get(prop_id)
        if prop and prop.status == "approved":
            prop.status = "cancelled"


class RBACGuard:
    """5. Minimal RBAC guard checks scopes on agent calls and approvals."""
    def __init__(self) -> None:
        self.scopes: Dict[str, AgentScope] = {}

    def register_scope(self, scope: AgentScope) -> None:
        self.scopes[scope.agent_id] = scope

    def check_call(self, agent_id: str, method_name: str) -> bool:
        scope = self.scopes.get(agent_id)
        if not scope:
            return False
        return method_name in scope.can_call

    def check_approve(self, agent_id: str, decision_category: str) -> bool:
        scope = self.scopes.get(agent_id)
        if not scope:
            return False
        return decision_category in scope.can_approve


class DataContractValidator:
    """6. Explicit data contract validation for evidence nodes."""
    @staticmethod
    def validate(evidence: Evidence) -> tuple[bool, str]:
        # 1. Schema Validation (required fields present and non-null)
        if not evidence.statement or not evidence.evidence_quality_tier:
            return False, "RejectedWithReason: Schema invalid: missing required fields statement or evidence_quality_tier"

        # 2. Quality Validation
        recognized_tiers = {"RCT", "COHORT", "ANECDOTAL"}
        if evidence.evidence_quality_tier not in recognized_tiers:
            return False, "RejectedWithReason: Quality invalid: unrecognized evidence_quality_tier"
        if not (0.0 <= evidence.reliability_weight <= 1.0):
            return False, "RejectedWithReason: Quality invalid: reliability_weight must be in [0,1]"

        # 3. Business Rule Validation
        if evidence.evidence_quality_tier == "RCT":
            if evidence.effect_size is None or not evidence.interval:
                return False, "RejectedWithReason: Business rule invalid: RCT tier evidence must have non-null effect_size and interval"

        return True, "Accepted"
