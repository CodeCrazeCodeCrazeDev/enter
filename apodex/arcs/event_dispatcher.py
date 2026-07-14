from __future__ import annotations
import asyncio
import logging
import uuid
from datetime import datetime
from typing import Any, Callable, Dict, List, Type, TypeVar, Coroutine, Awaitable
from pydantic import BaseModel, Field

logger = logging.getLogger("arcs.event_dispatcher")


# =====================================================================
# Domain Events Definition
# =====================================================================

class DomainEvent(BaseModel):
    """Base schema for all event-sourced messages in ARCS."""

    event_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class MarketOpportunityDiscoveredEvent(DomainEvent):
    """Broadcasted when a new viable market gap is mined."""

    opportunity_id: uuid.UUID
    domain: str
    estimated_market_size_cents: int
    confidence: float


class ProductLaunchApprovedEvent(DomainEvent):
    """Broadcasted when a product transitions from sandbox to active."""

    product_id: uuid.UUID
    tenant_id: uuid.UUID
    approved_pricing_model: str
    initial_budget_cents: int


class CampaignLaunchedEvent(DomainEvent):
    """Broadcasted when a new marketing outreach workflow starts."""

    campaign_id: uuid.UUID
    channels: List[str]
    target_icp: str
    budget_cents: int


class LeadQualifiedEvent(DomainEvent):
    """Broadcasted when a prospective buyer passes qualification metrics."""

    customer_id: uuid.UUID
    score: float
    needs: List[str]
    estimated_deal_value_cents: int


class PaymentReceivedEvent(DomainEvent):
    """Broadcasted on successful payment processing via treasury gateways."""

    invoice_id: uuid.UUID
    customer_id: uuid.UUID
    amount_cents: int
    currency: str
    transaction_id: str


class PaymentFailedEvent(DomainEvent):
    """Broadcasted when a transaction charge fails."""

    invoice_id: uuid.UUID
    customer_id: uuid.UUID
    failure_reason: str
    retry_count: int


class CapitalAllocatedEvent(DomainEvent):
    """Broadcasted when budget is moved from treasury to departments."""

    allocation_id: uuid.UUID
    target_department: str  # e.g., 'marketing', 'sales', 'product'
    amount_cents: int
    restriction_codes: List[str] = Field(default_factory=list)


class PolicyViolationDetectedEvent(DomainEvent):
    """Broadcasted when an execution violates compliance boundaries."""

    violator_agent_id: str
    violated_policy_id: str
    action_taken: str
    severity: str  # low, medium, high, critical


# =====================================================================
# Domain Commands Definition
# =====================================================================

class DomainCommand(BaseModel):
    """Base schema for state-modifying requests."""

    command_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ScanMarketOpportunitiesCommand(DomainCommand):
    max_budget_cents: int
    allowed_domains: List[str]


class AllocateCapitalCommand(DomainCommand):
    recipient_id: str
    amount_cents: int
    funding_account: str


class ProvisionTenantCommand(DomainCommand):
    tenant_id: uuid.UUID
    tenant_name: str
    isolation_policy: str


class ProcessPaymentCommand(DomainCommand):
    invoice_id: uuid.UUID
    payment_method_id: str
    currency: str


class EscalateApprovalCommand(DomainCommand):
    exception_id: uuid.UUID
    approver_group: str
    context_data: Dict[str, Any]


# =====================================================================
# Bus and Dispatcher Implementations
# =====================================================================

E = TypeVar("E", bound=DomainEvent)
C = TypeVar("C", bound=DomainCommand)


class EventBus:
    """Asynchronous, thread-safe Event Bus for publishing and subscribing to DomainEvents."""

    def __init__(self) -> None:
        self._subscribers: Dict[Type[DomainEvent], List[Callable[[Any], Awaitable[None]]]] = {}
        self._lock = asyncio.Lock()

    def subscribe(self, event_type: Type[E], handler: Callable[[E], Awaitable[None]]) -> None:
        """Register an async handler function for a specific DomainEvent type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)
        logger.info(f"Subscribed handler '{handler.__name__}' to event type: {event_type.__name__}")

    async def publish(self, event: DomainEvent) -> None:
        """Asynchronously dispatch an event to all registered subscribers."""
        event_type = type(event)
        handlers = self._subscribers.get(event_type, [])
        if not handlers:
            logger.debug(f"No subscribers registered for event: {event_type.__name__}")
            return

        logger.debug(f"Publishing {event_type.__name__} (ID: {event.event_id}) to {len(handlers)} handlers.")
        # Schedule all handler coroutines in parallel. Isolate handler failures so a
        # single faulty subscriber does not prevent others from running, but surface
        # each error instead of silently swallowing it.
        tasks = [asyncio.create_task(handler(event)) for handler in handlers]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for handler, result in zip(handlers, results):
            if isinstance(result, Exception):
                logger.error(
                    "Handler '%s' failed while processing %s (ID: %s): %s",
                    getattr(handler, "__name__", repr(handler)),
                    event_type.__name__,
                    event.event_id,
                    result,
                    exc_info=result,
                )


class CommandDispatcher:
    """Synchronous/Asynchronous dispatcher for routing state-modifying DomainCommands to handlers."""

    def __init__(self) -> None:
        self._handlers: Dict[Type[DomainCommand], Callable[[Any], Awaitable[Any]]] = {}

    def register_handler(self, command_type: Type[C], handler: Callable[[C], Awaitable[Any]]) -> None:
        """Register a command handler for a specific DomainCommand type. There can only be one handler per command."""
        if command_type in self._handlers:
            raise ValueError(f"Handler already registered for command: {command_type.__name__}")
        self._handlers[command_type] = handler
        logger.info(f"Registered handler '{handler.__name__}' for command: {command_type.__name__}")

    async def dispatch(self, command: DomainCommand) -> Any:
        """Dispatch a command to its registered handler and return the result."""
        command_type = type(command)
        if command_type not in self._handlers:
            raise KeyError(f"No handler registered for command: {command_type.__name__}")

        handler = self._handlers[command_type]
        logger.debug(f"Dispatching command {command_type.__name__} to handler '{handler.__name__}'.")
        return await handler(command)
