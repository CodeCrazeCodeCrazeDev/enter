"""Unit and integration tests for the Ornith 1.0 Self-Scaffolding capability."""

from __future__ import annotations

import pytest
from agent_harness.core.runtime.reasoning.self_scaffolder import OrnithSelfScaffolder


def test_ornith_self_scaffolding():
    scaffolder = OrnithSelfScaffolder()

    # 1. Test search-based goal scaffolding
    plan_search = scaffolder.learn_and_generate_scaffold(
        goal="Search the web for chemical properties",
        available_tools=["web_search", "run_python_code"]
    )
    assert plan_search.plan_id == "ornith_plan_01"
    assert len(plan_search.steps) == 1
    assert plan_search.steps[0].target_tool == "web_search"
    assert plan_search.steps[0].retry_policy["max_retries"] == 3

    # 2. Test code-based goal scaffolding
    plan_code = scaffolder.learn_and_generate_scaffold(
        goal="Calculate the sum of primes",
        available_tools=["web_search", "run_python_code"]
    )
    assert len(plan_code.steps) == 1
    assert plan_code.steps[0].target_tool == "run_python_code"
