"""Workflow State Machine and State Transitions for the AI-EOS operating system."""

from __future__ import annotations
import logging
from enum import Enum
from typing import Dict, List, Optional
from uuid import UUID

logger = logging.getLogger("ai_eos.infrastructure.state_machine")


class VentureLifecyclePhase(str, Enum):
    PHASE_0_DISCOVERY = "Phase 0 - Opportunity Discovery"
    PHASE_1_VALIDATION = "Phase 1 - Hypothesis Validation"
    PHASE_2_DESIGN = "Phase 2 - Brand & Product Design"
    PHASE_3_GTM = "Phase 3 - Go-To-Market Launch"
    PHASE_4_REVENUE = "Phase 4 - Operations & Revenue Engine"
    PHASE_5_PORTFOLIO = "Phase 5 - Capital Portfolio Management"
    PHASE_6_OPERATIONS = "Phase 6 - Compliance & Legal Org"
    PHASE_7_EXPANSION = "Phase 7 - Geographical Expansion"
    PHASE_8_META_LEARNING = "Phase 8 - Continuous Meta-Learning"


class LifecycleStateMachine:
    """Manages legal state transitions and validations for a Venture Cell's lifecycle."""

    _ALLOWED_TRANSITIONS: Dict[VentureLifecyclePhase, List[VentureLifecyclePhase]] = {
        VentureLifecyclePhase.PHASE_0_DISCOVERY: [VentureLifecyclePhase.PHASE_1_VALIDATION],
        VentureLifecyclePhase.PHASE_1_VALIDATION: [VentureLifecyclePhase.PHASE_2_DESIGN, VentureLifecyclePhase.PHASE_0_DISCOVERY],
        VentureLifecyclePhase.PHASE_2_DESIGN: [VentureLifecyclePhase.PHASE_3_GTM, VentureLifecyclePhase.PHASE_1_VALIDATION],
        VentureLifecyclePhase.PHASE_3_GTM: [VentureLifecyclePhase.PHASE_4_REVENUE, VentureLifecyclePhase.PHASE_2_DESIGN],
        VentureLifecyclePhase.PHASE_4_REVENUE: [VentureLifecyclePhase.PHASE_5_PORTFOLIO, VentureLifecyclePhase.PHASE_3_GTM],
        VentureLifecyclePhase.PHASE_5_PORTFOLIO: [VentureLifecyclePhase.PHASE_6_OPERATIONS, VentureLifecyclePhase.PHASE_4_REVENUE],
        VentureLifecyclePhase.PHASE_6_OPERATIONS: [VentureLifecyclePhase.PHASE_7_EXPANSION, VentureLifecyclePhase.PHASE_5_PORTFOLIO],
        VentureLifecyclePhase.PHASE_7_EXPANSION: [VentureLifecyclePhase.PHASE_8_META_LEARNING, VentureLifecyclePhase.PHASE_6_OPERATIONS],
        VentureLifecyclePhase.PHASE_8_META_LEARNING: [VentureLifecyclePhase.PHASE_8_META_LEARNING, VentureLifecyclePhase.PHASE_7_EXPANSION],
    }

    def __init__(self, current_phase: VentureLifecyclePhase = VentureLifecyclePhase.PHASE_0_DISCOVERY) -> None:
        self.current_phase = current_phase

    def transition_to(self, target_phase: VentureLifecyclePhase) -> bool:
        """Attempt to transition to a target lifecycle phase, checking transition rules."""
        allowed = self._ALLOWED_TRANSITIONS.get(self.current_phase, [])
        if target_phase in allowed:
            logger.info(f"Venture cell transitioned: {self.current_phase.value} -> {target_phase.value}")
            self.current_phase = target_phase
            return True
        logger.warning(f"Illegal transition requested: {self.current_phase.value} -x-> {target_phase.value}")
        return False
