"""Score creative-thinking demands the episode places on the viewer."""

from __future__ import annotations

from typing import Any

from mock_client import get_client
from stages.common import rubric_score


def score_creative_thinking(stage_c: dict[str, Any]) -> dict[str, Any]:
    client = get_client()
    scenes = stage_c["scenes"]
    prompt = f"Rate the creative-thinking demand across {len(scenes)} scenes."
    reasoning = client.llm_medium(prompt, output_schema="creative_v1")

    score = rubric_score("creative_thinking", len(scenes))
    return {"creative_thinking_score": score, "creative_thinking_reasoning": reasoning}
