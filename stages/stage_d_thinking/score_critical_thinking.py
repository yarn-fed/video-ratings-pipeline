"""Score critical-thinking demands the episode places on the viewer."""

from __future__ import annotations

from typing import Any

from mock_client import get_client
from stages.common import rubric_score


def score_critical_thinking(stage_c: dict[str, Any]) -> dict[str, Any]:
    client = get_client()
    scenes = stage_c["scenes"]
    prompt = f"Rate the critical-thinking demand across {len(scenes)} scenes."
    reasoning = client.llm_medium(prompt, output_schema="critical_v1")

    score = rubric_score("critical_thinking", len(scenes))
    return {"critical_thinking_score": score, "critical_thinking_reasoning": reasoning}
