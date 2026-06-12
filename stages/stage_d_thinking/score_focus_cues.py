"""Score attention/focus cues from the scene and transcript shape."""

from __future__ import annotations

from typing import Any

from mock_client import get_client
from stages.common import rubric_score


def score_focus_cues(stage_c: dict[str, Any], stage_a: dict[str, Any]) -> dict[str, Any]:
    client = get_client()
    scenes = stage_c["scenes"]
    prompt = f"Rate the strength of attention cues across {len(scenes)} scenes."
    reasoning = client.llm_medium(prompt, output_schema="focus_v1")

    score = rubric_score("focus_cues", len(scenes), len(stage_a["align"]["aligned_segments"]))
    return {"focus_cue_score": score, "focus_cue_reasoning": reasoning}
