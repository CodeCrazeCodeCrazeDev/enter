"""Pipeline spec: ``agent_harness_v2``.

Next-generation multi-agent, plan-and-act research orchestration pipeline.
Coexists safely with react_base.
"""

from __future__ import annotations

from agent_harness.models.pipeline_spec import (
    CompressionConfig,
    ContextPolicy,
    NodeDefinition,
    PipelineSpec,
    TransitionSpec,
)

AGENT_HARNESS_V2_SPEC = PipelineSpec(
    pipeline_id="agent_harness_v2",
    name="AgentHarness Next-Gen V2",
    description=(
        "Next-generation research orchestration framework incorporating Hierarchical "
        "Multi-Agent, Graph-of-Thought, Plan-and-Act, World Model, Semantic Memory, "
        "and Concurrent Verification."
    ),
    entry_point="evolved_agent",
    terminal_nodes=["evolved_agent"],
    nodes=[
        NodeDefinition(
            node_id="evolved_agent",
            role_id="react_solver",
            node_function=(
                "workflows.react_base.nodes.evolved_node.evolved_agent_node"
            ),
            context_policy=ContextPolicy(
                include_fields=[
                    "original_question", "language", "task_id", "metadata",
                ],
            ),
            compression=CompressionConfig(enabled=False),
            output_fields=[
                "final_answer", "final_content",
                "answer_confidence", "react_steps",
            ],
        ),
    ],
    transitions=[
        TransitionSpec(from_phase="evolved_agent", to_phase="__END__"),
    ],
)
