from __future__ import annotations

import json
import os
from typing import Any

from harness_core import AgentHarness, HarnessConfig, load_config
from langgraph.graph import END, StateGraph
from pydantic import BaseModel

_DEFAULT_MODEL = "openai/gpt-oss-120b"


def _llm_settings() -> tuple[str, str, str]:
    missing = [v for v in ("LLM_API_KEY", "LLM_BASE_URL") if not os.environ.get(v, "").strip()]
    if missing:
        raise OSError(f"{' and '.join(missing)} must be set (see .env.example)")
    model = os.environ.get("LLM_MODEL", "").strip() or _DEFAULT_MODEL
    return os.environ["LLM_API_KEY"].strip(), os.environ["LLM_BASE_URL"].strip(), model


def _strip_markdown(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        parts = text.split("```")
        if len(parts) >= 2:
            inner = parts[1].strip()
            if inner.startswith("json"):
                inner = inner[4:].strip()
            return inner
    return text


def make_analyze_node(system_prompt: str):
    async def analyze_node(state: dict[str, Any]) -> dict[str, Any]:
        from openai import AsyncOpenAI

        api_key, base_url, model = _llm_settings()
        client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        input_payload = json.dumps(
            {k: v for k, v in state.items() if not k.startswith("_")},
            indent=2,
            default=str,
        )
        user_content = f"Analyze this data and return ONLY valid JSON:\n{input_payload}"
        response = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
            temperature=0.1,
        )
        raw = response.choices[0].message.content
        return json.loads(_strip_markdown(raw))

    return analyze_node


def build_supply_chain_harness(
    agent_name: str,
    agent_version: str,
    input_schema: type[BaseModel],
    output_schema: type[BaseModel],
    system_prompt: str,
    config: HarnessConfig | None = None,
) -> AgentHarness:
    node = make_analyze_node(system_prompt)
    graph: StateGraph = StateGraph(dict)
    graph.add_node("analyze", node)
    graph.set_entry_point("analyze")
    graph.add_edge("analyze", END)
    compiled = graph.compile()
    cfg = config or load_config("config/harness.yaml")
    return AgentHarness(
        graph=compiled,
        agent_name=agent_name,
        agent_version=agent_version,
        input_schema=input_schema,
        output_schema=output_schema,
        config=cfg,
    )
