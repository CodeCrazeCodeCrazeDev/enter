import pytest
import asyncio
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.arcs.kernel.kernel import EIOSKernel, EntrepreneurialCompiler
from apodex.aean.coordination.hive_mind import HiveMind
from apodex.world_model.world_model import WorldModel
from apodex.ai_eos.research.integration import ResearchToSystemBridge


@pytest.mark.asyncio
async def test_unified_4layer_cross_layer_workflow():
    # 1. Layer 1: Research OS
    ros = ResearchOS()
    hyp = ros.register_hypothesis(
        title="Autonomous Agent Token Market Equilibrium",
        description="Token bidding incentivizes optimal compute allocation in multi-agent networks.",
        null_hypothesis="Token bidding does not improve allocation performance.",
        target_metric="token_efficiency"
    )
    exp = ros.create_experiment(hypothesis_id=hyp.hypothesis_id, seed=123)

    # Force validation for bridge testing
    validated_exp = ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=2.5)
    assert validated_exp.is_statistically_significant
    assert hyp.status == "validated"

    # 2. Bridge & Layer 2: EIOS Kernel & EOS Engine
    compiler = EntrepreneurialCompiler()
    kernel = EIOSKernel()
    eos = EOSEngine()

    dag = ros.export_validated_hypothesis_to_kernel(hyp.hypothesis_id, compiler)
    assert dag is not None
    assert len(dag.nodes) > 0

    success = await kernel.execute_dag(dag)
    assert success

    ros.promote_hypothesis_to_eos(hyp.hypothesis_id, eos)
    assert len(eos.active_hypotheses) == 1
    assert eos.active_hypotheses[0].hypothesis_id == hyp.hypothesis_id

    # 3. Layer 3: AEAN HiveMind & Layer 4: APODEX WorldModel
    hive_mind = HiveMind(token_budget=100)
    world_model = WorldModel()

    ros.hand_off_to_aean_and_world_model(hyp.hypothesis_id, hive_mind, world_model)

    assert len(hive_mind.granted_history) > 0
    node_id = f"hyp_{hyp.hypothesis_id}"
    assert node_id in world_model.beliefs
    assert node_id in world_model.nodes
