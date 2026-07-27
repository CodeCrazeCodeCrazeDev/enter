"""Unit tests for Phase 2 Knowledge Operating System (KOS) epistemic engines."""

import pytest
from uuid import uuid4
from apodex.ai_eos.domain.models import Hypothesis, Evidence
from apodex.ai_eos.memory.knowledge_infrastructure import KnowledgeInfrastructure


def test_bayesian_belief_engine_conjugate_update():
    """Verify that incoming Evidence nodes update linked Hypothesis posterior confidence correctly."""
    ki = KnowledgeInfrastructure()

    # Prior confidence = 0.50
    hyp = Hypothesis(
        hypothesis_id=uuid4(),
        statement="Pricing elasticity is highly non-linear",
        domain="pricing",
        prior_confidence=0.50,
        posterior_confidence=0.50,
        status="active"
    )
    ki.hypotheses.save(str(hyp.hypothesis_id), hyp)
    ki.record_node(str(hyp.hypothesis_id), "hypothesis", {"statement": hyp.statement})

    # Record strong supporting Evidence
    ev_strong = Evidence(
        evidence_id="ev_strong",
        source="paid_onboarding_cell_A",
        method="pilot",
        strength={"p_value": 0.002, "sample_size": 250, "effect_size": 1.8},
        causal_or_correlational="causal"
    )

    ki.update_hypothesis_belief(str(hyp.hypothesis_id), ev_strong)

    # Posterior should shift significantly upwards from 0.50
    updated_hyp = ki.hypotheses.get(str(hyp.hypothesis_id))
    assert updated_hyp.posterior_confidence > 0.50
    assert len(updated_hyp.supporting_evidence) == 1
    assert "ev_strong" in updated_hyp.supporting_evidence


def test_contradiction_detection_agent():
    """Verify that inconsistent hypothesis beliefs in the same domain raise a Contradiction."""
    ki = KnowledgeInfrastructure()

    h1 = Hypothesis(
        hypothesis_id=uuid4(),
        statement="Ad placements on top yield high CTR",
        domain="ads",
        prior_confidence=0.50,
        posterior_confidence=0.90,  # Highly confident
        status="active"
    )
    h2 = Hypothesis(
        hypothesis_id=uuid4(),
        statement="Ad placements on top yield poor CTR",
        domain="ads",
        prior_confidence=0.50,
        posterior_confidence=0.10,  # Deeply unconfident
        status="active"
    )

    ki.hypotheses.save(str(h1.hypothesis_id), h1)
    ki.hypotheses.save(str(h2.hypothesis_id), h2)

    contradictions = ki.detect_contradictions()

    assert len(contradictions) == 1
    assert contradictions[0].node_a == str(h1.hypothesis_id)
    assert contradictions[0].node_b == str(h2.hypothesis_id)


def test_theory_formation_loop_promotion():
    """Verify that generalized, highly-supported hypotheses are promoted to Theory nodes."""
    ki = KnowledgeInfrastructure()

    hyp = Hypothesis(
        hypothesis_id=uuid4(),
        statement="Minimal onboarding clicks increase conversion",
        domain="onboarding",
        prior_confidence=0.50,
        posterior_confidence=0.85,
        supporting_evidence=["ev1", "ev2"],  # At least 2 supporting evidences
        status="active"
    )
    ki.hypotheses.save(str(hyp.hypothesis_id), hyp)
    ki.record_node(str(hyp.hypothesis_id), "hypothesis", {"statement": hyp.statement})

    promoted_theories = ki.promote_to_theories()

    assert len(promoted_theories) == 1
    assert promoted_theories[0].confidence == 0.85
    assert "onboarding" in promoted_theories[0].predictive_scope[0]

    # Hypothesis status is promoted
    updated_hyp = ki.hypotheses.get(str(hyp.hypothesis_id))
    assert updated_hyp.status == "theory-promoted"
