# -*- coding: utf-8 -*-
"""
test_unified_4layer_integration.py: Integration tests for the Unified 4-Layer Cognitive OS.
Validates active inference state handoffs across Layer 1 Research OS, Layer 2 EIOS/EOS,
Layer 3 AEAN, and Layer 4 APODEX WorldModel.
"""

import pytest
from uuid import uuid4
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.ai_eos.domain.models import Hypothesis
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind
from apodex.world_model.world_model import WorldModel
from apodex.ai_eos.research.integration import ResearchToSystemBridge, CodeRewriteEngine, RewriteProposal

def test_unified_4layer_active_inference_handoff():
    # Instantiate Layer 1: Research OS
    ros = ResearchOS()
    hyp = ros.register_hypothesis(
        title="Active Inference Acceleration",
        description="Active inference EFE reduction accelerates multi-agent strategy convergence.",
        null_hypothesis="Active inference has no effect on multi-agent convergence.",
        target_metric="convergence_speed"
    )

    # Instantiate Layer 2: EIOS Kernel & EOS Engine
    kernel = EIOSKernel()
    eos = EOSEngine()

    # Instantiate Layer 3: AEAN HiveMind
    hive = HiveMind()

    # Instantiate Layer 4: APODEX WorldModel
    wm = WorldModel()

    # Instantiate Cross-Layer Bridge
    bridge = ResearchToSystemBridge(
        research_os=ros,
        eios_kernel=kernel,
        eos_engine=eos,
        hive_mind=hive,
        world_model=wm
    )

    # Run Active Inference Handoff
    result = bridge.bridge_research_to_system_state(hyp)

    assert result["status"] == "HANDOFF_COMPLETED"
    assert result["hypothesis_id"] == str(hyp.hypothesis_id)
    assert len(eos.active_hypotheses) == 1
    assert eos.active_hypotheses[0].statement == hyp.statement

def test_code_rewrite_engine_ast_hawkes_safety(tmp_path):
    target_file = tmp_path / "test_script.py"
    target_file.write_text("def safe_func():\n    return 42\n")

    engine = CodeRewriteEngine(allowed_paths=[str(tmp_path)], max_ast_recursion_depth=2)

    # Safe rewrite
    proposal = engine.propose_rewrite(
        filepath=str(target_file),
        original_snippet="return 42",
        proposed_snippet="return 100",
        rationale="Update return value"
    )

    assert engine.verify_proposal_ast(proposal) is True
    assert engine.commit_rewrite(proposal) is True
    assert "return 100" in target_file.read_text()

    # Vetoed recursive rewrite exceeding max depth
    recursive_code = """def recursive_trap(n):
    if n > 0:
        recursive_trap(n - 1)
        recursive_trap(n - 2)
        recursive_trap(n - 3)
    return n
"""
    proposal_bad = engine.propose_rewrite(
        filepath=str(target_file),
        original_snippet="return 100",
        proposed_snippet=recursive_code,
        rationale="Unsafe deep recursion"
    )

    assert engine.verify_proposal_ast(proposal_bad) is False
