"""Unit and integration tests for Multi-Format Reasoning + Tool Calls parser."""

from __future__ import annotations

import pytest
from agent_harness.core.runtime.reasoning.reasoning_parser import ReasoningToolCallParser


def test_reasoning_and_multi_format_tool_calls():
    parser = ReasoningToolCallParser()

    # 1. Test OpenAI format output
    raw_openai = (
        "<think>\nNeed to search for local files.\n</think>\n"
        "Here is the code block:\n"
        "```json\n"
        "{\n"
        '  "name": "web_search",\n'
        '  "args": {"query": "deep learning"}\n'
        "}\n"
        "```"
    )
    res_openai = parser.parse_response(raw_openai)
    assert res_openai.thinking == "Need to search for local files."
    assert "web_search" in res_openai.content
    assert len(res_openai.tool_calls) == 1
    assert res_openai.tool_calls[0]["name"] == "web_search"
    assert res_openai.tool_calls[0]["args"]["query"] == "deep learning"
    assert res_openai.format_detected == "openai"

    # 2. Test Anthropic XML format output
    raw_anthropic = (
        "<thinking>\nCall search utility\n</thinking>\n"
        'Let\'s execute: <invoke name="web_fetch">{"url": "http://example.com"}</invoke>'
    )
    res_anthropic = parser.parse_response(raw_anthropic)
    assert res_anthropic.thinking == "Call search utility"
    assert len(res_anthropic.tool_calls) == 1
    assert res_anthropic.tool_calls[0]["name"] == "web_fetch"
    assert res_anthropic.tool_calls[0]["args"]["url"] == "http://example.com"
    assert res_anthropic.format_detected == "anthropic"

    # 3. Test Gemini format output
    raw_gemini = (
        "<think>Compute sum</think>\n"
        "Executing: call:run_python_code(code='1+1')"
    )
    res_gemini = parser.parse_response(raw_gemini)
    assert res_gemini.thinking == "Compute sum"
    assert len(res_gemini.tool_calls) == 1
    assert res_gemini.tool_calls[0]["name"] == "run_python_code"
    assert res_gemini.tool_calls[0]["args"]["code"] == "1+1"
    assert res_gemini.format_detected == "gemini"

    # 4. Test format conversions
    calls = [{"name": "web_search", "args": {"query": "HLE"}}]
    openai_spec = parser.convert_to_format(calls, "openai")
    assert openai_spec[0]["type"] == "function"
    assert openai_spec[0]["function"]["name"] == "web_search"

    anthropic_spec = parser.convert_to_format(calls, "anthropic")
    assert anthropic_spec[0]["type"] == "tool_use"
    assert anthropic_spec[0]["name"] == "web_search"
