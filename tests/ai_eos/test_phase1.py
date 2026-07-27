"""Unit tests for Phase 1 System Composition Platform and Core Foundations."""

import pytest
from uuid import uuid4
from apodex.ai_eos.interfaces.services import IEventBus
from apodex.ai_eos.infrastructure.composition import CompositionContainer
from apodex.ai_eos.infrastructure.event_bus import EventBus
from apodex.ai_eos.infrastructure.identity import DeterministicIdentityGenerator
from apodex.ai_eos.infrastructure.state_machine import VentureLifecyclePhase, LifecycleStateMachine
from apodex.ai_eos.domain.events import VentureCellCreatedEvent


def test_composition_container_di():
    """Verify that services are resolved cleanly through the DI container."""
    container = CompositionContainer()
    container.reset()

    event_bus = EventBus()
    container.register(IEventBus, event_bus)

    assert container.has_service(IEventBus) is True
    resolved = container.resolve(IEventBus)
    assert resolved == event_bus


def test_event_bus_pub_sub():
    """Verify that the Event Bus correctly publishes and handles events."""
    event_bus = EventBus()
    received_events = []

    def handle_create(event: VentureCellCreatedEvent):
        received_events.append(event)

    event_bus.subscribe(VentureCellCreatedEvent, handle_create)

    cell_id = uuid4()
    evt = VentureCellCreatedEvent(
        cell_id=cell_id,
        name="VentureAlpha",
        namespace="namespace_alpha",
        allocated_capital_cents=500000
    )

    event_bus.publish(evt)

    assert len(received_events) == 1
    assert received_events[0].cell_id == cell_id
    assert received_events[0].name == "VentureAlpha"


def test_deterministic_identity():
    """Verify deterministic UUID and SHA-256 generation."""
    uuid1 = DeterministicIdentityGenerator.generate_uuid_from_seed("test-seed")
    uuid2 = DeterministicIdentityGenerator.generate_uuid_from_seed("test-seed")
    uuid3 = DeterministicIdentityGenerator.generate_uuid_from_seed("different-seed")

    assert uuid1 == uuid2
    assert uuid1 != uuid3

    hash1 = DeterministicIdentityGenerator.compute_sha256("test-payload")
    hash2 = DeterministicIdentityGenerator.compute_sha256("test-payload")
    assert hash1 == hash2


def test_state_machine_transitions():
    """Verify lifecycle state-machine state transitions."""
    sm = LifecycleStateMachine(VentureLifecyclePhase.PHASE_0_DISCOVERY)

    # Valid transition
    success = sm.transition_to(VentureLifecyclePhase.PHASE_1_VALIDATION)
    assert success is True
    assert sm.current_phase == VentureLifecyclePhase.PHASE_1_VALIDATION

    # Invalid transition (Phase 1 cannot skip to Phase 4)
    fail = sm.transition_to(VentureLifecyclePhase.PHASE_4_REVENUE)
    assert fail is False
    assert sm.current_phase == VentureLifecyclePhase.PHASE_1_VALIDATION
