"""Score how much the episode relies on the viewer remembering earlier beats."""

from __future__ import annotations

from typing import Any

from mock_client import get_client
from stages.common import rubric_score


def score_memory_demand(stage_c: dict[str, Any]) -> dict[str, Any]:
    client = get_client()
    scenes = stage_c["scenes"]
    prompt = f"Rate the memory demand across {len(scenes)} scenes."
    reasoning = client.llm_medium(prompt, output_schema="memory_v1")

    score = rubric_score("memory_demand", len(scenes))
    return {"memory_demand_score": score, "memory_demand_reasoning": reasoning}
