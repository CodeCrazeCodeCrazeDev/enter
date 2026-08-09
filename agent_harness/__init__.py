"""AgentHarness — evaluate LLM agents on public benchmarks."""
import os

__version__ = "1.0.0"

# Extend __path__ to fallback to AgentHarness/agent_harness submodule
_sub_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "AgentHarness", "agent_harness")
if os.path.exists(_sub_path):
    __path__.append(_sub_path)
